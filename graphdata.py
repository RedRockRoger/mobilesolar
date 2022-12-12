"""
    File:  graphdata.py
    Author:  Dion Hollenbeck   Dec 10, 2022
"""
import logging

import pandas as pd  # (version 1.0.0)
import plotly  # (version 4.5.4) #pip install plotly==4.5.4
import plotly.express as px
import plotly.io as pio



#==========================  FUNCTION TO USE PROCESSED COMBINED FILE AS INPUT TO BAR GRAPH  ==========================
def makebar(input_fname, whichcolor, debug, mobile):
    if (not mobile): import PySimpleGUI as sg

    if (debug):  
        logging.info("makebar called")
        logging.info("MAKEBAR called with input file %s" % input_fname)


    #df = pd.read_csv("Sunny_Boy_parsed.csv")
    df = pd.read_csv(input_fname)
    if (debug):
        logging.info("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")  
        logging.info (df[:5])
        logging.info("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        if (not mobile): sg.PopupScrolled(df[:30], size=(130, 40))

    barchart = px.bar(
    #barchart = px.scatter(
        data_frame=df,
        x="DATE",
        y="KWH",
        color=whichcolor,               # differentiate color of marks
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
    #barchart.show()
    #barchart.write_html('first_figure.html', auto_open=True)


    return True

