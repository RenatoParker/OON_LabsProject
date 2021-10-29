import State
import json

with open("states.json", "r") as read_file:
    data = json.load(read_file)

print(data["states"])
dataState = data["states"]
print("tipo", type(dataState))
print(dataState)

with open("data_file.json", "w") as write_file:
    json.dump(data, write_file)

json_string = json.dumps(data)
print(type(json_string))

ordered = sorted(data)
with open("ordered_data_file.json", "w") as write_file:
    json.dump(ordered, write_file)

print(json.dumps(ordered, indent=4))

for state in dataState:
    state.pop("area_codes", None)

print(dataState)
with open("noCode_data_file.json", "w") as write_file:
    json.dump(dataState, write_file)
