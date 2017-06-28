# Change Detection Preparation (cd_prep)

The Change Detection Preparation task performs a series of operations on a pair of input images to prepare them for the application of downstream change detection algorithms.  It accomplishes this via the following operations:

    1. Initial crop of the input images to their region of overlap  
    2. Image-to-image registration
    3. Alignment of the images to a common grid, cloud removal and final cropping

The input imagery for this task is two orthorectified, atmospherically compensated images in geotiff format and UTM projection from the [Advanced Image Preprocessor](https://github.com/TDG-Platform/docs/blob/master/Advanced_Image_Preprocessor.md).

### Table of Contents
 * [Quickstart](#quickstart) - Get started!
 * [Inputs](#inputs) - Required and optional task inputs.
 * [Outputs](#outputs) - Task outputs and example contents.
 * [Advanced Options](#advanced-options) - Examples linking to a second task and running VNIR+SWIR
 * [Known Issues](#known-issues)

### Quickstart

The Change Detection Preparation GBDX task can be run through a simple Python script using  [gbdxtools](https://github.com/DigitalGlobe/gbdxtools/blob/master/docs/user_guide.rst), 
which requires some initial setup, or through the [GBDX Web Application](https://gbdx.geobigdata.io/materials/).
Tasks and workflows can be added (described here in [gbdxtools](https://github.com/DigitalGlobe/gbdxtools/blob/master/docs/running_workflows.rst)) 
or run separately after the cd_prep process is completed.

**Example Script:** These basic settings will run CDPrep from a pair of input orthorectified, AComped image output from the Advanced Image Preprocessor. See also examples listed under the [Advanced Options](#advanced-options).

```python
# Run The Change Detection Preparation Task on a pair of images
from gbdxtools import Interface
gbdx = Interface()

# The data input and lines must be edited to point to an authorized customer S3 location)
cd_prep = gbdx.Task('cd_prep', 
                    pre_image_dir='s3://gbd-customer-data/CustomerAccount#/PathToPreImage/',
                    post_image_dir='s3://gbd-customer-data/CustomerAccount#/PathToPostImage')
    
workflow = gbdx.Workflow([cd_prep])
#Edit the following line(s) to reflect specific folder(s) for the output file (example location provided)
workflow.savedata(cd_prep.outputs.final_pre_image_dir, location='CDPrep/pre_image_dir')
workflow.savedata(cd_prep.outputs.final_post_image_dir, location='CDPrep/post_image_dir')
workflow.execute()

print workflow.id
print workflow.status
```

**Example Run in IPython:**

    In [1]: from gbdxtools import Interface
    In [2]: gbdx = Interface()
    In [3]: cd_prep = gbdx.Task('cd_prep', 
                                 pre_image_dir='s3://gbd-customer-data/7d8cfdb6-13ee-4a2a-bf7e-0aff4795d927/jkoenig/cd_prep_test/Borneo/test2/AOP/pre/', 
                                 post_image_dir = 's3://gbd-customer-data/7d8cfdb6-13ee-4a2a-bf7e-0aff4795d927/jkoenig/cd_prep_test/Borneo/test2/AOP/post/')
    In [4]: workflow = gbdx.Workflow([cd_prep])
    In [5]: workflow.savedata(cd_prep.outputs.final_pre_image_dir, location='cd_prep_test/pub_test/pre_image_dir')
    In [6]: workflow.savedata(cd_prep.outputs.final_post_image_dir, location='cd_prep_test/pub_test/post_image_dir')
    In [7]: workflow.execute()
    Out [7]: 
    u'4498407427801810318'
    In [8]: print workflow.status
    {u'state': u'running', u'event': u'started'} [9]:

### Inputs

This task takes as input two orthorectified, atmospherically compensated images in geotiff format.
It is intended to work as a following task to the AOP_Strip_Processor, with only the AComp option specified.

Example overlapping 1B images that can be processed by Advanced Image Preprocessor prior Change Detection Preparation are:

    pre-image in India: 1040010004D5AD00
    post-image in India:  105041001259EA00

**Description of Basic Input Parameters for the Change Detection Preparation GBDX task**

The following table lists the cd_prep GBDX inputs.
All inputs are optional with default values, with the exception of
'pre_image_dir', 'post_image_dir', 'final_pre_image_dir', and 'final_post_image_dir'
which specify the task's input and output data locations.

Name        | Required             |       Default         |        Valid Values             |   Description
------------|-------------|:---------------------:|---------------------------------|-----------------
pre_image_dir   | Yes     |  N/A  |  S3 URL | Pre-image input directory containing one or more TIFF files
post_image_dir   |  Yes     | N/A  |  S3 URL | Post-image input directory containing one or more TIFF files


### Outputs

On completion, the processed imagery will be written to your specified S3 Customer 
Location (i.e., s3://gbd-customer-data/unique customer id/pre_image_dir/, s3://gbd-customer-data/unique customer id/post_image_dir/).
Each output directory will contain a single geotif file with one of the names: pre_image_cdprep.tif or post_image_cdprep.tif.


Name        | Required             |       Default         |        Valid Values             |   Description
------------|-------------|:---------------------:|---------------------------------|-----------------
final_pre_image_dir |  Yes    |N/A | S3 URL | Pre-image output directory for cd_prep
final_post_image_dir | Yes     |N/A | S3 URL | Post-image output directory for cd_prep 



[Contact Us](#contact-us) If your Customer has questions regarding required inputs,
expected outputs and [Advanced Options](advanced-options).

### Advanced Options

The options in the following table provide additional control over the resulting output.  All of the directories are generally
for diagnostic purposes.

Name                     |       Default         |        Valid Values             |   Description
-------------------------|:---------------------:|---------------------------------|-----------------
buffer_in_meters   |   1500.0  |  string | Amount in meters by which to buffer the intersection polygon of the initial crop
resampling_method   |   near  |  string | Method for resampling the images to a common grid.  Choices are 'near', 'bilinear', 'cubic', 'cubicspline', 'lanczos', 'average' 
resolution_in_meters   |   2.0  |  string | The resolution in meters of the pair of output images
enable_cloud_mask   |   true |  string | Enable/disable cloud mask. Choices are 'true' or 'false'
shrink_buffer_in_meters   |   0.0  |  string | Distance in meters by which to shrink the final intersection polygon for final crop
crop_pre_image_dir | N/A | S3 URL | Pre-image output directory for the cropping task (for diagnostic purposes)
crop_post_image_dir | N/A | S3 URL | Post-image output directory for the cropping task (for diagnostic purposes)
crop_work_dir | N/A | S3 URL | Working output directory for the initial cropping task (for diagnostic purposes)
crop_log_dir | N/A | S3 URL | Log output directory for the initial cropping task (for diagnostic purposes)
image2image_dir | N/A | S3 URL | Log output directory for the image2image task (for diagnostic purposes)

#### Advanced Script

This script runs the Advanced Image Preprocessor and Change Detection Preparation end to end.  Note that you must write the output from the Advanced Image Preprocessor to a file which the Change Detection Preparation task will read.

```python
# Runs the Advanced Image Preprocessor end to end with Change Detection Preparation Task
# This example uses the posted data from India.
from gbdxtools import Interface
gbdx = Interface()

#Edit the following path to reflect a specific path to an image
data1 = "s3://receiving-dgcs-tdgplatform-com/054661384050_01_003" # Hyderabad GE01
data2 = "s3://receiving-dgcs-tdgplatform-com/055775971010_01_003" # Hyderabad WV03

# Run the Advanced Image Preprocessor
aoptask1 = gbdx.Task("AOP_Strip_Processor", data=data1, enable_acomp=True, enable_pansharpen=False, enable_dra=False, bands='MS', ortho_epsg="UTM")
aoptask2 = gbdx.Task("AOP_Strip_Processor", data=data2, enable_acomp=True, enable_pansharpen=False, enable_dra=False, bands='MS', ortho_epsg="UTM")

# Edit the following path to reflect a specific path to an image
data1A = "s3://gbd-customer-data/full path to customer's s3 bucket containing preprocessed imagery"
data2A = "s3://gbd-customer-data/full path to customer's s3 bucket containing preprocessed imagery"

# The data input and lines must be edited to point to an authorized customer S3 location)
cd_preptask = gbdx.Task('cd_prep', pre_image_dir=data1A, post_image_dir=data2A)
    
workflow = gbdx.Workflow([ aoptask1, aoptask2, cd_preptask ])
    
# Edit the following line(s) to reflect specific folder(s) for the output file (example location provided)
workflow.savedata(aoptask1.outputs.data, location='path to customers3 bucket for preprocessed imagery/')
workflow.savedata(aoptask2.outputs.data, location='path to customer s3 bucket for preprocessed imagery/')
workflow.savedata(cd_prep_test.outputs.final_pre_image_dir, location='customer final output directory/end2end/GE01_Hyderabad/pre/')
workflow.savedata(cd_prep_test.outputs.final_post_image_dir, location='customer final output directory/end2end/WV03_Hyderabad/post/')

workflow.execute()

print workflow.id
print workflow.status

```


### Runtime

Runtime is a function of the overlap region between the two images.  The following table lists applicable runtime outputs.
For details on the methods of testing the runtimes of the task visit the following link:(INSERT link to GBDX U page here)
(TBD: need info on how to do this.  Is GBDX overhead included or just the CPU runtime for the individual tasks?)

  CatId Pair  |  Total Pixels within Overlap |  Total Area of Overlap (k2)  |  Time(secs)  |  Time/Area k2
--------|:----------:|-----------|----------------|---------------
1040010004D5AD00 105041001259EA00|###|###| ### | ### |


###Known Issues

* The Change Detectio Preparation task only processes multispectal images (MS) and UTM projrcted images. Make sure the [Advanced Image Preprocessing](https://github.com/TDG-Platform/docs/blob/master/Advanced_Image_Preprocessor.md) step is set to bands="MS" and ortho_epsg="UTM" (most common reasons for failure).
* You should also be aware of the following:
    * See issues for [Pairwise Image Registration](https://github.com/TDG-Platform/docs/blob/master/Pairwise_Image_Registration.md): fails if not enough tie points (<20).
    * See issues for the [8-Band Cloud Mask](https://github.com/TDG-Platform/docs/blob/master/protogenV2RAC.md)



### Contact Us
Tech Owners: [Jeff Collins](#jcollins@digitalglobe.com), [Carsten Tusk](#ctusk@digitalglobe.com)

Document Owner: [Kathleen Johnson](#kajohnso@digitalglobe.com)
