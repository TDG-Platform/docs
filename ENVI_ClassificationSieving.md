# ENVI_ClassificationSieving

**ENVI_ClassificationSieving** The Sieving task solves the issue of isolated single pixels in a classification . With a classification image as input, the task uses a filter of 4 to 8 pixels to determine if a pixel is isolated within a group.  The isolated pixels identified by the algorithm will then be written in a new raster as 'unclassified'. Use ENVIClassificationClumpingTask to remove the black pixels.

### Table of Contents
 * [Quickstart](#quickstart) - Get started!
 * [Inputs](#inputs) - Required and optional task inputs.
 * [Outputs](#outputs) - Task outputs and example contents.
 * [Runtime](#runtime) - Example estimate of task runtime.

 ### Quickstart
**Example Script:** Run in IPython using the GBDXTools Interface

```python
from gbdxtools import Interface
gbdx = Interface()

isodata = gbdx.Task("ENVI_ISODATAClassification")
#Edit the following path to reflect a specific path to an image
isodata.inputs.input_raster = 's3://gbd-customer-data/CustomerAccount#/PathToImage/'

sieve = gbdx.Task("ENVI_ClassificationSieving")
sieve.inputs.input_raster = isodata.outputs.output_raster_uri.value

workflow = gbdx.Workflow([isodata, sieve])
#Edit the following line(s) to reflect specific folder(s) for the output file (example location provided)
workflow.savedata(
    isodata.outputs.output_raster_uri,
          location="classification/isodata"
)

workflow.savedata(
    sieve.outputs.output_raster_uri,
      location="classification/sieve"
)

print workflow.execute()
```


### Inputs
**Description of Input Parameters and Options for "ENVI_ClassificationSieving":**
This task will function on a classification image located in the S3 location.  The file type input of the classification is preferred in the .hdr format.  An example of ENVI ISO Data Classification is provided in the sample script above. Additional options include:

All inputs are **required**

Name        | Required             |       Default         |        Valid Values             |   Description
---------------|:----------|:---------------------:|---------------------------------|-----------------
input_raster     |    True        |          N/A          | S3 URL   ENVI .hdr only         | S3 location of input data specify a raster on which to perform classification sieving
input_raster_format  |	False  |       N/A   |	string  |	A string for selecting the raster format (non-DG format). Please refer to Supported Datasets table below for a list of valid values for currently supported image data products.
input_raster_band_grouping    |	False  |    N/A	|   string   |	A string name indentify which band grouping to use for the task.
input_raster_filename    |  False   |   N/A    | string   |  Provide the explicit relative raster filename that ENVI will open. This overrides any file lookup in the task runner.
minimum_size    | False           |         3 X 3         | string                          | Specify the minimum size of a blob to keep. If a minimum size is not defined, the minimum size will be set to two
pixel_connectivity  |     False       |   The default is 8    | string                          | Specify 4 (four-neighbor) or 8 (eight-neighbor) regions around a pixel are searched, for continuous blobs.
class_order     | False           |     first to last     | string                          | Specify the order of class names in which sieving is applied to the classification image.



### Outputs

The following table lists the Sieving task outputs.

Name                | Required |   Description
--------------------|:--------:|-----------------
output_raster_uri   |  True    | Specify a string with the fully-qualified path and file name for OUTPUT_RASTER.
task_meta_data          |  False          | Output location for task meta data such as execution log and output JSON
output_raster_uri_filename |     False    | Folder name in S3 location with the specified file name


### Runtime

The following table lists all applicable runtime outputs. (This section will be completed the Algorithm Curation team)
For details on the methods of testing the runtimes of the task visit the following link:(INSERT link to GBDX U page here)

  Sensor Name  | Total Pixels |  Total Area (k2)  |  Time(secs)  |  Time/Area k2
--------|:----------:|-----------|----------------|---------------
QB | 41,551,668 | 312.07 | 172.11 | 0.55  
WV02|35,872,942|329.87| 175.47| 0.53
WV03|35,371,971|196.27| 189.05| 0.96
GE| 57,498,000|332.97|171.95 | 0.52


**Data Structure for Expected Outputs:**

Your processed classification file will be written to the specified S3 Customer Location in the ENVI .hdr file format and tif format(e.g.  s3://gbd-customer-data/unique customer id/named directory/output.hdr).  


For background on the development and implementation of Classification Sieving refer to the [ENVI Documentation](https://www.harrisgeospatial.com/docs/sievingclasses.html)
