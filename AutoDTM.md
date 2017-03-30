## AutoDTM GBDX Task 

This document shows how to call the AutoDTM GBDX Task within the context of a GBDX Workflow. This task builds a float-32 DTM (Digital Terrain Model) from a float-32 DSM (Digital Surface Model) Tiff image and an unsigned 8-bit LULC (Land Use Land Cover) Tiff image. The input images are assumed to have square pixels (and possibly 2m pixels only), identical extent, and identical pixel resolution. The DTM is built from DSM pixels whose counterparts in the LULC do not have index of tree (5), shrub (6), building (9), or no-data (0). The no-data value in the DSM must be -9999. The file name of the input DSM (excluding extension) must end with '_RDSMLULC'. The file name  of the input LULC (excluding extension) must end with '_RCUTLULC'. The output DTM will have no-data value -9999 and this will occur wherever the DSM is -9999 or the LULC is 0. An example usage of the AutoDTM Task is on the PSMA project (Seth Malitz, Dan Getman) in the construction of Tree Digital Height Model product.

<!--
***************************************************************************
-->

**_AutoDTM Workflow:_** 

```shell
import os
from gbdxtools import Interface
gbdx = Interface()

# NOTE: Make sure these directory strings have the trailing "/" as shown
in_base_dir = "s3://xxxxxxxxxxxxx/"
out_base_dir = "s3://xxxxxxxxxxxxx/"

####### INPUTS ########
dsm_dir = os.path.join(in_base_dir, "XXXXXXX/") 
lulc_dir = os.path.join(in_base_dir, "XXXXXXX/")

####### OUTPUTS #######
out_dtm_dir = os.path.join(out_base_dir, "DTM") 

##########################################################
dtm_task = gbdx.Task("AutoDTM",
                     working_dir = "docker_scratch",
                     dsm_path = dsm_dir, 
                     lulc_path = lulc_dir) 

# Name EC2 file
dtm_dir = dtm_task.outputs.data.value

save_dtm_task = gbdx.Task("StageDataToS3",
                           data = dtm_dir,
                           destination = out_dtm_dir)
						   
##########################################################
workflow = gbdx.Workflow([dtm_task,
                          save_dtm_task])

workflow.execute()
print workflow.id
```

<!--
***************************************************************************
-->

In order to run the workflow:
 
* Set **_in_base_dir_** -- this is the top-level S3 input directory that contains your input data 
* Set **_out_base_dir_** -- this is the top-level S3 output directory
* Set **_dsm_dir_** -- this is the s3 directory that contains the DSM image
* Set **_lulc_dir_** -- this is the s3 directory that contains the LULC image





















