#!/usr/bin/python3

import requests
import argparse

#from requests.packages.urllib3.exceptions import InsecureRequestWarning
#requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def get_states(url, key):
  headers = {'x-ha-access': key}
  apiurl = url + "/api/states"
  r = requests.get(apiurl, headers=headers)
  return r.json()
  
def main():

  # Get command line args
  
  parser = argparse.ArgumentParser()

  parser.add_argument("url", help="url for Home Assistant instance")
  parser.add_argument("key", help="API Key of Home Assistant instance")
  parser.add_argument("-s", "--scenename", help="Name of scene to generate", default = "My New Scene")
  parser.add_argument("-c", "--colortype", help="color type to use", default = "color_temp", choices= ["xy_color", "rgb_color", "color_temp"])
  args = parser.parse_args()
  
  try:

    states = get_states(args.url, args.key)
    print("name: {}".format(args.scenename))
    for state in states:
      parts = state["entity_id"].split(".")
      type = parts[0]
      name = parts[1]
      if type == "light" or type == "switch":
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
  except:
    raise
 
if __name__ == "__main__":
    main()