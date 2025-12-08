Netmiko + YAML Interface Automation Lab

This is a small project I built to practice network automation using Python, Netmiko, and YAML. The script connects to a Cisco device via SSH, reads interface information from a YAML file, and applies interface descriptions and IP addresses automatically. It then prints the result of "show ip int br" so you can verify the changes.

The logic is straightforward: the YAML file defines the interfaces and the configs to apply, the Python script loops through each interface, builds the commands, and sends them to the device using Netmiko. This is a dynamic workflow that can take any YAML file and parse it for the relevant details to add the loopback addresses and descriptions.

The project is focused on practicing network automation basics: reading configuration data from a file, generating commands dynamically, and applying them to a device. I did this to get hands-on experience with Python, Netmiko, and YAML in a lab environment.

In the future, I will work on more complex tasks like configuring multiple devices. Playing with the scalability of network automation tools like Netmiko is exciting to me.
