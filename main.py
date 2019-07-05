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
    
  def build(self):
    documents = []
    for ip in self.ips:
      for i in range(len(self.info[ip])):
        documents.append(self.info[ip][i])
    return documents
    
  def run(self):
    for ip in self.ips:
      self.info[ip] = []
      for line in self.snmpRun(ip, 'ifDescr'):
        self.info[ip].append({
          'ip': ip,
          'interface': line.split('=')[-1].strip()
        })
      for oid in self.oids:
        v = self.snmpRun(ip, self.oids[oid])
        for i in range(len(self.info[ip])):
          self.info[ip][i][oid] = v[i].split('=')[-1].strip()
        print('ip: ' + ip)
        pprint.pprint(self.info[ip])
      return
    
  def snmpRun(self, ip, oid):
    return self.localAccessRun([
      '/usr/bin/snmpwalk',
      '-v', '2c',
      '-c', self.snmpCommunity,
      ip, oid
    ]).stdout.decode('utf-8').strip().split('\n')
    
def insert_documents(documents, database_credentials, database_name, table_name, table_info):
  db = mySQL(
    database_credentials = database_credentials,
    database_name = database_name,
  )
  db.create_table(
    table_info = table_info,
    table_name = table_name,
  )
  db.insert_into(
    table_info = table_info,
    table_name = table_name,
    values = documents,
  )

def main():
  config = readJson(current_filepath + 'config.json')
  magic = SNMP(
    snmpCommunity = sys.argv[1],
    ips = readJson(config['ipsFilepath']),
    oids = readJson(current_filepath + 'oid.json')
  )
  magic.run()
  insert_documents(
    documents = magic.build(),
    database_credentials = readJson(config['databaseCredentialsFilepath']),
    database_name = config['database_name'],
    table_name = config['table_name'],
    table_info = readJson(current_filepath + 'tableInfo.json')
  )

def readJson(filepath):
  with open(filepath, 'rb') as file:
    return json.load(file, encoding = 'utf-8')

main()