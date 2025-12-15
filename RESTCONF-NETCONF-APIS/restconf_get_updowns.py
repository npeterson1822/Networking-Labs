import requests

url = "https://devnetsandboxiosxec9k.cisco.com/restconf/data/ietf-interfaces:interfaces/"

headers = {
    "Content-Type": "application/json",
    "Accept": "application/yang-data+json"
}

# Note for auth - no need to pass base64 encoded credentials, requests will handle
response = requests.get(url, auth=("USERNAME", "PASSWORD"), headers=headers, verify=False).json()

for iface in response["ietf-interfaces:interfaces"]["interface"]:
    status = "up" if iface["enabled"] else "down"
    print(iface["name"] + " is " + status)
