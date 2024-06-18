# rrc-pc

This is the basic setup of a car pc for a Range Rover Classic

Components 

Raspberry Pi
- Preferably a 5 with an NVMe hat for improved boot time
- 7in Touch screen
- GPS receiver
- USB sound card
- Programmable relay to auto power off the PC

Optional hardware
- TTL serial cable for RoverGauge
- DVB receiver for DAB radio

Software
- Lollypop - off line media
- Pure-Maps - off line and online mapping/satnav
- Gnome-Shortwave - Internet radio
- Welle-io - DAB radio

Optional software
- Waydroid - for Amazon Music or whatever else.

Build the RPi4 PMOS image with Plasma Mobile and these optional packages
```
 pure-maps,lollypop,sof-firmware,pipewire,pipewire-pulse,wireplumber,geoclue,gnss-share-geoclue,gnss-share,kid3,pipewire-spa-bluez,gpsd-clients,py3-rpigpio,gnome-shortwave,raspberrypi-userland,py3-libgpiod,wireless-tools,iw,welle-io,qt5-qttools,konsole
```
