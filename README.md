# vgpu-openstack
The purpose of this project is to provide instructions on how to enable vgpu_unlock (https://github.com/DualCoder/vgpu_unlock) in an OpenStack environment, using OpenStack-Ansible All-in-One (AIO) to deploy the environment.

## Why VGPU-OpenStack?
That's a good question. There are a lot of fantastic virtualization management systems (Proxmox, Unraid, etc.). All I'm trying to provide is another option. Personally I think OpenStack is great if you want to provide a front end system to remote users that they can manage the virtualized resources themselves, only requiring you to manage the underlying backend. Think of it like providing your own AWS. Combined with a project like vGPU I think it's a fantastic way to setup and provide some virtualized gaming instances with your resources 

## Instructions
#### Requirements
* **CPU**: As many cores as you can get with support for virtualization.
* **RAM**: I'd recommend AT LEAST 16GB, but as much as you can get, the better
* **GPU**: An NVidia Maxwell, Pascal or Turing GPU supported by vgpu_unlock. Limited support is available as well for Volta and Ampere models, but check the vgpu_unlock project as new models are added all the time. For my example, I will be using an RTX 2080Ti. More VRAM allows the use of more and/or larger VMs.
* **Disk**: At least 256GB but I'd recommend 500GB+ if you plan on running more than 1-2 VMs. Also recommend using an SSD.
* **Network**: At least one 1Gbps network port. This project will work on a single, flat network, however having VLAN support will allow you to have separate the front-end access to the VMs and use non-tunneled networks.

#### Preparation
Install Ubuntu 20.04 on the host. You CAN use a Red Hat-based distro, such as CentOS 8, however you will need to adjust the commands in this guide to your distro.

