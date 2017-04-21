## Supercube (Unaligned) GBDX Workflow 

This document introduces the Supercube (Unaligned) GBDX Workflow and describes how to modify it in order to build an unaligned 16-band "supercube" stack from WV3 8-band VNIR and 8-band SWIR data. The input data can be DN data or Acomp'd data. This workflow does not perform ortho-processing. In the workflow, the VNIR is resampled to the SWIR, or vice versa, and the resulting datasets are then clipped to the common overlap and stacked, to form a 16-band supercube. 

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

####### OUTPUTS #######
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

############# Resample VNIR to SWIR and cut to common overlap
rc_task = gbdx.Task("resample_and_cut_001",
                    input_A = mosaic_vnir_dir,
                    input_B = swir_dir,
                    nodata_A  = '0',
                    r_meth = 'dg_average', 
                    prefixLen = '39',
                    osuffA = 'RC',
                    osuffB = 'CUT')

rc_vnir_dir = rc_task.outputs.out_A.value
rc_swir_dir = rc_task.outputs.out_B.value

############# Stack SWIR on VNIR
cmd22 = "infile=`ls $indir/dataS/*.tif`; "  # Note: back-ticks not single quotes
cmd22 += 'infname=$(basename "$infile" .tif); '  
cmd22 += "infprefix=${infname::39}; "
cmd22 += "outfname=$infprefix'_SCUBE.tif'; "
cmd22 += "mkdir $outdir/data; "
cmd22 += "gdal_merge.py -separate -o $outdir/data/$outfname $indir/dataV/*.tif $indir/dataS/*.tif"
stack_task = gbdx.Task("gdal-cli-multiplex")
stack_task.inputs.dataV = rc_vnir_dir
stack_task.inputs.dataS = rc_swir_dir
stack_task.inputs.command = cmd22
stack_task.execution_strategy='runonce'

scube_dir = stack_task.outputs.data.value

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
* In the rc_task, **_input_A_** (source) is resampled to **_input_B_** (target), and then both are clipped to the common overlap. Set those ports as desired. Set the resampling method **_r_meth_** to be any of the resampling methods available for gdalwarp in GDAL 2.0. For proper fractional pixel aggregation, however, set it to 'dg_average'.






















