import unittest

from network_tools import IPV4Address


class TestIPV4Address(unittest.TestCase):

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



if __name__ == '__main__':
    unittest.main()
