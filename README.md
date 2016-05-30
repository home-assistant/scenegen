# SceneGen

Scenegen is a scene generation tool for [Home Assistant](https://home-assistant.io/) home automation software. It creates scenes by example, by reading the current states of devices and outputting a corresponding scene. Scenegen is written in python using Home Assistant's RESTFul API so can be run from anywhere. It currently supports lights and switches only.

## Basic Operation

```
usage: scenegen [-h] [-s SCENENAME] [-m MAPFILE] [-f FILTER]
                [-c {xy_color,rgb_color,color_temp,color_name}] [-t TYPES]
                url key

positional arguments:
  url                   url for Home Assistant instance
  key                   API Key of Home Assistant instance

optional arguments:
  -h, --help            show this help message and exit
  -s SCENENAME, --scenename SCENENAME
                        Name of scene to generate
  -m MAPFILE, --mapfile MAPFILE
                        Name of mapfile to enable device filtering
  -f FILTER, --filter FILTER
                        Comma separated list of device collections as defined
                        in mapfile
  -c {xy_color,rgb_color,color_temp,color_name}, --colortype {xy_color,rgb_color,color_temp,color_name}
                        color type to use
  -t TYPES, --types TYPES
                        list of device types to include
```

For basic operation just supply the url and api key on the command line and scenegen will output a list of all lights and switches with their attributes. Optionally use the `--scenename` flag to explicitly set the scenename.

```
$ scenegen https://<some url> <some api key>
name: My New Scene
entities:
  light.bedroom:
    state: on
    brightness: 28
  light.kitchen:
    state: off
  light.living_room:
    state: off
  light.bedside:
    state: on
    brightness: 125
    color_temp: 412
  light.office_level_29:
    state: on
    brightness: 28
```

This output can be cut and pasted into your configuration.yaml file as required (ensuring correct indentatation of course).

Scenegen supports all documented effects for lights including transitions and flash effects, however generally it is easier to run scenegen to get the basic setup and add any effects manually later.

Note that depending on the type of light there may be a delay in actually setting up its parameters and Home Assistant actually recieving that state. For instance, if you set a scene up with the Hue App, Home Assistant won't see those changes for up to 10 seconds. Turning on a ZWave light might not be seen for an entire poll interval. For this reason, its good practice to wait for a while after the scene is setup before running scenegen. Alternatively, perform all setup using the Home Assistant frontend and it will instantly have the required state for capture.

## Advanced Usage

For a more advanced way to use the output try the following. In configuration.yaml add the following line:

```
scene: !include_dir_list scenes
```

This will tell home assistant to look in the subdirectory `scenes` for yaml files containing scene information. Each file will be named for the scene it will create and should contain information formatted as above. Then simply run Scenegen and redirect its output to the scenes subdirectory:

```
$ scenegen https://<some url> <some api key> > scenes/my_new_scene.yaml
```

This will create a new scene called `my_new_scene` which will automatically be picked up by Home Assistant on the next restart.

## Colors

Scenegen allows colors to be captured, and in fact Home Assistant light entities store up to 4 different ways of specifying the colors. This is redundant for creating scenes so Scenegen picks 1 and goes with it. The default is `color_temp` but you can change this with the `--colortype` flag, supported options are xy_color, rgb_color, color_temp and color_name.

## Types

By default, Scenegen will list all lights and switches. To restrict the device type use the `--types` option and supply a comma separated list (no spaces) of types to output. e.g.:

```
scenegen https://<some url> <some api key> --types light,switch
```

or:

```
scenegen https://<some url> <some api key> --types light
```

This will make more sense as and when more types are added.

## Maps and Filters

Maps allow you to specify and label various subsets of devices that you want to work on together. A mapfile is specified using the `--mapfile` option and is a `.ini` style file consisting of section headers and entries. The section headers specify a region or zone or otherwise organized selection of entities you want to filter on, and it is mandatory to have at least one. If you create a map file like this:

```
[entities]
light.living_room
light.dining_room
```

If you run scenegen with the `--mapfile` argument pointing to that file you will only get output for the listed entities (the name of the section is irrelevant if not using the `--filter` option). A more complex mapfile might look like this:

```
[Outside]
light.porch
switch.path_lights
[Living Room]
light.living_room_front
light.living_room_back
[Bedroom]
light.bedside
```

Again, if you run with that map file it will output all of the entities listed, however you now have the possibility of restricting output devices based on the sections they are in, using the `--filter` option and supplying a comma separated list of sections you want to include, for instance:

```
scenegen https://<some url> <some api key> --mapfile map.cfg --filter "Outside,Living Room"
```

The intended use of the mapfile and filter is that you create a map of all your devices and organize them into zones that you are interested in creating scenes for and use the filter to limit output to that zone. For instance you might want to create 3 or 4 scenes for your living room, and once the map is set up you can easily do so without the addition of unwanted devices.

