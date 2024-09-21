import argparse
import datetime
import os

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.tensorboard import SummaryWriter

import pandas as pd

from tqdm import tqdm

from dataset import PriceDataset

tqdm.pandas()


class DLinear(nn.Module):
    def __init__(self, input_size, output_size, kernel_size=25):
        super(DLinear, self).__init__()
        self.input_size = input_size
        self.output_size = output_size
        self.kernel_size = kernel_size

        # Linear layers for trend and remainder components
        self.trend_linear = nn.Linear(input_size, output_size)
        self.remainder_linear = nn.Linear(input_size, output_size)

    def moving_average(self, x):
        # Apply moving average to extract trend
        cumsum = torch.cumsum(x, dim=1)
        cumsum[:, self.kernel_size :] = (
            cumsum[:, self.kernel_size :] - cumsum[:, : -self.kernel_size]
        )
        cumsum[:, : self.kernel_size] /= torch.arange(
            1, self.kernel_size + 1, device=x.device
        )
        cumsum[:, self.kernel_size :] /= self.kernel_size
        return cumsum

    def forward(self, x):
        # Decompose input into trend and remainder
        trend = self.moving_average(x)
        remainder = x - trend

        # Apply linear layers
        trend_out = self.trend_linear(trend)
        remainder_out = self.remainder_linear(remainder)

        # Combine the outputs
        output = trend_out + remainder_out
        return output


def read_dataset(path: str) -> PriceDataset:
    df: pd.DataFrame = pd.read_csv(path)
    return PriceDataset(df)


def main() -> None:
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--dataset",
        type=str,
        default="datasets/crypto_combine.csv",
    )
    arg_parser.add_argument(
        "--batch_size",
        type=int,
        default=8,
    )
    arg_parser.add_argument(
        "--epochs",
        type=int,
        default=100,
    )
    arg_parser.add_argument(
        "--lookback",
        type=int,
        default=64,
    )
    arg_parser.add_argument(
        "--lr",
        type=float,
        default=1e-3,
    )
    arg_parser.add_argument(
        "--is_debug",
        type=bool,
        default=False,
    )
    arg_parser.add_argument(
        "--log_dir",
        type=str,
        default="runs",
    )
    arg_parser.add_argument(
        "--device",
        type=str,
        default="cuda" if torch.cuda.is_available() else "cpu",
    )
    arg_parser.add_argument(
        "--seed",
        type=int,
        default=42,
    )
    arg_parser.add_argument(
        "--save_interval",
        type=int,
        default=10,
    )

    args = arg_parser.parse_args()

    device: torch.device = torch.device(args.device)
    save_interval: int = args.save_interval
    epochs: int = args.epochs

    dataset: PriceDataset = read_dataset(args.dataset)

    # train/val split
    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size

    # look-back window size * features (4, open, high, low, close)
    input_size: int = dataset.lookback * 4
    # forecasted steps (1, up or down compared to the last close price)
    output_size: int = 1

    model = DLinear(input_size=input_size, output_size=output_size).to(device)

    if args.is_debug:
        print(model)
        x: torch.Tensor = torch.randn(32, input_size).to(device)  # Batch size of 32
        output: torch.Tensor = model(x)
        print(output.shape)  # Should be (32, output_size)

    task_name: str = (
        f"DLinear_UPnDown_{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}"
    )
    writer: SummaryWriter = SummaryWriter(f"{args.log_dir}/{task_name}")
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)
    criterion = nn.MSELoss()

    train_progress: tqdm = tqdm(range(epochs))
    for epoch in train_progress:
        model.train()
        for i in range(train_size):
            x, y = dataset[i]
            x: torch.Tensor = x.reshape(1, -1).to(device)
            y: torch.Tensor = y.reshape(1, -1).to(device)

            optimizer.zero_grad()
            output: torch.Tensor = model(x)
            loss: torch.Tensor = criterion(output, y)
            loss.backward()
            optimizer.step()

        writer.add_scalar("Loss/train", loss.item(), epoch)
        train_progress.set_postfix({"loss": loss.item()})

        model.eval()
        val_loss = 0.0
        for i in range(val_size):
            x, y = dataset[train_size + i]
            x: torch.Tensor = x.reshape(1, -1).to(device)
            y: torch.Tensor = y.reshape(1, -1).to(device)

            output: torch.Tensor = model(x)
            loss: torch.Tensor = criterion(output, y)
            val_loss += loss.item()

        writer.add_scalar("Loss/val", val_loss / val_size, epoch)

        if (epoch + 1) % save_interval == 0 and epoch > 0 and (epoch + 1) != epochs:
            print(f"Saving checkpoint of epoch {epoch}...")

            if not os.path.exists("ckpts"):
                os.makedirs("ckpts")

            torch.save(model.state_dict(), f"ckpts/{task_name}_epoch_{epoch}.pt")

    writer.close()
    print("Saving checkpoint the final...")
    if not os.path.exists("ckpts"):
        os.makedirs("ckpts")
    torch.save(model.state_dict(), f"ckpts/{task_name}_final.pt")

    print(f"Finished training task: {task_name}")


if __name__ == "__main__":
    main()
