# Image2Image (Prelim Vesrion)
Image de-shearing and registration

# Inputs:
1. Source image s3 directory, *source_directory*, that will be warped.
2. OPTIONAL source image filename, *source_filename*, if there are multiple images in the source directory.
3. Reference image s3 directory, *reference_directory*, which the source will be registered to.
4. OPTIONAL reference image filename, *reference_filename*, if there are multple images in the reference directory.
5. OPTIONAL boundary shapefile s3 directory, *boundary_directory*, to be used as the warp boundary.
6. OPTIONAL boundary shapefile name, *boundary_filename*, if there are multiple shapefiles in the boundary directory.

# Output:
The warped source

# Example GBDX Run with Postman:
The following example will warp "test_01ss.tif" to "test_02ss.tif" inside the "right_boundary.shp" shapefile. Just paste it into a JSON file and submit it to GBDX via postman.  Note that the source and reference are in the same directory so we must use *source_filename* and *reference_filename* to explicitly specify which files to use. 

    {
        "name": "test_im2im_workflow",
        "tasks": [
            {
                "name": "im2im_task_test",
                "outputs": [
                    {
                        "name": "out"
                    }
                ],
                "inputs": [
                    {
                        "name": "source_directory",
                        "value": "s3://gbd-customer-data/596bd3ed-ffad-496f-9394-291648fb8250/small/"
                    },
                    {
                    	"name": "source_filename",
                    	 "value": "test2_01.tif"
                    },
                    {
                        "name": "reference_directory",
                        "value": "s3://gbd-customer-data/596bd3ed-ffad-496f-9394-291648fb8250/small/"
                    },
                    {
                    	"name": "reference_filename",
                    	"value": "test2_02.tif"
                    },
                    {
                    	"name": "boundary_directory",
                    	"value": "s3://gbd-customer-data/596bd3ed-ffad-496f-9394-291648fb8250/small/"
                    },
                    {
                    	"name": "boundary_filename",
                    	"value": "right_boundary.shp"
                    }
                ],
                "taskType": "image2image_1_2_0"
            },
            {
                "name": "StagetoS3",
                "inputs": [
                    {
                        "name": "data",
                        "source": "radwarp_task_test:out"
                    },
                    {
                        "name": "destination",
                        "value": "s3://gbd-customer-data/596bd3ed-ffad-496f-9394-291648fb8250/outSmallTest"
                    }
                ],
                "taskType": "StageDataToS3"
            }
        ]
    }

# Example GBDX Run with the Python GBDX Task Interface:
The following example is an identical run to the previous example but uses GBDX Task Interface within python.  Here is the python code:

	from gbdxtools import Interface
	from os.path import join
	import uuid
	gbdx = Interface()
	
	# set my s3 bucket location:
	my_bucket = 's3://gbd-customer-data/596bd3ed-ffad-496f-9394-291648fb8250/'
	
	# create task object
	radwarp_task = gbdx.Task('image2image_1_2_0')
	
	# set the values of source_directory, reference_directory
	radwarp_task.inputs.source_directory = join(my_bucket,'WarpTest/Desert/im1/')
	radwarp_task.inputs.reference_directory = join(my_bucket,'WarpTest/Desert/im2/')
	radwarp_task.inputs.boundary_directory = join(my_bucket,'WarpTest/Desert/')
	radwarp_task.inputs.boundary_filename =  'nonconvex.shp'
	
	# put the task in a workflow
	workflow = gbdx.Workflow([radwarp_task])
	
	# save the data to an output_location of your choice
	output_location = 'Output/DesertRun'
	workflow.savedata(radwarp_task.outputs.out, output_location)
	
	# execute
	workflow.execute()
	

# Running Your Own:
1. Make sure you have postman set up properly with a current access key.  Also, have your source image, reference image, and optional shapefile stored in an s3 bucket.

2. Name your workflow.  In the example above, replace "test_im2im_workflow" with whatever you want to use as your workflow name.

3. Name your image2image task.  In the example above, replace "im2im_task_test" with your the task name you want to use.

4. Identify which image you want to use as the source and which one you want to use as the reference.  Modify the "Inputs" object to reflect this as follows:
    1. Specify the s3 directory of the source image as the value to the name *source_directory*.  In the above example, you will remove "s3://gbd-customer-data/596bd3ed-ffad-496f-9394-291648fb8250/small/" and replace it with the full path to your source file.
    2. Repeat for the *reference_directory* key.
    3. Set the *source_filename* to be the name of the file if there are multiple images in *source_directory*.  In the above example, this value is set as "test2_01.tif"
    4. Repeat for the *reference_filename* key if necessary.
    5. Optionally set the *boundary_directory* key to be the s3 directory containing your shapefile similarly to step 4.1
    6. If you specified a *boundary_directory* and there are multiple boundary files in that directory, set the *boundary_filename* value as the shapefile name you're using.similarly to step 4.3.


6. The second task in the example workflow stages the output to an s3 bucket.  Make sure the "source" key's value matches the image2image task from part 3.  Also modify the destination to be an s3 location of your choice.  The example above puts the output in the following location: "s3://gbd-customer-data/596bd3ed-ffad-496f-9394-291648fb8250/small/outSmallTest".

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
*  There is a 20 pixel (in the coarser resolution) search radius (reduced to 5 if factor of five resolution difference)
  *  No warping beyond this radius
*  Supports up to a factor of 5 resolution difference

