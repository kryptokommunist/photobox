#!/bin/sh

echo 0 > /sys/devices/platform/bcm2708_usb/buspower

sleep 1

echo 1 > /sys/devices/platform/bcm2708_usb/buspower

sleep 2
