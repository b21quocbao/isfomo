import os
import sys
import time
import argparse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd

from datetime import datetime, timedelta
from tqdm import tqdm
from flask import Flask, request, jsonify
from feelLLM.src.model_gaianet import GaiaNetCausalModelForClassification
from feelLLM.src.NewsAPI import get_news
import hashlib

app = Flask(__name__)
tqdm.pandas()


def compute_sha256(input_string: str) -> str:
    sha256_hash = hashlib.sha256()

    sha256_hash.update(input_string.encode("utf-8"))

    return sha256_hash.hexdigest()


def asset_info(asset_name: str) -> str:
    if (
        "doge" in asset_name.lower()
        or "dogecoin" in asset_name.lower()
        or "musk" in asset_name.lower()
        or "elon" in asset_name.lower()
    ):
        return "Dogecoin is a cryptocurrency that was created as a joke in 2013. It has since gained popularity and has a large community of supporters. The price of Dogecoin has been known to be volatile and is often influenced by social media trends and celebrity endorsements. Dogecoin has a unique culture and community, with a strong emphasis on charity and fun. The Dogecoin community has been involved in various charitable initiatives and fundraising efforts. Overall, Dogecoin has a dedicated following and a strong sense of community, which has contributed to its lasting popularity and relevance in the cryptocurrency space. Elon Musk is one of the richest people in the world. Conversely, if he expresses skepticism or negativity towards Doge, it can result in a sharp decline in its price. His statements often draw attention to Dogecoin, making it a trending topic, which can attract more retail investors. This raises concerns about the ethical implications of a single individual's influence over a cryptocurrency's value.His endorsement can lend credibility to DOGE, potentially leading to greater acceptance and usage in transactions.In summary, Elon Musk's statements and actions can significantly impact Dogecoin's price through market sentiment, public interest, and potential market manipulation risks. His influence can either lead to price surges or declines, making the relationship between his news and Dogecoin prices complex and multifaceted."
    if (
        "donald" in asset_name.lower()
        or "trump" in asset_name.lower()
        or "trumpcoin" in asset_name.lower()
    ):
        return "Donald Trump is a former President of the United States and a prominent public figure. His statements and actions have the potential to influence public opinion and market sentiment. Trump's tweets and public statements have been known to impact financial markets, including cryptocurrencies. There is a strong correlation between Trump's statements and the price movements of assets like Bitcoin, Dogecoin and TrumpCoin on Solana. Trump's endorsement or criticism of a cryptocurrency can lead to significant price fluctuations. His influence on the market is driven by his large following and the media attention his statements receive. Trump's impact on the cryptocurrency market is a reflection of his broader influence on public discourse and market sentiment. TrumpCoin (DTC) is a cryptocurrency that was created to support the political agenda of former President Donald Trump. The coin was launched in 2016 as a digital currency for Trump supporters and conservative investors. TrumpCoin aims to promote the policies and initiatives of the Trump administration through blockchain technology. The coin's value and popularity are influenced by political events, public sentiment, and media coverage related to Donald Trump. TrumpCoin has a dedicated community of supporters who believe in the coin's mission and vision. The coin's price and market performance are closely tied to developments in US politics and the conservative movement. TrumpCoin's success is linked to the political landscape and the public's perception of Donald Trump and his policies."


args_parser = argparse.ArgumentParser()
args_parser.add_argument(
    "--data_path",
    type=str,
    default="precomputed_sentiments.csv",
)

# Initialize the model once
model = GaiaNetCausalModelForClassification()

try:
    args = args_parser.parse_args()
    df = pd.read_csv(args.data_path, index_col="nid")
except Exception as e:
    print(f"[ERROR] Failed to load precomputed sentiments: {e}")

    df: pd.DataFrame = pd.DataFrame(
        columns=[
            "nid",  # format: str, unique identifier
            "Date",  # format: 2021-01-01T00:00:00
            "Content",  # format: string
            "Source",  # format: string
            "Asset",  # format: string (DOGE/TrumpCoin)
            "Sentiment",  # format: string (good/bad/neutral)
        ],
    )

    # Sample data for demonstration
    df = pd.concat(
        [
            df,
            pd.DataFrame(
                {
                    "nid": ["1", "2", "3"],
                    "Date": [
                        "2021-01-01T00:00:00",
                        "2021-01-02T00:00:00",
                        "2021-01-03T00:00:00",
                    ],
                    "Content": [
                        "I love DOGE",
                        "I hate DOGE",
                        "DOGE is ok, but nothing special",
                    ],
                    "Source": ["Twitter", "Reddit", "Facebook"],
                    "Asset": ["DOGE", "DOGE", "DOGE"],
                    "Sentiment": ["good", "bad", "neutral"],
                }
            ),
        ]
    )

    df.set_index("nid", inplace=True)

###########################################
########## Fetch External News ############
###########################################

# 30 days doge coin news
time.sleep(1)
API_KEY = os.getenv("NEWSAPI_KEY", "YOUR_API_KEY")
news = get_news(API_KEY, "Dogecoin", 30, "relevancy")
for news_item in news:
    url_plus_date = f"{news_item['url']}_{news_item['publishedAt']}"
    nid = compute_sha256(url_plus_date)

    if nid in df.index:
        continue

    _df: pd.DataFrame = pd.DataFrame(
        {
            "nid": [nid],
            "Date": [news_item["publishedAt"]],
            "Content": [
                f"Title: {news_item['title']}\n\n{news_item['description']}\n\n{news_item['content']}"
            ],
            "Source": [news_item["source"]],
            "Asset": ["DOGE"],
            "Sentiment": [None],
        }
    )
    _df.set_index("nid", inplace=True)
    df = pd.concat([df, _df])

# 30 days Elon Musk news
time.sleep(1)
API_KEY = os.getenv("NEWSAPI_KEY", "YOUR_API_KEY")
news = get_news(API_KEY, "musk", 30, "relevancy")
for news_item in news:
    url_plus_date = f"{news_item['url']}_{news_item['publishedAt']}"
    nid = compute_sha256(url_plus_date)

    if nid in df.index:
        continue

    _df: pd.DataFrame = pd.DataFrame(
        {
            "nid": [nid],
            "Date": [news_item["publishedAt"]],
            "Content": [
                f"Title: {news_item['title']}\n\n{news_item['description']}\n\n{news_item['content']}"
            ],
            "Source": [news_item["source"]],
            "Asset": ["DOGE"],
            "Sentiment": [None],
        }
    )
    _df.set_index("nid", inplace=True)
    df = pd.concat([df, _df])

# 30 days Donald Trump news
time.sleep(1)
API_KEY = os.getenv("NEWSAPI_KEY", "YOUR_API_KEY")
news = get_news(API_KEY, "Trump", 30, "relevancy")
for news_item in news:
    url_plus_date = f"{news_item['url']}_{news_item['publishedAt']}"
    nid = compute_sha256(url_plus_date)

    if nid in df.index:
        continue

    _df: pd.DataFrame = pd.DataFrame(
        {
            "nid": [nid],
            "Date": [news_item["publishedAt"]],
            "Content": [
                f"Title: {news_item['title']}\n\n{news_item['description']}\n\n{news_item['content']}"
            ],
            "Source": [news_item["source"]],
            "Asset": ["TrumpCoin"],
            "Sentiment": [None],
        }
    )
    _df.set_index("nid", inplace=True)
    df = pd.concat([df, _df])

# 30 days TrumpCoin news
time.sleep(1)
API_KEY = os.getenv("NEWSAPI_KEY", "YOUR_API_KEY")
news = get_news(API_KEY, "TrumpCoin", 30, "relevancy")
for news_item in news:
    url_plus_date = f"{news_item['url']}_{news_item['publishedAt']}"
    nid = compute_sha256(url_plus_date)

    if nid in df.index:
        continue

    _df: pd.DataFrame = pd.DataFrame(
        {
            "nid": [nid],
            "Date": [news_item["publishedAt"]],
            "Content": [
                f"Title: {news_item['title']}\n\n{news_item['description']}\n\n{news_item['content']}"
            ],
            "Source": [news_item["source"]],
            "Asset": ["TrumpCoin"],
            "Sentiment": [None],
        }
    )
    _df.set_index("nid", inplace=True)
    df = pd.concat([df, _df])

###########################################
########## Fetch External News ############
###########################################


# Precompute sentiments only once
def compute_sentiments():
    for idx, row in tqdm(df.iterrows(), total=len(df)):
        if row["Sentiment"] not in ["good", "bad", "neutral"]:
            prompt = model.prompt(
                info_text=row["Content"],
                asset_name=row["Asset"],
                asset_info=asset_info(row["Asset"]),
            )
            status_code, sentiment = model.classify(prompt)

            if status_code != 200:
                print(f"[WARNING] Failed to classify sentiment for {row['nid']}")
                sentiment = "unknown"  # Handle classification fail

            df.loc[idx, "Sentiment"] = sentiment


@app.route("/", methods=["GET"])
def index():
    return "Welcome to the Sentiment Analysis API!"


@app.route("/STE", methods=["POST"])
def analyze_sentiment():
    data = request.json

    if "start_date" not in data or "end_date" not in data:
        return jsonify({"error": "start_date and end_date are required"}), 400

    date_format: str = "%Y-%m-%d"
    datetime_format: str = "%Y-%m-%dT%H:%M:%S"
    start_date: datetime = datetime.strptime(data["start_date"], date_format)
    end_date: datetime = datetime.strptime(data["end_date"], date_format)

    try:
        asset_name: str = data["asset_name"]

        filtered_df = df[
            (df["Date"] >= start_date.strftime(datetime_format))
            & (df["Date"] <= end_date.strftime(datetime_format))
            & (asset_name == df["Asset"])
        ]
    except:
        filtered_df = df[
            (df["Date"] >= start_date.strftime(datetime_format))
            & (df["Date"] <= end_date.strftime(datetime_format))
        ]

    sentiment_counts = filtered_df["Sentiment"].value_counts().to_dict()

    x: int = sentiment_counts.get("good", 0)
    y: int = sentiment_counts.get("bad", 0)
    z: int = sentiment_counts.get("neutral", 0)
    score: int = round(5.5 + 4.5 * (x - y) / (x + y + z))
    news_list: list[dict] = []

    if score == 5 or score == 6:
        # pick a good & a bad from the date range
        news1 = filtered_df[filtered_df["Sentiment"] == "good"].sample(1)
        news2 = filtered_df[filtered_df["Sentiment"] == "bad"].sample(1)
    elif score >= 7:
        # pick two goods from the date range
        news1 = filtered_df[filtered_df["Sentiment"] == "good"].sample(1)
        news2 = filtered_df[filtered_df["Sentiment"] == "good"].sample(1)
    else:
        # pick two bads from the date range
        news1 = filtered_df[filtered_df["Sentiment"] == "bad"].sample(1)
        news2 = filtered_df[filtered_df["Sentiment"] == "bad"].sample(1)

    news_list: list[dict] = [
        {
            "content": news1["Content"].values[0],
            "date": news1["Date"].values[0],
        },
        {
            "content": news2["Content"].values[0],
            "date": news2["Date"].values[0],
        },
    ]

    response = {
        "sentiment": {
            "good": x,
            "bad": y,
            "neutral": z,
        },
        "score": score,
        "news": news_list,
    }

    return jsonify(response)


@app.route("/recent/<asset_name>", methods=["GET"])
def recent_analyze_sentiment(asset_name: str):
    data: dict = {"asset_name": asset_name}

    datetime_format: str = "%Y-%m-%dT%H:%M:%S"

    start_date: str = datetime.now() - timedelta(days=7)
    end_date: str = datetime.now()

    print(start_date)
    print(end_date)
    print(data["asset_name"])

    try:
        asset_name: str = data["asset_name"]

        filtered_df = df[
            (df["Date"] >= start_date.strftime(datetime_format))
            & (df["Date"] <= end_date.strftime(datetime_format))
            & (asset_name == df["Asset"])
        ]
    except:
        filtered_df = df[
            (df["Date"] >= start_date.strftime(datetime_format))
            & (df["Date"] <= end_date.strftime(datetime_format))
        ]

    sentiment_counts = filtered_df["Sentiment"].value_counts().to_dict()

    x: int = sentiment_counts.get("good", 0)
    y: int = sentiment_counts.get("bad", 0)
    z: int = sentiment_counts.get("neutral", 0)
    try:
        score: int = round(5.5 + 4.5 * (x - y) / (x + y + z))
    except:
        score: int = 0

    response = {
        "data": score,
    }

    return jsonify(response)


if __name__ == "__main__":
    print("Precomputing sentiments...")
    compute_sentiments()
    df.to_csv(args.data_path, index=True)
    print("Sentiments precomputed!")

    app.run(debug=True)
