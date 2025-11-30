I built this project to get hands-on practice with route-maps and policy-based NAT. While studying for the CCNA, NAT/PAT is covered in detail, but I was curious about how you would direct different parts of a LAN to use different outside interfaces.

This lab had to be done in CML, since Packet Tracer doesn’t support route-map–based NAT. I’m working within the free CML limit of five nodes (excluding unmanaged switches and external connectors), but that was still enough to model a dual-homed router and test NAT behavior. A more complete version would add networks behind the ISP routers to better represent the external side of the topology.

The topology is a simple dual-homed design: R1 connects to two separate ISP routers. Instead of treating this strictly as a failover setup, I wanted to split outbound traffic across both uplinks. The LAN uses a /24, which I divided into two /25s. The goal was for the lower half of the /24 to be translated out ISP1, and the upper half to be translated out ISP2. All traffic leaving the LAN must be NATed.

To implement this, I used ACLs to match each /25, applied them in route-maps, and tied each route-map to a different NAT rule. As a result, a host like 192.168.0.5 is translated and sent out E0/1 (ISP1), while a host like 192.168.0.200 is translated out E0/2 (ISP2).

One practical note: because the NAT split is based on source addressing, load distribution depends entirely on how the IPs are assigned. Even usage across both ISP links requires assigning devices evenly across the two halves of the subnet.
