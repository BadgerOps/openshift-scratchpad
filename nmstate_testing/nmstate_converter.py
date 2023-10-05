#!/usr/bin/env python3

import csv
import argparse
import yaml

def csv_to_nmstate(filename):
    with open(filename, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        interfaces = {}
        for row in reader:
            interface_name = row['interface_name']
            if interface_name not in interfaces:
                interfaces[interface_name] = []
            interfaces[interface_name].append(row)

        # Create nmstate configuration
        nmstate_config = {
            'apiVersion': 'nmstate.io/v1alpha1',
            'kind': 'NodeNetworkConfigurationPolicy',
            'metadata': {},
            'spec': {
                'nodeSelector': {},
                'desiredState': {
                    'interfaces': []
                }
            }
        }

        for interface_name, data in interfaces.items():
            vlan_interfaces = []
            for entry in data:
                vlan_interface = {
                    'name': f'{interface_name}.{entry["vlan"]}',
                    'type': 'vlan',
                    'state': 'up',
                    'ipv4': {
                        'enabled': True,
                        'address': [{
                            'ip': entry['ip_address'],
                            'prefix-length': int(entry['cidr'])
                        }],
                        'gateway': entry['gateway']
                    },
                    'vlan': {
                        'base-iface': interface_name,
                        'id': int(entry['vlan'])
                    }
                }
                vlan_interfaces.append(vlan_interface)

            bond_interface = {
                'name': interface_name,
                'type': 'bond',
                'state': 'up',
                'bond': {
                    'mode': '802.3ad',
                    'options': {}
                }
            }
            nmstate_config['spec']['desiredState']['interfaces'].extend(vlan_interfaces)
            nmstate_config['spec']['desiredState']['interfaces'].append(bond_interface)

        return nmstate_config

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a CSV file to a nmstate OpenShift NodeNetworkConfiguration policy in YAML format.")
    parser.add_argument("-f", "--file", required=True, help="Input CSV file")
    parser.add_argument("-o", "--output", default="output.yaml", help="Output YAML file (default is 'output.yaml')")
    args = parser.parse_args()

    config = csv_to_nmstate(args.file)
    
    with open(args.output, 'w') as outfile:
        yaml.dump(config, outfile, default_flow_style=False)
