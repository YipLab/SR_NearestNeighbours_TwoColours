import sys
import os
import glob
import time

FolderName = sys.argv[1]

os.chdir(FolderName)
CfgFile = 'Cfg.tmp'

CurrentFiles = glob.glob('*.csv')
print "\n//////////////////////////\nSelect Files to work on (the order doesn't matter):\n\n"
for kat in range(len(CurrentFiles)):
    print  str(kat) + " : " + CurrentFiles[kat]

WorkFolderNum1 = raw_input("Enter First Channel to process and press ENTER (i.e. 4):  ")
WorkFolderNum2 = raw_input("Enter Second Channel to process and press ENTER (i.e. 8):  ")

FileName1 = CurrentFiles[int(WorkFolderNum1)]
FileName2 = CurrentFiles[int(WorkFolderNum2)]

while os.path.exists(CfgFile):
    print 'Configuration file already present \n waiting for clean up ....\n'
    time.sleep(5)


f = open(CfgFile, 'w')
f.write(FileName1 + ';' + FileName2)
f.close()


