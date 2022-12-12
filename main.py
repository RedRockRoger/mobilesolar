"""
    main.py (should be msolargraph.py)
    Author:  Dion Hollenbeck
    December 6, 2022
"""

import kivy
from kivy.app import App
from kivy.config import Config
import kivy.core.window
#kivy.require('1.0.6')
from kivy.uix.button import Label

import logging

import math
import re
import sys

# my modules in current directory
import processdata as data
import graphdata as gd


### Global Variables
debug = False # False or True
debugdataframe = True # False or True
debugmatch = False # False or True
globalcolor = "KWH"  # ENERGY or RADIATION OR CLOUDS or KWH or TEMPAVG
maxlines = 200000

globalmobile = True  # True turns on kivy and off PySimpleGUI

globalfnamekwh = "kwh.csv"
globalfnameclouds = "WeatherData.csv"




def hello(msg):
    logging.debug('Hello From DEBUG %s' % msg)
    logging.info('Hello From INFO %s' % msg)
    logging.warning('Hello From WARNING %s' % msg)

class SolarGraph(App):

    def build(self):

        #Window.delete()
        hello("Called from SolarGraph:build()")

        combined_fname = data.pdata(globalfnamekwh, globalfnameclouds, maxlines, debug, debugmatch, globalmobile)
        if (debug):  logging.info("MAIN:  Intermediate Output file is %s" % combined_fname)
        if (combined_fname == ""):
            logging.critical("MAIN: Intermediate Output file NOT DEFINED")
            sys.exit(1)
    
        status = gd.makebar(combined_fname, globalcolor, debug, globalmobile)
        if not status:
            logging.critical("MAIN:  makebar failed, exiting")
            sys.exit(2)

        #self.root_window.hide()
        #return
        return Label(text='Hello World!')

        


if __name__ == '__main__':

    # does not work to suppress console output
    #console_log_level = 300
    logging.basicConfig(filename='solargraph.log', filemode='w', 
        format='%(levelname)s:%(message)s', level=logging.DEBUG,  force=True)
    logging.info('Logging started %s')

    Config.set('graphics', 'width', '100')
    Config.set('graphics', 'height', '100')


    SolarGraph().run()
    
