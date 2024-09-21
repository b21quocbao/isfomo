# isfomo Backend Calling Convention

## Connection Test

- Path: `/isfomo/`
- Type: GET

## Sentiment Analysis

- Path: `/isfomo/STE`
- Type: POST
- Header: `Content-Type: application/json`
- Request Args:
  - `start_date`: String of the starting date, i.e. `2024-09-10`
  - `end_date`: String of the ending date, same as above
  - `asset_name`: Optional, `DOGE` or `TrumpCoin`
- Response Args:
  - `news`: List of news
    - `content`: Content of the news
    - `date`: Time when the news was published
  - `score`: A sentiment score of the news, representing the LLM's judge on it's social sentiment: 0-5 is negative, 6-7 is neutral, 7-10 is positive
  - `sentiment`: Count of each type of news
        `bad`: Negative ones
        `good`: Positive ones
        `neutral`: Neutral ones

For example,

```json
{
    "start_date": "2024-09-13",
    "end_date": "2024-09-19"
}
```

will return:

```json
{
    "news": [
        {
            "content": "Title: Elon Musk Is Getting Better at the Whole Oligarchy Thing\n\nA new report shows the tech billionaire recently bankrolled an effort to unseat a liberal district attorney in Texas.\n\nElon Musk has been monkeying around with the U.S. political system with increasing regularity. Another example of this unfortunate trend presented itself this week, with the Wall Street Journal repor\u2026 [+3716 chars]",
            "date": "2024-09-13T19:40:47Z"
        },
        {
            "content": "Title: Larry Ellison says he and Elon Musk 'begged' Jensen Huang for GPUs over dinner\n\nLarry Ellison said he and Elon Musk were \"begging\" Nvidia CEO Jensen Huang for GPUs over dinner at Nobu in Palo Alto.\n\nLarry Ellison and Elon Musk.Getty Images\r\n<ul><li>Larry Ellison said he and Elon Musk begged Nvidia's Jensen Huang for more GPUs at a dinner.</li><li>Ellison made the comment during Oracle's earnings\u2026 [+1994 chars]",
            "date": "2024-09-16T10:04:05Z"
        }
    ],
    "score": 4,
    "sentiment": {
        "bad": 39,
        "good": 23,
        "neutral": 3
    }
}
```

Another example:

```json
{
    "start_date": "2024-09-13",
    "end_date": "2024-09-19",
    "asset_name": "DOGE"
}
```

will return:

```json
{
    "news": [
        {
            "content": "Title: DOGE,GEGG & SHIB: 3 Cryptocurrencies Positioned To Generate Major Profits In September\n\nDogecoin (DOGE) has long been a favorite among meme coin enthusiasts and crypto whales, thanks to its massive community and frequent endorsements from figures like Elon Musk. However, as the market evolves, new contenders like GoodEgg (GEGG) are emerging, off\u2026\n\nDogecoin (DOGE) has long been a favorite among meme coin enthusiasts and crypto whales, thanks to its massive community and frequent endorsements from figures like Elon Musk. However, as the market e\u2026 [+3739 chars]",
            "date": "2024-09-13T12:00:31Z"
        },
        {
            "content": "Title: Elon Musk spent hundreds of thousands of dollars trying to unseat a Texas prosecutor, report says. It didn't work.\n\nTesla CEO Elon Musk funneled money to a PAC to oppose Jose\u0301 Garza in Texas, The Wall Street Journal reported, but it failed to make a difference.\n\nElon Musk channeled hundreds of thousands of dollars to a Texas PAC to try to unseat a Texas prosecutor, per The Wall Street Journal.Jared Siskin/Patrick McMullan via Getty Images\r\n<ul><li>Elon Musk \u2026 [+2389 chars]",
            "date": "2024-09-13T12:50:29Z"
        }
    ],
    "score": 5,
    "sentiment": {
        "bad": 22,
        "good": 19,
        "neutral": 2
    }
}
```

## GET Sentiment Analysis

- PATH: `/recent/<asset_name>`
- Request Args:
  - `asset_name`: Required, either `DOGE` or `TrumpCoin`
- Response Args:
  - `data`: Same to `score` above

For example,

```
/recent/DOGE
```

will return:

```json
{
  "data": 6
}
```
