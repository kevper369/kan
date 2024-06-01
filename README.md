# kangaroo
Find PrivateKey of corresponding Pubkey(s) using Pollard Kangaroo algo 

# Usage
- python kangaroo.py
```
(base) C:\anaconda3>python kangaroo.py
[+] Starting CPU Kangaroo.... Please Wait
[+] Working on Pubkey: 0452b1af31d67e6a83ec7931c148f56b0755ce40c836f20c6fe2b6da612c89cf3e2d22dceb73a2648739bfc45c9a305e385a5c1fbeea35a8f946fd78c9fc67a615
[+] Using  [Number of CPU Threads: 7] [DP size: 10] [MaxStep: 1]
[+] ............................................
[+] Scanning Range  0x935da71d7350734c3472fe305fef82ab8aca644fb : 0x935da71d7350734c3472fe305fff82ab8aca644fa
[+] [646.03 TeraKeys/s][Kang 7168][Count 2^27.34/2^29.07][Elapsed 09s][Dead 0][RAM 19.8MB/44.9MB]
============== KEYFOUND ==============
Kangaroo FOUND PrivateKey : 0x00000000000000000000000935da71d7350734c3472fe305fef82ab8aca644fb
======================================
Program Finished
```

python kangaroo.py -p 03633cbe3ec02b9401c5effa144c5b4d22f87940259634858fc7e59b1c09937852 -keyspace 200000000000000000000000000000000:3ffffffffffffffffffffffffffffffff -n 7205759403792793500 -rand -ncore 128




python kangaroo.py -p 0230210c23b1a047bc9bdbb13448e67deddc108946de6de639bcc75d47c0216b1b -keyspace 1a000000000000000:1bfffffffffffffff -rand -ncore 128
