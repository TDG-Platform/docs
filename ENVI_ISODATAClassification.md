# ENVI_ISODATAClassification

**ENVI_ISODATAClassification** The ISODATA method for unsupervised classification starts by calculating class means evenly distributed in the data space, then iteratively clusters the remaining pixels using minimum distance techniques. Each iteration recalculates means and reclassifies pixels with respect to the new means. This process continues until the percentage of pixels that change classes during an iteration is less than the change threshold or the maximum number of iterations is reached.   For details regarding the operation of ENVI Tasks on the Platform refer to [ENVI Task Runner](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md) documentation.

### Table of Contents
 * [Quickstart](#quickstart) - Get started!
 * [Inputs](#inputs) - Required and optional task inputs.
 * [Outputs](#outputs) - Task outputs and example contents.
 * [Runtime](#runtime) - Results of task benchmark tests.
 * [Advanced Options](#advanced-options)
 * [Contact Us](#contact-us) - Contact tech or document owner.

**Example Script:** Run in IPython using the GBDXTools Interface

```python
# Quickstart **Example Script Run in Python using the gbdxTools Interface
# First Initialize the Environment

    from gbdxtools import Interface
    gbdx = Interface()

    envitask = gbdx.Task("ENVI_ISODATAClassification")
    #Edit the following path to reflect a specific path to an image
    envitask.inputs.input_raster = 's3://gbd-customer-data/CustomerAccount#/PathToImage/'

    workflow = gbdx.Workflow([ envitask ])

    workflow.savedata(
        #Edit the following line(s) to reflect specific folder(s) for the output file (example location provided)
        envitask.outputs.output_raster_uri,
        location="ISODATA/output_raster_uri"
    )
    
    workflow.execute()

    print workflow.id
	workflow.status
```

### Inputs

**Description of Input Parameters and Options for the "ENVI_ISODATAClassification":**
This task will function on a multi-spectral image located in the S3 location:
Input imagery sensor types include but may not be limited to: QuickBird, WorldView 1, WorldView 2, WorldView 3 and GeoEye
Tif files from the AOP_Strip_Processor were tested with this task to confirm functionality; however, the task may ingest additional raster image file types such as: ENVI .hdr,  

The following table lists the ENVI ISO DATA Classification task:

All inputs are **required**

Name                     | Required   |      Default         |        Valid Values             |   Description
-------------------------|:-------------:|:------------:|---------------------------------|-----------------
input_raster             |   YES     |       N/A          | S3 URL   .TIF only              | S3 location of input data. S raster on which to perform ISODATA classification
input_raster_format  |    NO     | N/A  |  string  |  A string for selecting the raster format (non-DG format). Please refer to Supported Datasets table below for a list of valid values for currently supported image data products.
input_raster_band_grouping     |  NO  |    N/A   |  string   |  A string name indentify which band grouping to use for the task.
change_threshold_percent   |    NO    |     3 X 3         | string                          | The change threshold percentage that determines when to complete the classification.  When the percentage of pixels that change classes during an iteration is less than the threshold value, the classification completes
number_of_classes          |   NO    |       2            | string                          | The requested number of classes to generate
iterations                 |    NO    |      N/A          | string                          | The maximum iterations to perform.  If the change threshold percent is not met before the maximum number of iterations is reached, the classification completes
task_meta_data             |    NO    |      N/A          | string                          | Output location for task meta data such as execution log and output JSON

### Outputs

The following table lists the ISO DATA Classification task outputs.

Name                | Required |   Default  | Valid Values  |Description
--------------------|:--------:|------------|---------------|---------------------
output_raster_uri   |     YES   |   N/A |  .TIF, .HDR       | This will explain the output file location 
output_raster_uri_filename |  NO      |  N/A    |   string  | Specify filename in S3 output location      


This task will function on an image located in the S3 location.  The file type input is preferred in the .hdr format.   Additional options include:

### Runtime

The following table lists all applicable runtime outputs for the QuickStart Script. (This section will be completed the Algorithm Curation team)
For details on the methods of testing the runtimes of the task visit the following link:(INSERT link to GBDX U page here)

  Sensor Name  |  Total Pixels  |  Total Area (k2)  |  Time(secs)  |  Time/Area k2
--------|:----------:|-----------|----------------|---------------
QB | 41,551,668 | 312.07 | 308.27 | 0.99
WV02|35,872,942|329.87|1,939.17 | 5.88
WV03|35,371,971|196.27| 858.28|4.37
GE| 57,498,000|332.97|490.32| 1.47

**Data Structure for Expected Outputs:**

Your Processed classification file will be written to the specified S3 Customer Location in the ENVI file format and tif format(e.g.  s3://gbd-customer-data/unique customer id/named directory/classification.hdr).  


For background on the development and implementation of ISO Classification refer to the [ENVI Documentation](https://www.harrisgeospatial.com/docs/classificationtutorial.html)

### Advanced Options

This script links the [Advanced Image Preprocessor](https://github.com/TDG-Platform/docs/blob/master/Advanced_Image_Preprocessor.md) to the ENVI ISODATA Classification task.

```python
# This Advanced Script links the output of the Advanced Image Preprocessor (AOP) to the ENVI ISODATA Classification	
	from gbdxtools import Interface
	gbdx = Interface()

	# Import the Image from s3. Edit the following path to reflect a specific path to an image
	data = "s3://gbd-customer-data/CustomerAccount#/PathToImage/"
	
	aoptask = gbdx.Task(
		"AOP_Strip_Processor", data=data, enable_acomp=True, bands='MS', 
		enable_pansharpen=False, enable_dra=False
	)

	isodata = gbdx.Task("ENVI_ISODATAClassification")
	# Import the AOP output to the ENVI Task and run the task.
	isodata.inputs.input_raster = aoptask.outputs.data.value
	workflow = gbdx.Workflow([ aoptask, isodata ])
	
	# Edit the following line(s) to reflect specific folder(s) for the output file.
	workflow.savedata(isodata.outputs.output_raster_uri, location='customer output directory')

	workflow.execute()
	print workflow.id
	print workflow.status
```



###Contact Us
Document Owner - Carl Reeder - creeder@digitalglobe.com
