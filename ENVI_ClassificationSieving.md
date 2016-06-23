# ENVI_ClassificationSieving

**ENVI_ClassificationSieving** The Sieving task solves the issue of isolated single pixels in a classification . Using a classification image as input, the task uses a filter of 4 to 8 pixels to determine if a pixel is isolated within a group.  The isolated pixels identified by the algorithm will then be written in a new raster as 'unclassified'. Use ENVIClassificationClumpingTask to remove the black pixels.

*Example Script:** Run in IPython using the GBDXTools Interface

    from gbdxtools import Interface
​    gbdx = Interface()

    isodata = gbdx.Task("ENVI_ISODATAClassification")
    isodata.inputs.input_raster = "s3://gbd-customer-data/PathToImageFolder"
    isodata.inputs.file_types = "tif"
​
    sieve = gbdx.Task("ENVI_ClassificationSieving")
    sieve.inputs.input_raster = isodata.outputs.output_raster_uri.value
    sieve.inputs.file_types = "hdr"
	
    workflow = gbdx.Workflow([isodata, sieve])

    workflow.savedata(
        isodata.outputs.output_raster_uri,
        location="classification/isodata"
    )
​
    workflow.savedata(
        sieve.outputs.output_raster_uri,
        location="classification/sieve"
    )
​    
    print workflow.execute()
	

**Description of Input Parameters and Options for the "ENVI_ClassificationSieving":**
This task will function on a classification image located in the S3 location.  The file type input of the classification is preferred in the .hdr format.  An example of ENVI ISO Data Classification is provided in the sample script above. Additional options include:
	
**REQUIRED SETTINGS AND DEFINITIONS:**

* S3 location of input data (Input classification file must be in ENVI format ):
    * Required = true
    * type = ‘directory’
	* Description = Specify a raster on which to perform classification sieving 
    * name = ‘input_raster’

* Define the Output Directory: (a gbd-customer-data location)
    * Required = true
    * type = ‘directory’
	* description = Specify a string with the fully-qualified path and file name for OUTPUT_RASTER
    * name = "output_raster_uri"


**OPTIONAL SETTINGS AND DEFINITIONS:**

* Define the File Types",
    * Required = false 
	* Description = Comma separated list of permitted file type extensions. Use this to filter input files
    * type = 'string'
    * name =  "file_types"

* Define the Minimum Size",
    * Required = false 
	* Description = Specify the minimum size of a blob to keep. If a minimum size is not defined, the minimum size will be set to two.
    * type = 'string'
    * name =  "minimum_size"
	
* Define the Pixel Connectivity",
    * Required = false 
	* Description = Specify 4 (four-neighbor) or 8 (eight-neighbor) regions around a pixel are searched, for continuous blobs. The default is 8
    * type = 'string'
    * name =  "pixel_connectivity"

* Define the Class Order",
    * Required = false 
	* Description = Specify the order of class names in which sieving is applied to the classification image. If you do not specify this keyword, the classes are processed from first to last
    * type = 'string'
    * name =  "class_order"	
	
* Define the Output Metadata Directory",
    * Required = false 
	* Description = GBDX Requirement. Output location for task meta data such as execution log and output JSON
    * type = 'string'
    * name =  "task_meta_data"
	
	
	
###Postman status @ 09:13 6/21/16
completed_time": "2016-06-21T15:13:49.155121+00:00",
  "state": {
    "state": "complete",
    "event": "succeeded"
  },
  "submitted_time": "2016-06-21T14:32:14.671243+00:00,


**Data Structure for Expected Outputs:**

Your Processed ROI file will be written to the specified S3 Customer Location in the ENVI .hdr file format and tif format(e.g.  s3://gbd-customer-data/unique customer id/named directory/output.hdr).  


For background on the development and implementation of Classification Sieving refer to the [ENVI Documentation](https://www.harrisgeospatial.com/docs/sievingclasses.html)

