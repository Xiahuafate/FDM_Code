import numpy as np
import os
import math
import time
import matplotlib.pyplot as plt
from xml.dom import minidom


# a function for the input card read
# this is a function for the error massage information
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
                    "Error 15 :the Matrix Solution Method is not correct!\n",\
                    "Error 16 :the input of file name is not correct!,Must be xml!\n",\
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
            leak_rate_tag = settings_tag.getElementsByTagName("leak_rate")[0]
            self.leak_rate = int(leak_rate_tag.firstChild.data)
        except:
            self.leak_rate = 0
        try:
            boundary_tag = settings_tag.getElementsByTagName("boundary")[0]
            self.boundary_left = boundary_tag.getAttribute("left")
            self.boundary_left = float(self.boundary_left)
            self.boundary_right = boundary_tag.getAttribute("right")
            self.boundary_right = float(self.boundary_right)
        except:
            self.boundary_left = 1.0
            self.boundary_right = 1.0
        try:
            criterion_tag = settings_tag.getElementsByTagName("criterion")[0]
            self.ferrinlimit = criterion_tag.getAttribute("FerrInLimit")
            self.ferrinlimit = float(self.ferrinlimit)
            self.ferroutlimit = criterion_tag.getAttribute("FerrOutLimit")
            self.ferroutlimit = float(self.ferroutlimit)
            self.kerrlimit = criterion_tag.getAttribute("KerrLimit")
            self.kerrlimit = float(self.kerrlimit)
            self.maxniniter = criterion_tag.getAttribute("MaxNinIter")
            self.maxniniter = int(self.maxniniter)
            self.maxnoutiter = criterion_tag.getAttribute("MaxNoutIter")
            self.maxnoutiter = int(self.maxnoutiter)
        except:
            self.ferrinlimit = 1.0E-5
            self.ferroutlimit = 1.0E-4
            self.kerrlimit = 1.0E-5
            self.maxniniter = 10
            self.maxnoutiter = 200
        try:
            matrixsolutionmethod_tag = settings_tag.getElementsByTagName("MatrixSolutionMethod")[0]
            self.matrixsolutionmethod = matrixsolutionmethod_tag.firstChild.data
        except:
            self.matrixsolutionmethod = "matrix inversion"

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
            self.numnodes = int(pin_tag.getAttribute("NumNodes"))
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
        elif self.partitionform == "uniform":
            coordinates = np.linspace(0,self.width,num = int(self.numnodes))
            coordinates = coordinates.tolist()
            coordinates.pop(0)
            [self.coordinates.append(float(i)) for i in coordinates]
            matids_tag = pin_tag.getElementsByTagName("MatIDs")[0]
            matids = matids_tag.firstChild.data
            matids = matids.strip("\n").split()
            matids = int(matids[0])
            for i in range(len(coordinates)):
                self.matids.append(matids)

        
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


def FigSvae(x,y,title,x_label,y_label,):
    plt.plot(x, y, color='r',marker='o',linestyle='dashed')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.savefig(title+".jpg")
    plt.close()

# a function for the outputing of data
def ScreenPrint(fileinput):
    screen_str = ["--------------------------------------------------------------------------------------------------------------------------------\n",\
                  "--------------------------------------------------------------------------------------------------------------------------------\n",\
                  "|                                                                                                                              |\n",\
                  "|                                                                                                                              |\n",\
                  "|                                                                                                                              |\n",\
                  "|                                                                                                                              |\n",\
                  "|                                                                                                                              |\n",\
                  "|                                                                                                                              |\n",\
                  "|                                                                                                                              |\n",\
                  "|                                                                                                                              |\n",\
                  "|                                                                                                                              |\n",\
                  "|                                                                                                                              |\n",\
                  "|                                                                                                                              |\n",\
                  "|                                                                                                                              |\n",\
                  "|                                                                                                                              |\n",\
                  "|                                                                                                                              |\n",\
                  "--------------------------------------------------------------------------------------------------------------------------------\n",\
                  "--------------------------------------------------------------------------------------------------------------------------------\n",\
                  ""]
    if fileinput[-3:] != "xml":
        ErrorFunction(16)
        os._exit(0)
    fileout = fileinput[:-3] + "out"
    f = open(fileout,"w+")
    f.close()
    command = "copy " + fileout + "+" + fileinput
    os.system(command)
    os.system("cls")
    f = open(fileout,"a+")
    f.write("\n")
    for i in range(len(screen_str)):
        print(screen_str[i])
        f.write(screen_str[i])
    now_time = "Now Time Is: " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\n"
    print(now_time)
    f.write(now_time)
    f.close()
    return fileout


def DataPrint(fileout,setting,k_inf,k_error,nodes,flux,absorption_rate,nufission_rate,leak_rate):
    f = open(fileout,"a+")
    #print the k change in the screen
    str1 = "The initial effective proliferation factor is {:.8f}\n".format(k_inf[0])
    print("\n"+str1)
    f.write(str1)
    str1 = "     Iterations_step                       K_inf                                    K_error\n"
    print(str1)
    f.write(str1)
    for i in range(len(k_error)):
        str1 = "            {:}                           {:.8f}                                {:.8f}\n".format((i+1),k_inf[i+1],k_error[i])
        print(str1)
        f.write(str1)
    now_time = "Now Time Is: " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\n"
    print(now_time)
    f.write(now_time)
    # check the options of output
    if setting.flux_density == 1:
        flux = flux.tolist()
        print("Start printing the distribution of neutron flux density over space\n")
        str1 = "\n" + "                 nodes                           FluxDensity                     \n"
        f.write(str1)
        for i in range(len(nodes)):
            str1 = "                 {:.4}                          {:.9f}                     \n".format(nodes[i],flux[i][0])
            f.write(str1)
        FigSvae(nodes,flux,"Neutron flux density distribution","Nodes","Neutron flux density")
        print("End of the print\n")
    if setting.fission_rate == 1:
        nufission_rate = nufission_rate.tolist()
        print("Start printing the distribution of Nufission rate over space\n")
        str1 = "\n" + "                 nodes                           NufissionRate                     \n"
        f.write(str1)
        for i in range(len(nodes)):
            str1 = "                 {:.4}                          {:.9f}                     \n".format(nodes[i],nufission_rate[i][0])
            f.write(str1)
        FigSvae(nodes,nufission_rate,"Nufission rate distribution","Nodes","Nufission Rate")
        print("End of the print\n")
    if setting.absorption_rate == 1:
        absorption_rate = absorption_rate.tolist()
        print("Start printing the distribution of Absorption rate over space\n")
        str1 = "\n" + "                 nodes                           AbsorptionRate                     \n"
        f.write(str1)
        for i in range(len(nodes)):
            str1 = "                 {:.4}                          {:.9f}                     \n".format(nodes[i],absorption_rate[i][0])
            f.write(str1)
        FigSvae(nodes,absorption_rate,"Absorption rate distribution","Nodes","Absorption Rate")
        print("End of the print\n")
    if setting.leak_rate == 1:
        leak_rate = leak_rate.tolist()
        print("Start printing the distribution of Leak rate over space\n")
        str1 = "\n" + "                 nodes                           LeakRate                     \n"
        f.write(str1)
        for i in range(len(nodes)):
            str1 = "                 {:.4}                          {:.9f}                     \n".format(nodes[i],leak_rate[i][0])
            f.write(str1)
        FigSvae(nodes,leak_rate,"Leak rate distribution","Nodes","Leak Rate")
        print("End of the print\n")
    f.close()


def InputRead(inputfile):
    file_xml = minidom.parse(inputfile)
    input_tag = file_xml.getElementsByTagName("input")[0]
    settings_tag = input_tag.getElementsByTagName("settings")[0]
    setting = settings(settings_tag)
    materials_tag = input_tag.getElementsByTagName("materials")[0]
    material_tag = materials_tag.getElementsByTagName("material")
    material_list = [0]
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
    # get the martix of yhe equation 
    matrix_m = np.matrix(np.zeros((int(len(nodes)),int(len(nodes)))))
    matrix_f = np.matrix(np.zeros((int(len(nodes)),1)))
    # deal the boundary
    # the boundary in left side
    beta_left = setting.boundary_left
    D1 = 1.0/(3 * material_list[mat_nodes[0]].transport[0])
    deta1  = nodes[1] - nodes[0]
    matrix_m[0,0] = (1 - beta_left)/4.0 + (1 + beta_left)/2.0 * (D1/deta1)
    matrix_m[0,1] = -(1 + beta_left)/2.0 * ((D1/deta1))
    matrix_f[0,0] = 0
    # the boundary in right side
    beta_right = setting.boundary_right
    DN = 1.0/(3 * material_list[mat_nodes[-1]].transport[0])
    detaN = nodes[-1] - nodes[-2]
    matrix_m[-1,-1] = (1 - beta_right)/4.0 + (1 + beta_right)/2.0 * (DN/detaN)
    matrix_m[-1,-2] = -(1 + beta_right)/2.0 * ((DN/detaN))
    matrix_f[-1,0] = 0
    # Process intermediate grid points
    for i in range(1,len(nodes) - 1):
        Di = 1.0/(3 * material_list[mat_nodes[i-1]].transport[0])
        Di_1 = 1.0/(3 * material_list[mat_nodes[i]].transport[0])
        detai = nodes[i] - nodes[i-1]
        detai_1 = nodes[i+1] - nodes[i]
        absorptioni = material_list[mat_nodes[i-1]].absorption[0]
        absorptioni_1 = material_list[mat_nodes[i]].absorption[0]
        nufissioni = material_list[mat_nodes[i-1]].nufission[0]
        nufissioni_1 = material_list[mat_nodes[i]].nufission[0]
        matrix_m[i,i-1] = -Di/detai
        matrix_m[i,i] = (absorptioni * detai)/2.0 + (absorptioni_1 * detai_1)/2 + Di_1/detai_1 + Di/detai
        matrix_m[i,i+1] = -Di_1/detai_1
        matrix_f[i,0] = nufissioni * detai /2.0 + nufissioni_1* detai_1 / 2.0
    return matrix_m,matrix_f,nodes,mat_nodes


# get the flux and calculate other parameter
def DataCalculate(mode,material_list,setting,mat_nodes,nodes,flux):
    #calculate the absorption
    if mode=="absorption":
        absorption_xs = np.matrix(np.zeros((int(len(mat_nodes)),1)))
        absorption_rate = np.matrix(np.zeros((int(flux.shape[0]),1)))
        for i in range(len(mat_nodes)):
            absorption_xs[i,0] = material_list[mat_nodes[i]].absorption[0]
        absorption_rate[0,0] = flux[0,0] * absorption_xs[0,0]
        for i in range(len(mat_nodes)):
            absorption_rate[i+1,0] = flux[i+1,0] * absorption_xs[i,0]
        returndata = absorption_rate
    elif mode == "nufission":
        nufission_xs = np.matrix(np.zeros((int(len(mat_nodes)),1)))
        nufission_rate = np.matrix(np.zeros((int(flux.shape[0]),1)))
        for i in range(len(mat_nodes)):
            nufission_xs[i,0] = material_list[mat_nodes[i]].nufission[0]
        nufission_rate[0,0] = flux[0,0] * nufission_xs[0,0]
        for i in range(len(mat_nodes)):
            nufission_rate[i+1,0] = flux[i+1,0] * nufission_xs[i,0]
        returndata = nufission_rate
    elif mode == "leak":
        beta_left = setting.boundary_left
        beta_right = setting.boundary_right
        d_xs = np.matrix(np.zeros((int(len(mat_nodes)),1)))
        leak_rate = np.matrix(np.zeros((int(flux.shape[0]),1)))
        for i in range(len(mat_nodes)):
            d_xs[i,0] = material_list[mat_nodes[i]].transport[0]
            d_xs[i,0] = 1/(3*d_xs[i,0])
        leak_rate[0,0] = -d_xs[0,0] *(flux[1,0] - flux[0,0])/(nodes[1]-nodes[0])
        for i in range(len(mat_nodes)):
            leak_rate[i+1,0] =  - d_xs[i,0] * (flux[i+1,0] - flux[i,0])/(nodes[i+1] - nodes[i])
        leak_rate[0,0],leak_rate[-1,0] = (1-beta_left)*leak_rate[0,0],(1-beta_right)*leak_rate[-1,0]
        returndata = leak_rate
    return returndata


# a function for solving the martix
def SolveMatrix(matrix_m,matrix_f,setting,material_list,coredata):
    # get the first value of k and flux ?
    flux = np.ones(matrix_f.shape)
    F1 = np.zeros(matrix_f.shape)
    F2 = np.zeros(matrix_f.shape)
    k_inf = [1.0]
    k_error = []
    ord_num = 1# fanshu
    for i in range(setting.maxnoutiter):# this is the outside iteration

        for j in range(matrix_f.shape[0]):
            F1[j,0] = matrix_f[j,0] * flux[j,0]

        if setting.matrixsolutionmethod == "matrix inversion":
            flux_i = np.linalg.inv(matrix_m)@(F1/k_inf[i])
        elif setting.matrixsolutionmethod == "thomas":
            flux_i = np.zeros(matrix_f.shape)
            c=[]
            u=[]
            l=[]
            y=[]
            u.append(matrix_m[0,0])
            y.append(F1[0,0]/k_inf[i])
            for j in range(1,matrix_f.shape[0]):
                l.append(matrix_m[j,j-1]/u[-1])
                c.append(matrix_m[j-1,j])
                u.append(matrix_m[j,j]-l[-1]*c[-1])
                y.append(F1[j,0]/k_inf[i] - l[-1]*y[-1])
            flux_i[-1,0] = y[-1]/u[-1]
            for j in range(1,matrix_f.shape[0]):
                flux_i[-1-j,0] = (y[-1-j]-c[-j]*flux_i[-j,0])/u[-1-j]
        else:
            ErrorFunction(15)
            os._exit(0)

        for j in range(matrix_f.shape[0]):
            F2[j,0] = matrix_f[j,0] * flux_i[j,0]
             
        k_inf.append((k_inf[i] * np.linalg.norm(F2,ord = ord_num)/np.linalg.norm(F1,ord = ord_num)))

        if np.abs((k_inf[i+1] - k_inf[i])/k_inf[i + 1]) <= setting.kerrlimit:
            k_error.append(np.abs((k_inf[i+1] - k_inf[i])/k_inf[i + 1]))
            break
        else:
            flux = flux_i
            k_error.append(np.abs((k_inf[i+1] - k_inf[i])/k_inf[i + 1]))
    return k_inf,k_error,flux
# a function for the checking of other functions
# a function for main
def main():
    fileout = ScreenPrint("FDM_Code_input.xml")
    setting, material_list, coredata = InputRead("FDM_Code_input.xml")
    matrix_m,matrix_f,nodes,mat_nodes = CreateMartix(setting,material_list,coredata)
    k_inf,k_error,flux = SolveMatrix(matrix_m,matrix_f,setting,material_list,coredata)
    absorption_rate,nufission_rate,leak_rate = DataCalculate("absorption",material_list,setting,mat_nodes,nodes,flux),DataCalculate("nufission",material_list,setting,mat_nodes,nodes,flux),DataCalculate("leak",material_list,setting,mat_nodes,nodes,flux)
    DataPrint(fileout,setting,k_inf,k_error,nodes,flux,absorption_rate,nufission_rate,leak_rate)
    os.system("pause")

main()
