# Morey Simulator

This purpose of this project is to simulate a [Morey Connect MC-3 device](http://www.moreycorp.com/expertise/technologies/wireless-devices/morey-connect/).

## Background

The [Morey Connect MC-3 device](http://www.moreycorp.com/expertise/technologies/wireless-devices/morey-connect/) is an embedded hardware device that connects to a vehicle's OBD2 port. When the vehicle's ignition is in the 'run' position, the MC-3 will receive power, and will be collecting ODB2 message traffic (J1939, J1708, VPW & PWM, KW2000, ISO 9141). The MC-3 also contains a cellular transciever, and can report this message traffic via UDP to a listening server.

In order to simulate this (initially), an actual MC-3 device is used to transmit real data from a real vehicle to a real listener. The real listener is modified to dump the byte stream sent by the MC-3 to a file on disk. This file can then be used to "replay" the real data back to a listener via a Python app at a later date.

As the project gets more sophisticated, it will move away from the "record-and-playback" model to a better "generate data on the fly" model.

## Installation

The project consists of:
    - a Python playback application: ./src/simulateMorey.py
    - sample replay data: ./data/trip1.txt
    - a configuration file: ./config/morey.conf_template

Rename morey.conf_template to morey.conf, and fill in the values for the listener. You can execute via ./scripts/simulateMorey.sh

## Operation

All project logs will be stored in the ./logs directory.

When the task starts, it will begin parsing the replay data file. It will simulate the MC-3 by sending the byte streams represented in the file to the listener in real time, following the real time offsets of the timestamps in the file. e.g.:

```
# Mon May 23 01:53:31 2016 - ignition on
15020001007d006600a1000021d18b220000000[...]900000000106c000000003027ffff3026ffffa0380000

# Mon May 23 01:54:41 2016 - in motion
15020001005f006700574262fb2007101501d1a[...]e000003bf502dff502eff301a0446301b041f401c0051
```
The second byte stream will be transmitted one minute and 10 seconds after the first. 

The original timestamps embedded in the byte stream (see the MC-3 documentation) will be overriden with the current time. This will make the trip appear to be happening in real time.

## Problems

Only the first timestamp in a multi-message stream is getting replaced with the current timestamp.

