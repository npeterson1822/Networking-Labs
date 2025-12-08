from netmiko import ConnectHandler
import yaml

# Initial device details for SSH
device = {
    "host":"devnetsandboxiosxec9k.cisco.com",
    "username":"<SSH USERNAME>",
    "password":"<SSH PASSWORD",
    "device_type":"cisco_xe"
}

# Load YAML config file
with open("catalyst_config.yaml") as f:
    config = yaml.safe_load(f)

connection = ConnectHandler(**device)

cmds = []

# Iterate thru config dict, adding each command to the cmds list
for item in config["interfaces"]:
    cmds.append(f"interface {item['name']}")
    cmds.append(f"description {item['description']}")
    cmds.append(f"ip address {item['ip']} {item['netmask']}")

connection.send_config_set(cmds)

output = connection.send_command("show ip int br")

print(output)
