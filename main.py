import json
import os
import pprint
import subprocess
import sys
import datetime
os.sys.path.append('/home/gardusi/github/sql_library/')
from sql_json import mySQL
from dateutil.parser import parse

def processDate(s):
  s = " ".join(s.split('=')[-1].split(':')[-4:])
  s = " ".join(s.split(',')).strip()
  s = (" ".join(s.split(' ')[0].split('-') + s.split(' ')[1:])).strip()
  s = s.split(' ')
  s = '{}-{}-{} {}:{}:{}{}:{}'.format(s[0], s[1], s[2], s[3], s[4], s[5], s[6], s[7])

  return parse(s)


current_filepath = os.path.realpath(
  os.path.join(os.getcwd(), os.path.dirname(__file__))
) + '/'

class SNMP:
  info = {}

  def __init__(self, snmpCommunity, ips, oids):
    self.snmpCommunity = snmpCommunity
    self.ips = ips
    self.oids = oids

  def build(self):
    documents = []
    for ip in self.ips:
      for i in range(len(self.info[ip])):
        documents.append(self.info[ip][i])
      return documents

  def getValue(self, s):
    return s.split('=')[-1].split(':')[-1].strip()

  def localAccessRun(self, command):
    return subprocess.run(
      args = command,
      stdout = subprocess.PIPE,
      stderr = subprocess.STDOUT,
    )

  def run(self):
    for ip in self.ips:
      self.info[ip] = []
      localDate = self.snmpRun(ip, ".1.3.6.1.2.1.25.1.2.0") # The host's notion of the local date and time of day.
      localDate = processDate(localDate[0])

      dia = datetime.datetime.now()

      for line in self.snmpRun(ip, 'ifDescr'):
        self.info[ip].append({
          'ip': ip,
          'interface': self.getValue(line),
          'hrSystemDate': localDate,
          'dia': dia,
        })
      for oid in self.oids:
        v = self.snmpRun(ip, self.oids[oid])
        for i in range(len(self.info[ip])):
          self.info[ip][i][oid] = self.getValue(v[i])
      print('ip: ' + ip)
      pprint.pprint(self.info[ip])
      return

  def snmpRun(self, ip, oid):
    return self.localAccessRun([
      '/usr/bin/snmpwalk',
      '-v2c',
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
  docs = magic.build()
  for d in docs:
      print(d)

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
