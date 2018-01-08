# -*- coding: utf-8 -*-
import os
import json
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, GLib
from gi.repository import AppIndicator3 as AppIndicator
import requests

class CryptoCoinPrice(object):
    def __init__(self):

        self.ind = AppIndicator.Indicator.new(
            "cryptocoin-mongolia",
            os.path.dirname(os.path.realpath(__file__)) + "/img/btc.png",
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
        item.set_label("About")
        item.connect("activate", self.about_window)
        item.show()
        self.menu.append(item)
        
        item = Gtk.MenuItem()
        item.set_label("Currency")
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
        
    def currency_menu(self):
		pass

    def about_window(self, source):
        dialog = Gtk.AboutDialog()
        dialog.set_program_name('Cryptocoin Price')
        dialog.set_version('1.0.0')
        dialog.set_copyright('Copyright 2017 Techstar, Inc.')
        dialog.set_license('MIT License\n'+
            'Copyright (c) 2017 Techstar, Inc.\n\n'+
            'Permission is hereby granted, free of charge, to any person obtaining a \n'+
            'copy of this software and associated documentation files (the "Software"), \n'+
            'to deal in the Software without restriction, including without limitation \n'+
            'the rights to use, copy, modify, merge, publish, distribute, sublicense, \n'+
            'and/or sell copies of the Software, and to permit persons to whom the \n'+
            'Software is furnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.')
        dialog.set_wrap_license(True)
        dialog.set_comments('An Ubuntu desktop indicator displays prices of Bitcoin, Ethereum, Litecoin etc.')
        dialog.set_website('https://github.com/techstar-inc/cryptocoin-price')
        
        dialog.run()
        dialog.destroy()

    def get_price (self, currency_pair):
        url = 'https://api.coinbase.com/v2/prices/'+currency_pair+'/spot'
        response = requests.get(url)
        json = response.json()
        return str(json['data']['base'])+"-"+str(json['data']['amount'])+""+self.set_currency(str(json['data']['currency']))
    
    def set_currency(self, currency):
        if currency == 'EUR':
            return u'\u20AC'
        elif currency == 'USD':
            return u'\u0024'
	elif currency == 'GDP':
		return u'\u00A3'
	
        else:
            return currency

    def handler_timeout(self):
        try:
            self.ind.set_label(self.get_price('BTC-USD')+" | "+self.get_price('ETH-USD')+" | "+self.get_price('LTC-USD'), "")
        except Exception, e:
            print str(e)
            self.ind.set_label("!", "")
        return True

    def main(self):
        Gtk.main()

if __name__ == "__main__":
    ind = CryptoCoinPrice()
ind.main()
