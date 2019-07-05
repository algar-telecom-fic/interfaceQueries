import json
import os

current_filepath = os.path.realpath(
  os.path.join(os.getcwd(), os.path.dirname(__file__))
) + '/'

def main():
  config = read_json(current_filepath + 'config.json')
  ips = read_json(config['ipsFilepath'])

def readJson(filepath):
  with open(filepath, 'rb') as file:
    return json.load(file, encoding = 'utf-8')

main()