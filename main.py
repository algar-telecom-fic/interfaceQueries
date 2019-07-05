import json
import os
import subprocess
import sys

import pprint

current_filepath = os.path.realpath(
  os.path.join(os.getcwd(), os.path.dirname(__file__))
) + '/'

class SNMP:
  info = {}
  
  def __init__(self, snmpCommunity, ips, oids):
    self.snmpCommunity = snmpCommunity
    self.ips = ips
    self.oids = oids
    
  def localAccessRun(self, command):
    return subprocess.run(
      args = command,
      stdout = subprocess.PIPE,
      stderr = subprocess.STDOUT,
    )
    
  def run(self):
    for ip in self.ips:
      self.info[ip] = []
      for line in self.snmpRun(ip, 'ifDescr'):
        self.info[ip].append({
          'interface': line.split('=')[-1].strip()
        })
      for oid in self.oids:
        v = self.snmpRun(ip, self.oids[oid])
        print(v)
        for i in range(len(self.info[ip])):
          self.info[ip][i][oid] = v[i].split('=')[-1].strip()
        pprint.pprint(self.info[ip])
      return
    
  def snmpRun(self, ip, oid):
    return self.localAccessRun([
      '/usr/bin/snmpwalk',
      '-v', '2c',
      '-c', self.snmpCommunity,
      ip, oid
    ]).stdout.decode('utf-8').strip().split('\n')

def main():
  config = readJson(current_filepath + 'config.json')
  magic = SNMP(
    snmpCommunity = sys.argv[1],
    ips = readJson(config['ipsFilepath']),
    oids = readJson(current_filepath + 'oid.json')
  )
  magic.run()

def readJson(filepath):
  with open(filepath, 'rb') as file:
    return json.load(file, encoding = 'utf-8')

main()