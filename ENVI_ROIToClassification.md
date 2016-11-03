
# ENVI ROI to Classification

This task creates a classification image from regions of interest (ROIs).  The input ROI file must be created using the [ENVI_ImageThresholdToROI Task](https://github.com/TDG-Platform/docs/blob/master/ENVI_ImageThresholdtoROI.md).  You may use a pre-existing ROI dataset or  produce the final classification as part of a larger workflow. Examples are included in the Advanced Options.  For the best result, the thresholds may need to be manually adjusted.

### Table of Contents
 * [Quickstart](#quickstart) - Get started!
 * [Runtime](#runtime) - Detailed Description of Inputs
 * [Inputs](#inputs) - Required and optional task inputs.
 * [Outputs](#outputs) - Task outputs and example contents.
 * [Advanced](#advanced) - Script performing multiple tasks in one workflow
 * [Contact Us](#contact-us)

### Quickstart

This task requires that the image has been pre-processed using the [Advanced Image Preprocessor](https://github.com/TDG-Platform/docs/blob/master/AOP_Strip_Processor.md), and that a ROI file exists or has been created.

```python
  	from gbdxtools import Interface
	gbdx = Interface()

	# The data input and output lines must be edited to point to an authorized customer S3 location
	input_raster_data = "s3://gbd-customer-data/<customer account>/input directory/"
	input_roi_data = "s3://gbd-customer-data/<customer account>/input directory/"

	classtask = gbdx.Task("ENVI_ROIToClassification")
	classtask.inputs.input_raster = input_raster_data
	classtask.inputs.input_roi = input_roi_data
	classtask.outputs.output_roi_uri_filename = "<classification output file>"

	workflow = gbdx.Workflow([ classtask ])

	workflow.savedata(classtask.outputs.output_raster_uri, location='S3 gbd-customer-data location<customer account>/output directory')

	workflow.execute()
	print workflow.id
	print workflow.status
```


### Runtime

The following table lists all applicable runtime outputs for the ENVI ROI to Classification. An estimated Runtime for the Advanced Script example can be derived from adding the result for the two pre-processing steps. 

  Sensor Name  |  Total Pixels  |  Total Area (k2)  |  Time(secs)  |  Time/Area k2
--------|:----------:|-----------|----------------|---------------
QB02 | 41,551,668 | 312.07 | 172.56 | 0.55 |
WV02|35,872,942 | 329.87 | 173.40 | 0.53 |
WV03|35,371,971 | 196.27 | 197.48 | 0.88 |
GE01| 57,498,000 | 332.97 | 184.30 | 0.55 |


### Inputs
The following table lists all taskname inputs.
Mandatory (optional) settings are listed as Required = True (Required = False).

  Name       |  Required  |  Valid Values       |  Description  
-------------|:-----------:|:--------------------|---------------
input_raster | True       | s3 URL, .hdr, .tiff  | Specify the input raster to apply ROIs to generate a classification image.
input_roi    | True       | .xml ROI file | Specify a single or an array of ROI to create the classification image from.

### Outputs
The following table lists all taskname outputs.
Mandatory (optional) settings are listed as Required = True (Required = False).

  Name            |  Required  |  Valid Values             | Description  
------------------|:---------: |:------------------------- |---------------
output_raster_uri | True       | s3 URL, .hdr, .tiff, .xml | Specify a string with the fully qualified filename and path of the output raster. If you do not specify this property, the output raster is only temporary. Once the raster has no remaining references, ENVI deletes the temporary file.


**OPTIONAL SETTINGS AND DEFINITIONS:**

Name                 |       Default    | Valid Values |   Description
---------------------|:----------------:|---------------------------------|-----------------
ignore_validate      |          N/A     |     1        |Set this property to a value of 1 to run the task, even if validation of properties fails. This is an advanced option for users who want to first set all task properties before validating whether they meet the required criteria. This property is not set by default, which means that an exception will occur if any property does not meet the required criteria for successful execution of the task.

### Advanced

To link the workflow of 1 input image into AOP_Strip_Processor into the ENVI ROI To CLassification task you must use the following GBDX tools script in python:

```python
	# Advanced Task Script:  AOP=>ROI=>Classification
	# This Task runs using IPython in the gbdxtools Interface
	# Initialize the gbdxtools Interface
	from gbdxtools import Interface
	gbdx = Interface()
	
	# Import the Image from s3. Here we are using a GE01 image from the Benchmark Dataset.
	data = "s3://receiving-dgcs-tdgplatform-com/<file directory>"
	aoptask = gbdx.Task("AOP_Strip_Processor", data=data, enable_acomp=True, bands='MS', enable_pansharpen=False, enable_dra=False)
	# Capture AOP task outputs
	log = aoptask.get_output('log')
	orthoed_output = aoptask.get_output('data')

	# Run Threshold To Classification
	threshold = gbdx.Task("ENVI_ImageThresholdToROI")
	threshold.inputs.input_raster = aoptask.outputs.data.value
	threshold.inputs.roi_name = "[\"Water\", \"Land\"]"
	threshold.inputs.roi_color = "[[0,255,0],[0,0,255]]"
	threshold.inputs.threshold = "[[138,221,0],[222,306,0]]"
	threshold.inputs.output_roi_uri_filename = "roi"

	# Run ROI to Classification
	input_raster_data = aoptask.outputs.data.value
	input_roi_data = threshold.outputs.output_roi_uri.value
	roitoclass.inputs.input_roi_data = threshold.outputs.output_roi_uri.value
	roitoclass = gbdx.Task("ENVI_ROIToClassification")
	roitoclass.inputs.input_raster = input_raster_data
	roitoclass.inputs.input_roi = input_roi_data
	roitoclass.outputs.output_roi_uri_filename = "class1" # or some resonable classification output filename

	# Run Workflow and Send output to S3 Bucket
	workflow = gbdx.Workflow([ aoptask, threshold, roitoclass ])
	workflow.savedata(aoptask.outputs.data, location='S3 gbd-customer-data location/<customer account>/output directory')
	workflow.savedata(threshold.outputs.output_roi_uri, location='S3 gbd-customer-data location/<customer account>/output directory')
	workflow.savedata(roitoclass.outputs.output_raster_uri, location='S3 gbd-customer-data location/<customer account>/output directory')
	
	workflow.execute()
	print workflow.id
	print workflow.status
```	

**Data Structure for Expected Outputs:**

Your classification file will be written to the specified S3 Customer Location in the ENVI file format and tif format(e.g.  s3://gbd-customer-data/unique customer id/named directory/classification.hdr).  

For background on the development and implementation of ROI to Classification refer to the [ENVI Documentation](http://www.harrisgeospatial.com/docs/enviroitoclassificationtask.html).


###Contact Us
Document Owner - [Kathleen Johnson](kajohnso@digitalglobe.com)

