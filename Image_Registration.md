# Image Registration (image2image)

The Image Registration task will remove misregistrations between two images.  It will attempt to find similar image features that are misregistered by up to 200 pixels and warp the source image accordingly.  There is also an option to specify a warp boundary via a polygon shapefile.  In this case, there is a full warp nested inside the boundary and no warp outside the boundary, with a smooth transition in between.  The warped source will have the same metadata as the source and be output with the suffix “warped” appended to the original filename.

### Table of Contents
 * [Quickstart](#quickstart) - Get started!
 * [Inputs](#inputs) - Required and optional task inputs.
 * [Technical Notes](#technical-notes) - Detailed Description of Inputs
 * [Outputs](#outputs) - Task outputs and example contents.
 * [Contact Us](#contact-us)

### Quickstart

This script uses the Image Registration task to produce co-registered images that are in separate directories.  If both images are in the same directory, then the source_filename and reference filename of the tifs must be added to the script.

```python
   	from gbdxtools import Interface
	from os.path import join
	import uuid
	gbdx = Interface()
	
	# set my s3 bucket location:
	my_bucket = 's3://gbd-customer-data/acct#'
	
	# create task object
	im2im_task = gbdx.Task('image2image_1_2_0')
	
	# set the values of source_directory, reference_directory
	# if the images are in the same directory, you must include the tif file name.  See Input options below.
	im2im_task.inputs.source_directory = join(my_bucket,'short path to source image directory')
	im2im_task.inputs.reference_directory = join(my_bucket,'short path to reference image directory')
	im2im_task.inputs.boundary_directory = join(my_bucket,'directory-name')
	im2im_task.inputs.boundary_filename =  'customer_boundary.shp' # optional
	
	# put the task in a workflow
	workflow = gbdx.Workflow([im2im_task])
	
	# save the data to an output_location of your choice
	workflow.savedata(im2im_task.outputs.out, location='path to customer S3 output directory')
	
	# Execute the Workflow
	workflow.execute()
	print workflow.id
	print workflow.status
```


          
### Inputs:

Name      |     Required          |       File Type       |   Description
--------------|:-----------|:---------------------:|---------------------------------
source_directory    | YES     |  directory   | S3 location of the Image that provides the base layer for warping
source_filename   | NO  |  geotiff     | source file must be set in the task command line if both files are located in the same directory    
reference_directory  | YES    |  directory   | S3 location of the Image that will be warped
reference_filename  | NO |  geotiff     | reference file must be set in the task command line if both files are located in the same directory
boundary_directory   |  NO |  directory   | S3 location of the all the input data; only required if there is a boundary shapefile 
boundary_filename  |  NO |  shapefile   | file that limits the areal extent of the image warping (optional)

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
*  There is a 200 pixel search radius in the coarser of the two resolutions
*  Supports up to a factor of 25 resolution difference



### Output:
RADWarp outputs the warped source image that is registered to the reference image.

The warped source will be placed in the output s3 bucket.  This tiff image will have the same metadata as the source.  It will be output with the suffix “warped” appended to the original source filename.


### Contact Us
Tech Owner: [Mike Aschenbeck](#michael.aschenbeck@digitalglobe.com) & Editor:  [Kathleen Johnson](#kathleen.johnson@digitalglobe.com)
