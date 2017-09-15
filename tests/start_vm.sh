#!/usr/bin/env bash
#cp ../Downloads/fortimail-kvm.qcow2 .
#cp ../Downloads/fml/250.qcow2 .

virt-install --connect qemu:///system --noautoconsole --filesystem ${PWD},shared_dir --import --name FortiMail --ram 2048 --vcpus 1 --disk fortimail-kvm.qcow2,size=3 --disk 250.qcow2,size=250 --network bridge=virbr0,mac=00:80:01:01:01:01,model=virtio

exit 0


config system interface
  edit port1
    set ip 192.168.122.12/24
    set allowaccess http https ssh ping telnet
  next
end

config system global
   set rest-api enable
end

config system global
   set pki-mode enable
end