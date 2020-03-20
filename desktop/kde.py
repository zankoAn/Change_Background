#!/usr/bin/python
' This file is for changing the background in the KDE desktop '

import dbus
import argparse

def address(addr):
    print(addr)
    jscript = """
        var allDesktops = desktops();
        print (allDesktops);
        for (i = 0 ; i < allDesktops.length ; i++) {
            d = allDesktops[i];
            d.wallpaperPlugin = "org.kde.image";
            d.currentConfigGroup = Array("Wallpaper", "jpg", "General");
            d.writeConfig("Image", "file://{0}")
        }""".format(addr)
try:
    bus = dbus.SessionBus()
    plasma = dbus.Interface(
        bus.get_object('org.kde.plasmashell', '/PlasmaShell'), dbus_interface='org.kde.PlasmaShell'
        )
except dbus.DBusException as err:
    pass
