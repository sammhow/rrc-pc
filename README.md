# Range Rover Classic CarPC

This is the basic setup of a car pc - I built it for a Range Rover Classic

I used PostmarketOS with PlasmaMobile because it gives the best experience for a touch interface that I have tried.

The system has a small Python script which monitors a GPIO pin to detect when the ignition is switched off and a programmanble relay which cuts power after 10 minutes, saving the battery.

By using Pure Maps and your preferred media player the system also works entirely off line.

***See the wiki for more details, but basically -***

Components 

- Raspberry Pi
	- Preferably a 5 with an NVMe hat for improved boot time and general performance
- 7in Touch screen
- GPS receiver
	- I used a GlobalSat BU-353-S4 USB GPS Receiver 
- USB sound card
    - Or bluetooth if your head unit supports it.

You could also add a DVB receiver and a host of other sensors.

Note that this has pre-built versions of RoverGauge and libcomm14cux
https://github.com/colinbourassa/rovergauge
https://github.com/colinbourassa/libcomm14cux


