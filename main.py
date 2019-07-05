import json
import os
import subprocess

current_filepath = os.path.realpath(
  os.path.join(os.getcwd(), os.path.dirname(__file__))
) + '/'

def main():
  config = readJson(current_filepath + 'config.json')
  ips = readJson(config['ipsFilepath'])
  for ip in ips:
    aux = localAccessRun([
      '/usr/bin/snmpwalk',
      '-v', '2c',
      '-c', 'V01prO2005',
      ip,
      '.1.3.6.1.2.1.2.2.1.2'
    ])
    print(aux)

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