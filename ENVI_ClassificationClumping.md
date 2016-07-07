# ENVI_ClassificationClumping

**ENVI_ClassificationClumping** The Clumping task resolves the unclassified pixels produced from the Sieving classification task.  The selected classes are clumped together by first performing a dilate operation then an erode operation on the classification image using a kernel of the size specified in the parameters dialogue.  This task requires a classification has been run through the [Sieving Classification] (https://github.com/TDG-Platform/docs/blob/envi_tasks_docs/ENVI_ClassificationSieving.md)

*Example Script:** Run in IPython using the GBDXTools Interface

    from gbdxtools import Interface
    gbdx = Interface()
	
    isodata = gbdx.Task("ENVI_ISODATAClassification")
    isodata.inputs.input_raster = "s3://gbd-customer-data/PathToImageFolder"
	isodata.inputs.file_types = "tif"
	
    sieve = gbdx.Task("ENVI_ClassificationSieving")
    sieve.inputs.input_raster = isodata.outputs.output_raster_uri.value
    sieve.inputs.file_types = "hdr"

    clump = gbdx.Task("ENVI_ClassificationClumping")
    clump.inputs.input_raster = sieve.outputs.output_raster_uri.value
    clump.inputs.file_types = "hdr"
	
    workflow = gbdx.Workflow([isodata, sieve, clump])
	
    workflow.savedata(
        isodata.outputs.output_raster_uri,
        location="classification/isodata"
    )
	
    workflow.savedata(
        sieve.outputs.output_raster_uri,
        location="classification/sieve"
    )
	
    workflow.savedata(
        clump.outputs.output_raster_uri,
        location="classification/clump"
    )

    print workflow.execute()
	

**Description of Input Parameters and Options for the "ENVI_ClassificationClumping":**
This task will function on a Sieving classification image located in the S3 location.  The file type input of the classification is preferred in the .hdr format.  An example of ENVI ISO Data Classification and Sieving are provided in the sample script above to demonstrate a full workflow. Additional options include:
	
**REQUIRED SETTINGS AND DEFINITIONS:**

* S3 location of input data (Input classification file must be in ENVI format ):
    * Required = true
    * type = ‘directory’
	* Description = Specify a sieving output raster on which to perform classification clumping 
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

* Define the Dilate Kernel",
    * Required = false 
	* Description = Specify 2D array of zeros and ones that represents the structuring element (kernel) used for a dilate operation. If no kernel is specified, a 3 x 3 array will be used with a value of 1 for all of the array elements. Dilation is a morphological operation that uses a structuring element to expand the shapes contained in the input image.
    * type = 'string'
    * name =  "dilate_kernel"
	
* Define the Erode Kernel",
    * Required = false 
	* Description = Specify 2D array of zeros and ones that represents the structuring element (kernel) used for an erode operation. If no kernel is specified, a 3 x 3 array will be used with a value of 1 for all of the array elements. Erosion is a morphological operation that uses a structuring element to reduce the shapes contained in the input image.
    * type = 'string'
    * name =  "erode_kernel"

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

* Define the Output file name",
    * Required = false 
	* Description = Specify a string with the fully-qualified path and filename for OUTPUT_RASTER
    * type = 'string'
    * name =  "output_raster_uri_filename"
	
###Postman status @ 09:13 6/21/16
completed_time": "2016-06-21T15:13:49.155121+00:00",
  "state": {
    "state": "complete",
    "event": "succeeded"
  },
  "submitted_time": "2016-06-21T14:32:14.671243+00:00,


**Data Structure for Expected Outputs:**

Your post-classification file will be written to the specified S3 Customer Location in the ENVI .hdr file format and tif format(e.g.  s3://gbd-customer-data/unique customer id/named directory/output.hdr).  


For background on the development and implementation of Classification Clumping refer to the [ENVI Documentation](https://www.harrisgeospatial.com/docs/clumpingclasses.html)

