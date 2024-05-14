import unittest

from src.network_tools import IPV4Address


class TestIPV4Address(unittest.TestCase):
    def setUp(self):
        self.ip_address = IPV4Address(["192", "168", "1", "1"])

    def test_valid_initialization(self):
        ip = IPV4Address(["192", "168", "1", "10"])
        self.assertEqual(str(ip), "192.168.1.10")

    def test_invalid_initialization(self):
        with self.assertRaises(ValueError):
            IPV4Address(["256", "168", "1", "10"])  # Out of range value
        with self.assertRaises(ValueError):
            IPV4Address(["192", "168", "1"])       # Insufficient octets

    def test_invalid_characters(self):
        with self.assertRaises(ValueError):
            IPV4Address(["192", "abc", "1", "10"])  # Non-integer characters

    def test_setitem_valid(self):
        ip = IPV4Address(["192", "168", "1", "10"])
        ip[2] = "100"
        self.assertEqual(ip[2], "100")

    def test_setitem_invalid(self):
        ip = IPV4Address(["192", "168", "1", "10"])
        with self.assertRaises(ValueError):
            ip[2] = "256"  # Out of valid range

    def test_copy_from(self):
        ip1 = IPV4Address(["192", "168", "1", "10"])
        ip2 = IPV4Address(["10", "0", "0", "1"])
        ip1.copy_from(ip2)
        self.assertEqual(str(ip1), "10.0.0.1")
        self.assertNotEqual(id(ip1.octets), id(ip2.octets))  # Ensure it's not the same list

    def test_valid_subnet_mask(self):
        ip = IPV4Address(["255", "255", "255", "0"])
        self.assertTrue(ip.is_valid_subnet_mask())

    def test_invalid_subnet_mask(self):
        ip = IPV4Address(["255", "255", "255", "10"])
        self.assertFalse(ip.is_valid_subnet_mask())

    def test_string_representation(self):
        ip = IPV4Address(["192", "168", "1", "10"])
        self.assertEqual(str(ip), "192.168.1.10")

    def test_equality(self):
        ip1 = IPV4Address(["192", "168", "1", "10"])
        ip2 = IPV4Address(["192", "168", "1", "10"])
        ip3 = IPV4Address(["10", "0", "0", "1"])
        self.assertEqual(ip1, ip2)
        self.assertNotEqual(ip1, ip3)

    def test_from_string(self):
        ip = IPV4Address.from_string("192.168.1.10")
        self.assertEqual(ip.octets, ["192", "168", "1", "10"])

    def test_boundary_values(self):
        # Testing boundary values for octets
        with self.assertRaises(ValueError):
            IPV4Address(["-1", "168", "1", "10"])
        with self.assertRaises(ValueError):
            IPV4Address(["256", "168", "1", "10"])
        ip = IPV4Address(["0", "0", "0", "0"])
        self.assertEqual(str(ip), "0.0.0.0")
        ip = IPV4Address(["255", "255", "255", "255"])
        self.assertEqual(str(ip), "255.255.255.255")


    def test_update_from_string_valid(self):
        """Test updating IPV4Address with a valid string."""
        self.ip_address.update_from_string("10.0.0.1")
        self.assertEqual(self.ip_address.octets, ["10", "0", "0", "1"])
        self.assertEqual(str(self.ip_address), "10.0.0.1")

    def test_update_from_string_invalid(self):
        """Test updating IPV4Address with an invalid string raises ValueError."""
        with self.assertRaises(ValueError):
            self.ip_address.update_from_string("256.100.100.1")  # Invalid octet value
        with self.assertRaises(ValueError):
            self.ip_address.update_from_string("10.0.0")  # Not enough octets

    def test_update_from_string_preserves_instance(self):
        """Test that update_from_string preserves the instance."""
        original_id = id(self.ip_address)
        self.ip_address.update_from_string("10.0.0.1")
        updated_id = id(self.ip_address)
        self.assertEqual(original_id, updated_id)

    def test_update_from_string_boundary(self):
        """Test updating IPV4Address with boundary values."""
        self.ip_address.update_from_string("0.0.0.0")
        self.assertEqual(self.ip_address.octets, ["0", "0", "0", "0"])
        self.ip_address.update_from_string("255.255.255.255")
        self.assertEqual(self.ip_address.octets, ["255", "255", "255", "255"])

    def test_equality_with_ipv4address_instance(self):
        """Test equality between IPV4Address instances."""
        other_ip = IPV4Address(["192", "168", "1", "1"])
        self.assertTrue(self.ip_address == other_ip)

    def test_equality_with_string(self):
        """Test equality comparison with a valid IP address string."""
        self.assertTrue(self.ip_address == "192.168.1.1")

    def test_inequality_with_different_ipv4address_instance(self):
        """Test inequality between different IPV4Address instances."""
        other_ip = IPV4Address(["192", "168", "1", "2"])
        self.assertFalse(self.ip_address == other_ip)

    def test_inequality_with_different_string(self):
        """Test inequality comparison with a different IP address string."""
        self.assertFalse(self.ip_address == "192.168.1.2")

    def test_inequality_with_invalid_string(self):
        """Test that comparison with an invalid IP address string returns False."""
        self.assertFalse(self.ip_address == "192.168.300.1")

    def test_equality_with_non_ip_string(self):
        """Test that comparison with a non-IP address string returns False."""
        self.assertFalse(self.ip_address == "not an ip")

    def test_equality_with_other_object_types(self):
        """Test that comparison with different types like list returns NotImplemented."""
        self.assertFalse(self.ip_address == ["192", "168", "1", "1"])


if __name__ == '__main__':
    unittest.main()
