# Telegram polls summarizer

This is a simple `python` script that can be used to count how often users participated
in polls in a group chat and how often they picked the right answers.

Only possible for non-anonymous polls obviously.

## Setup

First, install the necessary packages with:
```shell
pip install -r ./requirements.txt
```

To use `telethon`, follow its guide on how to set up a telegram app
[here](https://docs.telethon.dev/en/stable/basic/signing-in.html).

Rename the `.env.example` to `.env` and paste the `app_id` and `app_hash` into it.

Run `python bot.py --get-chat-ids` to get a list of all your current chat group
IDs and look for the one that you want to analyze. Copy the ID (likely negative)
into the `.env` file as `CHAT_ID`.

## Run

Simply run `python bot.py` with the correct `python` environment.
