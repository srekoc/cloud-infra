
# vm-provisioning 

creates vsphere machine images and enables cloning of vms

## Overview
Packer is a tool for creating identical machine images for multiple platforms from a single source configuration file. It can build images for multiple private and public cloud hosting platforms, including vsphere. 

Terraform is an open source tool for building, changing, and versioning infrastructure safely and efficiently.

The repo is right now dedicated to spinning templates and vms in the private cloud (vsphere focussed)

## prerequisites
####software
In order for the software to work correctly, these are the bare minimum
- access to bastion (shell) hosts
- python3
- packer
- terraform
- python modules
    - urllib3
    - logging
    - requests
	
####ip procurement
To spin up vms it is imperative to reserve IP addresses via internal IPAM tool. 
https://intranet.dev.com/netops/networking/ip-assignments/srekoc/index.html

## credentials
The credentials are needed for vsphere and verdad to get the RESTful apis right. 
- vsphere (https://registry.terraform.io/providers/hashicorp/vsphere/latest/docs)
- verdad (http://verdad.sourceforge.net/)

## variables
The defaults for the template created are given in the table. If you would want to do things differently these variables must be updated for packer and terraform to pick up.

The variables are relevant inside of packer and terraform code. You can see the same variable names being used in packer code and as well in terraform code (.tfvars file)

| variable name  | data type | description | defaults
| ------------- | ------------- | ------------- | ------------- |
| vm_ips | string | IP addresses for assigning to vms, to procure IPs use IPAM tool | vm_ips = {   "0" = "10.81.7.33" "1" = "10.81.7.34" "2" = "10.81.7.35"} |
| iso_url | string  | iso_url (string) - A URL to the ISO containing the installation image or virtual hard drive (VHD or VHDX) file to clone.|[dc_cluster01_ssd03] CentOS-7-x86_64-Minimal-2003.iso|
| vm-cpu-num  | string | CPUs (int32) - Number of CPU cores. | 1 |
| vm-first-disk-size | string | primary or OS disk size | 25600 (25GB) |
| vm-second-disk-size (not optional) | string | data disk size (persistent volume) | 60000 (60GB)|
| vm-mem-size | string | RAM size | 1024 ( 1GB) |
| vm-template-name | string | vsphere vm template name | gold-template.dc.srekoc.net |
| vsphere-cluster | string | cluster (string) - Cluster onto which the virtual machine template should be placed. If cluster and resource_pool are both specified, resource_pool must belong to cluster. If cluster and host are both specified, host must be a member of cluster. | dc-CLUSTER01 |
| vsphere-datacenter | string | datacenter (string) - VMware datacenter name. Required if there is more than one datacenter in vCenter.| dc|
| vsphere-datastore | string | datastore (string) - VMWare datastore. Required if host is a cluster, or if host has multiple datastores. | dc_cluster01_ssd03 |
| vsphere-network | string | network_adapters ([]NIC) - Network adapters | DV_PG_OOS_INFRA1 |
| vsphere-server | string | vsphere url endpoint | vm-mgr01.infra.dc.srekoc.net |

## additional terraform variables
| variable name  | data type | description | defaults
| ------------- | ------------- | ------------- | ------------- |
| vm-domain | string | subnet name | dc.srekoc.net|
| vm-subname | string | dns name, terraform derives the server name from this string | sre-jenkins |
| verdad_network_name | string | verdad network zone verdad bit | nz-infra-oos.dc.srekoc.net |
| inventory_scope | string | helps with easy search in verdad item for oos, c2c & cde servers | oos|

## Usage

#### packer
punch in your vsphere credentials

```python
PACKER_LOG=1 packer build \
-var 'vsphere_username=<YOUR_dev_USERNAME>' \
-var 'vsphere_password=<YOUR_dev_PASSWORD>' \ 
centos-vsphere.json
```
#### terraform
punch in your vsphere credentials again :-)

```python
terraform init

terraform plan \
-var 'vsphere_username=<YOUR_dev_USERNAME>' \
-var 'vsphere_password=<YOUR_dev_PASSWORD>'

terraform apply \
-var 'vsphere_username=<YOUR_dev_USERNAME>' \
-var 'vsphere_password=<YOUR_dev_PASSWORD>'

# Do not use this unless you want to destroy what you created :-)
terraform destroy \
-var 'vsphere_username=<YOUR_dev_USERNAME>' \
-var 'vsphere_password=<YOUR_dev_PASSWORD>'

```
#### central-push
This is a standard process to get the correct network settings for the vms.  From any bastion/shell hosts execute the command

```python
ssh verdad01 central-push
```

#### reset vms
reboot the servers after the central-push is successful via the commands in the reset_vms file. This part can be automated, but not yet done. 

```python
cat ../shell/reset_vms
```

## Limitations
- The state files are not stored remotely yet. Feature will be added soon
- The soruce works for dc and is tested 

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Author
Sreekanth Kocharlakota
