# ENVI_ClassificationClumping

**ENVI_ClassificationClumping** This task performs a clumping method on a classification image. This operation clumps adjacent similar classified areas using morphological operators. Classified images often suffer from a lack of spatial coherency (speckle or holes in classified areas). Low pass filtering could be used to smooth these images, but the class information would be contaminated by adjacent class codes. Clumping classes solves this problem. The selected classes are clumped together by first performing a dilate operation then an erode operation on the classified image using one specified kernel (structuring element) for each operation

This task requires a classification has been run and in the example workflow below, the Sieving task is utilized ([Sieving Classification]). (https://github.com/TDG-Platform/docs/blob/envi_tasks_docs/ENVI_ClassificationSieving.md)

### Table of Contents
 * [Quickstart](#quickstart) - Get started!
 * [Inputs](#inputs) - Required and optional task inputs.
 * [Outputs](#outputs) - Task outputs and example contents.
 * [Advanced](#advanced) - Additional information for advanced users.
 * [Runtime](#runtime) - Example estimate of task runtime.

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
This task will function on an ENVI classification raster dataset.  
The following table lists the inputs for ENVI_ClassificationClumping task:

All inputs are **required**

Name                     |       Default         |        Valid Values             |   Description
-------------------------|:---------------------:|---------------------------------|-----------------
input_raster             |          N/A          | S3 URL   .hdr, .TIF             | S3 location of input data specify an ENVI classification raster output on which to perform classification clumping

### Outputs

The following table lists the Classification Clumping task outputs.

Name            | Required |   Description
----------------|:--------:|-----------------
output_raster   |     Y    | This will explain the output file location and provide the output in .TIF format.


This task will function on an ENVI classification raster located in the S3 location.  The file type input of the ENVI classification raster is preferred in the .hdr format.  An example of ENVI ISODATA Classification and Sieving are provided in the sample script above to demonstrate a full workflow. The Sieving task is recommended to precede the classification clumping task to further refine the ENVI classification raster.  Additional options include:


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

### Runtime

The following table lists all applicable runtime outputs. (This section will be completed the Algorithm Curation team)
For details on the methods of testing the runtimes of the task visit the following link:(INSERT link to GBDX U page here)

  Sensor Name  | Total Pixels |  Total Area (k2)  |  Time(secs)  |  Time/Area k2
--------|:----------:|-----------|----------------|---------------
QB | 41,551,668 | 155.93	| 0.50 |  
WV02|35,872,942|329.87| 171.72| 0.52
WV03|35,371,971|196.27|173.03 |0.88
GE| 57,498,000|173.03	|0.52 |


For background on the development and implementation of Classification Clumping refer to the [ENVI Documentation](http://www.harrisgeospatial.com/docs/enviclassificationclumpingtask.html)

###Contact Us
Document Owner - Carl Reeder - creeder@digitalglobe.com
