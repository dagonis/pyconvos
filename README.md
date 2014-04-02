pycapinfos_model
================

A Python (2.7.x) wrapper for Tshark that lists conversations (TCP by default) and presents you an interface to
view their contents. Wasn't sure if there was a way to do this in tshark, so this seemed like a more fun solution.

This doesn't work with older versions of tshark that don't support "-z follow".

I do call out to Subprocess, but I try to verify the filename passed is really a file and not something evil.


Usage
----------------
python pyconvos.py <file> -p (TCP|UDP)

If you don't specify -p it is set to TCP by default.

Here is an example:
    $ python pyconvos.py test1.pcap
    Which conversations would you like to follow?:
    0) 192.168.1.20:51956 <-> 74.125.224.170:80 (375219 Total bytes, Duration: 1.5576)
    1) 192.168.1.20:51957 <-> 74.125.224.139:80 (335493 Total bytes, Duration: 1.5653)
    2) 192.168.1.20:51915 <-> 74.125.225.212:443 (105124 Total bytes, Duration: 4.8353)
    3) 192.168.1.20:51953 <-> 74.125.224.170:80 (261884 Total bytes, Duration: 1.5861)
    4) 192.168.1.20:51919 <-> 74.125.239.9:443 (181329 Total bytes, Duration: 6.1140)
    5) 192.168.1.20:51961 <-> 74.125.224.170:80 (135973 Total bytes, Duration: 1.5078)
    Your selection: 1

    ===================================================================
    Follow: tcp,ascii
    Filter: ((ip.src eq 192.168.1.20 and tcp.srcport eq 51957) and (ip.dst eq 74.125.224.139 and tcp.dstport eq 80)) or ((ip.src eq 74.125.224.139 and tcp.srcport eq 80) and (ip.dst eq 192.168.1.20 and tcp.dstport eq 51957))
    Node 0: 192.168.1.20:51957
    Node 1: 74.125.224.139:80
    <output omitted>
    Would you like to see another conversation? (y/N):

