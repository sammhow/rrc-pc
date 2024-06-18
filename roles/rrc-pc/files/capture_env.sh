#!/bin/ash

export > /tmp/user_env_full
egrep 'XAUTHORITY|DISPLAY|DBUS_SESSION_BUS_ADDRESS' /tmp/user_env_full > /tmp/user_environment

