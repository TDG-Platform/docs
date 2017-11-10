# Change Detection Preparation (cd_prep)

The Change Detection Preparation task performs a series of operations on a pair of input images to prepare them for the application of downstream change detection algorithms.  It accomplishes this via the following operations:

    1. Initial crop of the input images to their region of overlap  
    2. Image-to-image registration
    3. Alignment of the images to a common grid, cloud removal and final cropping

The input imagery for this task is two multispectral orthorectified, atmospherically compensated images in geotiff format and UTM projection from the [Advanced Image Preprocessor](https://github.com/TDG-Platform/docs/blob/master/Advanced_Image_Preprocessor.md).

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

**Example Script:** These settings will run CDPrep from a pair of input orthorectified, AComped image output from the Advanced Image Preprocessor.

```python
# Quickstart Example running the task name.

# Initialize the Environment.
from gbdxtools import Interface
gbdx = Interface()

tasks = []
output_location = 'Digital_Globe/Change_Detection/task'

# Change Detection task setup
cd_prep_task = gbdx.Task('cd_prep')

# Pre-Image Auto ordering task parameters
pre_order = gbdx.Task("Auto_Ordering")
pre_order.inputs.cat_id = '10504100003E9200'
pre_order.impersonation_allowed = True
pre_order.persist = True
pre_order.timeout = 36000
tasks += [pre_order]

# Pre-Image AOP task parameters
pre_aop = gbdx.Task("AOP_Strip_Processor")
pre_aop.inputs.data = pre_order.outputs.s3_location.value
pre_aop.inputs.bands = 'MS'
pre_aop.inputs.enable_pansharpen = False
pre_aop.inputs.enable_dra = False
pre_aop.inputs.ortho_epsg = "UTM"
pre_aop.timeout = 36000
tasks += [pre_aop]

# Post-Image Auto ordering task parameters
post_order = gbdx.Task("Auto_Ordering")
post_order.inputs.cat_id = '103001001C423600'
post_order.impersonation_allowed = True
post_order.persist = True
post_order.timeout = 36000
tasks += [post_order]

# Post-Image AOP task parameters
post_aop = gbdx.Task("AOP_Strip_Processor")
post_aop.inputs.data = post_order.outputs.s3_location.value
post_aop.inputs.bands = 'MS'
post_aop.inputs.enable_pansharpen = False
post_aop.inputs.enable_dra = False
post_aop.inputs.ortho_epsg = "UTM"
post_aop.timeout = 36000
tasks += [post_aop]

# Add Change Detection task parameters
cd_prep_task.inputs.pre_image_dir = pre_aop.outputs.data.value
cd_prep_task.inputs.post_image_dir = post_aop.outputs.data.value
tasks += [cd_prep_task]

# Set up workflow save data
workflow = gbdx.Workflow(tasks)
workflow.savedata(cd_prep_task.outputs.final_pre_image_dir, location=output_location + "/pre")
workflow.savedata(cd_prep_task.outputs.final_post_image_dir, location=output_location + "/post")

# Execute workflow
workflow.execute()
```

### Inputs

This task takes as input two orthorectified, atmospherically compensated images in geotiff format.
It is intended to work as a following task to the AOP_Strip_Processor, with only the AComp option specified.

Example overlapping 1B images that can be processed by Advanced Image Preprocessor prior Change Detection Preparation are:

    pre-image: 10504100003E9200
    post-image: 103001001C423600

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


### Runtime

Runtime is a function of the overlap region between the two images.  The following table lists applicable runtime outputs for the example pair using the Quickstart script.
For details on the methods of testing the runtimes of the task visit the following link:(INSERT link to GBDX U page here)
(TBD: need info on how to do this.  Is GBDX overhead included or just the CPU runtime for the individual tasks?)

  CatId Pair  |  Total Pixels within Overlap |  Total Area of Overlap (k2)  |  Time(secs)  |  Time/Area k2
--------|:----------:|:-----------:|:----------------:|:---------------:
1040010004D5AD00 105041001259EA00|315,701,538|1168.27| 1347.00 | 1.15 |


### Known Issues

* The Change Detection Preparation task only processes multispectal images (MS) and UTM projrcted images. Make sure the [Advanced Image Preprocessing](https://github.com/TDG-Platform/docs/blob/master/Advanced_Image_Preprocessor.md) step is set to bands="MS" and ortho_epsg="UTM" (most common reasons for failure).
* The output from the Advanced Image Preprocessor must be written to a directory for use by this task.  You cannot use "aop.outputs.data.value" as input.
* You should also be aware of the following:
    * See issues for [Pairwise Image Registration](https://github.com/TDG-Platform/docs/blob/master/Pairwise_Image_Registration.md): fails if not enough tie points (<20).
    * The Cloud and Shadow Mask applied here sometimes confuses water and shadow.


### Contact Us
Tech Owners: [Jeff Collins](#jcollins@digitalglobe.com), [Carsten Tusk](#ctusk@digitalglobe.com)

Document Owner: [Kathleen Johnson](#kajohnso@digitalglobe.com)
