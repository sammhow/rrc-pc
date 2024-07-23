# Range Rover Classic PC

This is the basic setup of a car pc for a Range Rover Classic

I used PostmarketOS with PlasmaMobile because it gives the best experience for a touch interface that I have tried.

The system has a small Python script which monitors a GPIO pin to detect when the ignition is switched off. 
Once the ignition is switched off, the counter immediately blanks the screen, then waits 9 minutes - enough time to pay for petrol etc. - before soft powering off the RPi. 

After 10 minutes the programmable relay cuts power, saving the battery.

Components 

- Raspberry Pi
	- Preferably a 5 with an NVMe hat for improved boot time and general performance
- 7in Touch screen
- GPS receiver
	- I used a GlobalSat BU-353-S4 USB GPS Receiver 
- USB sound card
- Programmable relay to auto power off the PC
	- https://timers.shop/Multi-Functional-6V-28V-Time-Delay-Relay-Timer--10-amp-V8_p_79.html
- 2x 12v-5v converters - one for RPi power the other for a powered USB hub
- 12v-3v converter to trigger power-off counter.

Recommended

- Physical switch to be able to reboot RPi if needed

Optional hardware
- TTL serial cable for RoverGauge
- DVB receiver for DAB radio - note that welle.io is not avaiable in the default repos.
- Temperature probe for outside and or inside temps

Software
- Lollypop - off line media
- Pure-Maps - off line and online mapping/satnav
- Gnome-Shortwave - Internet radio

Optional software
- Waydroid - for Amazon Music or whatever else.
	- Instructions here https://wiki.postmarketos.org/wiki/Waydroid
	- You also need to add ```psi=1``` to cmdline.txt 
	- I would suggest downloading F-Droid and from there using Aurora Store
- To view output from the temperature sensor I used the 'Command Output [Plasma 6]' Widget
	- The command is `echo "Outside Temp:" ; echo $(/usr/local/bin/temp-sensor.py)"
	- And run it every 5000ms or so
	- You will also need to add ```w1-gpio``` and ```w1-therm``` to ```/etc/modules```
        - And ```dtoverlay=w1-gpio,gpiopin=27``` to ```usercfg.txt```

Build the RPi4 PMOS image with Plasma Mobile and these optional packages
```
 pure-maps,lollypop,sof-firmware,pipewire,pipewire-pulse,wireplumber,geoclue,gnss-share-geoclue,gnss-share,kid3,pipewire-spa-bluez,gpsd-clients,py3-rpigpio,gnome-shortwave,raspberrypi-userland,py3-libgpiod,wireless-tools,iw,qt5-qttools,konsole
```

Note that this has pre-built versions of RoverGauge and libcomm14cux
https://github.com/colinbourassa/rovergauge
https://github.com/colinbourassa/libcomm14cux

Notes

- There is an issue with permissions on WiFi connections, if it doesn't connect at boot time -
	- Edit /etc/NetworkManager/system-connections/[your wifi].nmconnection and remove the permissions
		- Before ```permissions=user:user:;```
		- After ```permissions=```
- If using a Raspberry Pi 4 I would suggest overclocking it
