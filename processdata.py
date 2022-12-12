"""
    File:  processdata.py
    Author:  Dion Hollenbeck  Dec 10, 2022

"""
import sys
import re
import logging
# import PySimpleGUI as sg

#==========================  FUNCTION FOR PROCESSING INPUT DATA FILES INTO SINGLE OUTPUT FILE  ==========================

def pdata(fnamekwh, fnameclouds, maxlines, debug, debugmatch, mobile):
    if(not mobile): import PySimpleGUI as sg

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


    if (debug):  logging.info ("processdata called")
    
   

    #############################################################
    #  Do the actual processing here
    #############################################################
    
    finkwh = open(fnamekwh)
    if not finkwh:  
        logging.critical("Could not open kwh input file")
        sys.exit(1)
    if (debug):  logging.info('kwh input file opened\n')

    finclouds = open(fnameclouds)
    if not finclouds:  
        logging.critical("Could not open clouds input file")
        sys.exit(2)
    if (debug):  logging.info('clouds input file opened\n')

    # read and discard header lines
    while True:
        linekwh = finkwh.readline()
        linecount = linecount +1
        if linecount > maxheaderlineskwh:
            break;
        linekwh = linekwh.rstrip('\n')
        if (debugheaders):  logging.info(linekwh)
        
    lineclouds = finclouds.readline()
    if (debug):  logging.info(lineclouds)
    


    # open output file
    try:
        f_out = open(fnameout, 'wt')
    except IOError: # pragma: no cover
        logging.critical("Could not open output file %s for writing" % (fnameout))
        sys.exit()

    if (debug):  logging.info("Opened output file %s for writing" % (fnameout))
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
            if (debug): logging.info(" LINECOUNT %d" % linecount)
        if (not linekwh) or (not lineclouds) :
            break

        # process line from KWH file
        linekwh = linekwh.rstrip('\n')
        if (debug):  logging.info(linekwh)
        matchkwh = re.search(regexkwh, linekwh)
        if matchkwh:
            day = matchkwh.group(1)
            month = matchkwh.group(2)
            year = matchkwh.group(3)
            kwh = matchkwh.group(5)
            kwhtoday = int(kwh) - int(lastkwh)
            lastkwh = int(kwh)
            if (firstline == True):
                if (debug):  logging.info(" SKIPPING FIRST LINE\n\t\t%s" % linekwh)
                firstline = False
                continue
        else:
            if (debugmatch):  logging.debug(" NO KWH match\n\t\t%s" % linekwh)
            continue

        # process line from CLOUDS file
        lineclouds = lineclouds.rstrip('\n')
        if (debug):  logging.info(lineclouds)


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
                logging.info("FTEMPMAX  %f" % ftempmax)
                logging.info("FTEMPMIN  %f" % ftempmin)
                logging.info("FTEMPAVG  %f" % ftempavg)
                logging.info("FPRECIP  %f" % fprecip)
                logging.info("FPRECIPCOVER  %f" % fprecipcover)
                logging.info("FSNOW  %f" % fsnow)
                logging.info("FSNOWDEPTH  %f" % fsnowdepth)
                logging.info("FCLOUDS  %f" % fclouds)
                logging.info("FRADIATION  %f" % fradiation)
                logging.info("FENERGY  %f" % fenergy)

        else:
            if (debugmatch):  logging.info(" NO CLOUDS match")
        if (debug):
            logging.info("   KWH:: %s-%s-%s,%d" % (year, month, day, kwhtoday))
            logging.info("CLOUDS:: %s,%f\n" % (dateclouds, fclouds))
        if (kwhtoday > 0):
            f_out.write("%s-%s-%s,%d,%f,%f,%f,%f,%f,%f,%f,%f\n" % (year, month, day, kwhtoday, 
                ftempavg, fprecip, fprecipcover, fsnow, fsnowdepth, fclouds, fradiation, fenergy))
        else:
            logging.debug("Skipping ==> KWH %d out of range" % kwhtoday)
        if(not mobile): sg.popup_animated(sg.DEFAULT_BASE64_LOADING_GIF, 'loading....', time_between_frames=100, keep_on_top=True, location=(0,0))
    if(not mobile): sg.popup_animated(None,location=(0,0))
    logging.info("\n====>  Number of frames processed %10d" % (linecount))


    finkwh.close()
    finclouds.close()

    f_out.close()



    return (fnameout)

