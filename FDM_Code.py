import numpy as np
import os
import math
import matplotlib as plot
from xml.dom import minidom

# a function for the main
# a function for the input card read
def ErrorFunction(i):
    ErrorMassage = ["Error 0 :the material do not have its ID！\n",\
                    "Error 1 :the material do not have its transport cross ssection! \n",\
                    "Error 2 :the material do not have its absorption cross ssection! \n",\
                    "Error 3 :the material do not have its nufission cross ssection! \n",\
                    "Error 4 :the material do not have its kappafission cross ssection! \n",\
                    "Error 5 :the material do not have its scattering cross ssection! \n",\
                    "Error 6 :the geometries do not have its core layer,and it is necsseary!\n",\
                    "Error 7 :the core layer do not have its coreGeo son-node, and it is necsseary!\n",\
                    "Error 8 :the lattice id defined in core that can not be found in lattice layer!\n",\
                    "Error 9 :the lattice layer do not have its latticeGeo son-node, and it is necsseary!\n",\
                    "Error 10 :the pin id defined in lattice that can not be found in pin layer!\n",\
                    "Error 11 :the defined pin do not have the lable of width!\n",\
                    "Error 12 :the defined pin do not have the lable of NumNodes!\n",\
                    "Error 13 :the pin layer do not have its coordinates son-node, and it is necsseary!\n",\
                    "Error 14 :the pin layer do not have its MatIDs son-node, and it is necsseary!\n",\
                    "Error 15 :",\
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
        try:
            boundary_tag = settings_tag.getElementsByTagName("boundary")
            self.boundary_left = boundary_tag.getAttribute("left")
            self.boundary_left = float(self.boundary_left)
            self.boundary_right = boundary_tag.getAttribute("right")
            self.boundary_right = float(self.boundary_right)
        except:
            self.boundary_left = 1.0
            self.boundary_right = 1.0

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

class pin:
    def __init__(self,geometries_tag,id):
        self.id = id
        self.coordinates = []
        self.matids = []
        self.mat_list = []
        pins_tag = geometries_tag.getElementsByTagName("pin")
        for pin_tag in pins_tag:
            id = pin_tag.getAttribute("ID")
            id = int(id)
            if id == self.id:
                break
        if id != self.id:
            ErrorFunction(10)
            os._exit(0)
        try:
            self.width = float(pin_tag.getAttribute("width"))
        except:
            ErrorFunction(11)
            os._exit(0)
        try:
            self.numnodes = float(pin_tag.getAttribute("NumNodes"))
        except:
            ErrorFunction(12)
            os._exit(0)
        try:
            self.partitionform = pin_tag.getAttribute("PartitionForm")
        except:
            self.partitionform = "input"
        
        if self.partitionform == "input":
            try:
                coordinates_tag = pin_tag.getElementsByTagName("coordinates")[0]
                coordinates = coordinates_tag.firstChild.data
                coordinates = coordinates.strip("\n").split()
                [self.coordinates.append(float(i)) for i in coordinates]
            except:
                ErrorFunction(13)
                os._exit(0)
            try:
                matids_tag = pin_tag.getElementsByTagName("MatIDs")[0]
                matids = matids_tag.firstChild.data
                matids = matids.strip("\n").split()
                [self.matids.append(int(i)) for i in matids]
            except:
                ErrorFunction(14)
                os._exit(0)
        
class lattice:
    def __init__(self,geometries_tag,id):
        self.id = id
        self.latticegeo = []
        self.pin_list = [0]
        lattices_tag = geometries_tag.getElementsByTagName("lattice")
        for lattice_tag in lattices_tag:
            id = lattice_tag.getAttribute("ID")
            id = int(id)
            if id == self.id:
                break
        if id != self.id:
            ErrorFunction(8)
            os._exit(0)
        try:
            self.latticetype = lattice_tag.getAttribute("LatticeType")
        except:
            self.latticetype = "Line"
        try:
            latticegeo_tag = lattice_tag.getElementsByTagName("latticeGeo")[0]
            latticegeo = latticegeo_tag.firstChild.data
            latticegeo = latticegeo.strip("\n").split()
            [self.latticegeo.append(int(i)) for i in latticegeo]
            self.latticegeo = np.array(self.latticegeo)
        except:
            ErrorFunction(9)
            os._exit(0)
        for pin_id in np.unique(self.latticegeo):
            self.pin_list.append(pin(geometries_tag,pin_id))

        

class core:
    # This is a class for the core
    # id: it is the core's id and usually it is 1
    # coregeo: it is the array of lattice and usually it is a list about integer
    def __init__(self,geometries_tag):
        cores_tag = geometries_tag.getElementsByTagName("core")
        self.coregeo = []
        self.lattice_list = [0]
        try:
            core_tag = cores_tag[0]
            self.id = int(core_tag.getAttribute("ID")) # get the value of core's ID
        except:
            ErrorFunction(6)
            os._exit(0)
        try:
            coregeo_tag = core_tag.getElementsByTagName("coreGeo")[0]
            coregeo = coregeo_tag.firstChild.data
            coregeo = coregeo.strip("\n").split()
            [self.coregeo.append(int(i)) for i in coregeo] # get the array of lattice 
            self.coregeo = np.array(self.coregeo)
        except:
            Errorfunction(7)
            os._exit(0)

        for lattice_id in np.unique(self.coregeo):
            self.lattice_list.append(lattice(geometries_tag,lattice_id)) 

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
    geometries_tag = input_tag.getElementsByTagName("geometries")[0]
    coredata = core(geometries_tag)
    return setting, material_list, coredata

# a function for creating the martix
def CreateMartix(setting,material_list,coredata):
    # get the Distribution of nodes and the Composition of grid 
    length = 0.0
    nodes = [0.0]
    mat_nodes = []
    for i in coredata.coregeo:
        lattice_geo = coredata.lattice_list[i]
        for j in lattice_geo.latticegeo:
            pin_geo = lattice_geo.pin_list[j]
            length = length + nodes[-1]
            for k in pin_geo.coordinates:
                nodes.append(length + k)
            for k in pin_geo.matids:
                mat_nodes.append(k)
    print(1)
# a function for solving the martix
# a function for the outputing of data
# a function for the checking of other functions
setting, material_list, coredata = InputRead("FDM_Code_input.xml")
CreateMartix(setting,material_list,coredata)