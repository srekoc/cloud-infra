#===========================#
# VMware vCenter connection #
#===========================#
variable "vsphere_username" {
type = string
description = "VMware vSphere user name"
}
variable "vsphere_password" {
type = string
description = "VMware vSphere password"
}
variable "vsphere-server" {
type = string
description = "VMWare vCenter server FQDN / IP"
}
variable "vsphere-unverified-ssl" {
type = string
description = "Is the VMware vCenter using a self signed certificate (true/false)"
}
variable "vsphere-datacenter" {
type = string
description = "VMWare vSphere datacenter"
}
variable "vsphere-cluster" {
type = string
description = "VMWare vSphere cluster"
default = ""
}
variable "vsphere-template-folder" {
type = string
description = "Template folder"
default = "Templates"
}
#================================#
# VMware vSphere virtual machine #
#================================#
variable "vm-count" {
type = string
description = "Number of VM"
default     =  1
}
variable "vm-name-prefix" {
type = string
description = "Name of VM prefix"
default     =  "playtftest"
}
variable "vsphere-datastore" {
type = string
description = "Datastore used for the vSphere virtual machines"
}
variable "vsphere-network" {
type = string
description = "Network used for the vSphere virtual machines"
}
variable "vm-linked-clone" {
type = string
description = "Use linked clone to create the vSphere virtual machine from the template (true/false). If you would like to use the linked clone feature, your template need to have one and only one snapshot"
default = "false"
}
variable "vm-cpu-num" {
type = string
description = "Number of vCPU for the vSphere virtual machines"
default = "2"
}
variable "vm-mem-size" {
type = string
description = "Amount of RAM for the vSphere virtual machines (example: 2048)"
}

variable "vm-subname" {
type = string
description = "The name of the vSphere virtual machines with appropriate naming convention"
}
variable "vm-guest-id" {
type = string
description = "The ID of virtual machines operating system"
}
variable "vm-template-name" {
type = string
description = "The template to clone to create the VM"
}
variable "vm-domain" {
type = string
description = "Linux virtual machine domain name for the machine. This, along with host_name, make up the FQDN of the virtual machine"
default = ""
}
variable "network_bitmask" {
  description = "CIDR network bits (e.g. 255.255.255.0 = 24)"
  #default     = "24"
  default     = "23"
}
variable "default_gateway" {
  description = "IP address of the default gateway"
  #default     = "10.80.133.1"
  default     = "10.81.7.1"
}
variable "dns_server_ips" {
  description = "List of DNS servers to assign to instances"

  default = [
    "10.80.217.32",
  ]
}
variable "dns_search_domains" {
  type = list
  description = "List of DNS domains to configure in resolv.conf"
}

variable "vm_ips" {
  type = map
  description = "vm ip addresses"
}

variable "verdad_network_name" {
  type = string
  description = "verdad network name"
  default     = "nz-infra-oos.dc.srekoc.net"
}

variable "inventory_scope" {
  type = string
  description = "verdad network name"
  default     = "oos"
}

variable "vm-first-disk-size" {
  type = string
  description = "OS or primary disk size"
  default     = 25
}

variable "vm-second-disk-size" {
  type = string
  description = "data disk size (for logs/persistent data)"
  default     = 60
}