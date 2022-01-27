import re
import sys
import json
import urllib3
import logging
import requests
import subprocess as sp
from datetime import datetime



vm_name = "sre-jenkins04.dc.srekoc.net"
vsphere_mac_address = "00:50:56:b0:6a:68"
ip_address = "10.81.7.36"
verdad_network_name= "nz-infra-oos.dc.srekoc.net" 
inventory_scope= "oos"
name = vm_name.split(".")
dns_name = name[0]

def trigger_push_truth():
    answer = input(f'Do you wish to central-push? (only "yes" or "no" answer will be accepted):')
    if (answer == "yes"):
        print ("triggering push truth, hang on....")
    else:
        print ("script exiting...")
        print ("The vms would only come up online if you central-push and reboot the vms")
        print ("This would be a manual process...good luck!")
        sys.exit()


data = f"""
{{
    "commitMsg":"creating verdad item",
    "items": [
     {{   
        "name": "{vm_name}",
        "tags": {{
            "provisioning_type": {{
                "policy": "append",
                "values": [
                "terraform"
                ]
            }},
            "is": {{
                "policy": "append",
                "values": [
                "hw-VM-2D",
                "{verdad_network_name}"
                ]
            }},
            "network.dnsname.1": {{
                "policy": "append",                
                "values": [
                "{dns_name}"
                ]
            }},
            "inventory.scope": {{
                "policy": "append",                
                "values": [
                "{inventory_scope}"
                ]
            }},
            "hardware.mac.1": {{
                "policy": "append",                
                "values": [
                "{vsphere_mac_address}"
                ]
            }},
            "network.hostname.1": {{
                "policy": "append",                
                "values": [
                "{vm_name}"
                ]
            }},
            "network.ip.1": {{
                "policy": "append",                
                "values": [
                "{ip_address}"
                ]
            }}
        }}  
      
      }}
    ]
}}
"""


api_key = argv[1]
headers = {
    'cache-control': 'no-cache',
    'verdad-api-key': f'{api_key}',
}
res = requests.post(f'https://internal.api.srekoc.net/v1/devops/configstore/v1/items/{vm_name}', headers=headers, data=data)
print (res.request.headers)
print (res.request.url)
print (res.request.body)
print (res.status_code)

trigger_push_truth()