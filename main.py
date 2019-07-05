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
  oids = readJson(current_filepath + 'oid.json')
  for ip in ips:
    info[ip] = []
    for line in snmpRun('ifDescr'):
      info[ip].append({
        'interface': line.split(' ')[-1].strip()
      })
    print(info[ip])

def readJson(filepath):
  with open(filepath, 'rb') as file:
    return json.load(file, encoding = 'utf-8')
    
def snmpRun(ip, oid):
  return localAccessRun([
    '/usr/bin/snmpwalk',
    '-v', '2c',
    '-c', snmpCommunity,
    ip, oid
  ]).stdout.decode('utf-8').strip().split('\n')
    
def localAccessRun(command):
  return subprocess.run(
    args = command,
    stdout = subprocess.PIPE,
    stderr = subprocess.STDOUT,
  )

main()