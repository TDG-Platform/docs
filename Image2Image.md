# Image2Image (RADWarp)

The image2image task will remove misregistrations between two images.  It will attempt to find similar image features that are misregistered by up to 20 pixels and warp the source image accordingly.  There is also an option to specify a warp boundary via a polygon shapefile.  In this case, there is a full warp nested inside the boundary and no warp outside the boundary, with a smooth transition in between.  The warped source will have the same metadata as the source and be output with the suffix “_radwarp” appended to the original filename.

### Table of Contents
 * [Quickstart](#quickstart) - Get started!
 * [Inputs](#inputs) - Required and optional task inputs.
 * [Technical Notes](#technical-notes) - Detailed Description of Inputs
 * [Outputs](#outputs) - Task outputs and example contents.
 * [Known Issues](#known-issues)
 * [Contact Us](#contact-us)

### Quickstart

This script uses Image2Image to produce co-registered images from the test dataset:

    # Image2Image Test Dataset
    from gbdxtools import Interface
    gbdx = Interface()
    import json
    
    source_data = "s3://gbd-customer-data/596bd3ed-ffad-496f-9394-291648fb8250/small/test_01ss.tif"
    reference_data = "s3://gbd-customer-data/596bd3ed-ffad-496f-9394-291648fb8250/small/test_02ss.tif"
    boundary_directory = "s3://gbd-customer-data/596bd3ed-ffad-496f-9394-291648fb8250/small"

    im2imtask = gbdx.Task('image2image', source_data=source_data, reference_data=reference_data, 
	    boundary_directory=boundary_directory, source_filename='test_01ss.tif', 
	    reference_filename='test_02ss.tif', boundary_filename='right_boundary')

    workflow = gbdx.Workflow([ im2imtask ])

    workflow.savedata(im2imtask.outputs.out, location='S3 gbd-customer-data location')
    workflow.execute()

    print workflow.id
    print workflow.status


#### Test Datasets:
Sensor                   |       CATID           |   S3 URL
-------------------------|:---------------------:|---------------------------------
Comming Soon             |                      |
     
     
     
### Inputs:

Name                     |       File Type       |   Description
-------------------------|:---------------------:|---------------------------------
source_data         |  directory   | S3 location of the Image that provides the base layer for warping
source_filename     |  geotiff     | source file must be set in the task command line
reference_data      |  directory   | S3 location of the Image that will be warped
reference_filename  |  geotiff     | reference file must be set in the task command line
boundary_directory  |  directory   | S3 location of the all the input data; only required if there is a boundary shapefile 
boundary_filename   |  shapefile   | file that limits the areal extent of the image warping

#### Technical Notes
*  Images should both be north up
*  Images with different number of bands will use blue band.  The following formats are assumed, but the program should work regardless.
  * PAN
  * RGB
  * BGRN
  * WV2 8 band
  * WV3 16 band
*  Images with different resolutions
  * Code uses coarsest resolution for tie points
  * Higher resolution image resampled using bilinear interpolation (just to find tie points)
*  Datatype
  * Input datatype can be byte, int, or float
  * Working arrays are scaled to unsigned 8 bit
  * Supports TIFFs (and vrts of TIFFs)
*  Images must be same projection
*  Images must fit in memory
*  There is a 20 pixel search radius (reduced to 5 if factor of five resolution difference)
  *  No warping beyond this radius
*  Supports up to a factor of 5 resolution difference



### Output:
RADWarp outputs the warped source image that is registered to the reference image.

The warped source will be placed in the output s3 bucket.  This tiff image will have the same metadata as the source.  It will be output with the suffix “_radwarp” appended to the original source filename.


### Contact Us
Tech Owner: [Mike Aschenbeck](#acomermichael.aschenbeck@digitalglobe.com) & Editor:  [Kathleen Johnson](#kathleen.johnsons@digitalglobe.com)
