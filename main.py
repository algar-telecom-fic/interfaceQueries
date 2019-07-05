import json
import os
import subprocess
import sys

current_filepath = os.path.realpath(
  os.path.join(os.getcwd(), os.path.dirname(__file__))
) + '/'

class SNMP:
  info = {}
  
  def __init__(self, snmpCommunity, ips, oids):
    self.snmpCommunity = snmpCommunity
    self.ips = ips
    self.oids = oids
    
  def run(self):
    for ip in self.ips:
      self.info[ip] = []
      for line in self.snmpRun(ip, 'ifDescr'):
        self.info[ip].append({
          'interface': line.split(' ')[-1].strip()
        })
      print(self.info[ip])
    
  def localAccessRun(self, command):
    return subprocess.run(
      args = command,
      stdout = subprocess.PIPE,
      stderr = subprocess.STDOUT,
    )
    
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