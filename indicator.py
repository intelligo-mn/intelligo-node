# -*- coding: utf-8 -*-
import os
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, GLib
from gi.repository import AppIndicator3 as AppIndicator
import requests


class Bittrex:
    def __init__(self, coin, base='btc'):
        self.code = base+'-'+coin

    def run(self):
        url = 'https://bittrex.com/api/v1.1/public/getticker?market='+self.code
        response = requests.get(url)
        json = response.json()
        if not json['success']:
            return json['message']
        else:
            result = json['result']
            return 'Bid: '+str(result['Bid'])+' | Ask: '+str(result['Ask'])+' | Last: '+str(result['Last'])


class Binance:
    def __init__(self, coin, base='btc'):
        self.code = coin+base
        self.code.upper()

    def run(self):
        url = 'https://api.binance.com/api/v1/ticker/price?symbol='+self.code
        response = requests.get(url)
        json = response.json()
        return 'Bid: - | Ask: - | Last: '+str(json['price'])


class VIP:
    def __init__(self, coin, base='btc'):
        self.code = coin+'_'+base

    def run(self):
        url = 'https://vip.bitcoin.co.id/api/'+self.code+'/ticker'
        response = requests.get(url)
        json = response.json()
        result = json['ticker']
        return 'Bid: '+str(result['buy'])+' | Ask: '+str(result['sell'])+' | Last: '+str(result['last'])


class CryptoCoinPrice:
    def __init__(self):

        self.menu = Gtk.Menu()
        self.ind = AppIndicator.Indicator.new(
            "cryptocoin-mongolia",
            os.path.dirname(os.path.realpath(__file__)) + "/img/bitcoin.png",
            AppIndicator.IndicatorCategory.SYSTEM_SERVICES
        )
        self.ind.set_status(AppIndicator.IndicatorStatus.ACTIVE)
        self.build_menu()

        self.exchange='coinbase'
        self.market = 'ltc'
        self.handler_timeout()
        GLib.timeout_add_seconds(60 * 3, self.handler_timeout)

    def build_menu(self):

        item = Gtk.MenuItem()
        item.set_label("Refresh")
        item.connect("activate", self.handler_menu_reload)
        item.show()
        self.menu.append(item)

        item = Gtk.MenuItem()
        item.set_label("Set Market")
        item.connect("activate", self.set_market_window)
        item.show()
        self.menu.append(item)

        item = Gtk.MenuItem()
        item.set_label("About")
        item.connect("activate", self.about_window)
        item.show()
        self.menu.append(item)

        item = Gtk.MenuItem()
        item.set_label("Exit")
        item.connect("activate", self.handler_menu_exit)
        item.show()
        self.menu.append(item)

        self.menu.show()
        self.ind.set_menu(self.menu)

    @staticmethod
    def handler_menu_exit(evt):
        Gtk.main_quit()

    def handler_menu_reload(self, evt):
        self.handler_timeout()

    @staticmethod
    def about_window(source):
        dialog = Gtk.AboutDialog()
        dialog.set_program_name('Cryptocoin Price')
        dialog.set_version('1.0.0')
        dialog.set_copyright('Copyright 2018 Techstar, Inc.')
        dialog.set_license('MIT License\n' +
                           'Copyright (c) \t2018 Techstar, Inc.\n' +
                           '\t\t\t2018 Muhammad Rifqi Fatchurrahman\n\n' +
                           'Permission is hereby granted, free of charge, to any person obtaining a \n' +
                           'copy of this software and associated documentation files (the "Software"), \n' +
                           'to deal in the Software without restriction, including without limitation \n' +
                           'the rights to use, copy, modify, merge, publish, distribute, sublicense, \n' +
                           'and/or sell copies of the Software, and to permit persons to whom the \n' +
                           'Software is furnished to do so, subject to the following conditions:\n\nThe above '
                           'copyright notice and this permission notice shall be included in all copies or '
                           'substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", '
                           'WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE '
                           'WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN '
                           'NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER '
                           'LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, '
                           'OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.')
        dialog.set_wrap_license(True)
        dialog.set_comments('An Ubuntu desktop indicator displays prices of Bitcoin, Ethereum, Litecoin etc.')
        dialog.set_website('https://www.techstar.cloud')

        dialog.run()
        dialog.destroy()

    def set_market_window(self, source):
        dialog = Gtk.MessageDialog(None, Gtk.DialogFlags.MODAL, Gtk.MessageType.QUESTION, Gtk.ButtonsType.OK_CANCEL, "Set Market")
        # dialog.set_default_size(200, 200)

        box = dialog.get_content_area()
        user_entry = Gtk.Entry()
        user_entry.set_size_request(100,0)
        box.pack_end(user_entry, False, False, 0)
        dialog.show_all()

        response = dialog.run()
        text = user_entry.get_text()
        dialog.destroy()
        if (response == Gtk.ResponseType.OK) and text != '':
            self.market = text
            self.handler_timeout()

    def get_price (self, currency_pair):
        url = 'https://api.coinbase.com/v2/prices/'+currency_pair+'/spot'
        response = requests.get(url)
        json = response.json()
        return str(json['data']['base']) + "-" + str(json['data']['amount']) + "" + self.set_currency(
            str(json['data']['currency']))

    @staticmethod
    def set_currency(currency):
        if currency == 'EUR':
            return u'\u20AC'
        elif currency == 'USD':
            return u'\u0024'
        else:
            return currency

    def handler_timeout(self):
        try:
            if self.exchange == 'bittrex':
                m = Bittrex(self.market)
                self.ind.set_label(m.run(),"")
            elif self.exchange == 'coinbase':
                self.ind.set_label(self.get_price('BTC-USD') + " | " + self.get_price('ETH-USD') + " | " + self.get_price('LTC-USD'), "")
        except Exception as e:
            print(str(e))
            self.ind.set_label("!","")
        return True

    @staticmethod
    def main():
        Gtk.main()

if __name__ == "__main__":
    ind = CryptoCoinPrice()
    ind.main()
