# Image2Image (RADWarp)

The image2image task will remove misregistrations between two images.  It will attempt to find similar image features that are misregistered by up to 20 pixels and warp the source image accordingly.  There is also an option to specify a warp boundary via a polygon shapefile.  In this case, there is a full warp nested inside the boundary and no warp outside the boundary, with a smooth transition in between.  The warped source will have the same metadata as the source and be output with the suffix “_radwarp” appended to the original filename.

### Table of Contents
 * [Quickstart](#quickstart) - Get started!
 * [Inputs](#inputs) - Required and optional task inputs.
 * [Outputs](#outputs) - Task outputs and example contents.
 * [Advanced Options](#advanced-options) - Examples linking to a second task and running VNIR+SWIR
 * [Known Issues](#known-issues)

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

     
### Inputs:
1. Source image that will be warped, staged in an s3 bucket: 'source_data'
2. Reference image which the source will be registered to, staged in an s3 bucket: 'reference_data'
3. OPTIONAL shapefile to be used as the warp boundary, staged in an s3 bucket: 'boundary_directory'

Name                     |       File Type       |   Description
-------------------------|:---------------------:|---------------------------------
source_data         |  directory   | S3 location of the Image that provides the base layer for warping
source_filename     |  geotiff     | source file must be set in the task command line
reference_data      |  directory   | S3 location of the Image that will be warped
reference_filename  |  geotiff     | reference file must be set in the task command line
boundary_directory  |  directory   | S3 location of the all the input data; only requiredt if there is a boundary shapefile 
boundary_filename   |  shapefile   | file that limits the areal extent of the image warping





4. Identify which image you want to use as the source and which one you want to use as the reference.  Modify the "Inputs" object to reflect this.
    1. Give the full s3 path to the source image as the value to the name "source_data".  In the above example, you will remove "s3://gbd-customer-data/596bd3ed-ffad-496f-9394-291648fb8250/small/test_01ss.tif" and replace it with the full path to your source file.
    2. Repeat for the "reference_data" key.
    3. Set the "source_filename" to be the name of the file.  This is equivalent to copying the filename in part (a) and using it for the "source_filename" value.
    4. Repeat for the "reference_filename" key.

5. If you want to only warp inside a boundary, make sure you have a polygon shapefile handy.  Find the directory where it resides in your s3 bucket, and modify the "boundary_directory" value in the example above.  i.e. remove "s3://gbd-customer-data/596bd3ed-ffad-496f-9394-291648fb8250/small" and replace it with the s3 location where your shapefile resides.  Also, modify the "boundary_filename" value "right_boundary" with your filename.  Do not include the extension.  For example, if your shapefile name is "CityBoundary.shp", only enter "CityBoundary".

6. The second task in the example workflow stages the output to an s3 bucket.  Make sure the "source" key's value matches the image2image task from part 3.  Also modify the destination to be an s3 location of your choice.  The example puts the output in the following location: "s3://gbd-customer-data/596bd3ed-ffad-496f-9394-291648fb8250/small/out".

7. Submit your workflow!

# Technical Notes
*  Images should both be north up
*  Images with different number of bands will use blue band.  The folling formats are assumed, but the program should work regardless.
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
The warped source
