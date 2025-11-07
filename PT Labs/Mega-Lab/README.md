This is the Megalab assignment as part of Jeremy's IT Lab course. He provided the lab environment, and I completed all the configurations.

Since the full list of commands and tasks for this lab is extensive, I'll cover an overview of what was configured.

L2 Etherchannel was configured between the distribution switches in the A and B segments of the network, while L3 Etherchannel was configured between the core switches. A PT glitch makes the core switch connection show up as down, but both switches show RU in the show etherchannel summary output.

All links between ASWs and DSWs are configured as trunks with the appropriate allowed VLANs and native VLAN.

DSWs A1 and B1 are VTP servers in their respective segments, while all other switches are clients.

The edge ports of access switches are configured as access in the correct VLAN. Where appropriate, voice VLANs and access VLANs are configured on the same port. PortFast and BPDUGuard are configured on edge ports. Port security is configured on all these ports as well, allowing only 1 MAC per port with the violation mode set as "restrict." MAC addresses are configured as sticky. DHCP snooping is also enabled, with uplinks trusted but edge links limited to 15 pps. Dynamic ARP inspection is also configured, with these ports being untrusted and all validation checks enabled.

IPv4 addresses are configured on the appropriate interfaces of the L3 switches. Access switches also have configured management IPs for interface vlan 99 (Management).

HSRP is enabled between DSWs in the A and B segments of the network. There is one group per VLAN (4 total) - with the active router in each being balanced across VLANs. Preemption is enabled on the configured active routers so that if they go down and come back up, they will retake their position as active. Spanning-Tree is configured in Rapid PVST+ mode and is synchronized with HSRP - the active router for each VLAN is the root bridge in that VLAN, and the standby router is the secondary in each VLAN.

OSPF is configured with process ID 1 and area 0 on R1 and each CSW and DSW. Every router ID is the router's loopback interface. All SVIs and loopbacks are configured as passive. Every link between neighbors is configured as point-to-point, with no DR/BDR election.

R1 is configured with a static default route to each ISP connection. The route via G0/1/0 is floating, with a manually set AD of 1. R1 is an ASBR in OSPF, having default-information originate applied to it so it advertises itself as a default route next hop for other members of the area.

R1 serves DHCP via helper addresses on the SVIs of the distribution switches. Each DHCP pool includes the subnet, default gateway (DSW SVI address), domain name, and DNS. DNS is configured on SRV1.

R1 serves as an NTP stratum 5 server. It references an IP over the internet as its NTP server. 

SNMP is configured on every device with a read-only community string.

Syslog is configured on every device, sending syslog traps of every severity to SRV1. Logging is configured to the buffer with a buffer size of 8192 bytes.

FTP credentials are set on R1 - as part of the project, a new IOS image was obtained via FTP, then set as the boot file.

SSH is configured for access on every device, with only version 2 connections allowed. An ACL applied to the vty lines restricts SSH access to inbound connections from Office A's PCs. Only SSH can access the vty lines. Local login is required for authentication. Synchronous logging is configured.

R1 has static NAT configured for SRV1, so it is reachable at a specific inside global address from the outside. PAT is also configured, using an ACL to only allow select traffic to be translated. A NAT pool is also used for the inside global addresses available. 

CDP is disabled on all devices, with LLDP enabled instead.

An extended ACL is configured on the LAN interfaces of the core switches to limit traffic between the subnets. ICMP is allowed from Office A to B, but no other traffic from A to B is. 

IPv6 routing is enabled between R1 and the core switches, and each interface is addressed appropriately. The port-channel between the core switches only uses link-local interface addresses.

Wireless LANs and corresponding dynamic interfaces are configured on the WLC. 
