# HotMaps GBDX Workflow Template

This document describes how to modify a HotMaps GBDX workflow template in order to identify the active fire pixels in a burn scene (a WV3 image), even through wood smoke. The inputs are WV3 DN 8-band VNIR and 8-band SWIR data with **_Level 3X_** processing. The SWIR sensor on WV3 is able to see through wood smoke. The output consists of three products: (1) Shape file whose polygons delimit active fire pixels; (2) False-color SWIR RGB raster image using bands 6, 3, 1, in that order, from bands 1 - 8 of the input SWIR image; (3) Cloud mask raster indicating water clouds that are impermeable to the SWIR sensor. 

At the beginning of the workflow, the VNIR is mosaicked and fractionally pixel-aggregated to agree with the SWIR pixels.  The VNIR and SWIR are then stacked, but not registered, and clipped to the common overlap. This results in a "crude supercube" 16-band stack at SWIR resolution. The HotMaps analysis task takes this crude supercube as input. 


<!--
***************************************************************************
-->

**HotMaps Workflow Template:** 

```shell
import os
from gbdxtools import Interface
gbdx = Interface()

# NOTE: Make sure these directory strings have the trailing "/" as shown
in_base_dir = "s3://xxxxxxxxxxxxx/"
out_base_dir = "s3://xxxxxxxxxxxxx/"

####### INPUTS ######

dn_dir = os.path.join(in_base_dir, "dn_data/")
dn_vnir_dir = os.path.join(dn_dir, "vnir/")
dn_swir_dir = os.path.join(dn_dir, "swir/")
recipe_dir = os.path.join(in_base_dir, "recipes/")

recipe11_filename = "stack_swir_on_vnir_recipe.txt"
recipe22_filename = "false_color_swir_recipe.txt"

####### OUTPUTS #######

out_scube_dir = os.path.join(out_base_dir, "SCUBE")
out_hotmap_dir = os.path.join(out_base_dir, "HOTMAP")
out_cloudmask_dir = os.path.join(out_base_dir, "SWIR_CLOUD_MASK")

########################################################

############# Mosaic the VNIR tiles
cmd = "gdalbuildvrt $indir/out.vrt $indir/*.TIF; "
cmd += "gdal_translate $indir/out.vrt $outdir/mosaic_dn_vnir.tif"
mosaic_task = gbdx.Task("gdal-cli",
                        command = cmd,
                        data = dn_vnir_dir,
                        execution_strategy = 'runonce')

mosaic_dn_vnir_dir = mosaic_task.outputs.data.value

save_mosaic_task = gbdx.Task("StageDataToS3",
                             data = mosaic_dn_vnir_dir,
                             destination = out_vnir_dir)

############# Resample-and-Cut (VNIR to SWIR)
rc_task = gbdx.Task("resample_and_cut_001",
                    input_A = mosaic_dn_vnir_dir,
                    input_B = dn_swir_dir,
                    nodata_A  = '0',
                    r_meth = 'dg_average',
                    prefixLen = '39',
                    osuffA = 'RC',
                    osuffB = 'CUT')

rc_vnir_dir = rc_task.outputs.out_A.value
rc_swir_dir = rc_task.outputs.out_B.value

save_rc_vnir_task = gbdx.Task("StageDataToS3",
                              data = rc_vnir_dir,
                              destination = out_rc_vnir_dir)

save_rc_swir_task = gbdx.Task("StageDataToS3",
                              data = rc_swir_dir,
                              destination = out_rc_swir_dir)

############# Stack SWIR on VNIR
stack_task = gbdx.Task("DGLayers_v_3_0",
                     SRC_vnir = rc_vnir_dir,
                     SRC_swir = rc_swir_dir,
                     recipe_dir = recipe_dir,
                     recipe_filename = recipe11_filename)

scube_dir_00 = stack_task.outputs.DST.value

############# Copy Scube and IMD's to new directory
cmd = "mkdir $outdir/data; "
cmd += "mv $indir/dataScube/*.tif $outdir/data; "
cmd += "cp $indir/dataV/*.IMD $outdir/data; "
cmd += "cp $indir/dataS/*.IMD $outdir/data"
copy_task = gbdx.Task('gdal-cli-multiplex')
copy_task.inputs.dataScube = scube_dir_00
copy_task.inputs.dataV = dn_vnir_dir
copy_task.inputs.dataS = dn_swir_dir
copy_task.inputs.command = cmd
copy_task.execution_strategy='runonce'

scube_dir = copy_task.outputs.data.value

save_scube_task = gbdx.Task("StageDataToS3",
                            data = scube_dir,
                            destination = out_scube_dir)

############# SWIR Cloud Mask
cloud_mask_task = gbdx.Task('SWIRcloudMask',
                            image=scube_dir)

cloud_mask_dir = cloud_mask_task.outputs.mask.value

save_cloud_mask_task = gbdx.Task("StageDataToS3",
                             data = cloud_mask_dir,
                             destination = out_cloudmask_dir)

############# HotMap With Cloud Mask
hotmap_task = gbdx.Task('hotmap',
                        data= scube_dir,
                        mask=cloud_mask_dir)

hotmap_dir = hotmap_task.outputs.out.value

save_hotmap_task = gbdx.Task("StageDataToS3",
                            data = hotmap_dir,
                            destination = out_hotmap_dir)

############# False color SWIR
fc_swir_task = gbdx.Task("DGLayers_v_3_0",
                      SRC = rc_swir_dir,
                      recipe_dir = recipe_dir,
                      recipe_filename = recipe22_filename)
 
fc_swir_dir = fc_swir_task.outputs.DST.value

save_fc_swir_task = gbdx.Task("StageDataToS3",
                             data = fc_swir_dir,
                             destination = out_hotmap_dir)

##########################################################
workflow = gbdx.Workflow([mosaic_task,
                          rc_task,
                          stack_task,
                          copy_task,
                          save_scube_task,
                          cloud_mask_task,
                          save_cloud_mask_task,
                          hotmap_task,
                          save_hotmap_task,
                          fc_swir_task,
                          save_fc_swir_task])

workflow.execute()
print workflow.id
```

<!--
***************************************************************************
-->

The above template should reflect the latest versions of all tasks. Here are the modifications you need to make:
 
* Set **_in_base_dir_** -- this is the top-level S3 input directory that contains your DN data 
* Set **_out_base_dir_** -- this is the top-level S3 output directory
* Set **_dn_dir_**, **_vnir_dn_dir_**, and **_swir_dn_dir_** -- these are the S3 locations of the input DN data that will be AComp'd and Supercube'd
* Set **_recipe_dir_** -- this is the directory containing your DGLayers recipe file **_and any auxiliary text files it refers to_** 

<!--
***************************************************************************
-->

The HotMaps workflow calls the DGLayers task on two recipe files:

**stack_swir_on_vnir_recipe.txt:**

```shell
#########################################################################
###################   DGLayers Recipe File    ##########################
#########################################################################

# Stack SWIR on VNIR

#------------------------------------------------------------------------
#	Optional renaming of output directories and files.
# 	Use sandwiched pair: BEGIN_RENAME_OUTPUTS, END_RENAME_OUTPUTS
#   PREFIX_LEN length of file name prefix from SRC file that will be 
#		used in the file name of corresponding output files
#   Triplets of form: <outdir_id> <outdir_name> <suffix>. Indicates 
#   	that directory <outdir_id> is to be renamed <outdir_name> and 
#		that the file names will involve the suffix string <suffix>
#------------------------------------------------------------------------

BEGIN_RENAME_OUTPUTS
PREFIX_LEN 39
n1 DST scube
END_RENAME_OUTPUTS

#------------------------------------------------------------------------
#                             Process Flow 
#------------------------------------------------------------------------

stack_bands --outdirID n1 --indirIDs (SRC_vnir, *) (SRC_swir, *) --deliver
```

<!--
***************************************************************************
-->

The above recipe file references the following pair of auxiliary files:

**false_color_swir_recipe.txt:**

```shell
#########################################################################
####################   DGLayers Recipe File    ##########################
#########################################################################

# Given an 8-band SWIR, create a false-color 3-band SWIR:  6, 3, 1 (RGB)

#------------------------------------------------------------------------
#	Optional renaming of output directories and files.
# 	Use sandwiched pair: BEGIN_RENAME_OUTPUTS, END_RENAME_OUTPUTS
#   PREFIX_LEN length of file name prefix from SRC file that will be 
#		used in the file name of corresponding output files
#   Triplets of form: <outdir_id> <outdir_name> <suffix>. Indicates 
#   	that directory <outdir_id> is to be renamed <outdir_name> and 
#		that the file names will involve the suffix string <suffix>
#------------------------------------------------------------------------

BEGIN_RENAME_OUTPUTS
PREFIX_LEN 39
n1 DST swir_6_3_1_RGB
END_RENAME_OUTPUTS

#------------------------------------------------------------------------
#                             Process Flow 
#------------------------------------------------------------------------

subset_bands --outdirID n1 --indirID SRC -bands 6 3 1 --deliver
```

<!--
***************************************************************************
-->

To run the HotMaps workflow, copy the two recipe files to your desired recipe directory on S3, set the directory paths (mentioned above) in the workflow as appropriate, and run. 















