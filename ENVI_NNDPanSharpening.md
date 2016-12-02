# ENVI NND Pansharpening  (Editing In Progress)

This task performs NNDiffuse pan sharpening using a low-resolution raster and a high-resolution panchromatic raster.

NNDiffuse pan sharpening works best when the spectral response function of each multispectral band has minimal overlap with one another, and the combination of all multispectral bands covers the spectral range of the panchromatic raster.
The following are input raster requirements for running the NNDiffuse pan sharpening algorithm:

 - The pixel size of the low-resolution raster must be an integral multiple of the pixel size of the high-resolution raster. If it is
   not, then pre-process (resample) the rasters.
 - When the rasters have projection information, it must be in the same
   projection. If it is not the same, then reproject the rasters.
 - The rasters must be aligned. If the rasters have misalignment, then
   register the rasters.
 - Ensure that the rasters line up, particularly in the upper-left
   corner (see the following diagram). When alignment is as little as
   1/2 pixel off between the two, pan sharpening accuracy will be
   affected. If both input rasters have map information, they will be
   automatically subsetted so that they line up. If the rasters do not
   line up and do not have map information, then use spatial subsetting.



### Table of Contents
 * [Quickstart](#quickstart) - Get started!
 * [Runtime](#runtime) - Detailed Description of Inputs
 * [Inputs](#inputs) - Required and optional task inputs.
 * [Outputs](#outputs) - Task outputs and example contents.
 * [Known Issues](#known-issues)
 * [Contact Us](#contact-us)

### Quickstart

This task requires that WorldView-2, Worldview-3, GeoEYE-1 and Quickbird imagery has been pre-processed using the Advanced Image Processor for proper orthorectification (ADD LINK).  For IKONOS, Landsat-8, Sentinel and similar sensors that have ortho-ready level 2A (OR2A) imagery, the ENVI NND Pansharpening task can be run directly on the data as shownin the QuickStart Script below:

	from gbdxtools import Interface
	gbdx = Interface()

	# Define Task and Data Types
	pansharpTask = gbdx.Task("ENVI_NNDiffusePanSharpening")
	pansharpTask.inputs.input_raster_metadata = '{"sensor type": "IKONOS"}'

	# Input High- and Low-Resolution data
	pansharpTask.inputs.input_low_resolution_raster =  "s3://gbd-customer-data/7d8cfdb6-13ee-4a2a-bf7e-0aff4795d927/kathleen_AComp_IKONOS_Data/po_1344103_0000000/po_1344103_bgrn_0000000.tif"
	pansharpTask.inputs.input_high_resolution_raster ="s3://gbd-customer-data/7d8cfdb6-13ee-4a2a-bf7e-0aff4795d927/kathleen_AComp_IKONOS_Data/po_1344103_0000000/po_1344103_pan_0000000.tif"

	# Run Workflow
	workflow = gbdx.Workflow([ pansharpTask ])
	workflow.savedata(pansharpTask.outputs.output_raster_uri, location='kathleen_ENVI_NND_PanSharpen/IKONOS_Data')
	workflow.execute()
	print workflow.id
	print workflow.status


Examples of different sensor data sets  | Script
----------------- | -------------------------------------------------------
IKONOS   |   task.inputs.input_raster_metadata = '{"sensor type": "IKONOS"}'
Landsat-8   |     task.inputs.input_raster_metadata = '{"sensor type": "Landsat OLI"}'
Sentinel     |     task.inputs.input_raster_metadata = '{"sensor type": "SENTINEL-2"}'


### Inputs
The following table lists all taskname inputs.
Mandatory (optional) settings are listed as Required = True (Required = False).

  Name  |  Required  |  Default  |  Valid Values  |  Description  
--------|:----------:|-----------|----------------|---------------


### Outputs
The following table lists all taskname outputs.
Mandatory (optional) settings are listed as Required = True (Required = False).

  Name  |  Required  |  Default  |  Valid Values  |  Description  
--------|:----------:|-----------|----------------|---------------


### Advanced
Include example(s) with complicated parameter settings and/or example(s) where the task is used as part of a workflow involving other GBDX tasks. (INCLUDE AOP Processer IN SCRIPT)

	# Advanced Task Script:  AOP=>NND Pansharpening 


### Runtime

The following table lists all applicable runtime outputs. (This section will be completed the Algorithm Curation team)
For details on the methods of testing the runtimes of the task visit the following link:(INSERT link to GBDX U page here)

  Sensor Name  |  Total Pixels  |  Total Area (k2)  |  Time(secs)  |  Time/Area k2
--------|:----------:|-----------|----------------|---------------
QB | 41,551,668 | 312.07 |  |  |
WV02|35,872,942|329.87| | |
WV03|35,371,971|196.27| | |
GE01| 57,498,000|332.97|| |
IKONOS |      |       |    |

     
     
### Inputs:

Name                     |       File Type       |   Description
-------------------------|:---------------------:|---------------------------------


#### Technical Notes



**Data Structure for Expected Outputs:**

Your Processed classification file will be written to the specified S3 Customer Location in the ENVI file format and tif format(e.g.  s3://gbd-customer-data/unique customer id/named directory/classification.hdr).  


For background on the development and implementation of Classification Smoothing refer to the [ENVI Documentation](https://www.harrisgeospatial.com/docs/classificationtutorial.html)

Additional References:
Sun, W., B. Chen, and D.W. Messinger. "Nearest Neighbor Diffusion Based Pan Sharpening Algorithm for Spectral Images." Optical Engineering 53, no. 1 (2014).

###Contact Us
Document Owner - Kathleen Johnson - kajohnso@digitalglobe.com
