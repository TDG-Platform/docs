# ENVI NNDiffuse PanSharpening  (Editing In Progress)

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

For IKONOS, Landsat-8, Sentinel and similar sensors that have ortho-ready level 2A (OR2A) imagery, the ENVI NND Pansharpening task can be run directly on the data as shown in the QuickStart Script below:

```python
	from gbdxtools import Interface
	gbdx = Interface()

	# Define Task and Data Types
	pansharpTask = gbdx.Task("ENVI_NNDiffusePanSharpening")
	pansharpTask.inputs.input_raster_metadata = '{"sensor type": "IKONOS"}'

	# Input High- and Low-Resolution data
	# Edit the following path to reflect a specific path to the imagery input files
	pansharpTask.inputs.input_low_resolution_raster = "s3://gbd-customer-data/account-full path to tiff file"
	pansharpTask.inputs.input_high_resolution_raster = "s3://gbd-customer-data/account-full path to tiff file"

	# Run Workflow
	workflow = gbdx.Workflow([ pansharpTask ])
	
	# Edit the following line to reflect specific folder(s) for the output file
	workflow.savedata(pansharpTask.outputs.output_raster_uri, location='Customer's Output S3 Location')
	workflow.execute()
	print workflow.id
	print workflow.status


```


Examples of different sensor data sets  | Script
----------------- | -------------------------------------------------------
IKONOS   |   task.inputs.input_raster_metadata = '{"sensor type": "IKONOS"}'
Landsat-8   |     task.inputs.input_raster_metadata = '{"sensor type": "Landsat OLI"}'
Sentinel     |     task.inputs.input_raster_metadata = '{"sensor type": "SENTINEL-2"}'


### Inputs
The following table lists all taskname inputs.
Mandatory (optional) settings are listed as Required = True (Required = False).

  Name  |  Required  |  Valid Values  |  Description  
--------|:----------:|----------------|---------------
input_low_resolution_raster |  YES  | raster  |Specify a low-resolution raster.
input_high_resolution_raster  |  YES  | raster | Specify a high-resolution panchromatic raster.
input_raster_metadata  |  YES  | text  | Describes sensor input type

### Outputs
The following table lists all taskname outputs.
Mandatory (optional) settings are listed as Required = True (Required = False).

  Name  |  Required  |  Default  |  Valid Values  |  Description  
--------|:----------:|-----------|----------------|---------------


### Advanced
This task requires that WorldView-2, Worldview-3, GeoEYE-1 and Quickbird imagery has been pre-processed using the Advanced Image Processor for proper orthorectification (ADD LINK).  The example below uses a WorldView-3 Image from Tracy California.


```python

	# Runs AOP to ENVI NND PanSharpen

	from gbdxtools import Interface
	gbdx = Interface()
	
	# Edit the following path(s) to reflect a specific path to the input imagery files; an example is given
	data = "s3://receiving-dgcs-tdgplatform-com/055442993010_01_003" # Example from Tracy, California
	
	# Process the MS and Pan Files Seperately
	aoptask1 = gbdx.Task("AOP_Strip_Processor", data=data, enable_acomp=True, enable_pansharpen=False, enable_dra=False, bands="MS")
	aoptask2 = gbdx.Task("AOP_Strip_Processor", data=data, enable_acomp=True, enable_pansharpen=False, enable_dra=False, bands="PAN")

	# Define Task and Data Types
	pansharpTask = gbdx.Task("ENVI_NNDiffusePanSharpening")

	# Input High- and Low-Resolution data
	pansharpTask.inputs.input_low_resolution_raster = aoptask1.outputs.data.value
	pansharpTask.inputs.input_high_resolution_raster = aoptask2.outputs.data.value

	# Run Workflow
	workflow = gbdx.Workflow([ aoptask1, aoptask2, pansharpTask ])
	
	# Edit the following line to reflect specific folder(s) for the output file
	workflow.savedata(pansharpTask.outputs.output_raster_uri, location='Customer's Output S3 Location')
	workflow.execute()
	print workflow.id
	print workflow.status

```


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
