#!/bin/bash

sudo apt install qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils
sudo adduser `id -un` libvirt

sudo apt install virt-manager
