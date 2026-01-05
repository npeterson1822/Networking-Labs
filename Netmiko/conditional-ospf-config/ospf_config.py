from netmiko import ConnectHandler
import json

# Function for converting subnet masks to wildcard masks
def subnet_to_wc(mask):
    octets = mask.split(".")
    wc_octets = [str(255 - int(octet)) for octet in octets]
    return ".".join(wc_octets)
# Parse JSON to pull relevant details
with open("devices.json") as f:
    data = json.load(f)

devices = data['devices']

# Iterate over devices for each command set and connection
for device in devices:
    # Enter OSPF process ID 1 to start
    commands = ["router ospf 1"]
    
    interfaces = device["interfaces"]
    
    for iface in interfaces:
        name = iface["name"]
        int_ip = iface["ip"]
        int_wc = subnet_to_wc(iface["mask"])
        commands.append(f"network {int_ip} {int_wc} area 0")
        # Make any LAN (192.168.0.0/16) interfaces passive
        if int_ip[0:7] == "192.168":
            commands.append(f"passive-interface {name}")
        
    # Define device parameters from devices.json
    device_params = {
        'device_type': device['device_type'],
        'host': device['management_ip'],
        'username': device['username'],
        'password': device['password']
    }
    # Initiate connection and pass commands with Netmiko
    with ConnectHandler(**device_params) as net_connect:
        output = net_connect.send_config_set(commands)
        print("\nCLI OUTPUT\n", output)
        net_connect.save_config()
    print("OSPF Configuration Set")


    
