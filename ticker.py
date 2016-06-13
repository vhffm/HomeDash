"""
Read, Parse, Post Stats to InfluxDB.
"""

import Common.sensors as sensors
import Common.influx as influx
import Common.net as net
import Common.fs as fs
import socket
import argparse


# #############################################################################
# Parse Arguments
# #############################################################################
parser = argparse.ArgumentParser()
parser.add_argument('--netatmo', action='store_true', \
                    help="Query and Push Netatmo Data.")
parser.add_argument('--vpn', action='store_true', \
                    help="Query and Push VPN Status.")
parser.add_argument('--fs', action='store_true', \
                    help="Filesystem Stats.")
args = parser.parse_args()

# Sanity Check
if not args.netatmo and not args.vpn and not args.fs:
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
# Get Filesystem Stats
# #############################################################################
if args.fs:
    fs_usage = fs.get_fs_usage(fs='/volume1')

# #############################################################################
# Get Hostname
# #############################################################################
hostname = socket.gethostname()

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
    line = "is_vpn_connected,host=%s value=%ii" % \
        ( hostname, is_vpn_connected )
    lines.append(line)

# Filesystem Status
if args.fs:
    line_01 = "fs_free,host=%s value=%ii" % ( hostname, fs_usage['free'] )
    line_02 = "fs_total,host=%s value=%ii" % ( hostname, fs_usage['total'] )
    line_03 = "fs_used,host=%s value=%ii" % ( hostname, fs_usage['used'] )
    lines.append(line_01)
    lines.append(line_02)
    lines.append(line_03)

# Join
data = "\n".join(lines)

# #############################################################################
# Post Data
# #############################################################################
influx.post_data(data)
