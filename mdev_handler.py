import os
import libvirt
import logging
import configparser
from xml.etree import ElementTree as et
conn = libvirt.openReadOnly('qemu:///system')

MDEV_BASE_DIR = '/sys/bus/mdev/devices/'
domains = conn.listAllDomains(0)
logging.basicConfig(filename = 'mdev_handler.log',
        format = '%(asctime)s %(levelname)s:%(message)s',
        level = logging.INFO,
        filemode='w')
nova_conf = configparser.ConfigParser()
nova_conf.read('/etc/nova/nova.conf')

def create_mdev(devices):
    for i in devices:
        mdev_base_name = f"mdev_{i.replace('-', '_')}"
        conn.listAllDevices()

def delete_mdev(devices):
    for device in devices:
        device_path = f'/sys/bus/mdev/devices/{device}/remove'
        print(os.system('echo "1" > {device_path}')
        logging.info(f'Removed vGPU device with UUID: {device}')

def get_pci_bus_id(device):
    pass

def get_mdev_device_info(uuid):
    pass

def get_uuids_from_bus():
    try:
        uuids = os.listdir(MDEV_BASE_DIR)
        return uuids
    except FileNotFoundError:
        logging.error(f"Directory {MDEV_BASE_DIR} does not exist. If these are sr-iov based cards please make sure /usr/lib/nvidia/sriov-manage was run successfully. Otherwise, I don't know, I'm just an error message.")
        print(f'Unable to locate directory {MDEV_BASE_DIR}')
        quit()


def get_uuids_from_libvirt():
    uuids = []
    for domain in domains:
        dom = conn.lookupByName(domain.name())
        raw_xml = dom.XMLDesc(0)
        xml = et.fromstring(raw_xml)
        for mdev in xml.findall('devices/hostdev'):
            for address in mdev.findall('source/address'):
                uuids.append(address.get('uuid'))
    return uuids

def return_not_matches(a, b):
    return [[x for x in a if x not in b], [x for x in b if x not in a]]


if __name__ == '__main__':
    bus_uuids = get_uuids_from_bus()
    virt_uuids = get_uuids_from_libvirt()
    orphan_mdev,orphan_libvirt = return_not_matches(bus_uuids, virt_uuids)
    devices = nova_conf['devices']['enabled_mdev_types']
    logging.info(f'MDEV Bus UUIDS - {bus_uuids}')
    logging.info(f'Libvirt UUIDS - {virt_uuids}')
    logging.info(f'MDEV Bus UUIDS missing from libvirt - {orphan_mdev}')
    logging.info(f'Libvirt UUIDS missing from MDEV - {orphan_libvirt}')
    logging.info(f'Enabled vGPU types = {devices}')
    if bool(orphan_mdev) == True:
        delete_mdev(orphan_mdev)
        pass
    if bool(orphan_libvirt) == True:
        create_mdev(orphan_libvirt)
    conn.close()
