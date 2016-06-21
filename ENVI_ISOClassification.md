# ENVI_ISODATAClassification

**ENVI_ISODATAClassification** The ISODATA method for unsupervised classification starts by calculating class means evenly distributed in the data space, then iteratively clusters the remaining pixels using minimum distance techniques. Each iteration recalculates means and reclassifies pixels with respect to the new means. This process continues until the percentage of pixels that change classes during an iteration is less than the change threshold or the maximum number of iterations is reached

**Example Script:** Run in IPython using the GBDXTools Interface
    

    from gbdxtools import Interface
    import json
	
    gbdx = Interface()
	
    envitask = gbdx.Task("ENVI_ISODATAClassification")
    envitask.inputs.file_types = 'tif'
    envitask.inputs.input_raster = "s3://gbd-customer-data/pathToImage/output_raster_uri/outputfile.tif"
    envitask.outputs.output_raster = "ENVI"
	
    workflow = gbdx.Workflow([ envitask ])
	
    workflow.savedata(
        envitask.outputs.output_raster_uri,
        location="output_raster_uri"
    )
    workflow.execute()
	
    print workflow.id
	workflow.status
	

**Description of Input Parameters and Options for the "ENVI_ISODATAClassification":**
This task will function on a multi-spectral image located in the S3 location: 
Input imagery sensor types include but may not be limited to: QuickBird, WorldView 1, WorldView 2, WorldView 3 and GeoEye
Tif files from the AOP_Strip_Processor were tested with this task to confirm functionality; however, the task may ingest additional raster image file types such as: ENVI .hdr,  
	
**REQUIRED SETTINGS AND DEFINITIONS:**

* S3 location of input data (1B data will process by TIL or a strip run through AOP will be in TIF format):
    * Required = true
    * type = ‘directory’
	* Description = specify the input raster for applying the thresholds
    * name = ‘input_raster’

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

* Define the Threshold Percent",
    * Required = false 
	* Description = The change threshold percentage that determines when to complete the classification.  When the percentage of pixels that change classes during an iteration is less than the threshold value, the classification completes.
    * type = 'string'
    * name =  "change_threshold_percent"
	
* Define the Number of Classes",
    * Required = false 
	* Description = The requested number of classes to generate
    * type = 'string'
    * name =  "number_of_classes"

* Define the Number of Iterations",
    * Required = false 
	* Description = The maximum iterations to perform.  If the change threshold percent is not met before the maximum number of iterations is reached, the classification completes
    * type = 'string'
    * name =  "iterations"	
	
* Define the Output Metadata Directory",
    * Required = false 
	* Description = GBDX Requirement. Output location for task meta data such as execution log and output JSON
    * type = 'string'
    * name =  "task_meta_data"
	
	
###Postman status @ 13:07 6/21/16
"completed_time": "2016-06-20T18:08:53.313140+00:00",
  "state": {
    "state": "complete",
    "event": "succeeded"
  },
  "submitted_time": "2016-06-20T17:58:56.112324+00:00",


**Data Structure for Expected Outputs:**

Your Processed ROI file will be written to the specified S3 Customer Location in the ENVI roi.xml file format(e.g.  s3://gbd-customer-data/unique customer id/named directory/roi.xml).  


For background on the development and implementation of Spectral Index refer to the [ENVI Documentation](https://www.harrisgeospatial.com/docs/classificationtutorial.html)

