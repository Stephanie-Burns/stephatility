
import argparse
from windows_ip_manager import WindowsIPManager  # Assuming your class is in this module


def main():
    parser = argparse.ArgumentParser(description="Manage IP configuration for Windows systems.")
    parser.add_argument('--set-ip', required=True, help='Set a new IP address')
    parser.add_argument('--subnet-mask', default="255.255.255.0", help='Subnet mask for the new IP')
    parser.add_argument('--gateway', default="192.168.1.1", help='Default gateway for the new IP')
    parser.add_argument('--interface', default='Ethernet', help='Interface to configure')
    args = parser.parse_args()

    ip_manager = WindowsIPManager(interface_name=args.interface)
    if ip_manager.is_admin():
        print(f"Running as admin! Current IP Address: {ip_manager.current_ip}")
        if ip_manager.set_ip(args.set_ip, args.subnet_mask, args.gateway):
            print(f"Updated IP Address: {ip_manager.current_ip}")
        else:
            print("Failed to update IP address.")
    else:
        print("Not running as admin.")

if __name__ == "__main__":
    main()
