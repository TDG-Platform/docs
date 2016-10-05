8-Band Vegetation Mask (protogenV2RAV)

RAV is an un-supervised protocol for computing vegetation masks from 8 band (optical + VNIR) image data-sets. The vegetation mask is a binary image in which intensity 255 indicates the presence of vegetation and intensity 0 the absence of vegetation. Vegetation is defined as any type of flora with healthy chlorophyll content.

RAV can be run with Python using gbdxtools or through the GBDX Web Application.

Table of Contents

Quickstart - Get started!
Inputs - Required and optional task inputs.
Outputs - Task outputs and example contents.
Advanced - Additional information for advanced users.
Runtime - Results of task benchmark tests.
Known Issues - Current or past issues known to exist.
Contact Us - Contact tech or document owner.
Quickstart

This script gives the example of RAV with a single tif file as input.

# Quickstart Example producing a single band vegetation mask from a tif file.
# First Initialize the Environment

from gbdxtools import Interface
gbdx = Interface()

raster = 's3://gbd-customer-data/PathToImage/image.tif'
prototask = gbdx.Task("protogenV2RAV", raster=raster)

workflow = gbdx.Workflow([ prototask ])  
workflow.savedata(prototask.outputs.data, location="RAV")
workflow.execute()

print workflow.id
print workflow.status
Inputs

This task will process only WorldView 2 or WorldView 3 multi-spectral imagery (8-band optical and VNIR data sets) that has been atmospherically compensated by the AOP processor. Supported formats are .TIF, .TIL, .VRT, .HDR.

The following table lists the RAV Protogen task inputs. All inputs are required

Name	Default	Valid Values	Description
raster	N/A	S3 URL .TIF only	S3 location of input .tif file processed through AOP_Strip_Processor.
OPTIONAL SETTINGS: Required = False

NA - No additional optional settings for this task exist
Outputs

The following table lists the RAV Protogen task outputs.

Name	Required	Description
data	Y	This will explain the output file location and provide the output in .TIF format.
log	N	S3 location where logs are stored.
Your Processed Imagery will be written as Binary .TIF image type UINT8x1 and placed in the specified S3 Customer Location (e.g. s3://gbd-customer-data/unique customer id/named directory/).

Advanced

To link the workflow of 1 input image into AOP_Strip_Processor into a protogen task you must use the follow GBDX tools script in python

#First initalize the environment
#AOP strip processor has input values known to complete the Protogen tasks

from gbdxtools import Interface
gbdx = Interface()

data = "s3://receiving-dgcs-tdgplatform-com/055026839010_01_003"

aoptask2 = gbdx.Task('AOP_Strip_Processor', data=data, bands='MS', enable_acomp=True, enable_pansharpen=False, enable_dra=False)     # creates acomp'd multispectral image

gluetask = gbdx.Task('gdal-cli')                                 
# move aoptask output to root where prototask can find it
gluetask.inputs.data = aoptask2.outputs.data.value
gluetask.inputs.execution_strategy = 'runonce'
gluetask.inputs.command = """mv $indir/*/*.tif $outdir/"""
prototask = gbdx.Task('protogenV2RAV')
prototask.inputs.raster = gluetask.outputs.data.value


workflow = gbdx.Workflow([aoptask2, gluetask, prototask])
workflow.savedata(prototask.outputs.data, 'RAV')

workflow.execute()

workflow.status
Runtime

The following table lists all applicable runtime outputs. (This section will be completed the Algorithm Curation team) For details on the methods of testing the runtimes of the task visit the following link:(INSERT link to GBDX U page here)

Sensor Name	Total Pixels	Total Area (k2)	Time(secs)	Time/Area k2
WV02	35,872,942	329.87	188.58	0.57
WV03	35,371,971	196.27	217.35	1.18
Known Issues

1) To run the task in a single workflow with AOP the tif file must first be removed from the AOP folder with the additional python commands listed in Advanced

2) Thin cloud (cloud edges) might be misinterpreted as vegetation.

3) Testing additional input formats still in progress. .VRT is currently not functioning (6/30/2016)**

For background on the development and implementation of Protogen Documentation under development

Contact Us

Tech Owner - Georgios Ouzounis - gouzouni@digitalglobe.com Document Owner - Carl Reeder - creeder@digitalglobe.com
