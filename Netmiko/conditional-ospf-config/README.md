Netmiko + OSPF Automation Lab

This is a small project I built to practice network automation using Python, Netmiko, and JSON. The script connects to Cisco devices via SSH, reads interface information from a JSON file, and automatically configures OSPF. It advertises all interfaces in OSPF but makes LAN interfaces passive so they don’t send LSAs.

The logic is straightforward: the JSON file defines the devices and their interfaces (this could be data you pull with an API or NETCONF), the Python script loops through each interface, calculates the correct wildcard mask, builds the OSPF commands, and sends them to the device using Netmiko. This way, any properly formatted JSON file can drive the OSPF configuration dynamically.

The project is focused on practicing network automation basics - reading structured data from a file, generating commands conditionally, and applying them to network devices. I built it to get hands-on experience with Python, Netmiko, and OSPF in a lab environment without having to manually type every command.

In the future, I plan to extend this to multiple OSPF areas, different network designs, or larger topologies. Experimenting with dynamically generating configs and automating network tasks is what makes this work fun for me.
