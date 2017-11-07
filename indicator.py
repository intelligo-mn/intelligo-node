# -*- coding: utf-8 -*-
import os
import json
from gi.repository import Gtk, GLib
try:
    from gi.repository import AppIndicator3 as AppIndicator
except:
    from gi.repository import AppIndicator
from urllib2 import urlopen
import requests

class CryptoCoinPrice:
    def __init__(self):

        self.ind = AppIndicator.Indicator.new(
            "cryptocoin-mongolia",
            os.path.dirname(os.path.realpath(__file__)) + "/img/bitcoin.png",
            AppIndicator.IndicatorCategory.SYSTEM_SERVICES
        )
        self.ind.set_status(AppIndicator.IndicatorStatus.ACTIVE)
        self.build_menu()
        self.handler_timeout()
        GLib.timeout_add_seconds(60 * 5, self.handler_timeout)

    def build_menu(self):
        self.menu = Gtk.Menu()

        item = Gtk.MenuItem()
        item.set_label("Refresh")
        item.connect("activate", self.handler_menu_reload)
        item.show()
        self.menu.append(item)

        item = Gtk.MenuItem()
        item.set_label("Exit")
        item.connect("activate", self.handler_menu_exit)
        item.show()
        self.menu.append(item)

        self.menu.show()
        self.ind.set_menu(self.menu)

    def handler_menu_exit(self, evt):
        Gtk.main_quit()

    def handler_menu_reload(self, evt):
        self.handler_timeout()

    def handler_timeout(self):
        try:
            url = 'https://api.coinbase.com/v2/prices/spot?currency=USD'
            response = requests.get(url)
            json = response.json()

            status_message = " Buy: "+str(json['data']['amount'])+" "+str(json['data']['currency'])
            self.ind.set_label(status_message, "")
        except Exception, e:
            print str(e)
            self.ind.set_label("!", "")
        return True

    def main(self):
        Gtk.main()

if __name__ == "__main__":
    ind = CryptoCoinPrice()
    ind.main()
