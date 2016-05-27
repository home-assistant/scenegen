#!/usr/bin/python3

import requests
import argparse
import configparser

def get_states(url, key):
  headers = {'x-ha-access': key}
  apiurl = url + "/api/states"
  r = requests.get(apiurl, headers=headers)
  return r.json()

def output_attrs(state, args):
  parts = state["entity_id"].split(".")
  type = parts[0]
  name = parts[1]
  if type == "light" and "light" in args.types:
    print ("  {}:".format(state["entity_id"]))
    print ("    state: {}".format(state["state"]))
    if 'brightness' in state["attributes"]:
      print("    brightness: {}".format(round(float(state["attributes"]['brightness']))))
    if 'xy_color' in state["attributes"] and args.colortype == 'xy_color':
      print("    xy_color: {}".format(state["attributes"]['xy_color']))
    if 'rgb_color' in state["attributes"] and args.colortype == 'rgb_color':
      print("    rgb_color: {}".format(state["attributes"]['rgb_color']))
    if 'color_temp' in state["attributes"] and args.colortype == 'color_temp':
      print("    color_temp: {}".format(state["attributes"]['color_temp']))
  if type == "switch" and "switch" in args.types:
    print ("  {}:".format(state["entity_id"]))
    print ("    state: {}".format(state["state"]))
  if type == "thermostat" and "thermostat" in args.types:
    print ("  {}:".format(state["entity_id"]))
  if type == "hvac" and "hvac" in args.types:
    print ("  {}:".format(state["entity_id"]))
    if 'operation_mode' in state["attributes"]:        
      print ("    operation_mode: {}".format(state["attributes"]["operation_mode"]))
    if 'temperature' in state["attributes"]:        
      print ("    temperature: {}".format(state["attributes"]["temperature"]))
    if 'fan_mode' in state["attributes"]:        
      print ("    fan_mode: {}".format(state["attributes"]["fan_mode"]))
    if 'swing_mode' in state["attributes"]:        
      print ("    swing_mode: {}".format(state["attributes"]["swing_mode"]))

  
def main():

  # Get command line args
  
  parser = argparse.ArgumentParser()

  parser.add_argument("url", help="url for Home Assistant instance")
  parser.add_argument("key", help="API Key of Home Assistant instance")
  parser.add_argument("-s", "--scenename", help="Name of scene to generate", default = "My New Scene")
  parser.add_argument("-m", "--mapfile", help="Name of mapfile to enable device filtering")
  parser.add_argument("-f", "--filter", help="Comma separated list of device collections as defined in mapfile")
  parser.add_argument("-c", "--colortype", help="color type to use", default = "color_temp", choices= ["xy_color", "rgb_color", "color_temp"])
  parser.add_argument("-t", "--types", help="list of device types to include", default = "light,switch")
  args = parser.parse_args()
  
  devices = {}
  if args.mapfile:
    config = configparser.ConfigParser()
    config.read_file(open(args.mapfile))
    for section in config.sections():
      devices[section] = {}
      for option in config.options(section):
        devices[section][option] = config.get(section, option)
  
  filters = []
  if args.filter:
    filters = args.filter.split(",")
  try:
    states = get_states(args.url, args.key)
    print("name: {}".format(args.scenename))
    for state in states:
      if args.mapfile:
        if args.filter:
          for filter in filters:
            if filter in devices and state["entity_id"] in devices[filter]:
              output_attrs(state, args)
        else:
          for section in devices:
            if state["entity_id"] in devices[section]:
              output_attrs(state, args)
      else:
        output_attrs(state, args)

  except:
    raise
 
if __name__ == "__main__":
    main()