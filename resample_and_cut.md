## Resample-And-Cut GBDX Task 

This document shows how to call the Resample-And-Cut GBDX Task within the context of a GBDX Workflow. This task resamples a source Tiff image to the pixel centers of a target Tiff image, clips the target image and resampled source image to the common overlap, and outputs the two clipped images.  

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
out_rc_vnir_dir = os.path.join(out_base_dir, "RC_SOURCE")
out_rc_swir_dir = os.path.join(out_base_dir, "RC_TARGET")

########################################################

rc_task = gbdx.Task("resample_and_cut_001",
                    input_A = source_dir,
                    input_B = target_dir,
                    nodata_A  = '0',
                    r_meth = 'dg_average', # or any of the resampling methods in gdalwarp for GDAL 2.0.0
                    prefixLen = '39',
                    osuffA = 'RC',
                    osuffB = 'CUT')

rc_source_dir = rc_task.outputs.out_A.value
rc_target_dir = rc_task.outputs.out_B.value

save_rc_source_task = gbdx.Task("StageDataToS3",
                              data = rc_source_dir,
                              destination = out_rc_source_dir)

save_rc_target_task = gbdx.Task("StageDataToS3",
                              data = rc_target_dir,
                              destination = out_rc_target_dir)

##########################################################
workflow = gbdx.Workflow([rc_task,
                          save_rc_source_task,
                          save_rc_target_task])

workflow.execute()
print workflow.id
```

<!--
***************************************************************************
-->

Regarding the above workflow:

The **_no_data_A_** port is set to the no-data value in the source image.
If there isn't a no-data value for the source image (i.e., you're expecting every pixel
is valid data) or you don't know what the no-data value is, then set the value 
to be some number that is not achievable in the source image (e.g., the value 2 is not 
achievable in a binary 0-1 or 0-255 image; the value -9999 is not achievable in an 
unsigned 16-bit image). Set this port as desired. 

The **_r_meth_** port is set to the desired resample method. This can be any of the 
resampling methods available in the gdalwarp command of GDAL 2.0.0, or you can set it to 'dg_average'.
The latter specifies DigitalGlobe's code for fractional aggregation
and has been certified correct. Prior to 2016, gdalwarp's resampling method called, 'average',
was not not producing correct answers for fractional aggregation. The 'average' method
has not be evaluated for correctness since 2016 -- GDAL may have fixed their code since then. 
Set this port as desired. 

The **_prefixLen_** port indicates how many characters of the input source file name will be 
used in both the output clipped target file name and the output clipped resampled source file name. 
If the value is set to '0', then none of the input source file name will be used. If the value 
is set to a large number (e.g., '250')then all of the input source file name will be used. 
Set this port as desired.

The **_osuffA_** port indicates the file name suffix that will be used for the output clipped resampled source.
Set this port as desired.

The **_osuffA_** port indicates the file name suffix that will be used for the output clipped target image.
Set this port as desired.

Batch Mode: The input source directory and input target directory are allowed to contain multiples images 
as long as they contain the same number of images. Source-target image pairs will be established by lexicographic 
ordering of the file names in each directory. These pairs will be processed in parallel.

The other modifications you need to make to run the workflow are as follows:
 
* Set **_in_base_dir_** -- this is the top-level S3 input directory that contains your input data 
* Set **_out_base_dir_** -- this is the top-level S3 output directory
* Set **_source_dir_** -- this is the s3 directory containing the source image(s)
* Set **_target_dir_** -- this is the s3 directory containing the target image(s)





















