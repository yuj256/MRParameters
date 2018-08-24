"""
Get relevant MR parameters from pdf text copied into a csv file.

MR pulse sequence parameters need to be copied into excel spreadsheets for 
protocol convergence. These parameters reside in lengthy pdf files and are 
difficult to extract quickly. This script searches through the data and pulls 
the relevant data out and places it into a csv file, to be pasted into excel 
easily. 

assumptions: Siemens pulse sequence pdf data pasted into txt files, one 
sequence per file. Txt files are named with sequence number and description. 
All files to be analyzed are located in the same directory.

usage: run from folder containing text files to be analyzed

author: Justin Yu
author affiliation: Mayo Clinic Arizona Diagnostic Physics group
written: August 2018
"""

import os
import re
import fnmatch
import math
import csv
import time

#define regular expressions for each variable
slicethick = re.compile(r'\nSlice thickness (\d+\.?\d?) mm')
distfact = re.compile(r'\nDist\. factor (\d+\.?) %')
fovp = re.compile(r'\nFoV phase (\d+\.?\d?) %')
fovr = re.compile(r'\nFoV read (\d+\.?) mm')
resolutionp = re.compile(r'\nPhase resolution (\d+\.?) %')
resolutionb = re.compile(r'\nBase resolution (\d+\.?)')
averages = re.compile(r'\nAverages (\d)')
tr = re.compile(r'\nTR (\d+\.?\d?) ms')
te = re.compile(r'\nTE (\d+\.?\d?) ms')
flipangle = re.compile(r'\nFlip angle (\d+\.?) deg')
bandwidth = re.compile(r'\nBandwidth (\d+\.?) Hz/Px')
fatsuppr = re.compile(r'\nFat suppr. (\w+\s?)\n')
respcontrol = re.compile(r'\nResp. control (\w+-?\w+)')
norm = re.compile(r'\nNormalize (\w+)')
prenorm = re.compile(r'\nPrescan Normalize (\w+)')
# ti = re.compile(r'\nTI (\d+\.?) ms')
scantime = re.compile(r'\nTA: (\d:?.?\d{2})')
accelpe = re.compile(r'\nAccel. factor PE (\d)')
# accel3d = re.compile(r'\nAccel. factor 3D (\d)')
partialfourier = re.compile(r'\nPhase partial Fourier (\d/\d|Off)')
interpolate = re.compile(r'\nInterpolation (\w+)')

#navigate to directory with txt files
os.chdir(r'H:\Programming\testing')

#create empty list of files, then fill with txt files in current directory
listoffiles = []
for file in os.listdir('.'):
	if fnmatch.fnmatch(file, '*.txt'):
		listoffiles.append(file)


#create empty list of txt file data, then fill with data from listoffiles
listoftextdata = []
for file in listoffiles:
	pulse = open(file, 'r')
	pulsetext = pulse.read()
	listoftextdata.append(pulsetext)
	if file.endswith('.txt'):
		filename = file[:-4]
	print(filename)
	
	for text in listoftextdata:
		#assign values to variable by searching text using defined regular expressions
		# problem with TI Accel3D these are not always there
		# TI is almost never there, ignore for now
		SliceThick = float(slicethick.search(text).group(1))
		print("SliceThick = ")
		print(SliceThick)
		time.sleep(1)
		DistFact = float(distfact.search(text).group(1))
		print("DistFact = ")
		print(DistFact)
		time.sleep(1)
		FOVP = float(fovp.search(text).group(1))
		print("FOVP = ")
		print(FOVP)
		time.sleep(1)
		FOVR = float(fovr.search(text).group(1))
		print("FOVR = ")
		print(FOVR)
		time.sleep(1)
		ResolutionP = float(resolutionp.search(text).group(1))
		print("ResolutionP = ")
		print(ResolutionP)
		time.sleep(1)
		ResolutionB = float(resolutionb.search(text).group(1))
		print("ResolutionB = ")
		print(ResolutionB)
		time.sleep(1)
		Averages = float(averages.search(text).group(1))
		print("Averages = ")
		print(Averages)
		time.sleep(1)
		TR = float(tr.search(text).group(1))
		print("TR = ")
		print(TR)
		time.sleep(1)
		TE = float(te.search(text).group(1))
		print("TE = ")
		print(TE)
		time.sleep(1)
		FlipAngle = float(flipangle.search(text).group(1))
		print("FlipAngle = ")
		print(FlipAngle)
		time.sleep(1)
		Bandwidth = float(bandwidth.search(text).group(1))
		print("Bandwidth = ")
		print(Bandwidth)
		time.sleep(1)
		FatSuppr = fatsuppr.search(text).group(1)
		print("FatSuppr = ")
		print(FatSuppr)
		time.sleep(1)
		RespControl = respcontrol.search(text).group(1)
		print("RespControl = ")
		print(RespControl)
		time.sleep(1)
		Norm = norm.search(text).group(1)
		print("Norm = ")
		print(Norm)
		time.sleep(1)
		PreNorm = prenorm.search(text).group(1)
		print("PreNorm = ")
		print(PreNorm)
		time.sleep(1)
		# TI = ti.search(text)
		ScanTime = scantime.search(text).group(1)
		print("ScanTime = ")
		print(ScanTime)
		time.sleep(1)
		AccelPE = accelpe.search(text).group(1)
		print("AccelPE = ")
		print(AccelPE)
		time.sleep(1)
		# Accel3D = accel3d.search(text)
		PartialFourier = partialfourier.search(text).group(1)
		print("PartialFourier = ")
		print(PartialFourier)
		time.sleep(1)
		Interpolate = interpolate.search(text).group(1)
		print("Interpolate = ")
		print(Interpolate)
		time.sleep(1)

		# derived values calculated here
		DistFactPer = DistFact*0.01
		Gap = int(SliceThick*DistFactPer)
		ResolutionPPer = ResolutionP*0.01
		Np = int(ResolutionB*ResolutionPPer)
		NpValue = str(Np) + " (" + str(ResolutionP) + "%)"

		if Norm == "On":
			IntCorr1 = "SCIC"
		else:
			IntCorr1 = "NA"

		if PreNorm == "On":
			IntCorr2 = "PURE"
		else:
			IntCorr2 = "NA"

		IntensityCorr = IntCorr1 + "-" + IntCorr2

		# TI and Accel3D logical tests here
		# TIValue = TI

		# if TI != "None":
			# TIValue = ti.search(text).group(1)

		# print(TIValue)

		values = [filename, SliceThick, Gap, FOVP, FOVR, NpValue, ResolutionB,
					Averages, TR, TE, FlipAngle, Bandwidth, FatSuppr, RespControl,
					IntensityCorr, ScanTime, AccelPE, PartialFourier, Interpolate]
				
		#dump variables into a CSV file

	with open('output.csv', 'a', newline="") as csvfile:
		valuewriter = csv.writer(csvfile, delimiter=';')
		valuewriter.writerow([values])
	pulse.close()
print("No errors")

time.sleep(1)