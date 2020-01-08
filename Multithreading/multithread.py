from concurrent.futures import ThreadPoolExecutor
import paramiko
import subprocess

def multi_threaded_execution(jobs, workers = 256):
    ans = []
    threads = []
    with ThreadPoolExecutor(max_workers = workers) as executor:
        for parameters in jobs:
            threads.append(
                executor.submit(
                parameters[0],
                *parameters[1:]
                )
            )
    for thread in threads:
        ans.append(thread.result())
    return ans


def localAccessRun(command):
    return subprocess.run(
      args = command,
      stdout = subprocess.PIPE,
      stderr = subprocess.STDOUT,
    )


def instruction(ip, oid):
    return localAccessRun([
        "/usr/bin/snmpwalk", "-v2c", "-Os", "-Oqv", "-c", "V01prO2005",
        ip,
        oid,
    ]).stdout.decode('utf-8').strip().split('\n')


def collect(ips, oids, credentials):
    dict_results = {}

    for ip in ips:
        dict_results[ip] = {}

    for oid in oids:
        jobs = []
        for ip in ips:
            dict_results[ip][oid] = {}

            jobs.append([
                instruction,
                ip,
                oid
            ])

        results = multi_threaded_execution(jobs)
        for ip, r in zip(ips, results):
            dict_results[ip][oid] = r

    return dict_results
