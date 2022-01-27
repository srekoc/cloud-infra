# =================== #
# Deploying VMware VM #
# =================== #
# Connect to VMware vSphere vCenter
provider "vsphere" {
user = var.vsphere_username
password = var.vsphere_password
vsphere_server = var.vsphere-server
# If you have a self-signed cert
allow_unverified_ssl = var.vsphere-unverified-ssl
}

# Define VMware vSphere
data "vsphere_datacenter" "dc" {
name = var.vsphere-datacenter
}

data "vsphere_datastore" "datastore" {
name = var.vsphere-datastore
datacenter_id = data.vsphere_datacenter.dc.id
}

data "vsphere_compute_cluster" "cluster" {
name = var.vsphere-cluster
datacenter_id = data.vsphere_datacenter.dc.id
}

data "vsphere_network" "network" {
name = var.vsphere-network
datacenter_id = data.vsphere_datacenter.dc.id
}

data "vsphere_virtual_machine" "template" {
name = "/${var.vsphere-datacenter}/vm/${var.vm-template-name}"
datacenter_id = data.vsphere_datacenter.dc.id
}

# Create VMs
resource "vsphere_virtual_machine" "vm" {
count = var.vm-count
name = "${var.vm-subname}${format("%02s", count.index+1)}.${var.vm-domain}"
resource_pool_id = data.vsphere_compute_cluster.cluster.resource_pool_id
datastore_id = data.vsphere_datastore.datastore.id
num_cpus = var.vm-cpu-num
memory = var.vm-mem-size
guest_id = var.vm-guest-id
network_interface {
network_id = data.vsphere_network.network.id
#use_static_mac = true
#mac_address = var.vm_macs[count.index]
}
# wait_for_guest_net_timeout = 0
disk {
  label = "${var.vm-subname}-${count.index + 1}-disk0"
  unit_number = 0
  size  = var.vm-first-disk-size
}
disk { 
  label = "${var.vm-subname}-${count.index + 1}-disk1"
  unit_number = 1
  size = var.vm-second-disk-size
}
clone {
    template_uuid = data.vsphere_virtual_machine.template.id
    customize {
      timeout = 0
      linux_options {
        host_name = "${var.vm-subname}${format("%02s", count.index+1)}"
        domain    = var.vm-domain
        time_zone = "US/Pacific"
      }
      network_interface {
        ipv4_address = var.vm_ips[count.index]
        ipv4_netmask = var.network_bitmask
      }
      ipv4_gateway    = var.default_gateway
      dns_server_list = var.dns_server_ips
      dns_suffix_list = var.dns_search_domains
    }
  }

}

resource "null_resource" "cluster" {
  count = var.vm-count
  #network_name = var.verdad_network_name 
  #inventory_scope = var.inventory_scope
  triggers = {
    script_checksum = filesha256("../python/post_processor.py")
  }
  provisioner "local-exec" {
    # Bootstrap script called with private_ip of each node in the clutser
    interpreter = ["/bin/bash" ,"-c"]
    command = <<-EOT
    python3 ../python/post_processor.py \
               ${vsphere_virtual_machine.vm[count.index].name} \
               ${vsphere_virtual_machine.vm[count.index].guest_ip_addresses[0]} \
               ${vsphere_virtual_machine.vm[count.index].network_interface[0].mac_address} \
               ${var.verdad_network_name} \
               ${var.inventory_scope} \
               ${var.vsphere_username} \
               ${var.vsphere_password} \
     EOT          
  }
}

resource "null_resource" "final_comments" {

  provisioner "local-exec" {
    interpreter = ["/bin/bash" ,"-c"]

    command = <<-EOT
     echo '#################### IMPORTANT #####################'
     echo 'you must run central-push to ensure the mac addresses are updated'
     echo 'on central-push success execute the commands in ../shell/reset_vms to reboot the servers'
     echo '#####################################################'
    EOT 
  }
  depends_on = [
    null_resource.cluster,
  ]
}
output "ip_and_mac_addresses" {
  value = "${
    concat(flatten([for s in vsphere_virtual_machine.vm[*].guest_ip_addresses: s[0]]), flatten(vsphere_virtual_machine.vm[*].network_interface[*].mac_address))
  }"
}

  