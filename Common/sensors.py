"""
Get Environmental Sensor Data.
"""

import External.lnetatmo as lnetatmo


def get_netatmo_readings(station='Ng58', modules=['Living Room', 'Bedroom']):
    """
    Get Netatmo Readings.

    Epochs are Unix Timestamps for each Modue in Seconds.
    Readings are Netatmo readings with the following units.
    - Noise             (dB)
    - Temperature       (C)
    - Humidity          (%)
    - Pressure          (Pa)
    - CO2               (PPM)

    For example, readings for the defaults args would look likes this:
    > readings = {'Living Room': {u'Pressure': 1011.7, u'Noise': 37, \
                                  u'Temperature': 20.7, u'CO2': 594, \
                                  u'Humidity': 40}, \
                  'Bedroom': {u'Temperature': 18.6, u'Humidity': 38}}

    Epochs would look like:
    > epochs = {'Living Room': 1461231951, 'Bedroom': 1461231922}

    @param: station     - Netatmo station to poll           [String]
    @param: modules     - Netatmo modules to poll           [List of Strings]
    @return: readings   - Netatmo Readings                  [Dict of Dicts]
    @return: epochs     - Timestamps of Readings  (Seconds) [Dict]
    """

    # Load Credentials
    with open('userpass_netatmo', 'r') as f:
        line = f.readline()
        line = line.strip().split(',')
        clientId = line[0]
        clientSecret = line[1]
        username = line[2]
        password = line[3]

    # Auth to Netatmo API
    authorization = lnetatmo.ClientAuth(clientId = clientId, \
                                        clientSecret = clientSecret, \
                                        username = username, \
                                        password = password)
    devList = lnetatmo.DeviceList(authorization)

    # Get Data
    epochs = {}
    readings = {}
    for module in modules:
        readings_raw = devList.lastData(station=station)[module]
        readings_sane = {}
        for key, value in zip(readings_raw.keys(), readings_raw.values()):
            if key in [ 'Noise', 'Temperature', 'Humidity', \
                        'Pressure', 'CO2']:
                readings_sane[key] = value
        epochs[module] = readings_raw['When']
        readings[module] = readings_sane

    # Return
    return readings, epochs
