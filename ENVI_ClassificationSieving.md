# ENVI_ClassificationSieving

**ENVI_ClassificationSieving** The Sieving task solves the issue of isolated single pixels in a classification . With a classification image as input, the task uses a filter of 4 to 8 pixels to determine if a pixel is isolated within a group.  The isolated pixels identified by the algorithm will then be written in a new raster as 'unclassified'. Use ENVIClassificationClumpingTask to remove the black pixels.

### Table of Contents
 * [Quickstart](#quickstart) - Get started!
 * [Inputs](#inputs) - Required and optional task inputs.
 * [Outputs](#outputs) - Task outputs and example contents.
 * [Advanced](#advanced) - Additional information for advanced users.

 ### Quickstart 
**Example Script:** Run in IPython using the GBDXTools Interface

```python
    from gbdxtools import Interface
    gbdx = Interface()

    isodata = gbdx.Task("ENVI_ISODATAClassification")
    isodata.inputs.input_raster = "s3://gbd-customer-data/PathToImageFolder"
    isodata.inputs.file_types = "tif"

    sieve = gbdx.Task("ENVI_ClassificationSieving")
    sieve.inputs.input_raster = isodata.outputs.output_raster_uri.value
    sieve.inputs.file_types = "hdr"
	
    workflow = gbdx.Workflow([isodata, sieve])

    workflow.savedata(
        isodata.outputs.output_raster_uri,
        location="classification/isodata"
    )

    workflow.savedata(
        sieve.outputs.output_raster_uri,
        location="classification/sieve"
    )

    print workflow.execute()
```python


### Inputs	
**Description of Input Parameters and Options for "ENVI_ClassificationSieving":**
This task will function on a classification image located in the S3 location.  The file type input of the classification is preferred in the .hdr format.  An example of ENVI ISO Data Classification is provided in the sample script above. Additional options include:

All inputs are **required**

Name                     |       Default         |        Valid Values             |   Description
-------------------------|:---------------------:|---------------------------------|-----------------
input_raster             |          N/A          | S3 URL   ENVI .hdr only         | S3 location of input data specify a raster on which to perform classification sieving 
	

### Outputs

The following table lists the Spectral Index task outputs.

Name                | Required |   Description
--------------------|:--------:|-----------------
output_raster_uri   |     Y    | Specify a string with the fully-qualified path and file name for OUTPUT_RASTER.
	

**OPTIONAL SETTINGS AND DEFINITIONS:**

Name                       |       Default         |        Valid Values             |   Description
---------------------------|:---------------------:|---------------------------------|-----------------
file_types                 |          N/A          | string                          | Comma separated list of permitted file type extensions. Use this to filter input files
minimum_size               |         3 X 3         | string                          | Specify the minimum size of a blob to keep. If a minimum size is not defined, the minimum size will be set to two
pixel_connectivity         |   The default is 8    | string                          | Specify 4 (four-neighbor) or 8 (eight-neighbor) regions around a pixel are searched, for continuous blobs. 
class_order                |     first to last     | string                          | Specify the order of class names in which sieving is applied to the classification image. 
task_meta_data             |          N/A          | string                          | Output location for task meta data such as execution log and output JSON
output_raster_uri_filename |         output         | Folder name in S3 location     | Specify the file name



**Data Structure for Expected Outputs:**

Your processed classification file will be written to the specified S3 Customer Location in the ENVI .hdr file format and tif format(e.g.  s3://gbd-customer-data/unique customer id/named directory/output.hdr).  


For background on the development and implementation of Classification Sieving refer to the [ENVI Documentation](https://www.harrisgeospatial.com/docs/sievingclasses.html)