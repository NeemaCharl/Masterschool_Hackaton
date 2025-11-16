import json
player_id = {
    "Max": 1000
}

# only for the first run
def create_scoreboard(player_id, filename="scoreboard.json"):
    with open(filename, 'w') as json_file:
        json.dump(player_id, json_file, indent=4)

def load_scoreboard(filename="scoreboard.json"):
    try:
        with open(filename, 'r') as json_file:
            scoreboard = json.load(json_file)
    except FileNotFoundError:
        scoreboard = {}
    return scoreboard


create_scoreboard(player_id)
print(load_scoreboard())