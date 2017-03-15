# ENVI_ImageThresholdToROI

**ENVI_ImageThresholdToROI** This task creates ROIs from band thresholds. You can specify one or more thresholds for one or more ROIs.

### Table of Contents
 * [Quickstart](#quickstart) - Get started!
 * [Inputs](#inputs) - Required and optional task inputs.
 * [Outputs](#outputs) - Task outputs and example contents.
 * [Runtime](#runtime) - Example estimate of task runtime.
 * [Advanced](#advanced) - Full task workflow with optional parameters used as example
 * [Contact Us](#contact-us) - Contact tech or document owner.

**Example Script:** Run in IPython using the GBDXTools Interface

```python
    from gbdxtools import Interface
    gbdx = Interface()

    task = gbdx.Task("ENVI_ImageThresholdToROI")
    #Edit the following path to reflect a specific path to an image
    task.inputs.input_raster = 's3://gbd-customer-data/CustomerAccount#/PathToImage/'
    task.inputs.file_types = "tif"
    task.inputs.roi_name = "[\"Water\", \"Land\"]"
    task.inputs.roi_color = "[[0,255,0],[0,0,255]]"
    task.inputs.threshold = "[[138,221,0],[222,306,0]]"
    task.inputs.output_roi_uri_filename = "roi.xml"

    workflow = gbdx.Workflow([task])
    workflow.savedata(
        task.outputs.output_roi_uri,
        location='ImgToROI'
    )

    print workflow.execute()

```
### Inputs

**Description of Input Parameters and Options for the "ENVI_ImageThresholdToROI":**
This task will function on a multi-spectral image located in the S3 location:
Input imagery sensor types include but may not be limited to: QuickBird, WorldView 1, WorldView 2, WorldView 3 and GeoEye
Tif files from the AOP_Strip_Processor were tested with this task to confirm functionality; however, the task may ingest additional raster image file types such as: ENVI .hdr,  

**REQUIRED SETTINGS AND DEFINITIONS:**

Name                     |       Default         |                 Valid Values                        |   Description
-------------------------|:---------------------:|-----------------------------------------------------|--------------------------------
input_raster             |          N/A          | S3 URL   directory                                  | S3 location of input data specify the input raster for applying the thresholds
input_raster_format   |  False    | N/A   |   string  | A string for selecting the raster format (non-DG format). Please refer to Supported Datasets table below for a list of valid values for currently supported image data products.
input_raster_band_grouping  False  |  N/A   | string   |  A string name indentify which band grouping to use for the task.
input_raster_filename   | False     |   N/A   |  string  |  Provide the explicit relative raster filename that ENVI will open. This overrides any file lookup in the task runner.
roi_color                |          N/A          | 3,n byte array with RGB color (see example script)  | Define ROI color where n is the number of ROIs specified by ROI_NAME
threshold                |          N/A          | [minimum, maximum, zero-based band number]          | specify an array that represents a threshold: [minimum, maximum, zero-based band number] You can have one or more thresholds to one or more ROIs
roi_name                 |          N/A          | String  (see example script)                        | Specify a string or array of strings with the names of each ROI


### Outputs

The following table lists the ENVI_ImageThresholdToROI task outputs.

Name          |  Required             |       Default         |        Valid Values             |   Description
---------------|------------|:---------------------:|---------------------------------|-----------------
output_raster_uri   |    True    | N/A     |       string    |Specify a string with the fully-qualified path and file name for OUTPUT_RASTER.
output_roi_uri_filename    |  False   |      N/A        | Folder name in S3 location      | Specify the file name
task_meta_data  |  False  |  N/A   | .json   | GBDX Option. Output location for task meta data such as execution log and output JSON

### Runtime

The following table lists all applicable runtime outputs. (This section will be completed the Algorithm Curation team)
For details on the methods of testing the runtimes of the task visit the following link:(INSERT link to GBDX U page here)

  Sensor Name  | Total Pixels |  Total Area (k2)  |  Time(secs)  |  Time/Area k2
--------|:----------:|-----------|----------------|---------------
QB | 41,551,668 | 312.07 |158.62 |0.51  
WV02|35,872,942|329.87|167.47	|0.51
WV03|35,371,971|175.47	|0.89 |.89
GE| 57,498,000|162.43	|0.49 |0.49

###Advanced

To link the workflow of 1 input image into AOP_Strip_Processor and the Image Threshold to ROI task, use the following GBDX tools script in python.

```python
    from gbdxtools import Interface
    gbdx = Interface()
    #Edit the following path to reflect a specific path to an image
    data = 's3://gbd-customer-data/CustomerAccount#/PathToImage/'
    aoptask = gbdx.Task("AOP_Strip_Processor", data=data, enable_acomp=True, enable_pansharpen=False, enable_dra=False, bands='MS')

    # Capture AOP task outputs
    #orthoed_output = aoptask.get_output('data')

    task = gbdx.Task("ENVI_ImageThresholdToROI")
    task.inputs.input_raster = aoptask.outputs.data.value
    task.inputs.file_types = "tif"
    task.inputs.roi_name = "[\"Water\", \"Land\"]"
    task.inputs.roi_color = "[[0,255,0],[0,0,255]]"
    task.inputs.threshold = "[[138,221,0],[222,306,0]]"
    task.inputs.output_roi_uri_filename = "roi.xml"

    workflow = gbdx.Workflow([ aoptask, task ])
    workflow.savedata(
        #Edit the following line(s) to reflect specific folder(s) for the output file (example location provided)
        task.outputs.output_roi_uri,
        location='ENVI/ImgToROI'
    )

    print workflow.execute()
```

**Data Structure for Expected Outputs:**

Your Processed ROI file will be written to the specified S3 Customer Location in the ENVI roi.xml file format(e.g.  s3://gbd-customer-data/unique customer id/named directory/roi.xml).  


For background on the development and implementation of Spectral Index refer to the [ENVI Documentation](https://www.harrisgeospatial.com/docs/enviimagethresholdtoroitask.html)

###Contact Us
Document Owner - Carl Reeder - creeder@digitalglobe.com
