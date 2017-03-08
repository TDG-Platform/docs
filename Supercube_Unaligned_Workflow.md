## Supercube (Unaligned) GBDX Workflow 

This document introduces the Supercube (Unaligned) GBDX Workflow and describes how to modify it in order to build an unaligned 16-band "supercube" stack from WV3 8-band VNIR and 8-band SWIR data. The input data can be DN data or Acomp'd data. This workflow does not perform ortho-processing. In the workflow, the VNIR is resampled to the SWIR, or vice versa, and the resulting datasets are then clipped to the common overlap and stacked, to form a 16-band supercube. The workflow calls the DGLayers GBDX task on a recipe file to perform the stacking of the VNIR and SWIR.

<!--
***************************************************************************
-->

**_Supercube (Unaligned) Workflow:_** 

```shell
import os
from gbdxtools import Interface
gbdx = Interface()

# NOTE: Make sure these directory strings have the trailing "/" as shown
in_base_dir = "s3://xxxxxxxxxxxxx/"
out_base_dir = "s3://xxxxxxxxxxxxx/"

####### INPUTS ######

data_dir = os.path.join(in_base_dir, "data/")
vnir_dir = os.path.join(data_dir, "vnir/")
swir_dir = os.path.join(data_dir, "swir/")
recipe_dir = os.path.join(in_base_dir, "recipe/")

recipe_filename = "stack_swir_on_vnir_recipe.txt"

####### OUTPUTS #######

"""
out_vnir_dir = os.path.join(out_base_dir, "VNIR")
out_rc_vnir_dir = os.path.join(out_base_dir, "RC_VNIR")
out_rc_swir_dir = os.path.join(out_base_dir, "RC_SWIR")
"""
out_scube_dir = os.path.join(out_base_dir, "SCUBE")

########################################################

############# Mosaic the VNIR tiles
cmd = "gdalbuildvrt $indir/out.vrt $indir/*.TIF; "
cmd += "gdal_translate $indir/out.vrt $outdir/mosaic_vnir.tif"
mosaic_task = gbdx.Task("gdal-cli",
                        command = cmd,
                        data = vnir_dir,
                        execution_strategy = 'runonce')

mosaic_vnir_dir = mosaic_task.outputs.data.value
"""
save_mosaic_task = gbdx.Task("StageDataToS3",
                             data = mosaic_vnir_dir,
                             destination = out_vnir_dir)
"""

############# Resample-and-Cut 
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

"""
save_rc_vnir_task = gbdx.Task("StageDataToS3",
                              data = rc_vnir_dir,
                              destination = out_rc_vnir_dir)

save_rc_swir_task = gbdx.Task("StageDataToS3",
                              data = rc_swir_dir,
                              destination = out_rc_swir_dir)
"""

############# Stack SWIR on VNIR
stack_task = gbdx.Task("DGLayers_v_3_0",
                     SRC_vnir = rc_vnir_dir,
                     SRC_swir = rc_swir_dir,
                     recipe_dir = recipe_dir,
                     recipe_filename = recipe11_filename)

scube_dir = stack_task.outputs.DST.value

save_scube_task = gbdx.Task("StageDataToS3",
                            data = scube_dir,
                            destination = out_scube_dir)

##########################################################
workflow = gbdx.Workflow([mosaic_task,
                          rc_task,
                          stack_task,
                          save_scube_task])

workflow.execute()
print workflow.id
```

<!--
***************************************************************************
-->

The above workflow should reflect the latest versions of all the participating tasks. 
Here are the modifications you need to make to run the workflow:
 
* Set **_in_base_dir_** -- this is the top-level S3 input directory that contains your DN data 
* Set **_out_base_dir_** -- this is the top-level S3 output directory
* Set **_data_dir_**, **_vnir_dir_**, and **_swir_dir_** -- these are the S3 locations of the input WV3 DN data 
* Set **_recipe_dir_** -- this is the directory containing the DGLayers recipe files
* In the rc_task, **_input_A_** (source) is resampled to **_input_B_** (target), and then both are clipped to the common overlap. Set those ports as desired. Set the resampling method **_r_meth_** to be any of the resampling methods available for gdalwarp in GDAL 2.0. For proper fractional pixel aggregation, however, set it to 'dg_average'.

<!--
***************************************************************************
-->

The above workflow calls the DGLayers GBDX task on the following recipe file:

**_stack_swir_on_vnir_recipe.txt:_**

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

To run the workflow, copy the recipe file (create the file using cut and paste out of this document) to the desired recipe directory on S3, set the directory paths (mentioned above) as desired, and run. 




















