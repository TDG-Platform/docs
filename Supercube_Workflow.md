# Suupercube Workflow

This document describes how to modify the Supercube GBDX workflow template in order to compute a 16-band stack from WV3 8-band DN VNIR and 8-band DN SWIR data that has undergone **_Level 3X_** processing. The resulting supercube is at the VNIR pixel resolution, and its extent is that of the overlap of the VNIR and SWIR. The processing involves the MutualInformationCoregister v8b task. (Version v10d of this task and workflow will be available shortly.) The algorithm for producing a supercube requires cloud and water processing; therefore a cloud and water mask are also generated -- both at VNIR resolution and cut to the extent of the supercube. For convenience, an RGB with the extent of the VNIR is also generated. This task serves as a precursor for a DGLayers workflow, where the latter might utilize the supercube, cloud mask, and water mask.  

**Supercube Workflow Template:** 

```shell
import os
from gbdxtools import Interface
gbdx = Interface()

in_base_dir = "s3://gbd-customer-data/58600248-2927-4523-b44b-5fec3d278c09/jm_images/"
out_base_dir = "s3://gbd-customer-data/58600248-2927-4523-b44b-5fec3d278c09/jm_images/Seth_OUT/"

####### INPUTS ########

dn_dir = os.path.join(in_base_dir, "scube_data/")
vnir_dn_dir = os.path.join(dn_dir, "vnir/")
swir_dn_dir = os.path.join(dn_dir, "swir/")

####### OUTPUTS #######

out_rgb_dir = os.path.join(out_base_dir, "RGB")
out_scube_dir = os.path.join(out_base_dir, "SCUBE")
out_water_scube_dir = os.path.join(out_base_dir, "WATER")
out_cloud_scube_dir = os.path.join(out_base_dir, "CLOUD")

####################################################################################
#################### Supercube, Cloud and Water Masks ##############################
####################################################################################

############## ACOMP
acomp_task = gbdx.Task("AComp_1.0-debug",
                       data = dn_dir,
                       verbose = True)

acomp_dir = acomp_task.outputs.data.value

############# Separate AComp VNIR, SWIR, and AUX directories
scube_prep_task = gbdx.Task("ScubePrep",
                            input_dir = acomp_dir)

acomp_vnir_dir = scube_prep_task.outputs.vnir_data.value

############## Mosaic the AComp'd VNIR
cmd = "gdalbuildvrt $indir/out.vrt $indir/*.TIF; "
cmd += "gdal_translate $indir/out.vrt $outdir/acomp_vnir.tif"
mosaic_task = gbdx.Task("gdal-cli",
                        command = cmd,
                        data = acomp_vnir_dir,
                        execution_strategy = 'runonce')

mosaic_acomp_vnir_dir = mosaic_task.outputs.data.value

############# RGB from mosaicked AComp'd VNIR
cmd22 = "gdal_translate -b 5 -b 3 -b 2 $indir/*.tif $outdir/vnir_5_3_2_rgb.tif"
rgb_task = gbdx.Task("gdal-cli",
                        command = cmd22,
                        data = mosaic_acomp_vnir_dir,
                        execution_strategy = 'runonce')

rgb_dir = rgb_task.outputs.data.value 

save_rgb_task = gbdx.Task("StageDataToS3",
                            data = rgb_dir,
                            destination = out_rgb_dir)

############# Water Mask
# Build a water mask boolean raster. water = 255; non-water = 0
water_task = gbdx.Task("protogenV2RAW",
                       raster = mosaic_acomp_vnir_dir)

water_dir = water_task.outputs.data.value

############# Cloud Mask
# Build a cloud mask boolean raster. cloud = 255; non-cloud = 0
cloud_task = gbdx.Task("protogenV2RAC",
                       raster = mosaic_acomp_vnir_dir)

cloud_dir = cloud_task.outputs.data.value

############# Supercube task
scube_task = gbdx.Task("MutualInformationCoregister_v8b",
                       vnirDNImages = vnir_dn_dir,
                       swirDNImages = swir_dn_dir,
                       waterMask = water_dir,
                       cloudMask = cloud_dir,
                       acompOutputFiles = acomp_dir)

scube_dir = scube_task.outputs.alignedSupercube.value

save_scube_task = gbdx.Task("StageDataToS3",
                            data = scube_dir,
                            destination = out_scube_dir)

# ########### Resample Water Mask to Supercube and cut to the overlap
rc_water_scube_task = gbdx.Task("resample_and_cut_001",
                    input_A = water_dir,
                    input_B = scube_dir,
                    nodata_A='-1',
                    r_meth='near',
                    prefixLen='31',
                    osuffA='WATER_SCUBE_RC')

water_scube_dir = rc_water_scube_task.outputs.out_A.value

save_water_scube_task = gbdx.Task("StageDataToS3",
                            data = water_scube_dir,
                            destination = out_water_scube_dir)

########### Resample Cloud Mask to Supercube and cut to the overlap
rc_cloud_scube_task = gbdx.Task("resample_and_cut_001",
                    input_A = cloud_dir,
                    input_B = scube_dir,
                    nodata_A='-1',
                    r_meth='near',
                    prefixLen='31',
                    osuffA='CLOUD_SCUBE_RC')

cloud_scube_dir = rc_cloud_scube_task.outputs.out_A.value

save_cloud_scube_task = gbdx.Task("StageDataToS3",
                            data = cloud_scube_dir,
                            destination = out_cloud_scube_dir)

###################################################################################
############################### Task List #########################################
###################################################################################

workflow = gbdx.Workflow([acomp_task,
                          scube_prep_task,
                          mosaic_task,
                          rgb_task,
                          save_rgb_task,
                          water_task,
                          cloud_task,
                          scube_task,
                          save_scube_task,
                          rc_water_scube_task,
                          save_water_scube_task,
                          rc_cloud_scube_task,
                          save_cloud_scube_task])

workflow.execute()
print(workflow.id)
```

The only modifications you need to make to this template are the following:
 
* Set **_in_base_dir_** -- this is the top-level S3 input directory that contains your DN data 
* Set **_out_base_dir_** -- this is the top-level S3 output directory
* Set **_dn_dir_**, **_vnir_dn_dir_**, and **_swir_dn_dir_** -- these are the S3 locations of the input DN data that will be AComp'd and Supercube'd
















