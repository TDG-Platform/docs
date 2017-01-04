
# ENVI Classification Aggregation

This task aggregates smaller class regions to a larger, adjacent region as part of the classification cleanup.

### Table of Contents
 * [Quickstart](#quickstart) - Get started!
 * [Runtime](#runtime) - Detailed Description of Inputs
 * [Inputs](#inputs) - Required and optional task inputs.
 * [Outputs](#outputs) - Task outputs and example contents.
 * [Advanced](#advanced) - Script performing multiple tasks in one workflow
 * [Contact Us](#contact-us)

### Quickstart

This task requires that the image has been pre-processed using the [Advanced Image Preprocessor](https://github.com/TDG-Platform/docs/blob/master/AOP_Strip_Processor.md), and that a classification has been run on the output from preprocessing. In the example workflow below, the  [ISODATA Classification](https://github.com/TDG-Platform/docs/blob/master/ENVI_ISODATAClassification.md) Task was utilized to perform the classification step on preprocessed data.

 ```python
	from gbdxtools import Interface
	gbdx = Interface()

	isodata = gbdx.Task("ENVI_ISODATAClassification")
	# The data input and output lines must be edited to point to an authorized customer S3 location)
	isodata.inputs.input_raster = 's3://gbd-customer-data/CustomerAccount#/PathToImage/'
	isodata.inputs.file_types = "tif"
	aggreg = gbdx.Task("ENVI_ClassificationAggregation")
	aggreg.inputs.input_raster = isodata.outputs.output_raster_uri.value
	aggreg.inputs_uri_file_types = "hdr"
	workflow = gbdx.Workflow([ isodata, aggreg ])
	workflow.savedata(isodata.outputs.output_raster_uri, location="S3 gbd-customer-data location/<customer account>/output directory")
	workflow.savedata(aggreg.outputs.output_raster_uri, location="S3 gbd-customer-data location/<customer account>/output directory")
	workflow.execute()
	print workflow.id
	print workflow.status
```

### Runtime

The following table lists all applicable runtime outputs for Classification Aggregation. An estimated Runtime for the Advanced Script example can be derived from adding the result for the two pre-processing steps. For details on the methods of testing the runtimes of the task visit the following link:(INSERT link to GBDX U page here)

  Sensor Name  |  Total Pixels  |  Total Area (k2)  |  Time(secs)  |  Time/Area k2
--------|:----------:|-----------|----------------|---------------
QB02 | 41,551,668 | 312.07 | 328.42 | 1.05 |
WV02|35,872,942 | 329.87 | 414.51 | 1.26 |
WV03|35,371,971 | 196.27 | 447.80 | 2.28 |
GE01| 57,498,000 | 332.97 | 419.17 | 1.26 |


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
minimum_size               |          9           |    any odd number >= 9          | Specify the aggregate minimum size in pixels. Regions with a size of this value or smaller are aggregated to an adjacent, larger region. The default value is 9.

### Advanced

Included below is a complete end-to-end workflow for Advanced Image Preprocessing => ISODATA Classification => Classification Aggregation:

```python
	# Advanced Task Script:  Advanced Image Preprocessor=>ISODATA=>Classification Aggregation
	# This Task runs using IPython in the gbdxtools Interface
	# Initialize the gbdxtools Interface
	from gbdxtools import Interface
	gbdx = Interface()

	# Import the Image from s3.
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
	aggreg = gbdx.Task("ENVI_ClassificationSmoothing")
	aggreg.inputs.input_raster = isodata.outputs.output_raster_uri.value

	# Run Workflow and Send output to  s3 Bucket
	workflow = gbdx.Workflow([ aoptask, isodata, aggreg ])
   	# The data input and output lines must be edited to point to an authorized customer S3 location)
	workflow.savedata(aoptask.outputs.data,location="S3 gbd-customer-data location/<customer account>/output directory")
	workflow.savedata(isodata.outputs.output_raster_uri,location="S3 gbd-customer-data location/<customer account>/output directory")
	workflow.savedata(aggreg.outputs.output_raster_uri,location="S3 gbd-customer-data location/<customer account>/output directory")
	workflow.execute()
	print workflow.id
	print workflow.status
```


**Data Structure for Expected Outputs:**

Your smoothed classification file will be written to the specified S3 Customer Location in the ENVI file format and tif format(e.g.  s3://gbd-customer-data/unique customer id/named directory/classification.hdr).  

For background on the development and implementation of Classification Aggregation refer to the [ENVI Documentation](https://www.harrisgeospatial.com/docs/classificationtutorial.html)


###Contact Us
Document Owner - [Kathleen Johnson](kajohnso@digitalglobe.com)
