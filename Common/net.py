"""
Networking Stuff.
"""

import requests
import socket


def is_vpn_connected():
    """
    Determine whether our VPN is connected. Checks whether our IP address
    comes from a pool of public addresses associated with our VPN provider.

    @return: is_vpn_connected - Connection Status [Bool]
    """

    # List of public IPs associated with VPN nodes.
    vpn_list = load_vpn_list()

    # Resolve using socket to avoid getting an IPv6 address
    r = requests.get("http://%s" % socket.gethostbyname('icanhazip.com'))
    ip = r.text.split()[0]

    if ip in vpn_list:
        return True
    else:
        return False


def load_vpn_list(fname='vpn_list'):
    """
    Load list of external IP addresses associated with a VPN provider.

    Format is one IP per line, i.e.
    1.1.1.1
    1.1.1.2
    ...

    See also vpn_list_example.

    @param: fname      - File name for list of external IPs [String]
    @returns: vpn_list - List of external IPs               [List of String]
    """

    # Loading gives lines = [ '1.1.1.1\n', '1.1.1.2\n' ].
    # After stripping, gives vpn_list = [ '1.1.1.1', '1.1.1.1' ].
    with open(fname, 'r') as f:
        lines = f.readlines()
        vpn_list = []
        for line in lines:
            vpn_list.append(line.strip())

    # Return
    return vpn_list
