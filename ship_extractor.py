import pathlib
import os
import sys
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import tkinter.messagebox as box


# Globals, used to control automatic naming
ships = []
name_info = []
variants = []
base = []
name_to_var = IntVar()
model_filter = StringVar()
name_filter = StringVar()
single = StringVar()

def load_file(path:str):
    """
    Parses an ES data file/save game into a set of nodes for internal use.\n
    parameter: path: path to the data file to parse.\n
    returns: data: list of dataNodes of [indent level, node 1, node 2, ...].
    """
    file = open(path, "r")
    text = file.read().split("\n")  # Separate the file into individual lines for loading
    file.close()

    line_number = 0
    num_lines = len(text)
    data = []  # This stores indentation level and nodes struct: data = [ [indentation level, node 0, node 1, node 2, node 3, ...], [...], [...], ... ]

    for line_number in range(num_lines):
        line = num_lines[line_number]
        if line == "" or line.startswith("#") or line.isspace():  # Skip empty lines and comments
            continue
        indent_level = line.count("\t")  # This provides our indentation level, and strips whitespace
        line = line.strip()
        indent_level -= line.count("\t")
        if line.startswith("#"):  # deal with indented comments
            continue

        nodes = [line_number]  # Separate out the line into nodes and strip outer quotation marks
        if (not "\"" in line) and (not "'" in line) and (not "`" in line):  # lines without quotes are quick and easy, just knock out the comments as well
            nodes = (line.split("#")[0]).split(" ")
            nodes.insert(0, line_number)
        else:
            quoted = False
            word = ""
            for i in line:
                if i == "\"" or i == "'" or i == "`":
                    if not quoted:
                        quoted = i
                    elif i == quoted:
                        quoted = False
                        nodes.append(word)
                        word = ""
                    else:
                        word += i
                elif i == " ":
                    if len(word):
                        if quoted:
                            word += i
                        else:
                            nodes.append(word)
                            word = ""
                elif i == "#" and (not quoted):  # deal with ending quotes
                    if len(word):
                        nodes.append(word)
                    break
                else:
                    word += i
        data.append(nodes)  # This contains all the nodes and their indentation levels, they can now be placed into a hierarchy
    return data


def save_file(path:str, data:list):
    """
    Saves ES data into the format required by the game.\n
    parameter 1: path: The path in which to save the file.\n
    parameter 2: data: the data which to save in the file.\n
    returns: None.
    """

    if data == []:  # Don't save empty files
        return None
    text = ""
    for i in data:
        line = ""
        indent = data[i][0]
        nodes = data[i][1:]
        line += "\t" * indent  # add the appropriate indentation
        for j in nodes:
            if j.count(" "):  # Add quotes if needed
                if j.count("\""):
                    quotes = "`"
                else:
                    quotes = "\""
                line += quotes + j + quotes
            else:
                line += j + " "
        line += "\n"
        text += line
    
    file = open(path, "w")
    file.write(text)
    file.close()
    return None

def extract_ships(data:list):
    """
    Extracts a list of ships from the provided save game data.\n
    parameter: data: The data from which to extract the ship list.\n
    returns: list: A list of ships each a list of their attributes, each attribute is a list also including indent level
    """

    ships = []

    for i in range(len(data)):
        if (not data[i][0]) and data[i][1] == "ship":  # If not indented and is a ship (root) node
            indent = 1
            pos = i + 1
            ship = []
            while indent > 0:
                indent = data[pos][0]
                if data[pos][0] == 1 and data[pos][1] == "uuid":  # Filter out any garbage we don't need
                    continue
                elif data[pos][0] == 1 and data[pos][1] == "position":
                    continue
                elif data[pos][0] == 1 and data[pos][1] == "system":
                    continue
                elif data[pos][0] == 1 and data[pos][1] == "planet":
                    continue
                elif data[pos][0] == 1 and data[pos][1] == "crew":
                    continue
                elif data[pos][0] == 1 and data[pos][1] == "fuel":
                    continue
                elif data[pos][0] == 1 and data[pos][1] == "shields":
                    continue
                elif data[pos][0] == 1 and data[pos][1] == "hull":
                    continue
                elif indent:
                    ship.append(data[pos])  # If we get this far, we need to add it
            ships.append(ship)
    base = ships.pop(0)
    return ships, base

def extract_info(ships:list):
    """
    Extracts model and name of ships in the list.\n
    parameter: ships: The ship list.\n
    returns: list: each element is a dict of {"model": model, "name": name}
    """

    info = []

    for i in ships:
        model = ""
        name = ""
        for j in i:
            if j[0] == 0 and j[1] == "ship":
                model = j[1]
            elif j[0] == 1 and j[1] == "name":
                name = j[1]
        info.append({"model": model, "name": name})
    return info

def open_save():  # Called to open a save file, or any other ES data file containing ships
    global ships
    global name_info
    global base
    global name_to_var
    global model_to_base
    global model_filter
    global name_filter

    path = filedialog.askopenfilename()
    ships, base = extract_ships(load_file(path))

    name_info = extract_info(ships)

    title = path.split("/")[-1]
    root.title(title)
    box.showinfo("Save file", "Ships loaded from file.")
    root.event_generate("<<rebuild_filters>>")

def open_variants():  # Called to open a file of variants to append to the variants list
    global variants

    path = filedialog.askopenfilename()
    temp_variants = extract_ships(load_file(path))

    for i in temp_variants:
        variants.append(i)
    box.showinfo("Variants", "Variants loaded from file.")

def save_variants():  # Called to save variants
    global variants

    path = filedialog.asksaveasfilename()
    save_file(path, variants)
    box.showinfo("Variants", "Variants saved to file.")

def clear_ships():
    global ships
    global name_info
    global base

    clear = box.askyesno("Clear Ships", "Clear all ship data?")
    if clear:
        ships = []
        name_info = []
        base = []
        box.showwarning("Clear Ships", "Ship list cleared!")
        root.event_generate("<<rebuild_filters>>")

def clear_variants():
    global variants

    clear = box.askyesno("Clear Variants", "Clear all variant data?")
    if clear:
        variants = []
        box.showwarning("Clear Variants", "Variant list cleared!")

def exit_exe(Garbage = None):
    root.destroy()
    sys.exit()

def about(Garbage = None):
    about_text = "Ship to Variant Extractor Copyright (C) 2022 pilover100"
    about_text += "\nThis program is distributed under the GNU GENERAL PUBLIC LICENSE version 3"
    about_text += "\nThis program comes with ABSOLUTELY NO WARRANTY; for details read the license."
    about_text += "\nThis is free software, and you are welcome to redistribute it"
    about_text += "\nunder certain conditions; read the license for details."
    box.showinfo("About", about_text)

def null(Garbage = None):  # Literally does nothing, used to provide a function for items that don't need to call functions
    pass

def build_filters(Garbage = None):
    global name_info

    names = ["ANY"]
    models = ["ANY"]

    for i in name_info:  # Grab all the different names and models and add them to the filters
        if not i["name"] in names:
            names.append(i["name"])
        if not i["model"] in models:
            models.append(i["model"])

    model_filter_box["values"] = models
    name_filter_box["values"] = names

def convert():
    global ships
    global base
    global variants
    global name_info
    global model_filter
    global name_filter
    global single
    global name_to_var

    # First, filter down the list after a sanity check

    if not len(ships):
        box.showerror("No Ships!", "Error: There are no ships loaded!")

    temp_ships = []
    temp_name_info = []

    if model_filter.get() == "ANY" and name_filter.get() == "ANY":
        temp_ships = ships
        temp_name_info = name_info
    else:
        for i in range(len(name_info)):
            ship_info = name_info[i]
            if not(model_filter.get() == "ANY" or model_filter.get() == ship_info["model"]):  # Weed out those which don't match the filters
                continue
            elif not(name_filter.get() == "ANY" or name_filter.get() == ship_info["name"]):
                continue
            else:
                temp_ships.append(ships[i])
                temp_name_info.append(name_info[i])

    if not len(temp_ships):
        box.showerror("No matching ships", "Error: There are no ships matching these filters!")
        return None

    base_outfits = []  # Get outfits
    base_attributes = {}  # Get attributes
    base_hardpoints = []  # Get hardpoint locations
    base_engines = []  # Engine locations
    base_bays = []  # Bay locations
    base_loadout = []  # Get what's in the hardpoints
    base_die = []  # What happens when the ship dies (leaks and explosions)
    for i in range(len(base)):
        if base[i][1] == "outfits":
            pos = i + 1
            indent = 2
            while indent > 1:
                indent = base[pos][0]
                if len(base[pos]) > 2:
                    for j in range(base[pos][2]):
                        base_outfits.append(base[pos][1])
                elif indent > 1:
                    base_outfits.append(base[pos][1])
                pos += 1
        elif base[i][1] == "attributes":
            pos = i + 1
            indent = 2
            while indent > 1:
                indent = base[pos][0]
                if len(base[pos]) > 2:
                    base_attributes[base[pos][1]] = base[pos][2]
                elif indent > 1:
                    base_attributes[base[pos][1]] = True
                pos += 1
        elif base[i][1] == "engine":
            pos = i +1
            indent = 2
            x = base[i][2]
            y = base[i][3]
            engine = [["engine", x, y]]
            while indent > 1:
                indent = base[pos][0]
                if indent > 1:
                    engine.append(base[pos][1:])
                pos += 1
            base_engines.append(engine)
        elif base[i][1] == "bay":
            pos = i + 1
            indent = 2
            bay_type = base[i][2]
            x = base[i][3]
            y= base[i][4]
            bay = [["bay", bay_type, x, y]]
            while indent > 1:
                indent = base[pos][0]
                if indent > 1:
                    bay.append(base[pos][1:])
                pos += 1
            base_bays.append(bay)

    base_outfits.sort()  # So that we can compare

    for ship in temp_ships:
        # Find the ship details
        ship_outfits = []
        ship_attributes = {}
        ship_hardpoints = []
        ship_loadout = []
        outfits_unsorted = []
        for i in range(len(ship)):
            if ship[i][1] == "outfits":
                pos = i + 1
                indent = 2
                while indent > 1:
                    indent = ship[pos][0]
                    if indent > 1 and len(ship[pos]) > 2:
                        outfits_unsorted.append([ship[pos][1], ship[pos][2]])
                        for j in range(ship[pos][2]):
                            ship_outfits.append(ship[pos][1])
                    elif indent > 1:
                        outfits_unsorted.append([ship[pos][1]])
                        ship_outfits.append(ship[pos][1])
                    pos += 1
                ship_outfits.sort()
            elif base[i][1] == "attributes":
                pos = i + 1
                indent = 2
                while indent > 1:
                    indent = ship[pos][0]
                    if len(ship[pos]) > 2:
                        ship_attributes[ship[pos][1]] = ship[pos][2]
                    elif indent > 1:
                        ship_attributes[ship[pos][1]] = True
                    pos += 1


# Init window
root = Tk()
root.title("Ship to Variant Extractor")

root.columnconfigure(100, weight = 1)
root.rowconfigure(100, weight = 1)

root.bind("<<rebuild_filters>>", build_filters)  # Event bindings

# menubar
root.option_add("*tearOff", False)

menubar = ttk.Menu(root)

# File menu
menu_file = ttk.Menu(menubar)
menu_file.add_command(label = "Open Save/Data File", command = open_save)
menu_file.add_command(label = "Open Variants File", command = open_variants)
menu_file.add_command(label = "Save Ship Variants", command = save_variants)
menu_file.add_command(label = "Quit", command = exit_exe)

menubar.add_cascade(menu=menu_file, label = "File")

# Edit menu
menu_edit = ttk.Menu(menubar)
menu_edit.add_command(label = "Clear ship data", command = clear_ships)
menu_edit.add_command(label = "Clear variant data", command = clear_variants)

menubar.add_cascade(menu=menu_edit, label = "Edit")

# Misc menu items
menubar.add_command(label = "About", command = about)

root["menu"] = menubar

# Interface layout, it's all here somewhere!
option_frame = ttk.Frame(root)
option_frame.grid(row = 0, column = 0)

model_filter_label = ttk.Label(option_frame, text = "Ship Model Filter:")  # Labels
name_filter_label = ttk.Label(option_frame, text = "Ship Name Filter:")
name_variant_label = ttk.Label(option_frame, text = "Vessel Name --> Variant Name")
single_label = ttk.Label(option_frame, text = "Single Ship Only")

model_filter_label.grid(row = 0, column = 0)
name_filter_label.grid(row = 1, column = 0)
name_variant_label.grid(row = 0, column = 3)
single_label.grid(row = 1, column = 3)

# Button
convert_button = ttk.Button(option_frame, text = "Convert!", command = convert)
convert_button.grid(row = 2, column = 0, columnspan = 5)

# checkboxes
name_varient_box = ttk.Checkbutton(option_frame, variable = name_to_var, onvalue = 1, offvalue = 0, command = null)
single_box = ttk.Checkbutton(option_frame, variable = single, onvalue = 1, offvalue = 0, command = null)

name_varient_box.grid(row = 0, column = 4)
single_box.grid(row = 1, column = 4)

# comboboxes
model_filter_box = ttk.Combobox(option_frame, textvariable = model_filter)
name_filter_box = ttk.Combobox(option_frame, textvariable = name_filter)

model_filter_box.grid(row = 0, column = 1)
name_filter_box.grid(row = 1, column = 1)

model_filter_box["values"] = ("ANY")
name_filter_box["values"] = ("ANY")

root.geometry('600x400+5+40')
root.mainloop()
