import torch
import torch.utils.data as data

import pandas as pd
import numpy as np


class PriceDataset(data.Dataset):
    def __init__(
        self,
        df: pd.DataFrame,  # Dataframe with columns: Date, Open, High, Low, Close
        lookback: int = 64,
        forecast: int = 1,
    ):
        self.df = df
        self.lookback = lookback
        self.forecast = forecast

        self.data: np.ndarray = self.df[["Open", "High", "Low", "Close"]].values

        self.data: torch.Tensor = torch.tensor(self.data, dtype=torch.float32)
        print(self.data.shape)

    def __len__(self):
        return len(self.data) - self.lookback - self.forecast

    def __getitem__(self, index):
        x = self.data[index : index + self.lookback]
        y_val = self.data[index + self.lookback + self.forecast - 1]

        y = (y_val[-1] - x[-1][-1]) / x[-1][-1] * 100.0

        return x, y


if __name__ == "__main__":
    df = pd.read_csv("datasets/crypto_combine.csv")
    dataset = PriceDataset(df)
    print(dataset[0])  # Should print a tuple containing x
    print(dataset[0][0].shape)  # Should print (64, 4)
    print(dataset[0][1].shape)  # Should print (1, 4)
