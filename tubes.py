#!/usr/bin/env python

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import Link, TCLink, Intf
from subprocess import Popen, PIPE
from mininet.log import setLogLevel

if '__main__' == __name__:
	setLogLevel('info')
	net = Mininet(link=TCLink) # buat kabel
	value = 0

	# Tambah Host
	h1 = net.addHost('h1')
	h2 = net.addHost('h2')

	# Tambah Router
	r1 = net.addHost('r1')
	r2 = net.addHost('r2')
	r3 = net.addHost('r3')
	r4 = net.addHost('r4')

	# Konfigurasi Bandwidth
	bw1={'bw':1} # Untuk 1Mbps
	bw2={'bw':0.5} # Untuk 0.5 Mbps

	# Konfigurasi Link 
	net.addLink(r1, h1, max_queue_size=60, use_htb = True, intfName1 = 'r1-eth0', intfName2 = 'h1-eth0', cls=TCLink, **bw1)
	net.addLink(r2, h1, max_queue_size=60, use_htb = True, intfName1 = 'r2-eth1', intfName2 = 'h1-eth1', cls=TCLink, **bw1)
	net.addLink(r1, r3, max_queue_size=60, use_htb = True, intfName1 = 'r1-eth1', intfName2 = 'r3-eth1', cls=TCLink, **bw2)
	net.addLink(r1, r4, max_queue_size=60, use_htb = True, intfName1 = 'r1-eth2', intfName2 = 'r4-eth2', cls=TCLink, **bw1)
	net.addLink(r2, r4, max_queue_size=60, use_htb = True, intfName1 = 'r2-eth0', intfName2 = 'r4-eth0', cls=TCLink, **bw1)
	net.addLink(r2, r3, max_queue_size=60, use_htb = True, intfName1 = 'r2-eth2', intfName2 = 'r3-eth2', cls=TCLink, **bw2)
	net.addLink(r3, h2, max_queue_size=60, use_htb = True, intfName1 = 'r3-eth0', intfName2 = 'h2-eth0', cls=TCLink, **bw1)
	net.addLink(r4, h2, max_queue_size=60, use_htb = True, intfName1 = 'r4-eth1', intfName2 = 'h2-eth1', cls=TCLink, **bw1)
	net.build()

	# Konfigurasi Host
	# HOST1
	h1.cmd("ifconfig h1-eth0 0")
	h1.cmd("ifconfig h1-eth1 0")
	h1.cmd("ifconfig h1-eth0 192.168.10.1 netmask 255.255.255.0")
	h1.cmd("ifconfig h1-eth1 192.168.17.2 netmask 255.255.255.0")
	#HOST2
	h2.cmd("ifconfig h2-eth0 0")
	h2.cmd("ifconfig h2-eht1 0")
	h2.cmd("ifconfig h2-eth0 192.168.13.2 netmask 255.255.255.0")
	h2.cmd("ifconfig h2-eth1 192.168.15.1 netmask 255.255.255.0") 
	
	# Konfigurasi Router
	# Forward Router
	r1.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
	r2.cmd("echo 2 > /proc/sys/net/ipv4/ip_forward")
	r3.cmd("echo 3 > /proc/sys/net/ipv4/ip_forward")
	r4.cmd("echo 4 > /proc/sys/net/ipv4/ip_forward")
	# Router1
	r1.cmd("ifconfig r1-eth0 0")
	r1.cmd("ifconfig r1-eth1 0")
	r1.cmd("ifconfig r1-eth2 0")
	r1.cmd("ifconfig r1-eth0 192.168.10.2 netmask 255.255.255.0")
	r1.cmd("ifconfig r1-eth1 192.168.11.1 netmask 255.255.255.0")
	r1.cmd("ifconfig r1-eth2 192.168.12.1 netmask 255.255.255.0")
	# Router2
	r2.cmd("ifconfig r2-eth0 0")
	r2.cmd("ifconfig r2-eth1 0")
	r2.cmd("ifconfig r2-eth2 0")
	r2.cmd("ifconfig r2-eth0 192.168.16.2 netmask 255.255.255.0")
	r2.cmd("ifconfig r2-eth1 192.168.17.1 netmask 255.255.255.0")
	r2.cmd("ifconfig r2-eth2 192.168.14.2 netmask 255.255.255.0")
	# Router3
	r3.cmd("ifconfig r3-eth0 0")
	r3.cmd("ifconfig r3-eth1 0")
	r3.cmd("ifconfig r3-eth2 0")
	r3.cmd("ifconfig r3-eth0 192.168.13.1 netmask 255.255.255.0")
	r3.cmd("ifconfig r3-eth1 192.168.11.2 netmask 255.255.255.0")
	r3.cmd("ifconfig r3-eth2 192.168.14.1 netmask 255.255.255.0")
	# Router4
	r4.cmd("ifconfig r4-eth0 0")
	r4.cmd("ifconfig r4-eth1 0")
	r4.cmd("ifconfig r4-eth2 0")
	r4.cmd("ifconfig r4-eth0 192.168.16.1 netmask 255.255.255.0")
	r4.cmd("ifconfig r4-eth1 192.168.15.2 netmask 255.255.255.0")
	r4.cmd("ifconfig r4-eth2 192.168.12.2 netmask 255.255.255.0")
	
	# Routing Host
	# Host1
	h1.cmd("ip rule add from 192.168.10.1 table 1")
	h1.cmd("ip rule add from 192.168.17.2 table 2")
	h1.cmd("ip route add 192.168.10.0/24 dev h1-eth0 scope link table 1")
	h1.cmd("ip route add default via 192.168.10.2 dev h1-eth0 table 1")
	h1.cmd("ip route add 192.168.17.0/24 dev h1-eth1 scope link table 2")
	h1.cmd("ip route add default via 192.168.17.1 dev h1-eth1 table 2")
	h1.cmd("ip route add default scope global nexthop via 192.168.10.2 dev h1-eth0")
	h1.cmd("ip route add default scope global nexthop via 192.168.17.1 dev h1-eth1")
	# Host2
	h2.cmd("ip rule add from 192.168.13.2 table 3")
	h2.cmd("ip rule add from 192.168.15.1 table 4")
	h2.cmd("ip route add 192.168.13.0/24 dev h2-eth0 scope link table 1")
	h2.cmd("ip route add default via 192.168.13.1 dev h2-eth0 table 1")
	h2.cmd("ip route add 192.168.15.0/24 dev h2-eth1 scope link table 2")
	h2.cmd("ip route add default via 192.168.15.2 dev h2-eth1 table 2")
	h2.cmd("ip route add default scope global nexthop via 192.168.13.1 dev h2-eth0")
	h2.cmd("ip route add default scope global nexthop via 192.168.15.2 dev h2-eth1")
	# Konfigurasi Jalur Keluar
	# Host 1
	h1.cmd("route default gw 192.168.10.2 dev h1-eth0")
	h1.cmd("route default gw 192.168.17.1 dev h1-eth1")
	# HOST 2
	h2.cmd("route default gw 192.168.13.1 dev h2-eth0")
	h2.cmd("route default gw 192.168.15.2 dev h2-eth1")
	
	# Konfigurasi Routing Static
	# Router 1
	r1.cmd("route add -net 192.168.13.0/24 gw 192.168.11.2")
	r1.cmd("route add -net 192.168.14.0/24 gw 192.168.11.2")
	r1.cmd("route add -net 192.168.15.0/24 gw 192.168.12.2")
	r1.cmd("route add -net 192.168.16.0/24 gw 192.168.12.2")
	r1.cmd("route add -net 192.168.17.0/24 gw 192.168.11.2")
	# Router 2
	r2.cmd("route add -net 192.168.10.0/24 gw 192.168.14.1")
	r2.cmd("route add -net 192.168.12.0/24 gw 192.168.16.1")
	r2.cmd("route add -net 192.168.15.0/24 gw 192.168.16.1")
	r2.cmd("route add -net 192.168.11.0/24 gw 192.168.14.1")
	r2.cmd("route add -net 192.168.13.0/24 gw 192.168.14.1")
	# Router 3
	r3.cmd("route add -net 192.168.10.0/24 gw 192.168.11.1")
	r3.cmd("route add -net 192.168.15.0/24 gw 192.168.14.2")
	r3.cmd("route add -net 192.168.17.0/24 gw 192.168.14.2")
	r3.cmd("route add -net 192.168.12.0/24 gw 192.168.11.1")
	r3.cmd("route add -net 192.168.16.0/24 gw 192.168.14.2")
	# Router 4
	r4.cmd("route add -net 192.168.17.0/24 gw 192.168.16.2")
	r4.cmd("route add -net 192.168.10.0/24 gw 192.168.12.1")
	r4.cmd("route add -net 192.168.14.0/24 gw 192.168.16.2")
	r4.cmd("route add -net 192.168.13.0/24 gw 192.168.12.1")
	r4.cmd("route add -net 192.168.11.0/24 gw 192.168.12.1")
	
	# Konfigurasi iperf
	h1.cmd('iperf -t 5 -B 192.168.10.1 -c 192.168.13.2')
	h1.cmd('iperf -t 5 -B 192.168.17.2 -c 192.168.15.1')
	h2.cmd('iperf -s &')
	
	CLI(net)
	net.stop()
