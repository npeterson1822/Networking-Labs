import json
import ipaddress
import xmltodict
from ncclient import manager
from netmiko import ConnectHandler

# Consts
HOST = "devnetsandboxiosxec9k.cisco.com"
USERNAME = ""
PASSWORD = ""

NEW_DEVICE_IP = "1" 
NEW_DEVICE_SUBNET = ""
TARGET_INTERFACE = ""
OSPF_PROCESS_ID = ""

def ensure_list(obj):
    if obj is None: return []
    return obj if isinstance(obj, list) else [obj]

# Use ipaddress to get NETCONF-returned RIDs into dotted decimal
def to_dotted_decimal(val):
    try:
        return str(ipaddress.IPv4Address(int(val)))
    except:
        return str(val)

# Find neighbor interface in the /30 from devices.json
new_iface_net = ipaddress.IPv4Network(NEW_DEVICE_SUBNET, strict=False)
try:
    with open("devices.json", "r") as f:
        devices_data = json.load(f)
except FileNotFoundError:
    print("Error: devices.json not found.")
    exit()

# Find neighbor and define reference config - what to normalize new device to
reference_config = None
for device in devices_data.get("devices", []):
    for iface in device.get("interfaces", []):
        if iface.get("ip"):
            iface_ip = ipaddress.IPv4Address(iface["ip"])
            if iface_ip in new_iface_net:
                reference_config = {
                    "neighbor_rid": device.get("router_id"),
                    "target_hello": int(iface.get("ospf", {}).get("hello", 10)),
                    "target_dead": int(iface.get("ospf", {}).get("dead", 40)),
                }
                break
    if reference_config: break

if not reference_config:
    print(f"Error: No neighbor found in JSON for {NEW_DEVICE_SUBNET}")
    exit()

# NETCONF call to get live state
with manager.connect(
    host=HOST, port=830, username=USERNAME, password=PASSWORD,
    hostkey_verify=False, device_params={"name": "iosxe"}
) as m:
    print(f"Analyzing {HOST} with NETCONF...")
    result = m.get(filter=("subtree", """<ospf-oper-data xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ospf-oper"/>"""))
    data = xmltodict.parse(result.xml)
    
    ospf_oper = data.get("rpc-reply", {}).get("data", {}).get("ospf-oper-data", {})
    instances = ensure_list(ospf_oper.get("ospfv2-instance"))
    instance = instances[0] if instances else {}
    
    live_rid = to_dotted_decimal(instance.get("router-id", "None"))
    live_hello, live_dead = "Unknown", "Unknown"

    # Search through areas for the interface
    for area in ensure_list(instance.get("ospfv2-area")):
        if not isinstance(area, dict): continue
        
        ifaces = ensure_list(area.get("ospfv2-interface"))
        for iface in ifaces:
            if not isinstance(iface, dict): continue
            
            # Check for the IP match in 'address' or 'dr-ip'
            found_ip = False
            for key, value in iface.items():
                if str(value) == NEW_DEVICE_IP:
                    found_ip = True
                    break
            
            if found_ip:
                live_hello = iface.get("hello-interval", "Unknown")
                live_dead = iface.get("dead-interval", "Unknown")
                break

# Compare, find issues, and issue CLI commands with Netmiko
issues = []
commands = []
final_rid = live_rid

# Router-ID match check
if live_rid == reference_config['neighbor_rid']:
    print(f"\nRID COLLISION: Neighbor uses {live_rid}!")
    final_rid = input("Enter unique Router ID for new device: ")
    commands.extend([f"router ospf {OSPF_PROCESS_ID}", f" router-id {final_rid}"])
    issues.append(f"Router-ID Collision: {live_rid} -> {final_rid}")

t_hello = str(reference_config['target_hello'])
t_dead = str(reference_config['target_dead'])

if str(live_hello) != t_hello or str(live_dead) != t_dead:
    commands.extend([
        f"interface {TARGET_INTERFACE}",
        f" ip ospf hello-interval {t_hello}",
        f" ip ospf dead-interval {t_dead}"
    ])
    issues.append(f"Timers: Live H:{live_hello}/D:{live_dead} -> Target H:{t_hello}/D:{t_dead}")

# Fix issues via Netmiko - send commands list
if issues:
    print("\nPending Changes:")
    for issue in issues: print(f" - {issue}")
    
    if input("\nApply changes via CLI? (y/n): ").lower() == 'y':
        device_params = {
            'device_type': 'cisco_xe',
            'host': HOST,
            'username': USERNAME,
            'password': PASSWORD,
        }
        with ConnectHandler(**device_params) as net_connect:
            output = net_connect.send_config_set(commands)
            print("\nCLI OUTPUT\n", output)
            net_connect.save_config()
        print("Fixed.")
else:
    print("Everything matches.")
