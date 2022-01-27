curl -X PATCH -H "vmware-api-session-id: $SESSION_ID" -H "Content-Type: application/json" 
-d @b.json https://vm-mgr01.infra.dc.srekoc.net/rest/vcenter/vm/vm-32039/hardware/ethernet/{nic} 

{
  "start_connected": true,
  "pci_slot_number": 192,
  "backing": {
    "connection_cookie": 874396100,
    "distributed_switch_uuid": "50 30 da 68 e0 24 83 85-95 2d d0 3a 5a 8b 9d be",
    "distributed_port": "410",
    "type": "DISTRIBUTED_PORTGROUP",
    "network": "dvportgroup-7775"
  },
  "mac_address": "00:50:56:b0:f8:80",
  "mac_type": "MANUAL",
  "allow_guest_control": true,
  "wake_on_lan_enabled": true,
  "label": "Network adapter 1",
  "state": "CONNECTED",
  "type": "VMXNET3",
  "upt_compatibility_enabled": true
}
