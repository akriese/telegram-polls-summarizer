import dotenv
import os
import sys

from telethon import TelegramClient, functions

dotenv.load_dotenv()

def get_env_var(var):
    res = os.getenv(var)
    if res is None:
        print(f"Variable {var} not in environemt!")
        sys.exit(1)
    return res

API_ID = int(get_env_var("API_ID"))
API_HASH = get_env_var("API_HASH")
CHAT_ID = int(get_env_var("CHAT_ID"))

def id_to_name(id, users):
    for u in users:
        if u.id == id:
            if u.first_name:
                if u.last_name:
                    return f"{u.first_name} {u.last_name}"
                return u.first_name
            if u.username:
                return u.username

    return ""

async def main(client):
    # shape of a key: user id
    # shape of a value: dict: username and points as entries
    user_points = {}

    # iterate over all messages in the chat, filtering for polls
    async for m in client.iter_messages(CHAT_ID):
        if m.poll is None:
            continue

        # request poll vote details
        result = await client(functions.messages.GetPollVotesRequest(
            peer=CHAT_ID,
            id=m.id,
            limit=100,
        ))
        if result is None:
            raise Exception()

        # find the answer marked correct
        correct_answer = -1
        for answer in m.poll.results.results:
            if answer.correct:
                correct_answer = answer.option
                break
        else:
            raise Exception("None of the answers seem correct!")

        # print(correct_answer, result.votes, result.users)

        # iterate over the votes, save points and attemps to a dict
        for vote in result.votes:
            id = vote.user_id
            if id not in user_points:
                user_points[id] = {
                    "points": 0,
                    "attempts": 0,
                    "name": id_to_name(id, result.users)
                }

            user_points[id]["attempts"] += 1
            if vote.option == correct_answer:
                user_points[id]["points"] += 1

    # sort dict's entries by points and print them nicely
    list_of_players = list(user_points.items())
    list_of_players.sort(key=lambda arr: arr[1]["points"])

    strings = []
    for arr in list_of_players:
        p, a = arr[1]["points"], arr[1]["attempts"]
        strings.append(f'{arr[1]["name"]}: {p}/{a} ({p/a:.3f})')

    print("\n".join(strings))


if __name__ == "__main__":
    client = TelegramClient('my_session', API_ID, API_HASH)
    client.start()

    with client:
        client.loop.run_until_complete(main(client))

