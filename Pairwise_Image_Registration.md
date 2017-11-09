# Pairwise Image Registration (image2image)

The Pairwise Image Registration task will remove misregistrations between two images.  It does so by attempting to find similar image features and warping the source image accordingly.  The warped source will have the same metadata as the source and be output with the suffix “_warped” appended to the original filename.


### Table of Contents
 * [Quickstart](#quickstart) - Get started!
 * [Inputs](#inputs) - Required and optional task inputs.
 * [Technical Notes](#technical-notes) - Detailed Description of Inputs
 * [Outputs](#outputs) - Task outputs and example contents.
 * [Advanced Options](#advanced-options) - Example Setting Tiepoints and Warping Boundaries
 * [Known Issues](#known-issues)
 * [Contact Us](#contact-us)

### Quickstart

This script uses the Pairwise Image Registration task to co-register two images.  The source image will be registered to the reference image and output to the specified directory.

```python
# Quickstart Example running the task name.

# Initialize the Environment.
from os.path import join, split
from gbdxtools import Interface
gbdx = Interface()

tasks = []
output_location = 'Digital_Globe/Image2Image/task'

# Change Detection task setup
im2im_task = gbdx.Task('image2image')
pre_cat_id = '10504100003E9200'
post_cat_id = '103001001C423600'

# Pre-Image Auto ordering task parameters
pre_order = gbdx.Task("Auto_Ordering")
pre_order.inputs.cat_id = pre_cat_id
pre_order.impersonation_allowed = True
pre_order.persist = True
pre_order.timeout = 36000
tasks += [pre_order]

# Pre-Image AOP task parameters
pre_aop = gbdx.Task("AOP_Strip_Processor")
pre_aop.inputs.data = pre_order.outputs.s3_location.value
pre_aop.outputs.data.persist = True
pre_aop.outputs.data.persist_location = output_location+'/pre_aop'
pre_aop.timeout = 36000
tasks += [pre_aop]

# Post-Image Auto ordering task parameters
post_order = gbdx.Task("Auto_Ordering")
post_order.inputs.cat_id = post_cat_id
post_order.impersonation_allowed = True
post_order.persist = True
post_order.timeout = 36000
tasks += [post_order]

# Post-Image AOP task parameters
post_aop = gbdx.Task("AOP_Strip_Processor")
post_aop.inputs.data = post_order.outputs.s3_location.value
post_aop.outputs.data.persist = True
post_aop.outputs.data.persist_location = output_location+'/post_aop'
post_aop.timeout = 36000
tasks += [post_aop]

# Get Image acquisition ID's for subdirectory in AOP
pre_acq_id = split(gbdx.catalog.get_data_location(pre_cat_id))[-1][:15]
post_acq_id = split(gbdx.catalog.get_data_location(post_cat_id))[-1][:15]

# Add Pairwise Image Registration task parameters
im2im_task.inputs.source_directory = join('s3://gbd-customer-data', gbdx.s3.info['prefix'], pre_aop.outputs.data.persist_location, pre_acq_id)
im2im_task.inputs.reference_directory = join('s3://gbd-customer-data', gbdx.s3.info['prefix'], post_aop.outputs.data.persist_location, post_acq_id)
tasks += [im2im_task]

# Set up workflow save data
workflow = gbdx.Workflow(tasks)
workflow.savedata(im2im_task.outputs.out, location=output_location + '/im2im')

# Execute workflow
workflow.execute()
```


          
### Inputs:

Name      |     Required          |       File Type       |   Description
--------------|:-----------|:---------------------:|---------------------------------
source_directory    | YES     |  directory   | S3 location of the Image that is layer to be warped
source_filename   | NO  |  geotiff     | source file must be set in the task command line if both files are located in the same directory    
reference_directory  | YES    |  directory   | S3 location of the Image that is the base layer
reference_filename  | NO |  geotiff     | reference file must be set in the task command line if both files are located in the same directory
boundary_directory   |  NO |  directory   | S3 location of the all the input data; only required if there is a boundary shapefile 
boundary_filename  |  NO |  shapefile   | file that limits the areal extent of the image warping (optional)

#### Technical Notes
*  Images should both be north up
*  Images with different number of bands will use blue band.  The following formats are assumed, but the program should work regardless.
  * PAN
  * RGB
  * BGRN (Includes GeoEye-1, IKONOS and QuickBird)
  * WV2 8 band
  * WV3 16 band
*  Images with different resolutions
  * Code uses coarsest resolution for tiepoints
  * Higher resolution image resampled using bilinear interpolation (just to find tiepoints)
*  Datatype
  * Input datatype can be byte, int, or float
  * Working arrays are scaled to unsigned 8 bit
  * Supports TIFFs (and vrts of TIFFs)
*  Images must be same projection
*  Images must fit in memory
*  There is a 200 pixel search radius in the coarser of the two resolutions.
*  Supports up to a factor of 25 resolution difference


### Outputs:
The Pairwaise Image Registration task outputs the warped source image that is registered to the reference image.

The warped source will be placed in the output s3 bucket.  This tiff image will have the same metadata as the source.  It will be output with the suffix “_warped” appended to the original filename.

### Advanced Options:

This Advanced Option permits the Customer to:
* input the source image and the reference image from the same directory
* use a boundary polygon (shapefile format) that selects the region from which tiepoints are selected; and thereby defines the extent of the image that is warped. 


```python
    
    from gbdxtools import Interface
    from os.path import join
    import uuid
    gbdx = Interface()

    # set my s3 bucket location:
    my_bucket = 's3://gbd-customer-data/acct#'

    # create task object
    im2im_task = gbdx.Task('image2image')

    # set the values of source_directory, reference_directory
    im2im_task.inputs.source_directory = join(my_bucket,'short path to source image directory')
    im2im_task.inputs.reference_directory = join(my_bucket,'short path to reference image directory')
	
    # set the image filenames in case there are multiple image files in a directory
    # note that the filenames do not include a filepath
    im2im_task.inputs.reference_filename = 'the reference image filename with extension'
    im2im_task.inputs.source_filename = 'the source image filename with extension'
	
    # assuming we are using a boundary polygon, we similarly set the boundary directory and the boundary filename 
    im2im_task.inputs.boundary_directory = join(my_bucket,'short path to boundary polygon shapefile directory')
    im2im_task.inputs.boundary_filename = 'the boundary polygon shapefile filename with .shp extension'
	
    # put the task in a workflow
    workflow = gbdx.Workflow([im2im_task])

    # save the data to an output location of your choice
    workflow.savedata(im2im_task.outputs.out, location='path to customer S3 output directory')

    # Execute the Workflow
    workflow.execute()
    print workflow.id
    print workflow.status

```

### Known Issues
Pairwise Image Registration has been certified for source image strips and mosaics up to 12 GB in size registered to a reference image of similar size. You may encounter a limit on the size of the image that can be processed for Mosaics larger than 12 GB, because the AWS system may time out. If you wish to process an image >12 GB please contact us.

### Contact Us
Tech Owner: [Mike Aschenbeck](#michael.aschenbeck@digitalglobe.com) & Editor:  [Kathleen Johnson](#kathleen.johnsons@digitalglobe.com)
