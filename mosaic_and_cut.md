## Mosaic-And-Cut GBDX Task 

This document shows how to call the Mosaic-And-Cut GBDX Task within the context of a GBDX Workflow. This task builds a virtual mosaic (VRT file) from the Tiff images in a target directory, chips that mosaic with the Tiff image that's in the source directory, clips the target chip and source image to the common overlap with the mosaic, and outputs both the target chip and the clipped source image. The target images are all assumed to be all of the same resolution, but are not assumed to be of the same resolution as the source image. The output target mosaic chip represents a nearest-neighbour resampling of the target images.

Depth 1

NOTE: Even if the source image and target images are of the same resolution and pixel alignment, you cannot assume that teh output target chip and the output clipped source image are of identical extent. The two extents may differ by a pixel. If you need teh resulting image sto be the same extent, same resolution, and row-column dimension, then a subsequent call to teh the Resample-And-Cut GBDX task is required. 

of source Tiff image to the pixel centers of a target Tiff image, clips the target image and the resampled source image to the common overlap, and outputs the two clipped images.  

<!--
***************************************************************************
-->

**_Resample-And-Cut Workflow:_** 

```shell
import os
from gbdxtools import Interface
gbdx = Interface()

# NOTE: Make sure these directory strings have the trailing "/" as shown
in_base_dir = "s3://xxxxxxxxxxxxx/"
out_base_dir = "s3://xxxxxxxxxxxxx/"

####### INPUTS ######
source_dir = os.path.join(in_base_dir, "XXXXXXX/")
target_dir = os.path.join(in_base_dir, "XXXXXXX/")

####### OUTPUTS #######
out_mc_source_dir = os.path.join(out_base_dir, "MC_SOURCE")
out_mc_target_dir = os.path.join(out_base_dir, "MC_TARGET")

########################################################

mc_task = gbdx.Task("mosaic_and_cut", 
                    input_A = source_dir, 
                    input_B = target_dir, 
                    prefixLen = '31',
                    osuffA = 'CUT',
                    osuffB = 'MC')

# Name EC2 directories
mc_source_dir = mc_task.outputs.out_A.value
mc_target_dir = mc_task.outputs.out_B.value

save_mc_source_task = gbdx.Task("StageDataToS3",
                           data = mc_source_dir,
                           destination = out_mc_source_dir)

save_mc_target_task = gbdx.Task("StageDataToS3",
                           data = mc_target_dir,
                           destination = out_mc_target_dir)

##########################################################
workflow = gbdx.Workflow([mc_task,
                          save_mc_source_task,
                          save_mc_target_task])

workflow.execute()
print workflow.id
```

<!--
***************************************************************************
-->

The **_prefixLen_** port indicates how many characters of the input source file name will be 
used in both the output target chip file name and the output clipped source file name. 
If the value is set to '0', then none of the input source file name will be used. If the value 
is set to a large number (e.g., '250'),then all of the input source file name will be used. 
Set this port as desired.

The **_osuffA_** port indicates the file name suffix that will be used for the output clipped source.
Set this port as desired.

The **_osuffB_** port indicates the file name suffix that will be used for the output clipped target image.
Set this port as desired.

Batch Mode: The input source directory is allowed to contain multiples images. (It is already assumed the 
input target directory contains one or more images). In this case, each source image will be used to chip the 
virtual mosaic. This source images will be processed in parallel.

The other modifications you need to make to run the workflow are as follows:
 
* Set **_in_base_dir_** -- this is the top-level S3 input directory that contains your input data 
* Set **_out_base_dir_** -- this is the top-level S3 output directory
* Set **_source_dir_** -- this is the s3 directory containing the source image(s)
* Set **_target_dir_** -- this is the s3 directory containing the target image(s)





















