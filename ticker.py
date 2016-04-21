"""
Read, Parse, Post Stats to InfluxDB.
"""

import Common.sensors as sensors
import Common.influx as influx


# #############################################################################
# Load Data from Netatmo
# #############################################################################
readings, epochs = sensors.get_netatmo_readings()

# #############################################################################
# Build Data Post
# NB: For InfluxDB >=0.9.3, integer data points require a trailing i.
#     For example, ncpus_allocated,parititon=cpu value=5i
# #############################################################################
lines = []

# Netatmo w/ Sanitized Strings (Remove Caps, Spaces to Underscore)
for module_name, module_values in zip(readings.keys(), readings.values()):
    for value_name, value in zip(module_values.keys(), module_values.values()):
        line = "%s,module=%s value=%.2f %i" % \
            ( value_name.lower(), \
              '_'.join(module_name.lower().split(' ')), \
              value, \
              epochs[module_name] )
        lines.append(line)

# Join
data = "\n".join(lines)

# #############################################################################
# Post Data
# #############################################################################
influx.post_data(data)
