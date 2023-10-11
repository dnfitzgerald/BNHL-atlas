from ij import IJ, ImageStack, CompositeImage, ImagePlus
from ij.io import DirectoryChooser, OpenDialog
from os import walk
import re
import os
from ij.gui import GenericDialog,  WaitForUserDialog
from java.awt import Color


imp = IJ.getImage()
overlay=imp.getOverlay()
stack = imp.getImageStack()
imp_dimensions=imp.getDimensions()

od = OpenDialog("Choose channel names file", None)  
datasetfile = od.getFileName() 
srcDir = od.getDirectory()
datasetpath = os.path.join(srcDir, od.getFileName())
datasetsource = open(datasetpath, "r+")
datasetlines=datasetsource.read().split('\n')
datasetsource.close()
print(len(datasetlines))





forever="yes"

while  forever=="yes" :


	filledwithTrue=[False for elem in datasetlines]
	
	gd = GenericDialog("channels")
	gd.addCheckboxGroup(len(datasetlines)//3+4, 4, datasetlines, filledwithTrue)
	gd.showDialog()
	checkedIDs=gd.getCheckboxes()
	IDs=[elem.getLabel() for elem in checkedIDs if elem.getState() is True]
	checkboxelements=[elem.getLabel() for elem in checkedIDs]
	indexes=[checkboxelements.index(elem) for elem in IDs]
	
	print(IDs)
	
	
	#gd = GenericDialog("How many markers do you wish to overlay")
	#gd.addNumericField("number of channels in result file", 3,0)
	#gd.addNumericField("number of channels in original file", 3,0)
	#gd.showDialog()
	Nchannels_in_result=len(IDs)
	Nchannels_in_ori=imp_dimensions[2]
	print(Nchannels_in_result)
	print(Nchannels_in_ori)
	
	
	frames=[]
	channels=[]



	combo = ImageStack(imp.width, imp.height)




	
	for i in range(0,Nchannels_in_result):

		frames.append(int(indexes[i]//imp_dimensions[2]+1))
		channels.append(((indexes[i]+1)-(frames[i]-1)*imp_dimensions[2])%(imp_dimensions[2]+1))
		print(str(i+1)+"	"+str(((indexes[i]+1)-(frames[i]-1)*imp_dimensions[2]))+"	"+str(frames[i])+"	"+str(channels[i]))
	
	for k in range(1, Nchannels_in_result+1):  
		extract = stack.getProcessor((frames[k-1]-1)*Nchannels_in_ori+channels[k-1])
		combo.addSlice(extract)

	for i in range(1,len(IDs)+1):
		combo.setSliceLabel(IDs[i-1],i)
	
	#				combo.addSlice(cpwhite)
	
	imp2 = ImagePlus("selected  markers combined", combo)  
	imp2.setCalibration(imp.getCalibration().copy())	   
	imp2.setDimensions(Nchannels_in_result, 1, 1)
	imp2.setOverlay(overlay)
	
	
	comp = CompositeImage(imp2, CompositeImage.COMPOSITE)
	
	
	comp.show()

	wait=WaitForUserDialog('channel combinator','press OK to continue')
	wait.show()



	  
                                                                                                                                                                                                                                                                                                                                                


