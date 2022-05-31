# ES developer tools

This repo contains a selection of tools created by pilover100 designed to aid Endless Sky development by providing save editing functionality, image swizzle checks and more to come!

## Instructions for use:

Many of these tools are written in python 3, this means that you'll need a python interpreter to run them which can be found at [https://python.org](https://python.org). many tools also have other dependencies such as pygame (see below).

### Transpiling using Nuitka

*Some of these programs can be transpiled into C and compiled into a binary, but correct functionality is not guaranteed.*

## Current dependencies:

pygame: install by running `python -m pip install pygame`
>required for colour swizzler.py

TkInter: bundled with the python distribution, install by selecting the option for `TkInter` when installing the interpreter
>required for ship_extractor.py

---
## *colour swizzler.py*
---

This tool allows you to load an image (most image types are supported, varies between python installations, `.bmp` images will always work.) and to alter the swizzle which is displayed.

Follow the prompts at the top of the screen to use and most of all, be patient.

It's only written in python (which is quite slow) and the image usually takes a second or 2 to form.

You can see your current image path and swizzle at the bottom of the screen, you can use backspace to clear any mistakes and the escape key exits the program.

---
## *ship name tool.py*
---

This tool is a command line save game editor that allows you to bulk rename ships, either effecting your entire fleet or ship of a specific model.

Menus are navigable by entering option numbers and responding to text prompts.

The tool is case sensitive so you **must** enter models exactly as the data files define them for the tool to match them.

In the future I will replace this tool with a better GUI version powered by TkInter (ToolKit Interface) which will make it much more user friendly and easier to use.

---
## *ship_extractor.py*
---

This WIP tool allows for the extraction of save game ships as variants or a base ship (the flagship, or first ship, in the save file provided)