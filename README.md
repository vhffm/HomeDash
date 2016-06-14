# Simple Home Dashboard, Collector Module

## Overview

This is a collection of Python scripts to poll your environmental data from a [Netatmo](http://netatmo.com) device as well as filesystem and VPN connectivity status from a Linux system, and then upload it to an instance of [InfluxDB](https://influxdb.com/). You can then use something like [Grafana](http://www.grafana.org) to visualise the measurements.

## Usage

- Put your InfluxDB access data in the *userpass_influx* file. See also *userpass_influx_example*.

### Netatmo

- Generate a API token for Netatmo by [Creating an Application](https://dev.netatmo.com/dev/createapp).
- Put your Netatmo access data in the *userpass_netatmo* file. See also the *userpass_netatmo_example* file.
- Modify your station and module names in *Common/sensors.py*.
- Run *python ./ticker.py --netatmo*. If it works, stick it in a Cronjob.

### VPN & Filesystem Status

- To detect whether the VPN connection is up or down, the script polls [http://icanhazip.com/](http://icanhazip.com/) to get your public IP which is checked against a list of addresses. You need to create a list of valid public IP addresses in *vpn_list*. See also *vpn_list_example*.
- If you want to check filesystem status, make sure to edit the relevant mount point in *ticker.py*. By default, it's */volume1*.
- To use the features, run *python ./ticker.py --vpn --fs*.

## Contact

Questions, comments, rants should be sent to [volker@cheleb.net](mailto:volker@cheleb.net).
