from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from currency import *
import os.path
from trip import *
import datetime
import time
from kivy.uix.textinput import TextInput

__author__ = 'jc299940'



class CurrencyConverterApp(App):
    def __init__(self):
        super(CurrencyConverterApp, self).__init__()
        self.trip_conversions = Details()

    # Builds the gui and loads gui.kv file
    def build(self):
        Window.size = (350, 700)
        self.title = 'Bills Budget Adventures GUI'
        self.root = Builder.load_file('gui.kv')
        self.set_details()
        self.conversion_rates = {}
        self.button_pressed = self.button_pressed
        self.root.ids.foreign_amount.disabled = True
        self.root.ids.home_amount.disabled = True
        return self.root


    # checks config.txt file for home country
    def set_details(self):

        valid_details = get_all_details()
        input_file = open('config.txt', encoding='utf-8')
        line = input_file.readline().strip()
        self.home_country = line
        self.root.ids.home_country.text = line
        lines = input_file.readlines()
        trip_countries = []

        self.root.ids.status.text = "Trip details accepted"

        #  countries
        for line in lines:
            parts = line.strip('\n').split(',')
            self.country_name = parts[0]
            self.start_date = parts[1]
            self.end_date = parts[2]
            # error checking within config.txt
            if not os.path.exists('config.txt'):
                self.root.ids.status = "Cannot find config file"
            elif self.home_country not in valid_details.keys():
                self.root.ids.status.text = "Trip invalid:\n" + self.home_country
            elif self.country_name not in valid_details.keys():
                self.root.ids.status.text = "Trip invalid:\n" + self.country_name
            elif self.start_date > self.end_date:
                self.root.ids.status.text = "Trip invalid:\n"

            trip_countries.append(parts[0])
            try:
                self.trip_conversions.add(parts[0], parts[1], parts[2])
            except Error:
                self.root.ids.status.text = "Trip details invalid\n" + self.start_date + "\n" + self.end_date
                self.root.ids.convert.disabled = True
                self.root.ids.select_country.disabled = True

        if "Trip invalid:\n" in self.root.ids.status.text:
            self.root.ids.convert.disabled = True
            self.root.ids.select_country.disabled = True

        # create no-value dictionary.
        self.trip_locations_dict = dict.fromkeys(trip_countries)
        self.root.ids.select_country.values = self.trip_locations_dict

        # sets current location
        self.date = datetime.date.today().strftime("%Y/%m/%d")
        self.current_country = self.trip_conversions.current_country(self.date)
        self.root.ids.current_location.text = 'Current trip location is:\n' + self.current_country

        # sets time
        date_today = datetime.date.today().strftime("%Y/%m/%d")
        self.root.ids.date_today.text = 'Today is:\n' + date_today

    def change_state(self, country_names):
        self.root.ids.foreign_amount.text = ''
        foreign_location_code = get_details(country_names)
        print ("changed to", country_names)

    def convert_home_to_foreign(self):
        # Converts currency's
        try:

            home_amount = float(self.root.ids.home_amount.text)
            foreign_country = self.root.ids.select_country.text
            rate = self.trip_locations_dict[foreign_country]
            convert = home_amount * rate
            self.root.ids.foreign_amount.text = '{:,.2f}'.format(convert)

            home_country_details = get_details(self.home_country)
            foreign_country_details = get_details(self.root.ids.select_country.text)

            try:
                self.root.ids.status.text = "From {} ({}) to {} ({})".format(home_country_details[1],
                                                                             home_country_details[2],
                                                                             foreign_country_details[1],
                                                                             foreign_country_details[2])
            except:

                self.root.ids.status.text = "From {} to {} ".format(home_country_details[1], foreign_country_details[1])
        except ValueError:
            self.root.ids.status.text = "Invalid amount"


    def convert_foreign_to_home(self):

        try:
            home_amount = float(self.root.ids.foreign_amount.text)
            foreign_country = self.root.ids.select_country.text
            rate = self.trip_locations_dict[foreign_country]
            convert = home_amount / rate
            self.root.ids.home_amount.text = '{:,.2f}'.format(convert)

            home_country_details = get_details(self.root.ids.select_country.text)
            foreign_country_details = get_details(self.home_country)

            try:
                self.root.ids.status.text = "From {} ({}) to {} ({})".format(home_country_details[1],
                                                                             home_country_details[2],
                                                                             foreign_country_details[1],
                                                                             foreign_country_details[2])
            except:

                self.root.ids.status.text = "From {} to {} ".format(home_country_details[1], foreign_country_details[1])
        except ValueError:
            self.root.ids.status.text = "Invalid amount"

    def button_pressed(self):

            self.root.ids.foreign_amount.disabled = False
            self.root.ids.home_amount.disabled = False

            if not self.root.ids.select_country.text:
                self.root.ids.select_country.text = self.current_country

            home_location_code = get_details(self.home_country)[1]
            amount = 1

            for country in self.trip_locations_dict:
                details = get_details(country)[1]
                converted_value = convert(amount, home_location_code, details)
                self.trip_locations_dict[country] = (converted_value)

            update_time = (time.strftime("%H:%M:%S"))
            self.root.ids.status.text = str('Last updated at ') + update_time

CurrencyConverterApp().run()
