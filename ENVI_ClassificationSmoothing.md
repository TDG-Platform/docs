# ENVI Classification Smoothing

This task removes speckling noise from a classification image. It uses majority analysis to change spurious pixels within a large single class to that class.  For details regarding the operation of ENVI Tasks on the Platform refer to [ENVI Task Runner]() documentation.

### Table of Contents
 * [Quickstart](#quickstart) - Get started!
 * [Runtime](#runtime) - Detailed Description of Inputs
 * [Inputs](#inputs) - Required and optional task inputs.
 * [Outputs](#outputs) - Task outputs and example contents.
 * [Advanced](#advanced) - Script performing multiple tasks in one workflow
 * [Contact Us](#contact-us)

### Quickstart

This task requires that the image has been pre-processed using the [Advanced Image Processor](https://github.com/TDG-Platform/docs/blob/master/AOP_Strip_Processor.md), and that a classification has been run on the output from preprocessing. In the example workflow below, the  [ISODATA Classification](https://github.com/TDG-Platform/docs/blob/master/ENVI_ISODATAClassification.md) Task was utilized to perform the classification step on preprocessed data.

```python  
	from gbdxtools import Interface
	gbdx = Interface()

	isodata = gbdx.Task("ENVI_ISODATAClassification")
  	# Edit the following path to reflect a specific path to an image
	isodata.inputs.input_raster = 's3://gbd-customer-data/CustomerAccount#/PathToImage/'
	smooth = gbdx.Task("ENVI_ClassificationSmoothing")
	smooth.inputs.input_raster = isodata.outputs.output_raster_uri.value
	workflow = gbdx.Workflow([ isodata, smooth ])
	
 	# Edit the following line(s) to reflect specific folder(s) for the output file (example location provided)
	workflow.savedata(isodata.outputs.output_raster_uri, location="ISODATAClassification")
	workflow.savedata(smooth.outputs.output_raster_uri, location="ISODATAClassification/Smoothing")
	workflow.execute()
	print workflow.id
	print workflow.status
```

### Runtime

The following table lists all applicable runtime outputs for Classification Smoothing. An estimated Runtime for the Advanced Script example can be derived from adding the result for the two pre-processing steps. For details on the methods of testing the runtimes of the task visit the following link:(INSERT link to GBDX U page here)

  Sensor Name  |  Total Pixels  |  Total Area (k2)  |  Time(secs)  |  Time/Area k2
--------|:----------:|-----------|----------------|---------------
QB02 | 41,551,668 | 312.07 | 173.91 | 0.56 |
WV02|35,872,942 | 329.87 | 174.86 | 0.53 |
WV03|35,371,971 | 196.27 | 161.52 | 0.82 |
GE01| 57,498,000 | 332.97 | 181.06 | 0.54 |


### Inputs
The following table lists all taskname inputs.
Mandatory (optional) settings are listed as Required = True (Required = False).

  Name       |  Required  |  Valid Values       |  Description  
-------------|:-----------:|:--------------------|---------------
input_raster | True       | s3 URL, .hdr, .tiff | Specify a classification raster on which to perform aggregation.

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
kernel_size                |           3           |    any odd number >= 3          | Specify an odd number with the smoothing kernel size. The minimum value is 3 pixels, and the default value is 3 pixels.

### Advanced

Included below is a complete end-to-end workflow for Advanced Image Preprocessing => ISODATA Classification => Classification Smoothing:

```python
	# Advanced Task Script:  Advanced Image Preprocessor=>ISODATA=>Classification Smoothing
	# This Task runs using IPython in the gbdxtools Interface
	# Initialize the gbdxtools Interface
	from gbdxtools import Interface
	gbdx = Interface()

  #Edit the following path to reflect a specific path to an image
	data = 's3://gbd-customer-data/CustomerAccount#/PathToImage/'
  aoptask = gbdx.Task("AOP_Strip_Processor", data=data, enable_acomp=True, bands='MS', enable_pansharpen=False, enable_dra=False)

	# Capture AOP task outputs
	log = aoptask.get_output('log')
	orthoed_output = aoptask.get_output('data')

	# Run ISODATA
	isodata = gbdx.Task("ENVI_ISODATAClassification")
	isodata.inputs.input_raster = aoptask.outputs.data.value
	isodata.inputs.file_types = "tif"

	# Run Smoothing
	smooth = gbdx.Task("ENVI_ClassificationSmoothing")
	smooth.inputs.input_raster = isodata.outputs.output_raster_uri.value
	smooth.inputs.file_types = "hdr"

	# Run Workflow and Send output to  s3 Bucket
	workflow = gbdx.Workflow([ aoptask, isodata, smooth ])
  #Edit the following line(s) to reflect specific folder(s) for the output file (example location provided)
	workflow.savedata(aoptask.outputs.data, location="Classification/AOP)
	workflow.savedata(isodata.outputs.output_raster_uri, location="Classification/ISODATA")
	workflow.savedata(smooth.outputs.output_raster_uri, location="Classification/Smoothing")
	workflow.execute()
	print workflow.id
	print workflow.status
```

**Data Structure for Expected Outputs:**

Your smoothed classification file will be written to the specified S3 Customer Location in the ENVI file format and tif format(e.g.  s3://gbd-customer-data/unique customer id/named directory/classification.hdr).  

For background on the development and implementation of Classification Smoothing refer to the [ENVI Documentation](https://www.harrisgeospatial.com/docs/classificationtutorial.html)


###Contact Us
Document Owner - [Kathleen Johnson](kajohnso@digitalglobe.com)
