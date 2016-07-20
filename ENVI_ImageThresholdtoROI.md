# ENVI_ImageThresholdToROI

**ENVI_ImageThresholdToROI** This task creates ROIs from band thresholds. You can specify one or more thresholds for one or more ROIs.

### Table of Contents
 * [Quickstart](#quickstart) - Get started!
 * [Inputs](#inputs) - Required and optional task inputs.
 * [Outputs](#outputs) - Task outputs and example contents.
 * [Advanced](#advanced) - Full task workflow with optional parameters used as example 
 * [Contact Us](#contact-us) - Contact tech or document owner.

**Example Script:** Run in IPython using the GBDXTools Interface

```python
    from gbdxtools import Interface
    gbdx = Interface()

    task = gbdx.Task("ENVI_ImageThresholdToROI")
    task.inputs.input_raster = "s3://gbd-customer-data/Imagepath/"
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
-------------------------|:---------------------:|-----------------------------------------------------|---------------------------------
input_raster             |          N/A          | S3 URL   directory                                  | S3 location of input data specify the input raster for applying the thresholds
roi_color                |          N/A          | 3,n byte array with RGB color (see example script)  | Define ROI color where n is the number of ROIs specified by ROI_NAME
threshold                |          N/A          | [minimum, maximum, zero-based band number]          | specify an array that represents a threshold: [minimum, maximum, zero-based band number] You can have one or more thresholds to one or more ROIs
roi_name                 |          N/A          | String  (see example script)                        | Specify a string or array of strings with the names of each ROI
	

### Outputs

The following table lists the ENVI_ImageThresholdToROI task outputs.

Name                | Required |   Description
--------------------|:--------:|-----------------
output_raster_uri   |     Y    | Specify a string with the fully-qualified path and file name for OUTPUT_RASTER.


**OPTIONAL SETTINGS AND DEFINITIONS:**

Name                       |       Default         |        Valid Values             |   Description
---------------------------|:---------------------:|---------------------------------|-----------------
file_types                 |          N/A          | string                          | Comma separated list of permitted file type extensions. Use this to filter input files
output_roi_uri_filename    |         true          | Folder name in S3 location      | Specify the file name

###Advanced

```python
    from gbdxtools import Interface
    gbdx = Interface()
    data = "s3://receiving-dgcs-tdgplatform-com/055026839010_01_003"
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
