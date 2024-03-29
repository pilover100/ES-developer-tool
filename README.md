# ES developer tools

This repo contains a selection of tools created by pilover100 designed to aid Endless Sky development by providing save editing functionality, image swizzle checks and more to come!

## Instructions for use:

Many of these tools are written in python 3, this means that you'll need a python interpreter to run them which can be found at [https://python.org](https://python.org). many tools also have other dependencies such as pygame (see below).

### Transpiling using Nuitka

*Some of these programs can be transpiled into C and compiled into a binary, but correct functionality is not guaranteed.*

All tools except win dev setup.py are compiled with each commit, [please see the actions tab for the latest builds](https://github.com/pilover100/ES-developer-tool/actions). Each run marked "CD" is an automated build of all the tools. to use just extract the tools (they may be in 2 levels of zip folders) and run the appropiate executable.

## Current dependencies:

pygame: install by running `python -m pip install pygame`
>required for colour swizzler.py

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
## *ship variant extractor.py*
---

This WIP tool allows for the extraction of save game ships as variants of a base ship specified.

---
## *win dev setup.py*
---

This tool downloads all the requirements for compiling ES on a windows computer. It requires admin permissions to run (though windows may launch UAC for these interactions) properly.
See the official ES compiling readme for more configuration info or ask in the ES discord.