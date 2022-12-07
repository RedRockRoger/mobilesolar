"""
    MobSol.py
    Author:  Dion Hollenbeck
    December 6, 2022
"""

import kivy
from kivy.app import App
from kivy.config import Config
import kivy.core.window
#kivy.require('1.0.6')
import logging

import math
import re
import sys

import pandas as pd  # (version 1.0.0)
import plotly  # (version 4.5.4) #pip install plotly==4.5.4
import plotly.express as px
import plotly.io as pio


### Global Variables
debug = False # False or True
debugdataframe = True # False or True
debugmatch = False # False or True
globalcolor = "KWH"  # ENERGY or RADIATION OR CLOUDS or KWH or TEMPAVG
maxlines = 200000

globalfnamekwh = "kwh.csv"
globalfnameclouds = "WeatherData.csv"



#==========================  FUNCTION FOR PROCESSING INPUT DATA FILES INTO SINGLE OUTPUT FILE  ==========================

def processdata():
    # infname = ""

    linecount = 0
    lastkwh = 0
    kwhtoday = 0

    maxheaderlineskwh = 8
    linecount = 0
    lastkwh = 0
    kwhtoday = 0
    
    debugheaders = False # False or True
    fnameout = "KWH_CLOUDS.csv"
    dateclouds = ""
    cloudstoday = 0
    fclouds = 1.0  # create as a float
    fradiation = 1.0  # create as a float
    fenergy = 1.0  # create as a float
    ftempmin = 1.0  # create as a float
    ftempmax = 1.0  # create as a float
    ftempavg = 1.0  # create as a float
    fnumtemps = 2.0  # create as a float
    fprecip = 1.0  # create as a float
    fprecipcover = 1.0  # create as a float
    fsnow = 1.0  # create as a float
    fsnowdepth = 1.0  # create as a float



    firstline = True
    logging.debug("processdata called")


       #############################################################
    #  Do the actual processing here
    #############################################################
    
    finkwh = open(globalfnamekwh)
    if not finkwh:  
        logging.critical("Could not open kwh input file")
        sys.exit(1)
    if (debug):  logging.debug('kwh input file %s opened\n' % globalfnamekwh)

    finclouds = open(globalfnameclouds)
    if not finclouds:  
        logging.critical("Could not open clouds input file")
        sys.exit(2)
    if (debug):  logging.debug('clouds input file %s opened\n' % globalfnameclouds)

    # read and discard header lines
    while True:
        linekwh = finkwh.readline()
        linecount = linecount +1
        if linecount > maxheaderlineskwh:
            break;
        linekwh = linekwh.rstrip('\n')
        if (debugheaders):  logging.debug(linekwh)
        
    lineclouds = finclouds.readline()
    if (debug):  logging.debug(lineclouds)
    


    # open output file
    try:
        f_out = open(fnameout, 'wt')
    except IOError: # pragma: no cover
        logging.critical("Could not open output file %s for writing" % (fnameout))
        sys.exit()

    if (debug):  logging.debug("Opened output file %s for writing" % (fnameout))
    # write header
    f_out.write("DATE,KWH,TEMPAVG,PRECIP,PRECIPCOVER,SNOW,SNOWDEPTH,CLOUDS,RADIATION,ENERGY\n")

    ##  There is data beyond date and Watt Hours, but we don't want any of it
    ## DD.MM.YYYY hh:mm:ss,[Wh]
    ## 14.06.2018 00:00:00,0

    #                                   datetime                 KWH
    regexkwh = "(^\d\d)\.(\d\d)\.(\d\d\d\d)\s*(\d\d:\d\d:\d\d,)(\d*),"

    # datetime,tempmax,tempmin,cloudcover,solarradiation,solarenergy
    # 2018-06-14,84.4,53.2,21.8,191.7,16.6

    #                  date                tempmax     tempmin    precip     precipcover    snow      snowdepth     cloud     radiation     energy
    regexclouds = "^(\d\d\d\d-\d\d-\d\d),(\d*\.*\d*),(\d*\.*\d*),(\d*\.*\d*),(\d*\.*\d*),(\d*\.*\d*),(\d*\.*\d*),(\d*\.*\d*),(\d*\.*\d*),(\d*\.*\d*)"


    linecount = 0
    while True:
        linekwh = finkwh.readline()
        lineclouds = finclouds.readline()
        linecount = linecount +1
        if linecount > maxlines:
            break;
        else:
            if (debug): logging.debug(" LINECOUNT %d" % linecount)
        if (not linekwh) or (not lineclouds) :
            break

        # process line from KWH file
        linekwh = linekwh.rstrip('\n')
        if (debug):  logging.debug(linekwh)
        matchkwh = re.search(regexkwh, linekwh)
        if matchkwh:
            day = matchkwh.group(1)
            month = matchkwh.group(2)
            year = matchkwh.group(3)
            kwh = matchkwh.group(5)
            kwhtoday = int(kwh) - int(lastkwh)
            lastkwh = int(kwh)
            if (firstline == True):
                if (debug):  logging.debug(" SKIPPING FIRST LINE\n\t\t%s" % linekwh)
                firstline = False
                continue
        else:
            if (debugmatch):  logging.debug(" NO KWH match\n\t\t%s" % linekwh)
            continue

        # process line from CLOUDS file
        lineclouds = lineclouds.rstrip('\n')
        if (debug):  logging.debug(lineclouds)


#                       1-date            2-tempmax   3-tempmin   4-precip   5-precipcover  6-snow   7-snowdepth   8-cloud    9-radiation  10-energy
#    regexclouds = "^(\d\d\d\d-\d\d-\d\d),(\d*\.*\d*),(\d*\.*\d*),(\d*\.*\d*),(\d*\.*\d*),(\d*\.*\d*),(\d*\.*\d*),(\d*\.*\d*),(\d*\.*\d*),(\d*\.*\d*)"

        matchclouds = re.search(regexclouds, lineclouds)
        
        if matchclouds:
            dateclouds = matchclouds.group(1)
            
            ftempmax = float(matchclouds.group(2))
            ftempmin = float(matchclouds.group(3))
            fprecip = float(matchclouds.group(4))
            fprecipcover = float(matchclouds.group(5))
            fsnow = float(matchclouds.group(6))
            fsnowdepth = float(matchclouds.group(7))
            fclouds = float(matchclouds.group(8))
            fradiation = float(matchclouds.group(9))
            fenergy = float(matchclouds.group(10))
            ftempavg = (ftempmax + ftempmin)/fnumtemps

            # cloudstoday = round(fclouds, 0)
            # cloudstoday = math.floor(float(matchclouds.group(2)))
            if (debug):  
                logging.debug("FTEMPMAX  %f" % ftempmax)
                logging.debug("FTEMPMIN  %f" % ftempmin)
                logging.debug("FTEMPAVG  %f" % ftempavg)
                logging.debug("FPRECIP  %f" % fprecip)
                logging.debug("FPRECIPCOVER  %f" % fprecipcover)
                logging.debug("FSNOW  %f" % fsnow)
                logging.debug("FSNOWDEPTH  %f" % fsnowdepth)
                logging.debug("FCLOUDS  %f" % fclouds)
                logging.debug("FRADIATION  %f" % fradiation)
                logging.debug("FENERGY  %f" % fenergy)

        else:
            if (debugmatch):  logging.debug(" NO CLOUDS match")
        if (debug):
            logging.debug("   KWH:: %s-%s-%s,%d" % (year, month, day, kwhtoday))
            logging.debug("CLOUDS:: %s,%f\n" % (dateclouds, fclouds))
        if (kwhtoday > 0):
            f_out.write("%s-%s-%s,%d,%f,%f,%f,%f,%f,%f,%f,%f\n" % (year, month, day, kwhtoday, 
                ftempavg, fprecip, fprecipcover, fsnow, fsnowdepth, fclouds, fradiation, fenergy))
        else:
            logging.info("Skipping ==> KWH %d out of range" % kwhtoday)
        # sg.popup_animated(sg.DEFAULT_BASE64_LOADING_GIF, 'loading....', time_between_frames=100, keep_on_top=True, location=(0,0))
    #sg.popup_animated(None,location=(0,0))
    logging.info("\n====>  Number of frames processed %10d" % (linecount))


    finkwh.close()
    finclouds.close()

    f_out.close()


    return fnameout


#==========================  FUNCTION TO USE PROCESSED COMBINED FILE AS INPUT TO BAR GRAPH  ==========================
def makebar(input_fname):
    logging.info("MAKEBAR called with input file %s" % input_fname)

    df = pd.read_csv(input_fname)
    if (debugdataframe):
        logging.debug("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")  
        logging.debug(df[:5])
        logging.debug("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        #sg.PopupScrolled(df)

    barchart = px.bar(
    #barchart = px.scatter(
        data_frame=df,
        x="DATE",
        y="KWH",
        color=globalcolor,               # differentiate color of marks
        opacity=0.9,                  # set opacity of markers (from 0 to 1)
        orientation="v",              # 'v','h': orientation of the marks
#        barmode='group',           # in 'overlay' mode, bars are top of one another.
        barmode='relative',           # in 'overlay' mode, bars are top of one another.
                                    # in 'group' mode, bars are placed beside each other.
                                    # in 'relative' mode, bars are stacked above (+) or below (-) zero.
        title='Hollenbeck Sunny Boy Production (Huge Spikes Because of NaN Data)', # figure title
        width=1800,                   # figure width in pixels
        height=800,                   # figure height in pixels
        template='gridon',            # 'ggplot2', 'seaborn', 'simple_white', 'plotly',
                                    # 'plotly_white', 'plotly_dark', 'presentation',
                                    # 'xgridoff', 'ygridoff', 'gridon', 'none'
    #----------------------------------------------------------------------------------------------
    # facet_row='caste',          # assign marks to subplots in the vertical direction
    # facet_col='caste',          # assigns marks to subplots in the horizontal direction
    # facet_col_wrap=2,           # maximum number of subplot columns. Do not set facet_row!

    # color_discrete_sequence=["pink","yellow"],               # set specific marker colors. Color-colum data cannot be numeric
    # color_discrete_map={"Male": "gray" ,"Female":"red"},     # map your chosen colors
    # color_continuous_scale=px.colors.diverging.Picnic,       # set marker colors. When color colum is numeric data
    # color_continuous_midpoint=100,                           # set desired midpoint. When colors=diverging
    # range_color=[1,10000],                                   # set your own continuous color scale
    #----------------------------------------------------------------------------------------------
    # text='convicts',            # values appear in figure as text labels
    # hover_name='CLOUDS',   # values appear in bold in the hover tooltip
    #hover_data=['RADIATION'],    # values appear as extra data in the hover tooltip
    hover_data=['TEMPAVG','PRECIP','PRECIPCOVER','SNOW','SNOWDEPTH','CLOUDS','RADIATION','ENERGY'],    # values appear as extra data in the hover tooltip
    
    # custom_data=['others'],     # invisible values that are extra data to be used in Dash callbacks or widgets
    custom_data=['TEMPAVG','PRECIP','PRECIPCOVER','SNOW','SNOWDEPTH','CLOUDS','RADIATION','ENERGY'], 
    labels={'TEMPAVG','PRECIP','PRECIPCOVER','SNOW','SNOWDEPTH','CLOUDS','RADIATION','ENERGY'},

    # log_x=True,                 # x-axis is log-scaled
    # log_y=True,                 # y-axis is log-scaled
    # error_y="err_plus",         # y-axis error bars are symmetrical or for positive direction
    # error_y_minus="err_minus",  # y-axis error bars in the negative direction

    )

    #barchart.update_traces(marker_color='green')
    pio.show(barchart)


    return True





def hello(msg):
    logging.debug('Hello From DEBUG %s' % msg)
    logging.info('Hello From INFO %s' % msg)
    logging.warning('Hello From WARNING %s' % msg)

class SolarGraph(App):

    def build(self):

        #Window.delete()
        hello("Called from SolarGraph:build()")
        combined_data_fname = processdata()
        makebar(combined_data_fname)

        return True


if __name__ == '__main__':

    # does not work to suppress console output
    #console_log_level = 300
    logging.basicConfig(filename='solargraph.log', filemode='w', 
        format='%(levelname)s:%(message)s', level=logging.DEBUG,  force=True)
    # console = logging.StreamHandler(sys.stdout)
    # console.setLevel(console_log_level)
    # root_logger = logging.getLogger("")
    # root_logger.addHandler(console)

    SolarGraph().run()
    