import asyncio
import random
import logging
from typing import Any, Coroutine
import azure.functions as func
import os
import socket
#from dns.asyncresolver import Resolver
#import dns.resolver
#import dns.rrset

target_ports = [
21,
22,
23,
25,
80,
110,
113,
135,
139,
443,
445,
465,
548,
587,
993,
995,
1433,
14331,
14332,
14333,
1720,
1723,
3306,
3389,
6001,
8080,
8888,
9090,
9080,
7878,
8443,
8880
]

async def scan_port(host, port, resolved_ips):
    timeout = 3
    coro = asyncio.open_connection(host, port)
    try:
        #reader, writer = await asyncio.open_connection(host, port)
        _, writer = await asyncio.wait_for(coro, timeout)
        #print(port)
        if port in [53,443]:
            logging.info(f"Port {port} is open on {host} maps to {resolved_ips[host]}")
        elif port in [21,23,3389,445,389,1433,14331,14332,14333,7878]:
            logging.error(f"Port {port} is open on {host} maps to {resolved_ips[host]}")
        else:
            logging.warning(f"Port {port} is open on {host} maps to {resolved_ips[host]}")
        writer.close()
        #await writer.wait_closed()
    except Exception as e: #fucking LOL
        pass
    #except (ConnectionRefusedError, asyncio.TimeoutError):
    #    pass

"""
async def resolve_domain(domain):
    # create an asyncio Resolver instance
    rs = Resolver()
    res: dns.resolver.Answer = await rs.resolve(domain)
    print(res.rrset)

async def resolve():
    resolved_ips = {}
    #coros = [dns_query(dom, rt, **kwargs) for dom, rt in list(queries)]
    coros = [resolve_domain(host) for host in target_hosts.strip().splitlines()]
    await asyncio.gather(*coros)
    #return resolved_ips
"""
async def process(resolved_ips):
    #target_ports = range(1, 1025)  # Scan common ports (1-1024)
    #targets = target_hosts.strip().splitlines()
    targets = list(resolved_ips.keys())
    random.shuffle(targets)
    for target_host in targets:
        tasks = [scan_port(target_host, port, resolved_ips) for port in target_ports]
        await asyncio.gather(*tasks)


app = func.FunctionApp()
@app.schedule(schedule="0 0 9 * * Tue", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def timed_port_scan(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function executed.')

    global target_hosts

    fad = os.path.dirname(os.path.abspath(__file__))
    text_file_path = os.path.join(fad, 'domains.txt')
    with open(text_file_path, 'r') as file:
        target_hosts = file.read()

    logging.info('Resolving domains.')
    #my_run(resolve())
    resolved_ips = {}
    for t in target_hosts.strip().splitlines():
        try:
            addr = socket.gethostbyname(t)
        except Exception as e:
            addr = ''
        if not addr in resolved_ips.keys():
            resolved_ips[addr] = [t]
        else:
            resolved_ips[addr].append(t)

    print("Scanning the following number of unique targets: "+str(len(resolved_ips.keys())))
    #links into exisintg azure function loop
    def my_run(coro: Coroutine[Any, Any, Any], *args, **kwargs) -> Any:
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.run(coro, *args, **kwargs)
        else:
            return loop.run_until_complete(coro(*args, **kwargs))

    logging.info("Beginning port scanning")
    my_run(process(resolved_ips))

    logging.info('Python timer trigger function execution completed.')
