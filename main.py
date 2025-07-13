from geopy.distance import geodesic as dist
import requests
import tomllib
from os import system
try: 
    with open("config.toml", "rb") as f:
        info = tomllib.load(f)
except:
    input("config.toml doesn't exist. Make sure to have config.toml in the same folder as the script. Press Enter to exit.")
    exit(1)
result = requests.post("https://bonk2.io/scripts/login_legacy.php", info["login"]).json()
if result["r"] != "success":
    if result["e"] == "password":
        input("Incorrect password. Make sure you specified the correct username and password in config.toml. Press Enter to exit.")
    elif result["e"] == "username_fail":
        input("Incorrect username. Make sure you specified the correct username and password in config.toml. Press Enter to exit.")
    exit()
token = result["token"]
print("Getting rooms...")
rooms = requests.post("https://bonk2.io/scripts/getrooms.php", {"token": token, "version": 49, "gl": "y"}).json()
gamemodes = {"sp": "Grapple", "b": "Classic", "ar": "Arrows", "ard": "Death Arrows", "f": "Football", "v": "VTOL"}
roomlist = []
roomlistsort = []
cols = 6
length = []
columns = ["Roomname", "Gamemode", "Players", "Region", "lvl", "km"]
for i in range(cols): length.append(len(columns[i]))
for a in rooms["rooms"]:
    if a["password"] and info["config"]["hidepassworded"]: continue
    if a["maxplayers"] == a["players"] and info["config"]["hidefull"]: continue
    distance = int(dist((rooms["lat"], rooms["long"]), (a["latitude"], a["longitude"])).km)
    roomlist.append([a["roomname"], gamemodes[a["mode_mo"]], str(a["players"]) + "/" + str(a["maxplayers"]), a["country"], a["minlevel"], distance])
    for i in range(cols):
        l = len(str(roomlist[-1][i]))
        if length[i] < l: length[i] = l
if length[0] > 20: length[0] = 20
roomlist = sorted(roomlist, key=lambda d: d[info["config"]["sortby"] - 1])
for b in range(cols):
    if b == (cols - 1): end="\n"
    else: end="│"
    print(columns[b].center(length[b], " "), end=end)
for b in range(cols):
    if b == (cols - 1): end="\n"
    else: end="┼"
    print("─" * length[b], end=end)
for a in roomlist:
    for b in range(cols):
        if b == (cols - 1): end="\n"
        else: end="│"
        item = str(a[b])
        if b == 0:
            if len(item) > 20:
                print(item[:17] + "...", end=end)
            else:
                print(item.ljust(length[b], " "), end=end)
        else:
            print(item.center(length[b], " "), end=end)