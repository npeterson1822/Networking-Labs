from netmiko import ConnectHandler

device = {
    "host":"devnetsandboxiosxec8k.cisco.com",
    "username":"", # Credentials in DevNet
    "password":"",
    "device_type":"cisco_xe"
}

connection = ConnectHandler(**device)

output = connection.send_command("show ip int br")

print(output)
