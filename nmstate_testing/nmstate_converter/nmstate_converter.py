#!/usr/bin/env python3

import csv
import argparse
import yaml

class CSVToNMStateConverter:
    """
      Convert the given CSV file to a nmstate OpenShift NodeNetworkConfiguration policy.

      Args:
      - filename (str): Path to the input CSV file.

      Returns:
      - dict: A dictionary representing the nmstate configuration.
      """
    def __init__(self, input_file, output_file="output.yaml", template_file="example_nmstate_config.yaml"):
        self.input_file = input_file
        self.output_file = output_file
        self.template_file = template_file

    def csv_to_nmstate(self):
        """Convert the CSV file to nmstate OpenShift NodeNetworkConfiguration policy."""

        # TODO: start using the given template instead of hardcoding in the below for loop...
        with open(self.template_file, 'r') as yamlfile:
            nmstate_config = yaml.safe_load(yamlfile)

        # Read the CSV and update the nmstate_config based on your needs.
        with open(self.input_file, mode='r') as csvfile:
            reader = csv.DictReader(csvfile)
            interfaces = {}

            for row in reader:
                interface_name = row['interface_name']
                if interface_name not in interfaces:
                    interfaces[interface_name] = []
                interfaces[interface_name].append(row)

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

                nmstate_config['spec']['desiredState']['interfaces'].extend(vlan_interfaces)

        return nmstate_config

    def save_to_yaml(self, nmstate_config):
        """Save the nmstate config to a YAML file."""
        with open(self.output_file, 'w') as outfile:
            yaml.dump(nmstate_config, outfile, default_flow_style=False)

    def convert(self):
        """Convert the input CSV to the nmstate format and save it to the output file."""
        config = self.csv_to_nmstate()
        self.save_to_yaml(config)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert a CSV file to a nmstate OpenShift NodeNetworkConfiguration policy in YAML format.")
    parser.add_argument("-f", "--file", required=True, help="Input CSV file")
    parser.add_argument("-t", "--template", required=False, help="Template file", default='./example_nmstate_config.yaml')
    parser.add_argument("-o", "--output", default="output.yaml", help="Output YAML file (default is 'output.yaml')")
    args = parser.parse_args()

    converter = CSVToNMStateConverter(args.file, args.output)
    converter.convert()
