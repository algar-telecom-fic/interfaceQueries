import json
import os
import subprocess
import sys

current_filepath = os.path.realpath(
  os.path.join(os.getcwd(), os.path.dirname(__file__))
) + '/'
info = {}
snmpCommunity = sys.argv[1]

def main():
  config = readJson(current_filepath + 'config.json')
  ips = readJson(config['ipsFilepath'])
  for ip in ips:
    info[ip] = []
    output = localAccessRun([
      '/usr/bin/snmpwalk',
      '-v', '2c',
      '-c', snmpCommunity,
      ip, '.1.3.6.1.2.1.2.2.1.2'
    ]).stdout.decode('utf-8')
    for line in output.split('\n'):
      print(line)
    # ~ info[ip]['desc'] = output

def readJson(filepath):
  with open(filepath, 'rb') as file:
    return json.load(file, encoding = 'utf-8')
    
def localAccessRun(command):
  return subprocess.run(
    args = command,
    stdout = subprocess.PIPE,
    stderr = subprocess.STDOUT,
  )

main()