import os
import json
from multithread import collect
import pprint
pp = pprint.PrettyPrinter(indent=2)



current_filepath = os.path.realpath(
  os.path.join(os.getcwd(), os.path.dirname(__file__))
) + '/'



def readJson(filepath):
    with open(filepath, 'rb') as file:
        return json.load(file, encoding = 'utf-8')


def main():
  config = readJson(current_filepath + 'config.json')
  credentials = readJson(current_filepath + 'credentials.json')
  ips = readJson(config['ips_filepath'])
  oids = readJson(current_filepath + 'oids.json')
  print(ips)
  print(oids)

  result = collect(ips, oids, credentials)

  pp.pprint(result)
  return result


if __name__ == "__main__":
    r = main()
