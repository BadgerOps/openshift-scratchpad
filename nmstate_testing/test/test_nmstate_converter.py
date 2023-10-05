#!/usr/bin/env python3 

import unittest
from nmstate_converter import CSVToNMStateConverter
import yaml

class TestCSVToNMState(unittest.TestCase):

    def setUp(self):
        """Setup method called before each test."""
        self.converter = CSVToNMStateConverter("test/example.csv", output_file="output.yaml", template_file="test/example_nmstate_config.yaml")

    def test_csv_to_nmstate(self):
        """Test the conversion of CSV data to nmstate configuration."""
        config = self.converter.csv_to_nmstate()

        # Validate the basic structure
        self.assertIn("apiVersion", config)
        self.assertIn("kind", config)
        self.assertIn("metadata", config)
        self.assertIn("spec", config)
        
        #  YOLO does the keys exist
        self.assertEqual(config["metadata"]["name"], "Linux Bridge and VLAN Configs")
        self.assertTrue(any(iface["name"] == "br1.vlan100" for iface in config["spec"]["desiredState"]["interfaces"]))

    def test_save_to_yaml(self):
        """Test that the nmstate configuration is saved correctly to a YAML file."""
        self.converter.convert()  # This will save the YAML to the default "output.yaml"
        
        with open("output.yaml", 'r') as yamlfile:
            output_config = yaml.safe_load(yamlfile)

        self.assertIn("apiVersion", output_config)
        self.assertIn("kind", output_config)
        self.assertIn("metadata", output_config)
        self.assertIn("spec", output_config)

        # TODO: more. MORE.

if __name__ == "__main__":
    unittest.main()
