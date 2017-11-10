#  Urban Change Detection (urban_change)

The urban_change GBDX library task performs change detection of builtup areas.  It takes as input a pair of overlapping 1b images and outputs the urban change
as a collection of polygons.  The processing includes ACOMP/FastOrtho (via 
the [Advanced Image Preprocessor](https://github.com/TDG-Platform/docs/blob/master/Advanced_Image_Preprocessor.md)), image/grid alignment, cloud detection and cropping (via
workflow equivalent to [Change Detection Preparation](https://github.com/TDG-Platform/docs/blob/master/Change_Detection_Preparation.md)) and urban change detection (via urban_change_task). 

### Table of Contents
 * [Quickstart](#quickstart) - Get started!
 * [Inputs](#inputs) - Required and optional task inputs.
 * [Outputs](#outputs) - Task outputs and example contents.
 * [Advanced Options](#advanced-options) 
 * [Known Issues](#known-issues)

### Quickstart

The Urban Change Detection GBDX task can be run using [gbdxtools](https://github.com/DigitalGlobe/gbdxtools/blob/master/docs/user_guide.rst) Python module, which requires some initial setup.
Tasks and workflows can be added (described here in [gbdxtools](https://github.com/DigitalGlobe/gbdxtools/blob/master/docs/running_workflows.rst))  or run separately after the urban_change process is completed.

**Example Script:** These basic settings will run Urban Change Detection from a pair of paths to 1b images.
See also examples listed under the [Advanced Options](#advanced-options).

```python
# Quickstart Example running the task name.

# Initialize the Environment.
from gbdxtools import Interface
gbdx = Interface()

tasks = []
output_location = 'Digital_Globe/Urban_Change/task'

# task parameters
uc_task = gbdx.Task('urban_change')

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

# Add Urban Change task parameters
uc_task.inputs.pre_image_dir = pre_aop.outputs.data.value
uc_task.inputs.post_image_dir = post_aop.outputs.data.value
tasks += [uc_task]

# Set up workflow save data
workflow = gbdx.Workflow(tasks)
workflow.savedata(uc_task.outputs.results_dir, location=output_location)

# Execute workflow
workflow.execute()

```

**Example Run in IPython:**

    In [1]: from gbdxtools import Interface
            gbdx = Interface()

            tasks = []
            output_location = 'Digital_Globe/Urban_Change/task'

    In [2]: uc_task = gbdx.Task('urban_change')

            pre_order = gbdx.Task("Auto_Ordering")
            pre_order.inputs.cat_id = '10504100003E9200'
            pre_order.impersonation_allowed = True
            pre_order.persist = True
            pre_order.timeout = 36000
            tasks += [pre_order]

            pre_aop = gbdx.Task("AOP_Strip_Processor")
            pre_aop.inputs.data = pre_order.outputs.s3_location.value
            pre_aop.inputs.bands = 'MS'
            pre_aop.inputs.enable_pansharpen = False
            pre_aop.inputs.enable_dra = False
            pre_aop.inputs.ortho_epsg = "UTM"
            pre_aop.timeout = 36000
            tasks += [pre_aop]

            post_order = gbdx.Task("Auto_Ordering")
            post_order.inputs.cat_id = '103001001C423600'
            post_order.impersonation_allowed = True
            post_order.persist = True
            post_order.timeout = 36000
            tasks += [post_order]

            post_aop = gbdx.Task("AOP_Strip_Processor")
            post_aop.inputs.data = post_order.outputs.s3_location.value
            post_aop.inputs.bands = 'MS'
            post_aop.inputs.enable_pansharpen = False
            post_aop.inputs.enable_dra = False
            post_aop.inputs.ortho_epsg = "UTM"
            post_aop.timeout = 36000
            tasks += [post_aop]

    In [3]: uc_task.inputs.pre_image_dir = pre_aop.outputs.data.value
            uc_task.inputs.post_image_dir = post_aop.outputs.data.value
            tasks += [uc_task]
            workflow = gbdx.Workflow(tasks)
            workflow.savedata(uc_task.outputs.results_dir, location=output_location)

    In [4]: workflow.execute()

    Out [5]:
    '4507220531957672228'
    In [6]: print workflow.status
    {u'state': u'running', u'event': u'started'}


### Inputs


**Description of Basic Input Parameters for the urban_change GBDX task**

The following table lists the urban_change GBDX inputs.
All inputs are optional with default values, with the exception of
'pre_image_dir' and 'post_image_dir',
which specify the task's input and output data locations.

Name        | Required             |       Default         |        Valid Values             |   Description
----------------|---------|:---------------------:|---------------------------------|-----------------
pre_image_dir   | Yes   | N/A  |  S3 URL | Pre-image input directory containing one or more 1b TIFF files
post_image_dir    | Yes   |   N/A  |  S3 URL | Post-image input directory containing one or more 1b TIFF files
cropping_rectangle    | No  |   N/A  |  ULx, ULy, LRx, LRy |Optional cropping rectangle in the form: ULX, ULY, LRX, LRY.  All in latlon coordinates (EPSG:4326)
enable_cloud_mask     | No   |   True  |  boolean | Enable/Disable the use of a cloudmask (default: true) 

### Outputs

On completion, the processed imagery will be written to your specified S3 Customer 
Location (i.e., s3://gbd-customer-data/unique customer id/<user supplied path>/Results). 

Name           |    Required      |       Default         |        Valid Values             |   Description
---------------|----------|:---------------------:|---------------------------------|-----------------
results_dir    | Yes      |  N/A      | customer's s3 bucket location | Contained in this directory are files of the name change_detection_latlon; with JSON, shapefile and zip (containing the shapefiles).


[Contact Us](#contact-us) If your Customer has questions regarding required inputs,
expected outputs and [Advanced Options](advanced-options).

### Advanced Options

The options in the following table provide additional diagnostic information. 


Name           |    Required      |       Default         |        Valid Values             |   Description
---------------|----------|:---------------------:|---------------------------------|-----------------
Work |  No     |  N/A | S3 URL | Output directory containing intermediate work files (for diagnostic purposes)
Log |  No   |  N/A | S3 URL | Output directory containing the runtime log (for diagnostic purposes)


### Known Issues ###

The Urban Change Task automatically inputs the appropriate settings for the four sub-tasks in the workflow library as listed below.  Refer to the documentation for those tasks for further details:

*	The Change Detection Preparation task only processes multispectral images (MS) and UTM projected images. 

*	The Advanced Image Preprocessor is run automatically with the appropriate settings.

*	The Pairwise Image Registration Task; fails if not enough tie points (<20).

*	The Cloud and Shadow Mask applied here sometimes confuses water and shadow. No documentation is available for this Task.


### Contact Us ###
Tech Owners: [Jeff Collins](#jcollins@digitalglobe.com), [Carsten Tusk](#ctusk@digitalglobe.com)

Document Owner: [Kathleen Johnson](#kathleen.johnson@digitalglobe.com)
