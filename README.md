# Simple Home Dashboard, Collector Module

## Overview

This is a collection of Python scripts to poll your environmental data from a [Netatmo](http://netatmo.com) device and then upload it to an instance of [InfluxDB](https://influxdb.com/). You can then use something like [Grafana](http://www.grafana.org) to visualise the measurements.

## Usage

- Generate a API token for Netatmo by [Creating an Application](https://dev.netatmo.com/dev/createapp).
- Put your Netatmo access data in the *userpass_netatmo* file. See also the *userpass_netatmo_example* file.
- Put your InfluxDB access data in the *userpass_influx* file. See also *userpass_influx_example*.
- Modify your station and module names in *Common/sensors.py*.
- Run *python ./ticker.py*. If it works, stick it in a Cronjob.

## Contact

Questions, comments, rants should be sent to [volker@cheleb.net](mailto:volker@cheleb.net).
