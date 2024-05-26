
import unittest
from src.engine.network_center.ipv4 import NetworkConfig, IPV4Address
from src.engine.network_center.enums import AdapterType


class TestNetworkConfig(unittest.TestCase):

    def setUp(self):
        # Set up initial configurations for use in multiple tests
        self.initial_ip = IPV4Address(["192", "168", "1", "100"])
        self.subnet = IPV4Address(["255", "255", "255", "0"])
        self.gateway = IPV4Address(["192", "168", "1", "1"])
        self.config = NetworkConfig(AdapterType.ETHERNET, "eth0", self.initial_ip, self.subnet, self.gateway)

    def test_initialization(self):
        # Test initialization and post-init validation
        self.assertEqual(self.config.ipv4_address, self.initial_ip)
        self.assertEqual(self.config.subnet_mask, self.subnet)
        self.assertEqual(self.config.default_gateway, self.gateway)

    def test_update_configuration(self):
        # Test updating the configuration
        new_ip = IPV4Address(["192", "168", "1", "101"])
        self.config.update_configuration({'ipv4_address': new_ip})
        self.assertEqual(self.config.ipv4_address, new_ip)

    def test_has_changed(self):
        # Test change detection
        new_ip = IPV4Address(["192", "168", "1", "102"])
        self.config.update_configuration({'ipv4_address': new_ip})
        self.assertTrue(self.config.has_changed())

    def test_reset_baseline(self):
        # Test resetting the baseline
        self.config.reset_baseline()
        self.assertFalse(self.config.has_changed())

    def test_clone(self):
        # Test cloning functionality
        clone = self.config.clone()
        self.assertEqual(clone, self.config)
        self.assertNotEqual(id(clone), id(self.config))  # Ensure it's a deep copy

    def test_to_dict(self):
        # Test exporting configuration to dictionary
        config_dict = self.config.to_dict()
        expected_dict = {
            "adapter_prefix": AdapterType.ETHERNET,
            "adapter_name": "eth0",
            "ipv4_address": "192.168.1.100",
            "subnet_mask": "255.255.255.0",
            "default_gateway": "192.168.1.1"
        }
        self.assertEqual(config_dict, expected_dict)

    def test_invalid_update(self):
        # Test handling of invalid update attempts
        with self.assertRaises(ValueError):
            self.config.update_configuration({'ipv4_address': "invalid_type"})

    def test_manual_octet_change(self):
        # Initially, ensure no changes are detected
        self.assertFalse(self.config.has_changed(), "Should start with no changes detected")

        # Manually change an octet
        new_octet_value = "102"
        self.config.ipv4_address.octets[2] = new_octet_value

        # Check if the change is detected
        self.assertTrue(self.config.has_changed(), "Change in octet should be detected as a configuration change")

    def test_from_dict(self):
        # Create a NetworkConfig instance from a dictionary
        config_dict = {
            "adapter_prefix": "ETHERNET",
            "adapter_name": "eth1",
            "ipv4_address": "10.0.0.1",
            "subnet_mask": "255.255.255.0",
            "default_gateway": "10.0.0.254"
        }
        config_from_dict = NetworkConfig.from_dict(config_dict)
        self.assertEqual(config_from_dict.adapter_name, "eth1")
        self.assertEqual(str(config_from_dict.ipv4_address), "10.0.0.1")

    def test_invalid_data_in_update(self):
        # Test invalid adapter_prefix update
        with self.assertRaises(ValueError):
            self.config.update_configuration({'adapter_prefix': 'INVALID_TYPE'})

    def test_edge_cases(self):
        # Testing edge case for minimal and maximal IP addresses
        edge_config = NetworkConfig(
            adapter_prefix=AdapterType.ETHERNET,
            adapter_name="edge_test",
            ipv4_address=IPV4Address(["0", "0", "0", "0"]),
            subnet_mask=IPV4Address(["255", "0", "0", "0"]),
            default_gateway=IPV4Address(["255", "255", "255", "255"])
        )
        self.assertTrue(edge_config, "Edge case configuration should be valid")

    def test_valid_initialization(self):
        ip = IPV4Address(["192", "168", "0", "1"])
        self.assertEqual(str(ip), "192.168.0.1")

    def test_invalid_initialization(self):
        with self.assertRaises(ValueError):
            IPV4Address(["300", "168", "0", "1"])  # Invalid octet
        with self.assertRaises(ValueError):
            IPV4Address(["192", "168", "0"])      # Not enough octets

    def test_from_string(self):
        ip = IPV4Address.from_string("192.168.0.1")
        self.assertEqual(ip.octets, ["192", "168", "0", "1"])

    def test_setitem_valid(self):
        ip = IPV4Address(["192", "168", "0", "1"])
        ip[2] = "10"
        self.assertEqual(ip[2], "10")

    def test_setitem_invalid(self):
        ip = IPV4Address(["192", "168", "0", "1"])
        with self.assertRaises(ValueError):
            ip[2] = "256"  # Invalid value

    def test_copy_from(self):
        ip1 = IPV4Address(["192", "168", "0", "1"])
        ip2 = IPV4Address(["10", "0", "0", "1"])
        ip1.copy_from(ip2)
        self.assertEqual(str(ip1), "10.0.0.1")

    def test_valid_subnet_mask(self):
        ip = IPV4Address(["255", "255", "255", "0"])
        self.assertTrue(ip.is_valid_subnet_mask())

    def test_invalid_subnet_mask(self):
        ip = IPV4Address(["255", "255", "255", "10"])
        self.assertFalse(ip.is_valid_subnet_mask())

    def test_equality(self):
        ip1 = IPV4Address(["192", "168", "0", "1"])
        ip2 = IPV4Address(["192", "168", "0", "1"])
        ip3 = IPV4Address(["10", "0", "0", "1"])
        self.assertEqual(ip1, ip2)
        self.assertNotEqual(ip1, ip3)

    def test_default_initialization(self):
        """Test that default values are correctly initialized."""
        config = NetworkConfig()
        self.assertEqual(config.adapter_prefix, AdapterType.ETHERNET)
        self.assertEqual(config.adapter_name, 'Ethernet')
        self.assertEqual(config.ipv4_address, IPV4Address.from_string('0.0.0.0'))
        self.assertEqual(config.subnet_mask, IPV4Address.from_string('255.255.255.0'))
        self.assertEqual(config.default_gateway, IPV4Address.from_string('0.0.0.0'))

    def test_instance_independence(self):
        """Test that each instance has independent default values."""
        config1 = NetworkConfig()
        config2 = NetworkConfig()

        # Modify config1
        config1.ipv4_address = IPV4Address.from_string('192.168.1.1')
        config1.subnet_mask = IPV4Address.from_string('255.255.0.0')

        # Ensure config2 is still at default
        self.assertEqual(config2.ipv4_address, IPV4Address.from_string('0.0.0.0'))
        self.assertEqual(config2.subnet_mask, IPV4Address.from_string('255.255.255.0'))

    def test_correct_default_values(self):
        """Ensure that fields have the expected default values."""
        config = NetworkConfig()
        self.assertEqual(str(config.ipv4_address), '0.0.0.0')
        self.assertEqual(str(config.subnet_mask), '255.255.255.0')
        self.assertEqual(str(config.default_gateway), '0.0.0.0')


if __name__ == '__main__':
    unittest.main()
