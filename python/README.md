
# mac address activation
We rely on static IPs and mac addresses that are centrally pushes to various dhcp servers across networks. So it becomes imperative to update the right network adapter details. This is accomplished via the post processing python script. This readme outlines the step by step design considerations.

## Design
#### Step 1: Get the vsphere vm id from vm name

```python
curl -X GET --header 'Accept: application/json' --header 'vmware-api-session-id: <SESSION_ID>' 'https://vm-mgr01.infra.dc.srekoc.net/rest/vcenter/vm?filter.names=sre-jenkins01.dc.srekoc.net'

{
  "value": [
    {
      "memory_size_MiB": 4096,
      "vm": "vm-32049",
      "name": "sre-jenkins01.dc.srekoc.net",
      "power_state": "POWERED_ON",
      "cpu_count": 2
    }
  ]
}
```

####Step 2: Get the VM mac address from vm id
```python
curl -X GET --header 'Accept: application/json' --header 'vmware-api-session-id: <SESSION_ID>' 'https://vm-mgr01.infra.dc.srekoc.net/rest/vcenter/vm/vm-32039'

{
  "value": {
    "cdroms": [
      {
        "value": {
          "start_connected": false,
          "backing": {
            "device_access_type": "PASSTHRU",
            "type": "CLIENT_DEVICE"
          },
          "allow_guest_control": false,
          "label": "CD/DVD drive 1",
          "ide": {
            "primary": true,
            "master": true
          },
          "state": "NOT_CONNECTED",
          "type": "IDE"
        },
        "key": "3000"
      }
    ],
    "memory": {
      "size_MiB": 1024,
      "hot_add_enabled": false
    },
    "disks": [
      {
        "value": {
          "scsi": {
            "bus": 0,
            "unit": 0
          },
          "backing": {
            "vmdk_file": "[dc_cluster01_ssd03] sre-jenkins.dc.srekoc.net/sre-jenkins.dc.srekoc.net.vmdk",
            "type": "VMDK_FILE"
          },
          "label": "Hard disk 1",
          "type": "SCSI",
          "capacity": 26843545600
        },
        "key": "2000"
      }
    ],
    "parallel_ports": [],
    "sata_adapters": [],
    "cpu": {
      "hot_remove_enabled": false,
      "count": 1,
      "hot_add_enabled": false,
      "cores_per_socket": 1
    },
    "scsi_adapters": [
      {
        "value": {
          "scsi": {
            "bus": 0,
            "unit": 7
          },
          "pci_slot_number": 160,
          "label": "SCSI controller 0",
          "type": "PVSCSI",
          "sharing": "NONE"
        },
        "key": "1000"
      }
    ],
    "power_state": "POWERED_ON",
    "floppies": [],
    "name": "sre-jenkins.dc.srekoc.net",
    "nics": [
      {
        "value": {
          "start_connected": true,
          "pci_slot_number": 192,
          "backing": {
            "connection_cookie": 874396100,
            "distributed_switch_uuid": "50 30 da 68 e0 24 83 85-95 2d d0 3a 5a 8b 9d be",
            "distributed_port": "410",
            "type": "DISTRIBUTED_PORTGROUP",
            "network": "dvportgroup-7775"
          },
          "mac_address": "00:50:56:b0:f8:8d",
          "mac_type": "MANUAL",
          "allow_guest_control": true,
          "wake_on_lan_enabled": true,
          "label": "Network adapter 1",
          "state": "CONNECTED",
          "type": "VMXNET3",
          "upt_compatibility_enabled": true
        },
        "key": "4000"
      }
    ],
    "boot": {
      "delay": 0,
      "retry_delay": 10000,
      "enter_setup_mode": false,
      "type": "BIOS",
      "retry": false
    },
    "serial_ports": [],
    "guest_OS": "CENTOS_7_64",
    "boot_devices": [
      {
        "disks": [
          "2000"
        ],
        "type": "DISK"
      },
      {
        "type": "CDROM"
      }
    ],
    "hardware": {
      "upgrade_policy": "NEVER",
      "upgrade_status": "NONE",
      "version": "VMX_13"
    }
  }
}
```
#### Step 3: Check if the verdad item with the server name exist  
```python
curl -I -s -k  -o /dev/null -w "%{http_code}"  -X GET \
-H 'cache-control: no-cache' -H 'verdad-api-key:$VERDAD_API_KEY' 
"https://internal.api.srekoc.net/v1/devops/configstore/v1/items/jim02.pool.dc.srekoc.net" 
```

#### Step 4: If doesnt exist, create a new verdad item
```python
curl -s -k -X POST \
-H 'cache-control: no-cache' -H 'verdad-api-key:$VERDAD_API_KEY' \
"https://internal.api.srekoc.net/v1/devops/configstore/v1/items/sre-jenkins04.dc.srekoc.net" \
-d @z.json

z.json:
{
    "commitMsg": "creating a new verdad item",
    "items": [
        {
     "tags": {
       "is": {
         "values": [
           "hw-VM-2D",
           "nz-infra-oos.dc.srekoc.net",
           "cde-cicd-users",
           "accessible-to-cicd-dc"
         ]
       },
       "network.ip.1": {
         "values": [
           "10.81.7.36"
         ]
       },
       "network.hostname.1": {
         "values": [
           "sre-jenkins04.dc.srekoc.net"
         ]
       },
       "inventory.scope": {
         "values": [
           "oos"
         ]
       },
       "network.dnsname.1": {
         "values": [
           "sre-jenkins04"
         ]
       },
       "hardware.mac.1": {
         "values": [
           "00:50:56:b0:37:00"
         ]
       }
     },
     "name": "sre-jenkins04.dc.srekoc.net",
     "policy": "create"
   }

   ]
 }
```

####Step 5: If verdad item for server exists, update mac address
```python
curl -k -X PUT  \
"https://internal.api.srekoc.net/v1/devops/configstore/v1/items/jim01.pool.dc.srekoc.net/tags/hardware.mac.1"  \
-H 'cache-control: no-cache' -H 'verdad-api-key:$VERDAD_API_KEY' \
-d '{ "commitMsg":"updating mac address", "policy":"replace", "values":[ "00:50:56:AF:9A:F2" ] }'
```

#### followup steps
run `central-push` manually

#### Reboot the VMs
Reboot the VMs else ssh'ng to server is impossible as network setting would not take effect
```python
curl -X POST  \
-H "vmware-api-session-id: $SESSION_ID" \
https:///vm-mgr01.infra.dc.srekoc.net/vcenter/vm/vm-32028/guest/power?action=reboot
```
### Some useful FAQs

#####How to write packer logs?
```shell
$ export PACKER_LOG_PATH="/var/log/packer.log"
$ export PACKER_LOG=10
$ packer build -debug <JSON file>
```
#####Whats packer build command?
```shell
PACKER_LOG=1 packer build centos-vsphere.json
```
##### Documentation for Verdad RESTful apis?
```shell
/home/mcuddy/public_html/home/work/tools/verdad/REST/ENDPOINTS.md
/home/skocharlakota/ENDPOINTS.md
```
##### How to fetch a vsphere session id?
```shell
curl -s -k -X POST --header 'Accept: application/json' -u "$USERNAME:$PASSWORD" "https://vm-mgr01.infra.dc.srekoc.net/rest/com/vmware/cis/session" --insecure -c session | jq -r .value
```
#####How to reboot VMs in vsphere via RESTful apis?
```shell
curl -X POST -H "vmware-api-session-id: $SESSION_ID" https:///vm-mgr01.infra.dc.srekoc.net/vcenter/vm/vm-32028/guest/power?action=reboot     
curl -X POST -H "vmware-api-session-id: $SESSION_ID" https:///vm-mgr01.infra.dc.srekoc.net/vcenter/vm/vm-32028/guest/power?action=reboot 
```

##### How to print verdad items of a server?
```shell
curl -s -k -X GET \
-H 'cache-control: no-cache' -H 'verdad-api-key:$VERDAD_API_KEY' \
"https://internal.api.srekoc.net/v1/devops/configstore/v1/items/jim01.pool.dc.srekoc.net" 
```
##### How to print just mac address of a server via verdad?
```shell
curl -s -k -X GET \
-H 'cache-control: no-cache' -H 'verdad-api-key:$VERDAD_API_KEY' \
"https://internal.api.srekoc.net/v1/devops/configstore/v1/items/sre-jenkins01.dc.srekoc.net/tags/hardware.mac.1" 
```
##### How to delete a verdad item?
```shell
curl -s -k  -X DELETE -H "cache-control: no-cache" -H "verdad-api-key:$VERDAD_API_KEY" "https://internal.api.srekoc.net/v1/devops/configstore/v1/items/sre-jenkins04.dc.srekoc.net?commitMsg=text&ignoreErr"
```
#####How to create a new verdad item?
```shell
curl -s -k  -X POST -H "cache-control: no-cache" -H "verdad-api-key:$VERDAD_API_KEY" https://internal.api.srekoc.net/v1/devops/configstore/v1/items/sre-jenkins04.dc.srekoc.net -d @a.json

a.json
{
    "commitMsg":"creating verdad item",
    "items": [
     {   
        "name": "{vm_name}",
        "tags": {
            "provisioning_type": {
                "policy": "append",
                "values": [
                "terraform"
                ]
            },
            "is": {
                "policy": "append",
                "values": [
                "hw-VM-2D",
                "{verdad_network_name}"
                ]
            },
            "network.dnsname.1": {
                "policy": "append",                
                "values": [
                "{dns_name}"
                ]
            },
            "inventory.scope": {
                "policy": "append",                
                "values": [
                "{inventory_scope}"
                ]
            },
            "hardware.mac.1": {
                "policy": "append",                
                "values": [
                "{vsphere_mac_address}"
                ]
            },
            "network.hostname.1": {
                "policy": "append",                
                "values": [
                "{vm_name}"
                ]
            },
            "network.ip.1": {
                "policy": "append",                
                "values": [
                "{ip_address}"
                ]
            }
        }  
      
      }
    ]
}
```

#### How to update a verdad item?
```shell
curl -k -X PUT  "https://internal.api.srekoc.net/v1/devops/configstore/v1/items/sre-jenkins01.dc.srekoc.net/tags/hardware.mac.1" \
-H 'cache-control: no-cache' -H 'verdad-api-key:$VERDAD_API_KEY' \
-d '{ "commitMsg":"updating mac address", "policy":"replace", "values":[ "00:50:56:b0:37:2e" ] }'
```

##### How to fetch a verdad item status?
```shell
curl -I -s -k  -o /dev/null -w "%{http_code}"  -X GET \
-H 'cache-control: no-cache' -H 'verdad-api-key:${api_key}' 
"https://internal.api.srekoc.net/v1/devops/configstore/v1/items/jim02.pool.dc.srekoc.net" 
'
```


#####Additional helpful REST apis

```shell
PROD_API="https://internal.api.srekoc.net/v1/devops/configstore/v1/items"
ITEM="mcuddy-test-1"
TAG="script-tag"
curl -s -S -k -X PUT -H "Verdad-Api-Key:$API_KEY,mcuddy" $PROD_API/$ITEM/tags/$TAG -d '{ "commitMsg":"test commit from API", "policy":"replace", "values":[ "value1", "value2" ] }'

curl -s -k -X GET https://internal.api.srekoc.net/v1/devops/configstore/v1/items/jim01.pool.dc.srekoc.net/tags/release.type -H 'cache-control: no-cache' -H 'verdad-api-key:$VERDAD_API_KEY'";

Working query:
curl -k -X PUT  "https://internal.api.srekoc.net/v1/devops/configstore/v1/items/jim01.pool.dc.srekoc.net/tags/hardware.mac.1"  -H 'cache-control: no-cache' -H 'verdad-api-key:$VERDAD_API_KEY'  -d '{ "commitMsg":"test commit from API", "policy":"replace", "values":[ "00:50:56:AF:9A:F2" ] }'


curl -X POST \
 -k \
 https://dev.api.dc.srekoc.net/v1/devops/configstore/v1/items/accessible-to-stream-cluster-dprc-bigdata \
 -H 'Verdad-Api-Key: $VERDAD_API_KEY' \
 -d @z.json
{12} shell03!skocharlakota@shell01 % cat z.json
{
   "commitMsg": "checkin message",
   "items": [
       {
           "name" : "accessible-to-stream-cluster-dprc-bigdata",
           "tags" : {
               "sudo-users": {
                   "policy": "append",
                   "values": [
                       "user1: - 2022-11-10",
                       "user2: - 2022-11-18"
                   ]
               }
           }
       }
   ]
}
```