"""
ship variant extractor
(C) pilover100#5368
"""

import os
import pathlib
from sys import platform

instructions = "This is the pi ship variant extractor.\n"
instructions += "In the file to parse, please ensure that each ship has a unique name.\n"
instructions += "The pi ship name tool can also help with this if required.\n"
instructions += "Then please follow the prompts below to extract your variants.\n"


print(instructions)
file_name = input("Enter save file name including extension: ")

# Windows version
if platform.startswith("win32"):
    path = str(pathlib.Path.home()) + "/AppData/Roaming/endless-sky/saves/" + file_name

# Linux version
elif platform.startswith("linux"):
    path = os.path.join("~/.local/share/endless-sky/saves", file_name)

else:  # Misc/Apple/unknown version
    path_start = input("Please enter the path to the saves directory: ")
    path = os.path.join(path_start, file_name)

file = open(path, "r")
text = file.read().split("\n")
file.close()

ship_section = text.index("# What you own:") + 1  # This finds the index of the first player ship in the file
pos = ship_section

ship_lines = []
ship_models = {}
sorting_ships = True
while sorting_ships: # This finds the next ship node
    if "ship " in text[pos] and (not "\t" in text[pos]):  # must be a root node, can't be indented
        model = " ".join((text[pos].split(" "))[1:])  # Extract the model of the ship itself
        model = model.replace("\"", "")  # Remove any quotes around ship models
        ship_lines.append(pos)  # save the starting index of the ship definition
        if model in ship_models:
            ship_models[model] += 1
        else:
            ship_models[model] = 1
    elif (not "\t" in text[pos]) and len(text[pos]) >= 1:  # If we are no longer in player ships, we're done here
        sorting_ships = False
        ship_lines.append(pos)
    pos += 1  # Move forwards through the file

    
print("Ships loaded into memory!\n")

print("Available models:")
for key in ship_models:
    print(f"{key}: {ship_models[key]} ships")
model = input("\nEnter the ship model you'd like to make variants of: ")


ships = []
block = []
names = []

for i in range(len(ship_lines)):
    if i == len(ship_lines) - 1:
        break
    start = ship_lines[i]
    end = ship_lines[i+1]
    if not model in text[start]:  # Skip over other ships
        continue
    block = text[start:end]

    vessel = []
    for line in block:  # Filter out stuff that isn't part of variants, or will influence the names of variants
        if not ("\tsystem " in line or "\tplanet " in line or line.startswith("\tshields") or line.startswith("\thull") or line.startswith("\tcrew") or line.startswith("\tfuel") or line.startswith("\tposition") or line.startswith("\tuuid")):
            vessel.append(line)
    ships.append(vessel)
    
    temp_text = block[1].replace("\t", "")
    name_parts = temp_text.split(" ")[1:]
    name = ""
    for i in name_parts:  # This pieces back together long names with white space in
        name += i + " "
    name = name.replace("\"", "")  # Remove quotes
    name = name.strip()
    names.append(name)

print("Vessels:")
for i in names:
    print(i)

base_name = input("\nEnter the name of the ship to use as the base ship for reference: ")

base = ships[names.index(base_name)]

variants = {}

def extract_info(vessel):
    outfits = []
    engines = []
    weapon_hard = []
    weapon_bays = []
    bays = []
    name = names[ships.index(vessel)]
    pos = 0
    loading_outfits = True
    while loading_outfits:
        if vessel[pos].startswith("\toutfits"):
            i = 1
            while True:
                line = vessel[pos + i]
                indent = line.count("\t")
                if indent != 2:
                    break
                line = line.strip()
                outfits.append(line)
                i += 1
            loading_outfits = False
        pos += 1
    for pos in range(len(vessel)):
        if vessel[pos].startswith("\tengine ") or vessel[pos].startswith('\t"reverse engine" '):
            i = 0
            while True:
                line = vessel[pos + i]
                indent = line.count("\t")
                if indent != 2:
                    break
                engines.append(line)
                i += 1
        pos += 1
    pos = 0
    loading_attributes = True
    while loading_attributes:
        break
    pos = 0
    loading_bays = True
    while loading_bays:
        break
    pos = 0
    for pos in range(len(vessel)):
        if vessel[pos].startswith("\tgun ") or vessel[pos].startswith("\tturret "):
            i = 0
            turret = vessel[pos].startswith("\tturret ")
            while True:
                line = vessel[pos + i]
                indent = line.count("\t")
                if indent != 2:
                    break
                if line.startswith("\tgun ") or line.startswith("\tturret "):  # Fishes out the installed weapon
                    parts = (line.strip()).split(" ")
                    installed_weapon = ""
                    try:
                        installed_weapon_parts = parts[3:]
                        for i in installed_weapon_parts:
                            installed_weapon += i
                    except:
                        pass
                    weapon_bays.append([installed_weapon, turret])
                    weapon_hard.append("\t" + parts[0] + parts[1] + parts[2])
                else:
                    weapon_hard.append(line)
                i += 1
        pos += 1
    return name, {"outfits": outfits, "engines": engines, "weapons": weapon_bays, "weapon hards": weapon_hard}

name, base_info = extract_info(base)  # Name is used just to satisfy assignment of variables,the var isn't actually used for anything productive

for vessel in ships:  # Extracts the information inside, then outputs it into variants if things differ
    if vessel != base:
        pass
    else:  # Skip doing the base ship
        continue
    name, info = extract_info(vessel)

    for key in info:
        if info[key] != base_info[key]:
            if name in variants:
                variants[name][key] = info[key]
            else:
                variants[name] = {key: info[key]}

output = ""

for vessel in variants:
    header = "ship \"" + model + "\" \"" + model + " (" + vessel + ")\"\n"
    body = ""
    if "outfits" in variants[vessel]:
        body += "\toutfits\n"
        for outfit in variants[vessel]["outfits"]:
            body += "\t\t" + outfit + "\n"
    if "engines" in variants[vessel]:
        for line in variants[vessel]["engines"]:
            body += line + "\n"
    if "weapons" in variants[vessel]:
        for weapon in variants[vessel]["weapons"]:
            if weapon[1]:
                body += "\tturret " + weapon[0] + "\n"
            else:
                body += "\tgun" + weapon[0] + "\n"
    if "weapon hards" in variants[vessel] and (not "weapons" in variants[vessel]):
        count = 0  # Counter to ensure that weapons mounted and the hardpoints tie up
        for line in variants[vessel]["weapon hards"]:
            if line.startswith("\tgun ") or line.startswith("\tturret "):
                body += line + " " + variants[vessel]["weapons"][count][0] + "\n"
                count += 1
            else:
                body += line + "\n"


    if not body in output:  # Anti-duplicate checker
        output += header + body
    else:
        print(f"Warning: \"{vessel}\" is a duplicate of another ship in the save file, skipping over...")

print("\n" + output + "\n")

filename = input("Enter save location and filename: ")
file = open(filename, "w")
file.write(output)
file.close()
print("Done!\nIf you are aiming to get these variants into vanilla, please ensure that the data output matches the existing style of variant definitions.")
