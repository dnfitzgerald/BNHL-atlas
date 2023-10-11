#this script locates and shows with crosses cells of a selected cluster
# niche_clustering.csv with is an export from Vortex and has cluster in the first column  is the input dataset file for this script

from ij import IJ
from ij.io import DirectoryChooser, OpenDialog
from os import walk
import re
import os
from ij.gui import GenericDialog, Overlay, Roi, PolygonRoi, TextRoi, WaitForUserDialog
from java.awt import Color
from ij.measure import ResultsTable
from ij.io import FileSaver 

overlay=Overlay()

imp = IJ.getImage()

if (imp.getOverlay()):
	print ("found overlay")
	overlay=imp.getOverlay()

forever="yes"

while  forever=="yes" :

	results=ResultsTable()

	od = OpenDialog("Choose a dataset file", None)  
	datasetfile = od.getFileName() 
	srcDir = od.getDirectory()
	datasetpath = os.path.join(srcDir, od.getFileName())
	datasetsource = open(datasetpath, "r+")
	datasetlines=re.split('\n|\r',datasetsource.read().replace('"', ''))
	print(len(datasetlines))

	datasetmatrix=[re.split(",|\t",datasetlines[i]) for i in range(len(datasetlines)) if len(re.split(",|\t",datasetlines[i]))>2]

	print("datasetmatrix size is "+str(len(datasetmatrix)))

	
	datacolnames=datasetmatrix[0]
	datasetmatrix=datasetmatrix[1:]

	gd = GenericDialog("table subsetting")
	gd.addStringField("subset the table", "no")
	gd.addChoice("Subsetting Column",datacolnames,datacolnames[0])
	gd.showDialog()
	subset_or_not=gd.getNextString()
	subsetting_column=gd.getNextChoiceIndex()

	if subset_or_not=="yes":
		results=ResultsTable()
		elements=[elem[subsetting_column] for elem in datasetmatrix]
		unique_elements=list(set(elements))
		filledwithTrue=[False for elem in unique_elements]
		gd = GenericDialog("select one element")
		gd.addCheckboxGroup(len(unique_elements), 1, unique_elements, filledwithTrue)
		gd.showDialog()
		checkedIDs=gd.getCheckboxes()
		IDs=[elem.getLabel() for elem in checkedIDs if elem.getState() is True]
		print(IDs)
		print(unique_elements)
		checkboxelements=[elem.getLabel() for elem in checkedIDs]
		indexes=[checkboxelements.index(elem) for elem in IDs]
		print(indexes)
		print(indexes[0])

		
		print(len(IDs))
		print(unique_elements[indexes[0]])
		datasetmatrix=[elem for elem in datasetmatrix if elem[subsetting_column]==unique_elements[indexes[0]]]
		print("subsetted datasetmatrix size is "+str(len(datasetmatrix)))

	
	gd = GenericDialog("scaling factor and shift params")
	gd.addNumericField("scaling factor", 0.5,3)
	gd.addNumericField("xshift", 0,3)
	gd.addNumericField("yshift", 0,3)
	
	gd.addChoice("X coord column",datacolnames,datacolnames[0])
	gd.addChoice("Y coord column",datacolnames,datacolnames[0])
	
	gd.showDialog()
	
	scalingfactor=gd.getNextNumber()
	xshift=gd.getNextNumber()
	yshift=gd.getNextNumber()
	
	X_coord_column=gd.getNextChoiceIndex()
	Y_coord_column=gd.getNextChoiceIndex()
		
	columnID = 0
	clusterID="1234"
	color_input="0,255,0"
	removeoverlay = "no"
	
	yesno='Yes'
	while yesno == 'Yes':
		
		gd = GenericDialog("name the celltype,region abd color ")
		gd.addChoice("Column with Value",datacolnames,datacolnames[columnID])
		gd.addStringField("Table field Value (e.g. name of CLusterID)", clusterID)
		gd.addStringField("color1", color_input)
		gd.addStringField("removeoverlay", removeoverlay)
		gd.showDialog()
		columnID = gd.getNextChoiceIndex()
		clusterID = gd.getNextString()	
		color_input=gd.getNextString()
		removeoverlay = gd.getNextString()

		if color_input == 'none':
			break
		if removeoverlay == 'none':
			break
		if clusterID == 'none':
			break
			
		subset=[elem for elem in datasetmatrix if elem[columnID] == clusterID]
		print("subset size is "+str(len(subset)))		
		print("color is "+color_input)	
		color=color_input.split(',')
	
		if removeoverlay == 'yes':
				overlay=Overlay()
		
		x=[xshift+float(elem[X_coord_column])*scalingfactor for elem in subset]
		y=[yshift+float(elem[Y_coord_column])*scalingfactor for elem in subset]
		
		
		for g in range(0,len(x)):
		
			col = Color(int(color[0]),int(color[1]),int(color[2]))
			roi = Roi(x[g]-5, y[g], 11, 1)
#			roi.setFillColor(col)
			roi.setStrokeColor(col)
#			roi.setStrokeWidth(1)
			overlay.add(roi)
			roi = Roi(x[g], y[g]-5, 1, 11)
#			roi.setFillColor(col)
			roi.setStrokeColor(col)
#			roi.setStrokeWidth(1)
			overlay.add(roi)
			
		imp.setOverlay(overlay)
		imp.show()
	
		wait=WaitForUserDialog('value driven cellfinder','press OK to continue')
		wait.show()
	
