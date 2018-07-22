# CLHue

## What is CLHue?
CLHue is a Python library + command line interface that allows a developer to interact with a [Philips Hue](https://www2.meethue.com/en-us) lighting system:
* Turn on/off lights
* Change colors
* Change brightness
* Manage groups of lights (like all lights in the Living Room, for example)

## How did CLHue come about?
I was interested in building something that would let me interact with my Hue lights in a programmatic way that could be scripted. I also figured it'd be a great way to learn more about how to interact with an API and expand on my Python programming skills. It started off as a command-line interpreter but has quickly turned into a library that I've used for other projects, such as pushing my Hue light statistics to an InfluxDB instance that could then be graphed with Grafana.

## This looks neat! How do I use it?
It's still pretty custom-built to be used for my own Hue. To use it for your own Hue, you'd have to edit a few things:
* The broadcast address in ConfigHandler.py to be that of your own network
* The username in HueInteract.py to be your own API token
* Optionally, the name in clHue.py

I do plan on abstracting out these values so it can be easily used by anyone else, though. :)

## What other features are planned?
Whatever comes to mind, mostly! I still need to build out the color changing features in HueInteract.py. I also want to build something like a "piano" of sorts that lets you mash buttons on a keyboard that have different lighting effects!
