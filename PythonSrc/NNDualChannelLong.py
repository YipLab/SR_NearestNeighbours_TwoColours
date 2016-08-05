#import matplotlib
#matplotlib.use('cairo')

from numpy import genfromtxt
import numpy as np
import sys
from math import atan2, degrees, pi
import os
import glob
import re

FolderName = sys.argv[1]
CfgFile = 'Cfg.tmp' 

os.chdir(FolderName)

f = open(CfgFile, 'r')
FN_lst = f.readline()
f.close()
FN_lst = FN_lst.split(";",1)
FileName1 = FN_lst[0]
FileName2 = FN_lst[1] 

os.remove(CfgFile)

my_data = np.loadtxt(FileName1, delimiter=',', skiprows = 1, usecols = (1,2,7))
my_data2 = np.loadtxt(FileName2, delimiter=',', skiprows = 1, usecols = (1,2,7))

##if (my_data.shape[0] == 3):
##    my_data = np.transpose(my_data)

if (my_data.shape[0] >= my_data2.shape[0]):
    DataBase = my_data
    DataSearch = my_data2
else:
    DataBase = my_data2
    DataSearch = my_data

del my_data
del my_data2

Dmax = 200

if 1:
    DistData = np.zeros([DataBase.shape[0],5])+np.nan 
    print "\n//////////////////////////\nAnalysis in Progress\n"
    print "\n///////////"
    for kat in np.arange(len(DataBase)):
        ##Temp = np.copy(DataBase)
        TempI = DataBase[kat,:]
        ##Temp[kat,:] = np.zeros(my_data.shape[1])+np.nan
        ##Temp = Temp[~np.isnan(Temp[:,1])]
        Dist = DataSearch - TempI
        Dist = (Dist[:,1]**2 + Dist[:,0]**2)**0.5
        MinDistPos = Dist.argmin()
        ##MinDist = Dist.min()
        if (Dist.min() < Dmax):
            DistData[kat,:] = [TempI[0],TempI[1],DataSearch[MinDistPos,0],DataSearch[MinDistPos,1],Dist.min()]
        del Dist
        if np.mod(kat,len(DataBase)*10/100) == 0:
            sys.stdout.write('.')
            sys.stdout.flush()


    dx = DistData[:,2]-DataBase[:,0]
    dy = DistData[:,3]-DataBase[:,1]
    Angs = np.arctan2(-dy,dx)* 180 / np.pi
    
    DistData = DistData[~np.isnan(DistData[:,1])]
    Angs = Angs[~np.isnan(Angs)]
 

T1_s = re.findall('.',FileName1)
T2_s = re.findall('.',FileName2)
Cstr = ''
for kat in range(len(T1_s)):
    if T1_s[kat] == T2_s[kat]:
        Cstr = Cstr + T1_s[kat]
    else:
        Cstr = Cstr + T1_s[kat] + T2_s[kat]
 ##print T1_s[kat]
        

#print Cstr
SaveName = Cstr + '_0_DistData.dat'
NoDupCnt = 0
while os.path.isfile(SaveName):
    NoDupCnt += 1
    SaveName = Cstr + '_' + str(NoDupCnt) + '_DistDataLong.dat'


print '\n FilenName = ' + SaveName
SaveData = np.zeros([DistData.shape[0],6])
SaveData[:,0:5] = DistData
SaveData[:,5] = Angs
f = open(SaveName,'w')
f.write(" %s , %s ,%s , %s , %s, %s  \n" % (" X1 [nm]", "Y1 [nm]" ," X2 [nm]", "Y2 [nm]" , "Dist [nm]", "Ang [rad]"))
for item in SaveData:f.write(" %s , %s, %s , %s , %s , %s \n" % (str(item[0]),str(item[1]),str(item[2]),str(item[3]),str(item[4]),str(item[5])))
f.close()
print "\n"
print "All done!"

