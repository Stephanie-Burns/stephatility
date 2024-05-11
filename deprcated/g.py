
import sys
import subprocess


def run_ip_change_as_admin(new_ip: str, subnet_mask: str, gateway: str, interface_name: str) -> None:
    script = 'script_ip_change.py'                                      # TODO set to abs path later
    command = [
        sys.executable, script,
        '--set-ip', new_ip,
        '--subnet-mask', subnet_mask,
        '--gateway', gateway,
        '--interface', interface_name
    ]
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to run script: {e}")
