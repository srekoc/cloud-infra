import os
import json
import sys
import urllib3
import logging
import requests
import subprocess
from datetime import datetime

def log_message(message):
    logtime = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    print (logtime + ": " + message)
    f.write (logtime + ": " + message + "\n")

def log_message_reset_vms(message):
    logtime = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    print (logtime + ": " + message)
    fs.write (logtime + ": " + message + "\n")

def update_mac_address_for_verdad_item(vsphere_mac_address, vm_name):
    
    api_key = '828f88b3-1fc2-444c-a984-a97829eeddae,spacekick'
    headers = {
        'cache-control': 'no-cache',
        'verdad-api-key': f'{api_key}',
    }
    value = f"[\"{vsphere_mac_address}\"]"
    print (value)
    data = f'"commitMsg":"updating mac address", "policy":"replace", "values": {value}'
    print (data)
    res = requests.put(f'https://internal.api.srekoc.net/v1/devops/configstore/v1/items/{vm_name}/tags/hardware.mac.1', headers=headers, data="{"+ f'{data}'+"}")
    print (res.request.headers)
    print (res.request.url)
    print (res.request.body)
    print (res.status_code)
    return (res.status_code)

def check_if_verdad_item_exists(vm_name, ip_address, mac_address):
    log_message("inside (fn) - check_if_verdad_item_exists")
    api_key = '828f88b3-1fc2-444c-a984-a97829eeddae,spacekick'

    headers = {
        'cache-control': 'no-cache',
        'verdad-api-key': f'{api_key}',
    }

    res = requests.get(f'https://internal.api.srekoc.net/v1/devops/configstore/v1/items/{vm_name}', headers=headers, verify=False)
    print (res.status_code)
    if (res.status_code == 200):
        verdad_item_dict = res.json()["result"]
        vm_mac_id = verdad_item_dict['tags']["hardware.mac.1"]['values'][0]
        return(vm_mac_id, res.status_code) 
    else:
        return ("none", res.status_code)

def get_vm_id_from_vm_name(session_id, vm_name):
    log_message("inside (fn) - get_vm_id_from_vm_name")
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)    
    headers = {
        'Accept': 'application/json',
        'vmware-api-session-id': f'{session_id}',
    }
    params = (
        ('filter.names', f'{vm_name}'),
    )
    res = requests.get('https://vm-mgr01.infra.dc.srekoc.net/rest/vcenter/vm', headers=headers, params=params, verify=False)
    #vm_dict = json.dumps(res)
    vm_dict = res.json()["value"]
    vm_id = vm_dict[0]["vm"]
    return(vm_id) 

def get_vm_mac_address(session_id, vm_id):
    headers = {
        'Accept': 'application/json',
        'vmware-api-session-id': f'{session_id}',
    }

    res = requests.get(f'https://vm-mgr01.infra.dc.srekoc.net/rest/vcenter/vm/{vm_id}', headers=headers, verify=False)
    vm_spec_dict = res.json()["value"]
    vm_mac_id = vm_spec_dict["nics"][0]['value']['mac_address']
    return(vm_mac_id) 
    print(vm_spec_dict)

def get_vsphere_session_id(vsphere_username, vsphere_password):
    log_message("inside (fn) - get_vsphere_session_id")

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)    
    headers = urllib3.make_headers(basic_auth=f'{vsphere_username}:{vsphere_password}', )
    url     = 'https://vm-mgr01.infra.dc.srekoc.net/rest/com/vmware/cis/session'
    payload = {}

    res = requests.post(url, data=payload, headers=headers, verify=False)
    session = res.json()["value"]
    return (session)

def create_verdad_item (verdad_network_name, vm_name, ip_address, mac_address, inventory_scope):
    name = vm_name.split(".")
    dns_name = name[0]
    verdad_item = f"""
    item {vm_name}
        hardware.mac.1 = {mac_address}
        inventory.scope = {inventory_scope}
        is = ( hw-VM-2D {verdad_network_name} )
        network.dnsname.1 = {dns_name}
        network.hostname.1 = {vm_name}
        network.ip.1 = {ip_address}
        provisioning_type = terraform
        release.type = generic_x64_linux6
        type = host
    """
    print (verdad_item)

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
                    "{mac_address}"
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

    api_key = '828f88b3-1fc2-444c-a984-a97829eeddae,spacekick'
    headers = {
        'cache-control': 'no-cache',
        'verdad-api-key': f'{api_key}',
    }
    res = requests.post(f'https://internal.api.srekoc.net/v1/devops/configstore/v1/items/{vm_name}', headers=headers, data=data)
    return (res.status_code)

def initiate_push_truth():
    answer = input(f'Do you wish to central-push? (only "yes" or "no" answer will be accepted):')
    if (answer == "yes"):
        print ("triggering push truth, hang on....")
        cmd = "ssh verdad01 central-push"
    
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        stdout = []
        while True:
            line = p.stdout.readline()
            if not isinstance(line, (str)):
                line = line.decode('utf-8')
                line = line.strip()
            stdout.append(line)
            print (line)
            if (line == '' and p.poll() != None):
                break
    else:
        print ("script exiting...")
        print ("The vms would only come up online if you central-push and reboot the vms")
        print ("This would be a manual process...good luck!")
        sys.exit()

def closure(session_id, vm_id):
    print ("")
    print ("###################  IMPORTANT  #####################")
    print ("central-push:")
    print ("here is the command to run from shell hosts")
    print (f"ssh verdad01 central-push")
    print ("reboot vms:")
    print ("here are the reboot commands")
    # 
    cmd = f'curl -k -X POST -H "vmware-api-session-id: {session_id}" "https://vm-mgr01.infra.dc.srekoc.net/rest/vcenter/vm/{vm_id}/power/reset"'
    print ("#####################################################")

    fs.write (cmd + "\n")
    print (cmd)

def main():
    vm_name = sys.argv[1]
    ip_address = sys.argv[2]
    mac_address = sys.argv[3]
    verdad_network_name = sys.argv[4]
    inventory_scope = sys.argv[5]
    vsphere_username = sys.argv[6]
    vsphere_password = sys.argv[7]

    logging.basicConfig(level=logging.DEBUG)

    # very basic command line check
    if len(sys.argv)<2:
        print ("script expects ipaddr and macaddr...exiting")
        sys.exit()
    try:
        log_message ("vm_name: " + vm_name)
        log_message ("ip_address: " + ip_address)
        log_message ("mac_address: " + mac_address)
        (verdad_mac_address, status_code) = check_if_verdad_item_exists(vm_name, ip_address, mac_address)
        session_id = get_vsphere_session_id(vsphere_username, vsphere_password)
        print ("vsphere session id -->", session_id)
        print ("verdad item status -->", status_code)
        print ("verdad mac address -->", verdad_mac_address)
        if (status_code == 200):
            vm_id = get_vm_id_from_vm_name(session_id, vm_name)
            vsphere_mac_address = get_vm_mac_address(session_id, vm_id)
            print ("vsphere vm id -->", vm_id)
            print ("vsphere mac address -->", vsphere_mac_address)
            if(vsphere_mac_address != verdad_mac_address):
                print ("mac mismatch, updating verdad item --> " + vsphere_mac_address + " in vsphere vs " + verdad_mac_address + "in verdad")
                status_code = update_mac_address_for_verdad_item(vsphere_mac_address, vm_name)
                if (status_code == 200):
                    print(f"successfully updated the verdad item for {vm_name}")
                    cmd = f'curl -k -X POST -H "vmware-api-session-id: {session_id}" "https://vm-mgr01.infra.dc.srekoc.net/rest/vcenter/vm/{vm_id}/power/reset"'
                    log_message_reset_vms(cmd)
                    #closure(session_id, vm_id)
                    # initiate_push_truth ()
            else:
                # PUT is anyway idempotent, but still avoiding a REST api hit. 
                print ("no mac mismatch between vsphere vs verdad..moving forward")
            print ("verdad item status -->", status_code)
            #closure(session_id, vm_id)
        else:
            print (f"no verdad item found for: {vm_name}")
            print (f"creating a new verdad item...")
            status_code = create_verdad_item (verdad_network_name, vm_name, ip_address, mac_address, inventory_scope)
            vm_id = get_vm_id_from_vm_name(session_id, vm_name)
            print ("vsphere vm id -->", vm_id)
            if (status_code == 200):
                print(f"successfully created the verdad item for {vm_name}")
                cmd = f'curl -k -X POST -H "vmware-api-session-id: {session_id}" "https://vm-mgr01.infra.dc.srekoc.net/rest/vcenter/vm/{vm_id}/power/reset"'
                log_message_reset_vms(cmd)
                # initiate_push_truth ()
            #closure(session_id, vm_id)
    except OSError:
        print ("Could not open/read file:", fname)
        sys.exit()
    
if __name__ == "__main__":
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    fname = "post_provisioning.log"
    script = "../shell/reset_vms"
    f = open(fname, 'a')
    fs = open(script, 'a')
    main()
    f.close()
    fs.close()

