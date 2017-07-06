#  Urban Change Detection (urban_change)

The urban_change GBDX library task performs change detection of builtup areas.  It takes as input a pair of overlapping 1b images and outputs the urban change
as a collection of polygons.  The processing includes ACOMP/FastOrtho (via 
the [Advanced Image Preprocessor](#https://github.com/TDG-Platform/docs/blob/master/Advanced_Image_Preprocessor.md)), image/grid alignment, cloud detection and cropping (via
workflow equivalent to [Change Detection Preparation](#https://github.com/TDG-Platform/docs/blob/master/Change_Detection_Preparation.md)) and urban change detection (via urban_change_task). 

### Table of Contents
 * [Quickstart](#quickstart) - Get started!
 * [Inputs](#inputs) - Required and optional task inputs.
 * [Outputs](#outputs) - Task outputs and example contents.
 * [Advanced Options](#advanced-options) - Examples linking to a second task and running VNIR+SWIR
 * [Known Issues](#known-issues)

### Quickstart

The urban_change GBDX task can be run using [gbdxtools](https://github.com/DigitalGlobe/gbdxtools/blob/master/docs/user_guide.rst) Python module, which requires some initial setup.
Tasks and workflows can be added (described here in [gbdxtools](https://github.com/DigitalGlobe/gbdxtools/blob/master/docs/running_workflows.rst))  or run separately after the urban_change process is completed.

**Example Script:** These basic settings will run urban_change from a pair of paths to 1b images.
See also examples listed under the [Advanced Options](#advanced-options).

```python
# Run urban_change on a pair of images

from gbdxtools import Interface
gbdx = Interface()

urban_change = gbdx.Task('urban_change', 
                        pre_image_dir='s3://receiving-dgcs-tdgplatform-com/056194460010_01_003',
                        post_image_dir='s3://receiving-dgcs-tdgplatform-com/056194461010_01_003')

workflow = gbdx.Workflow([urban_change])

#Edit the following line(s) to reflect specific folder(s) for the output file (example location provided)
workflow.savedata(urban_change.outputs.results_dir, location='UrbanChange/test1/Results')

workflow.execute()

print workflow.id
print workflow.status
```

**Example Run in IPython:**

    In [1]: from gbdxtools import Interface
    In [2]: gbdx = Interface()
    In [3]: urban_change = gbdx.Task('urban_change', 
                        pre_image_dir='s3://receiving-dgcs-tdgplatform-com/056194460010_01_003',
                        post_image_dir='s3://receiving-dgcs-tdgplatform-com/056194461010_01_003')
    In [4]: workflow = gbdx.Workflow([urban_change])
    In [5]: workflow.savedata(urban_change.outputs.results_dir, location='UrbanChange/test1/Results')    
    In [6]: workflow.execute()
    Out [6]: 
    u'4507220531957672228'
    In [7]: print workflow.status
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
bounding_rectangle    | ??  |   N/A  |  ULx, ULy, LRx, LRy (latlon) | Subregion (specified using bounding box coordinates) within the image pair overlap to process
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

TBD -- we have exposed many options, only a few of which will be eventually be retained

### Runtime

Runtime is a function of the size of the overlap region between the two images.  The following table lists applicable runtime outputs.
For details on the methods of testing the runtimes of the task visit the following link:(INSERT link to GBDX U page here)
(TBD: need info on how to do this.  Is GBDX overhead included or just the CPU runtime for the individual tasks?)

  CatId Pair  |  Total Pixels within Overlap |  Total Area of Overlap (k2)  |  Time(secs)  |  Time/Area k2
--------|:----------:|-----------|----------------|---------------
1030010005850300 1030010018700D00|###|###| ### | ### |




###Known Issues###

The Urban Change Task automatically inputs the appropriate settings for the four sub-tasks in the workflow library as listed below.  Refer to the documentation for those tasks for further details:

*	The Change Detection Preparation task only processes multispectral images (MS) and UTM projected images. 

*	The Advanced Image Preprocessor is run automatically with the appropriate settings.

*	The Pairwise Image Registration Task; fails if not enough tie points (<20).

*	The Cloud and Shadow Mask applied here sometimes confuses water and shadow. No documentation is available for this Task.


### Contact Us
Tech Owners: [Jeff Collins](#jcollins@digitalglobe.com), [Carsten Tusk](#ctusk@digitalglobe.com)

Document Owner: [Kathleen Johnson](#kathleen.johnson@digitalglobe.com)
