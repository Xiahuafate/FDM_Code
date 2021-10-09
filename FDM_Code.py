import numpy as np
import os
import math
import matplotlib as plot
from xml.dom import minidom

# a function for the main
# a function for the input card read
def ErrorFunction(i):
    ErrorMassage = ["the material do not have its ID！\n",\
                    "the material do not have its transport cross ssection! \n",\
                    "the material do not have its absorption cross ssection! \n",\
                    "the material do not have its nufission cross ssection! \n",\
                    "the material do not have its kappafission cross ssection! \n",\
                    "the material do not have its scattering cross ssection! \n",\
                    ]
    print(ErrorMassage[i])
    
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

class material:
    def __init__(self,material_tag):
        self.transport = []
        self.absorption = []
        self.nufission = []
        self.kappafission = []
        self.scattering = []
        try:
            self.id = int(material_tag.getAttribute("ID"))
        except:
            ErrorFunction(0)
            os._exit(0)
        try:
            self.numgroup=int(material_tag.getAttribute("NumGroup"))
        except:
            self.numgroup = 0
        try:
            self.xs_option = material_tag.getAttirbute("Xs_option")
        except:
            self.xs_option = "input"

        if self.xs_option == "input":
            transport_tag = material_tag.getElementsByTagName("transport")[0]
            absorption_tag = material_tag.getElementsByTagName("absorption")[0]
            nufission_tag = material_tag.getElementsByTagName("nufission")[0]
            kappafission_tag = material_tag.getElementsByTagName("kappafission")[0]
            scattering_tag = material_tag.getElementsByTagName("scattering")[0]
            transport = transport_tag.firstChild.data
            transport = transport.strip("\n").split()
            absorption = absorption_tag.firstChild.data
            absorption = absorption.strip("\n").split()
            nufission = nufission_tag.firstChild.data
            nufission = nufission.strip("\n").split()
            kappafission = kappafission_tag.firstChild.data
            kappafission = kappafission.strip("\n").split()
            scattering = scattering_tag.firstChild.data
            scattering = scattering.strip("\n").split()
            try:
                [self.transport.append(float(i)) for i in transport]
            except:
                ErrorFunction(1)
                os._exit(0)
            try:
                [self.absorption.append(float(i)) for i in absorption]
            except:
                ErrorFunction(2)
                os._exit(0)
            try:
                [self.nufission.append(float(i)) for i in nufission]
            except:
                ErrorFunction(3)
                os._exit(0)
            try:
                [self.kappafission.append(float(i)) for i in kappafission]
            except:
                ErrorFunction(4)
                os._exit(0)
            try:
                [self.scattering.append(float(i)) for i in scattering]
            except:
                ErrorFunction(5)
                os._exit(0)

def InputRead(inputfile):
    file_xml = minidom.parse(inputfile)
    input_tag = file_xml.getElementsByTagName("input")[0]
    settings_tag = input_tag.getElementsByTagName("settings")[0]
    setting = settings(settings_tag)
    materials_tag = input_tag.getElementsByTagName("materials")[0]
    material_tag = materials_tag.getElementsByTagName("material")
    material_list = []
    for i in range(len(material_tag)):
        material_list.append(material(material_tag[i]))
    print(1)

# a function for creating the martix
# a function for solving the martix
# a function for the outputing of data
# a function for the checking of other functions
print(1)
InputRead("FDM_Code_input.xml")
