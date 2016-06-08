"""
Read, Parse, Post Stats to InfluxDB.
"""

import Common.sensors as sensors
import Common.influx as influx
import Common.net as net
import argparse


# #############################################################################
# Parse Arguments
# #############################################################################
parser = argparse.ArgumentParser()
parser.add_argument('--netatmo', action='store_true', \
                    help="Query and Push Netatmo Data.")
parser.add_argument('--vpn', action='store_true', \
                    help="Query and Push VPN Status.")
args = parser.parse_args()

# Sanity Check
if not args.netatmo and not args.vpn:
    raise Exception('Nothing Queried. Terminating.')

# #############################################################################
# Load Data from Netatmo
# #############################################################################
if args.netatmo:
    readings, epochs = sensors.get_netatmo_readings()

# #############################################################################
# Check VPN Status
# #############################################################################
if args.vpn:
    is_vpn_connected = net.is_vpn_connected()

# #############################################################################
# Build Data Post
# NB: For InfluxDB >=0.9.3, integer data points require a trailing i.
#     For example, ncpus_allocated,parititon=cpu value=5i
# #############################################################################
lines = []

# Netatmo w/ Sanitized Strings (Remove Caps, Spaces to Underscore)
if args.netatmo:
    for module_name, module_values in zip(readings.keys(), readings.values()):
        for value_name, value in zip(module_values.keys(), module_values.values()):
            line = "%s,module=%s value=%.2f %i" % \
                ( value_name.lower(), \
                  '_'.join(module_name.lower().split(' ')), \
                  value, \
                  epochs[module_name] )
            lines.append(line)

# VPN Status
if args.vpn:
    line = "is_vpn_connected value=%s" % is_vpn_connected
    lines.append(line)

# Join
data = "\n".join(lines)

# #############################################################################
# Post Data
# #############################################################################
influx.post_data(data)
