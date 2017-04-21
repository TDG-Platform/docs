# HotMaps GBDX Workflow 

This document introduces the HotMaps GBDX Workflow and describes how to modify it in order to identify the active fire pixels in a WV3 image -- even through smoke clouds (but not water vapour clouds). The SWIR sensor on WV3 is able to see through wood smoke. The input is WV3 DN 8-band VNIR and 8-band SWIR data. This workflow does not perform ortho-processing. The output consists of three products: (1) a shape file whose polygons delimit active fire pixels; (2) a false-color SWIR RGB raster image using bands 6, 3, 1, in that order, from bands 1 - 8 of the input SWIR image; (3) a SWIR cloud mask raster indicating water clouds that are impermeable to the SWIR sensor. 

At the beginning of the workflow, the VNIR is mosaicked and fractionally pixel-aggregated to agree with the SWIR pixels.  The resulting VNIR and SWIR are then stacked, **_but not registered_**, and clipped to the common overlap, yielding a "crude supercube", a 16-band stack at SWIR resolution. The HotMap GBDX task takes this crude supercube as input. 

<!--
***************************************************************************
-->

**_HotMaps Workflow:_** 

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

####### OUTPUTS #######
out_scube_dir = os.path.join(out_base_dir, "SCUBE")
out_hotmap_dir = os.path.join(out_base_dir, "HOTMAP")
out_swir_cloud_dir = os.path.join(out_base_dir, "SWIR_CLOUD_MASK")

####################################################################################

############# Mosaic the VNIR tiles 
cmd = "gdalbuildvrt $indir/out.vrt $indir/*.TIF; "
cmd += "gdal_translate $indir/out.vrt $outdir/mosaic_dn_vnir.tif"
mosaic_task = gbdx.Task("gdal-cli",
                        command = cmd,
                        data = dn_vnir_dir,
                        execution_strategy = 'runonce')

mosaic_dn_vnir_dir = mosaic_task.outputs.data.value

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

############# Stack SWIR on VNIR  
cmd22 = "infile=`ls $indir/dataS/*.tif`; "  # Note: back-ticks not single quotes
cmd22 += 'infname=$(basename "$infile" .tif); '  
cmd22 += "infprefix=${infname::39}; "
cmd22 += "outfname=$infprefix'_SCUBE.tif'; "
cmd22 += "mkdir $outdir/data; "
cmd22 += "gdal_merge.py -separate -o $outdir/data/$outfname $indir/dataV/*.tif $indir/dataS/*.tif"
stack_task = gbdx.Task('gdal-cli-multiplex')
stack_task.inputs.dataV = rc_vnir_dir
stack_task.inputs.dataS = rc_swir_dir
stack_task.inputs.command = cmd22
stack_task.execution_strategy='runonce'

scube_dir_00 = stack_task.outputs.data.value

############# Copy IMD's to SCUBE directory
cmd33 = "mkdir $outdir/data; "
cmd33 += "mv $indir/dataScube/*.tif $outdir/data; "
cmd33 += "cp $indir/dataV/*.IMD $outdir/data; "
cmd33 += "cp $indir/dataS/*.IMD $outdir/data"
copy_task = gbdx.Task('gdal-cli-multiplex')
copy_task.inputs.dataScube = scube_dir_00
copy_task.inputs.dataV = dn_vnir_dir
copy_task.inputs.dataS = dn_swir_dir
copy_task.inputs.command = cmd33
copy_task.execution_strategy = 'runonce'

scube_dir = copy_task.outputs.data.value

save_scube_task = gbdx.Task("StageDataToS3",
                            data = scube_dir,
                            destination = out_scube_dir)

############# SWIR Cloud Mask
swir_cloud_task = gbdx.Task('SWIRcloudMask',
                            image = scube_dir)

swir_cloud_dir = swir_cloud_task.outputs.mask.value

save_swir_cloud_task = gbdx.Task("StageDataToS3",
                             data = swir_cloud_dir,
                             destination = out_swir_cloud_dir)

############# HotMap With SWIR Cloud Mask
hotmap_task = gbdx.Task('hotmap',
                        data = scube_dir,
                        mask = swir_cloud_dir)

hotmap_dir = hotmap_task.outputs.out.value

save_hotmap_task = gbdx.Task("StageDataToS3",
                            data = hotmap_dir,
                            destination = out_hotmap_dir)

############# False color SWIR 
cmd44 = "infile=`ls $indir/*.tif`; "  # Note: back-ticks not single quotes
cmd44 += 'infname=$(basename "$infile" .tif); '  
cmd44 += "infprefix=${infname::39}; "
cmd44 += "outfname=$infprefix'_swir_6_3_1_rgb.tif'; "
cmd44 += "gdal_translate -b 6 -b 3 -b 1 $indir/*.tif $outdir/$outfname; "
cmd44 += "rm $outdir/*.tif.aux.xml"
fc_swir_task = gbdx.Task("gdal-cli",
                        command = cmd44,
                        data = rc_swir_dir,
                        execution_strategy = 'runonce')

fc_swir_dir = fc_swir_task.outputs.data.value 

save_fc_swir_task = gbdx.Task("StageDataToS3",
                             data = fc_swir_dir,
                             destination = out_hotmap_dir)

##########################################################
workflow = gbdx.Workflow([mosaic_task,
                          rc_task,
                          stack_task,
                          copy_task,
                          save_scube_task,
                          swir_cloud_task,
                          save_swir_cloud_task,
                          hotmap_task,
                          save_hotmap_task,
                          fc_swir_task,
                          save_fc_swir_task])

#print workflow.generate_workflow_description()
workflow.execute()
print
print workflow.id
```

<!--
***************************************************************************
-->

The above workflow should reflect the latest versions of all the participating tasks. 
Here are the modifications you need to make to run the workflow:
 
* Set **_in_base_dir_** -- this is the top-level S3 input directory that contains your DN data 
* Set **_out_base_dir_** -- this is the top-level S3 output directory
* Set **_dn_dir_**, **_dn_vnir_dir_**, and **_dn_swir_dir_** -- these are the S3 locations of the input WV3 DN data 
















