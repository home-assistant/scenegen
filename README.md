# SceneGen

Scenegen is a scene generation tool for [Home Assistant](https://home-assistant.io/) home automation software. It creates scenes by example, by reading the current states of devices and outputting a corresponding scene. Scenegen is written in python using Home Assistant's RESTFul API so can be run from anywhere. It currently supports lights and switches only.

To set up SceneGen and install it locally, run the following from a shell in
the checkout:

    $ make

Then the script can be run locally from the checkout:

    $ ./bin/scenegen --help

See the Home Assistant documentation for [full usage instructions and
documentation](https://home-assistant.io/ecosystem/scenegen).
