import os
from os import listdir
from os.path import isfile, join,isdir
import shutil

path = join(os.path.abspath(os.getcwd()),"scl")
pathdest = join(os.path.abspath(os.getcwd()),"sclOrdered")
onlyfolders = [f for f in listdir(path) if (isdir(join(path, f)))]

for year in listdir(path):
    if (isdir(join(path, year))):
        for month in listdir(join(path,year)):
            for day in listdir(join(path,year,month)):
                file = join(path,year,month,day,"0","R20m","SCL.jp2")
                month1 = month
                day1 = day
                if(len(month1)<2):
                    month1 = "0"+month1
                
                if(len(day1)<2):
                    day1 = "0"+day1

                shutil.copy(file, join(pathdest,(year+"-"+month1+"-"+day1+".jp2")))
        
path = os.path.abspath(os.getcwd())
print(path)
print(onlyfolders)