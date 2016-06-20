# ENVI_ImageThresholdToROI

**ENVI_ImageThresholdToROI** This task creates ROIs from band thresholds. You can specify one or more thresholds for one or more ROIs.

**Example Script:** Run in IPython using the GBDXTools Interface
	
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
​
    print workflow.execute()
	
	

**Description of Input Parameters and Options for the "ENVI_ImageThresholdToROI":**
This task will function on a multi-spectral image located in the S3 location: 
Input imagery sensor types include but may not be limited to: QuickBird, WorldView 1, WorldView 2, WorldView 3 and GeoEye
Tif files from the AOP_Strip_Processor were tested with this task to confirm functionality; however, the task may ingest additional raster image file types such as: ENVI .hdr,  
	
**REQUIRED SETTINGS AND DEFINITIONS:**

* S3 location of input data (1B data will process by TIL or a strip run through AOP will be in TIF format):
    * Required = true
    * type = ‘directory’
	* Description = specify the input raster for applying the thresholds
    * name = ‘input_raster’

* Define ROI color 
    * Required = true
    * type = ‘string’
	* Description = Specify a (3,n) byte array with the RGB colors for each ROI, where n is the number of ROIs specified by ROI_NAME
    * name = ‘roi_color’
	
* Define ROI threshold 
    * Required = true
    * type = ‘string’
	* Description = specify an array that represents a threshold: [minimum, maximum, zero-based band number].  You can have one or more thresholds to one or more ROIs
    * name = ‘roi_color’

* Define ROI name 
    * Required = true
    * type = ‘string’
	* Description = Specify a string or array of strings with the names of each ROI
    * name = ‘roi_color’

* Define the Output Directory: (a gbd-customer-data location)
    * Required = true
    * type = ‘directory’
	* description = Specify a string with the fully-qualified path and filename for OUTPUT_ROI
    * name = "output_roi_uri"


**OPTIONAL SETTINGS AND DEFINITIONS:**

* Define the File Types",
    * Required = false 
	* Description = Comma separated list of permitted file type extensions. Use this to filter input files
    * type = 'string'
    * name =  "file_types"

* Define the Output log Directory",
    * Required = false 
	* Description = Specify a string with the fully-qualified path and file name for OUTPUT_ROI
    * type = 'string'
    * name =  "output_roi_uri_filename"

###Postman status @ 13:07 6/20/16
"completed_time": "2016-06-20T18:08:53.313140+00:00",
  "state": {
    "state": "complete",
    "event": "succeeded"
  },
  "submitted_time": "2016-06-20T17:58:56.112324+00:00",


**Data Structure for Expected Outputs:**

Your Processed ROI file will be written to the specified S3 Customer Location in the ENVI roi.xml file format(e.g.  s3://gbd-customer-data/unique customer id/named directory/roi.xml).  


For background on the development and implementation of Spectral Index refer to the [ENVI Documentation](https://www.harrisgeospatial.com/docs/enviimagethresholdtoroitask.html)

