
import numpy as np
import os
import math
import matplotlib as plot
from xml.dom import minidom

# a function for the main
# a function for the input card read
class settings:
    def __init__(self,settings_tag):

        try:
            flux_density_tag = settings_tag.getElementsByTagName("flux_density")[0]
            self.flux_density = int(flux_density_tag.firstChild.data)
        except:
            self.flux_density = 0
        try:
            fission_rate_tag = settings_tag.getElementsByTagName("fission_rate")[0]
            self.fission_rate = int(fission_rate_tag.firstChild.data)
        except:
            self.fission_rate = 0
        try:
            absorption_rate_tag = settings_tag.getElementsByTagName("absorption_rate")[0]
            self.absorption_rate = int(absorption_rate_tag.firstChild.data)
        except:
            self.absorption_rate = 0
        try:
            leak_rate_tag = settings_tag.getElementsByTagName("leak_rate")
            self.leak_rate = int(leak_rate_tag.firstChild.data)
        except:
            self.leak_rate = 0

def InputRead(inputfile):
    file_xml = minidom.parse(inputfile)
    input_tag = file_xml.getElementsByTagName("input")[0]
    settings_tag = input_tag.getElementsByTagName("settings")[0]
    setting = settings(settings_tag)
    print(1)

# a function for creating the martix
# a function for solving the martix
# a function for the outputing of data
# a function for the checking of other functions
print(1)
InputRead("FDM_Code_input.xml")
