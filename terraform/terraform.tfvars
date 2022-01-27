# VMware VMs configuration #
vm-count = "3"
vm-template-name = "gold-template.dc.srekoc.net"
vm-cpu-num = "2"
vm-mem-size = "4096"
vm-guest-id = "centos7_64Guest"
# VMware vSphere configuration #
# VMware vCenter IP/FQDN
vsphere-server = "vm-mgr01.infra.dc.srekoc.net"
# VMware vSphere username used to deploy the infrastructure
# vsphere-username = "skocharlakota"
# VMware vSphere password used to deploy the infrastructure
# vsphere-password = "Newyork#12"
# Skip the verification of the vCenter SSL certificate (true/false)
vsphere-unverified-ssl = "true"
# vSphere datacenter name where the infrastructure will be deployed 
vsphere-datacenter = "dc"
# vSphere cluster name where the infrastructure will be deployed
vsphere-cluster = "dc-CLUSTER01"
# vSphere Datastore used to deploy VMs 
vsphere-datastore = "dc_cluster01_ssd03"
# vSphere Network used to deploy VMs 
vsphere-network = "DV_PG_OOS_INFRA1"
# Linux virtual machine domain name
vm-domain = "dc.srekoc.net"
vm-subname = "sre-jenkins"
verdad_network_name = "nz-infra-oos.dc.srekoc.net" # if DV_PG_OOS_INFRA1 
inventory_scope = "oos"
vm-first-disk-size = 25
vm-second-disk-size = 60
vm_ips = {
    "0" = "10.81.7.33"
    "1" = "10.81.7.34"
    "2" = "10.81.7.35"
}

dns_search_domains = [
    "dc.srekoc.net",
    "srekoc.net",
    "srekoc",
]

