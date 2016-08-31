# ENVI_ClassificationClumping

**ENVI_ClassificationClumping** The Clumping task resolves the unclassified pixels produced from the Sieving classification task.  The selected classes are clumped together by first performing a dilate operation then an erode operation on the classification image using a kernel of the size specified in the parameters dialogue.  This task requires a classification has been run and in the example workflow below, the Sieving task is utilized ([Sieving Classification]). (https://github.com/TDG-Platform/docs/blob/envi_tasks_docs/ENVI_ClassificationSieving.md)

### Table of Contents
 * [Quickstart](#quickstart) - Get started!
 * [Inputs](#inputs) - Required and optional task inputs.
 * [Outputs](#outputs) - Task outputs and example contents.
 * [Advanced](#advanced) - Additional information for advanced users.

### Quickstart
*Example Script:* Run in IPython using the GBDXTools Interface

```python
# Quickstart **Example Script Run in Python using the gbdxTools Interface
# First Initialize the Environment 
   
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
```	

### Inputs	

**Description of Input Parameters and Options for the "ENVI_ClassificationClumping":**
This task will function on a classification raster dataset.  
The following table lists the inputs for ENVI_ClassificationClumping task:

All inputs are **required**

Name                     |       Default         |        Valid Values             |   Description
-------------------------|:---------------------:|---------------------------------|-----------------
input_raster             |          N/A          | S3 URL   .hdr, .TIF              | S3 location of input data specify a classification raster output raster on which to perform classification clumping

### Outputs

The following table lists the Classification Clumping task outputs.

Name            | Required |   Description
----------------|:--------:|-----------------
output_raster   |     Y    | This will explain the output file location and provide the output in .TIF format.


This task will function on a classification image located in the S3 location.  The file type input of the classification is preferred in the .hdr format.  An example of ENVI ISO Data Classification and Sieving are provided in the sample script above to demonstrate a full workflow. Additional options include:


**OPTIONAL SETTINGS AND DEFINITIONS:**

Name                       |       Default         |        Valid Values             |   Description
---------------------------|:---------------------:|---------------------------------|-----------------
file_types                 |          N/A          | string                          | Comma separated list of permitted file type extensions. Use this to filter input files
dilate_kernel              |         3 X 3         | string                          | Specify 2D array of zeros and ones that represents the structuring element (kernel) used for a dilate operation.Dilation is a morphological operation that uses a structuring element to expand the shapes contained in the input image
erode_kernel               |         3 X 3         | string                          | Specify 2D array of zeros and ones that represents the structuring element (kernel) used for an erode operation
class_order                |     first to last     | string                          | Specify the order of class names in which sieving is applied to the classification image. 
task_meta_data             |          N/A          | string                          | Output location for task meta data such as execution log and output JSON
output_raster_uri_filename |         output          | Folder name in S3 location      | Specify the file name
	


**Data Structure for Expected Outputs:**

Your post-classification file will be written to the specified S3 Customer Location in the ENVI .hdr file format and tif format(e.g.  s3://gbd-customer-data/unique customer id/named directory/output.hdr).  


For background on the development and implementation of Classification Clumping refer to the [ENVI Documentation](https://www.harrisgeospatial.com/docs/clumpingclasses.html)

###Contact Us
Document Owner - Carl Reeder - creeder@digitalglobe.com
