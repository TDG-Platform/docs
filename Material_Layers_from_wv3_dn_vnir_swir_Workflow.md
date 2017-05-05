# Material Layers (from WV3 DN VNIR and SWIR) GBDX Workflow 

This document introduces the Material Layers (from Orthorectified DN Data) GBDX Workflow and describes how to modify it in order to compute desired material layers (rasters and polygons) from WV3 orthorectified DN VNIR and SWIR data. This workflow assumes the input DN data has been orthorectified.  

The template has two parts: The first part computes a 16-band aligned AComp "supercube" from the 8-band DN VNIR plus 8-band DN SWIR data, as well as pixel-aligned water mask and cloud mask. The second part invokes the DGLayers task on a DGlayers recipe file. The recipe file describes the desired Material Layers operations and outputs (e.g., indices, SAM classification map, masks, polygons, etc.) 

To learn about the operations that can be called from within a DGLayers recipe file, see the documentation for [DGLayers] 
(https://github.digitalglobe.com/nw002655/dglayers/blob/master/DGLayers-GBDX.md)

<!--
***************************************************************************
-->

**_Material Layers (from WV3 DN VNIR and SWIR) Workflow:_** 

```shell
import os
from gbdxtools import Interface
gbdx = Interface()

in_base_dir = "s3://gbd-customer-data/58600248-2927-4523-b44b-5fec3d278c09/seth/"
out_base_dir = os.path.join(in_base_dir, "MATERIAL_LAYERS_050417_CC/")

####### INPUTS #######
input_data_is_1b = True  # True/False
dn_data_dir = os.path.join(in_base_dir, "fromAlex/")
dn_vnir_dir = os.path.join(dn_data_dir, "vnir_1b")
dn_swir_dir = os.path.join(dn_data_dir, "swir_1b")
recipe_dir = os.path.join(in_base_dir, "Mining_Layers/Recipes/")
recipe_filename = "seth_recipe_small_test.txt"

####### OUTPUTS #######
out_acomp_rgb_dir = os.path.join(out_base_dir, "ACOMP_RGB")
out_scube_dir = os.path.join(out_base_dir, "ACOMP_SCUBE")
out_water_scube_dir = os.path.join(out_base_dir, "WATER_SCUBE")
out_cloud_scube_dir = os.path.join(out_base_dir, "CLOUD_SCUBE")
out_layers_dir = os.path.join(out_base_dir, "LAYERS")

###### DEBUG OUTPUTS ################
out_acomp_dir = os.path.join(out_base_dir, "Ortho_and_AComp_UTM")
out_vnir_imd_dir = os.path.join(out_base_dir, "vnir_imd_dir")
out_swir_imd_dir = os.path.join(out_base_dir, "swir_imd_dir")
out_cloud_vnir_dir = os.path.join(out_base_dir, "CLOUD_VNIR")
out_water_vnir_dir = os.path.join(out_base_dir, "WATER_VNIR")
out_mi_mask_dir = os.path.join(out_base_dir, "MI_MASK")
out_mi_tmp_dir = os.path.join(out_base_dir, "MI_TMP")

####################################################################################

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
if input_data_is_1b:
    ############## Orthorectify 1B and AComp -- ALSO converts to UTM
    ughli_task = gbdx.Task('ughli', 
                        data = dn_vnir_dir, 
                        swir = dn_swir_dir, 
                        bands = "Multi,All-S",    # Suppress PAN processing in orthorectify and reproject
                        exclude_bands = "P",      # Suppress PAN processing in AComp
                        epsg_code = "EPSG:26713", 
                        pixel_size_ms = "2.0",
                        pixel_size_swir = "7.5",
                        compute_noise = "true")

    acomp_dir = ughli_task.outputs.data.value  

else: # ortho
    ############## Just do AComp #############
    acomp_task = gbdx.Task("AComp_internal",
                           data = dn_data_dir,
                           compute_noise = True)
    
    acomp_dir = acomp_task.outputs.data.value
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

save_acomp_task = gbdx.Task('StageDataToS3', 
                    data = acomp_dir, 
                    destination = out_acomp_dir)

############# Copy AComp VNIR and IMD's to their own directories
cmd = "mkdir $outdir/dataV $outdir/dataVimd $outdir/dataSimd; "

cmd += "infile=`ls $indir/data/*-M*.IMD`; "  # Note: back-ticks not single quotes
cmd += 'infname=$(basename "$infile" .IMD); '  
cmd += "infprefix=${infname::${#infname}-6}; " # Strip off "_ACOMP"
cmd += "outfname=$infprefix'.IMD'; "
cmd += "cp $indir/data/*-M*.IMD $outdir/dataVimd/$outfname; "

cmd += "infile=`ls $indir/data/*-A*.IMD`; "  # Note: back-ticks not single quotes
cmd += 'infname=$(basename "$infile" .IMD); '  
cmd += "infprefix=${infname::${#infname}-6}; " # Strip off "_ACOMP"
cmd += "outfname=$infprefix'.IMD'; "
cmd += "cp $indir/data/*-A*.IMD $outdir/dataSimd/$outfname; "

cmd += "cp $indir/data/*-M*_ACOMP.TIF $outdir/dataV"

copy_task = gbdx.Task('gdal-cli-multiplex')
copy_task.inputs.data = acomp_dir
copy_task.inputs.command = cmd
copy_task.execution_strategy='runonce'

vnir_imd_dir = copy_task.outputs.dataVimd.value
swir_imd_dir = copy_task.outputs.dataSimd.value
acomp_vnir_dir = copy_task.outputs.dataV.value

save_vnir_imd_task = gbdx.Task("StageDataToS3",
                            data = vnir_imd_dir,
                            destination = out_vnir_imd_dir)

save_swir_imd_task = gbdx.Task("StageDataToS3",
                            data = swir_imd_dir,
                            destination = out_swir_imd_dir)

############# RGB 
cmd22 = "infile=`ls $indir/*.TIF`; "              # Note: back-ticks not single quotes
cmd22 += 'infname=$(basename "$infile" .TIF); '
cmd22 += "outfname=$infname'_5_3_2_rgb.tif'; "
cmd22 += "gdal_translate -b 5 -b 3 -b 2 $indir/*.TIF $outdir/$outfname"   # TBD -- get the output file name right!!!!!!!!!!!!!!!!!!!!!!!!
rgb_task = gbdx.Task("gdal-cli",
                     command = cmd22,
                     data = acomp_vnir_dir,
                     execution_strategy = 'runonce')

acomp_rgb_dir = rgb_task.outputs.data.value # <-------------------------- Not used downstream

save_acomp_rgb_task = gbdx.Task("StageDataToS3",
                          data = acomp_rgb_dir,
                          destination = out_acomp_rgb_dir)

############# Water Mask
# Build a water mask boolean raster. water = 255; non-water = 0
water_task = gbdx.Task("protogenV2RAW",
                       raster = acomp_vnir_dir)

water_vnir_dir = water_task.outputs.data.value

save_water_vnir_task = gbdx.Task("StageDataToS3",
                            data = water_vnir_dir,
                            destination = out_water_vnir_dir)

############# Cloud Mask
# Build a cloud mask boolean raster. cloud = 255; non-cloud = 0
cloud_task = gbdx.Task("protogenV2RAC",
                       raster = acomp_vnir_dir)

cloud_vnir_dir = cloud_task.outputs.data.value

save_cloud_vnir_task = gbdx.Task("StageDataToS3",
                            data = cloud_vnir_dir,
                            destination = out_cloud_vnir_dir)

############# Union Cloud and Water Mask for MI
# NOTE: The output mask file needs a very specific naming convention in order 
# to be ingested by mi_setup task. Here is example of output file name:
# 14AUG28191207-M2AS-054759622010_01_ACOMP_LULC_MASK.tif
cmd33 = "infile=`ls $indir/dataC/*.tif`; "  # Note: back-ticks not single quotes
cmd33 += 'infname=$(basename "$infile" .tif); '  
cmd33 += "infprefix=${infname::34}; "
cmd33 += "outfname=$infprefix'_ACOMP_LULC_MASK.tif'; "
cmd33 += "mkdir $outdir/data; "
cmd33 += 'gdal_calc.py -A $indir/dataW/*.tif -B $indir/dataC/*.tif --outfile=$outdir/data/$outfname '
cmd33 += '--calc="numpy.where(B,B,A)" --type=Byte'
union_task = gbdx.Task('gdal-cli-multiplex')
union_task.inputs.dataC = cloud_vnir_dir
union_task.inputs.dataW = water_vnir_dir
union_task.inputs.command = cmd33
union_task.execution_strategy='runonce'

mi_mask_dir = union_task.outputs.data.value

save_mi_mask_task = gbdx.Task("StageDataToS3",
                            data = mi_mask_dir,
                            destination = out_mi_mask_dir)

############# Mutual Information v10
mi_task = gbdx.Task("mi_setup", 
                       vnirPort = vnir_imd_dir,
                       swirPort = swir_imd_dir, 
                       acompPort = acomp_dir,
                       classPort = mi_mask_dir, 
                       resamplingKernel = 'nearestNeighbour', # bilinear, bicubic
                       useAComp = True, 
                       lulcMask = True,
                       waterMask = False,
                       cloudMask = False,
                       darkMask = True,
                       buildVrt = True,
                       buildAComp = False,
                       buildClassifier = False,
                       buildMask = True,
                       buildAlignImages = True)

# Wierd Gregory arguments 
dockerRoot = "/mnt/work/"
mi_task.inputs.vnirDir = os.path.join(dockerRoot, "input/vnirPort")
mi_task.inputs.swirDir = os.path.join(dockerRoot, "input/swirPort")
mi_task.inputs.acompDir = os.path.join(dockerRoot, "input/acompPort")
mi_task.inputs.classDir = os.path.join(dockerRoot, "input/classPort")
mi_task.inputs.outDir = os.path.join(dockerRoot, "output/outPort")
mi_task.inputs.tmpDir = os.path.join(dockerRoot, "output/tmpPort")
mi_task.inputs.statusFile = os.path.join(dockerRoot, "status.json")

# Name EC2 directories
mi_out_dir = mi_task.outputs.outPort.value
mi_tmp_dir = mi_task.outputs.tmpPort.value

save_mi_tmp_task = gbdx.Task("StageDataToS3",
                            data = mi_tmp_dir,
                            destination = out_mi_tmp_dir)

############# Stack MI SWIR on MI VNIR 
cmd44 = "infile=`ls $indir/*-A*.TIF`; "  # Note: back-ticks not single quotes
cmd44 += 'infname=$(basename "$infile" .TIF); '  
cmd44 += "infprefix=${infname::34}; "
cmd44 += "outfname=$infprefix'_ACOMP_SCUBE.TIF'; "
cmd44 += "gdal_merge.py -separate -o $outdir/$outfname $indir/*-M*.TIF $indir/*-A*.TIF"
stack_task = gbdx.Task("gdal-cli",
                      command = cmd44,
                      data = mi_out_dir,
                      execution_strategy = 'runonce')

scube_dir = stack_task.outputs.data.value

save_scube_task = gbdx.Task("StageDataToS3",
                            data = scube_dir,
                            destination = out_scube_dir)

# ########### Resample Water Mask to Supercube and cut to the overlap.
rc_water_scube_task = gbdx.Task("resample_and_cut_001",
                    input_A = water_vnir_dir,
                    input_B = scube_dir,
                    nodata_A='-1',
                    r_meth='near',
                    prefixLen='34', # Stops prior to part name
                    osuffA='ACOMP_WATER_MASK')

water_scube_dir = rc_water_scube_task.outputs.out_A.value

save_water_scube_task = gbdx.Task("StageDataToS3",
                            data = water_scube_dir,
                            destination = out_water_scube_dir)

########### Resample Cloud Mask to Supercube and cut to the overlap.
rc_cloud_scube_task = gbdx.Task("resample_and_cut_001",
                    input_A = cloud_vnir_dir,
                    input_B = scube_dir,
                    nodata_A='-1',
                    r_meth='near',
                    prefixLen='34', # Stops prior to part name 
                    osuffA='ACOMP_CLOUD_MASK')

cloud_scube_dir = rc_cloud_scube_task.outputs.out_A.value

save_cloud_scube_task = gbdx.Task("StageDataToS3",
                            data = cloud_scube_dir,
                            destination = out_cloud_scube_dir)

############# Compute Material Layers
# SRCXXX is an input symbol in the DGLayers recipe 
layers_task = gbdx.Task("DGLayers",  
                     SRC1_SCUBE = scube_dir, 
                     SRC2_CLOUD = cloud_scube_dir,
                     SRC3_WATER = water_scube_dir,
                     generate_top_dir = 'True',
                     recipe_dir = recipe_dir, 
                     recipe_filename = recipe_filename)

layers_dir = layers_task.outputs.DST_LAYERS.value

save_layers_task = gbdx.Task("StageDataToS3",
                          data = layers_dir,
                          destination = out_layers_dir)

####################################################################################

if input_data_is_1b:
    first_task = ughli_task
else:
    first_task = acomp_task

workflow = gbdx.Workflow([ughli_task,
                          save_acomp_task,
                          copy_task,
                          save_vnir_imd_task, 
                          save_swir_imd_task, 
                          rgb_task,
                          save_acomp_rgb_task, 
                          cloud_task,
                          save_cloud_vnir_task,
                          water_task,
                          save_water_vnir_task,
                          union_task,
                          save_mi_mask_task, 
                          mi_task,
                          save_mi_tmp_task,
                          stack_task,
                          save_scube_task,
                          rc_water_scube_task, 
                          save_water_scube_task,
                          rc_cloud_scube_task,
                          save_cloud_scube_task, 
                          layers_task,
                          save_layers_task])

#print workflow.generate_workflow_description()
workflow.execute()
print 
print workflow.id
```

<!--
***************************************************************************
-->

The above workflow should reflect the latest versions of all tasks. Here are the modifications you need to make:
 
* Set **_in_base_dir_** -- this is the top-level S3 input directory that contains your DN data 
* Set **_out_base_dir_** -- this is the top-level S3 output directory
* Set **_dn_dir_**, **_vnir_dn_dir_**, and **_swir_dn_dir_** -- these are the S3 locations of the input DN data that will be AComp'd and Supercube'd
* Set **_recipe_dir_** -- this is the directory containing your DGLayers recipe file **_and any auxiliary text files it refers to_** 
* Set **_recipe_filename_** -- this is the file name of your DGLayers recipe file 
* Set **_out_layers_dir_** -- this is the desired output directory on s3

<!--
***************************************************************************
-->

The above workflow presently calls the following DGLayers recipe file (but you can make your own):

**mining_layers_dgl_recipe.txt:**

```shell
#########################################################################
###################   DGLayers Recipe File    ##########################
#########################################################################

# Build Mining Layers -- Masked Indices and Masked Class Map
# Assumes the following input symbols:
# 	SRC1_SCUBE -- AComp'd supercube 0 - 10000 uint16 image
# 	SRC2_CLOUD -- cloud mask with 255 = cloud, 0 = non-cloud
# 	SRC3_WATER -- water mask with 255 = water, 0 = non-water

#------------------------------------------------------------------------
#          Optional file symbols must begin with "FILE_" 
#------------------------------------------------------------------------

FILE_1 = WV3_mineral_indices_small.exp
FILE_2 = WV3_mineral_spectra_small.txt

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
PREFIX_LEN 31
n1i DST_INDICES indices
n1m DST_CLASSMAP classmap
n5s DST_COMBO_MASK comboMask
n3v DST_VEG_POLYS veg_polys
END_RENAME_OUTPUTS

#------------------------------------------------------------------------
#                             Process Flow 
#------------------------------------------------------------------------

#######################
### black fill
#######################

subset_bands --outdirID n1b --indirID SRC1_SCUBE -bands 9
n2b = np.where(n1b == 0, 1, 0).astype(np.bool) 

#######################
### veg mask 
#######################

indices -outdirID n1v -indirID SRC1_SCUBE -indexIDandExp NDVI (B7-B5)/(B7+B5) -noDataValIn 0 -noDataValOut 0 
n2v = np.where(n1v > 0.3, 1, 0).astype(np.bool) 

#######################
### Dark mask 
#######################

indices -outdirID n1d -indirID SRC1_SCUBE -indexIDandExp AVG (B2+B3+B5)/3 -noDataValIn 0 -noDataValOut 0 
n2d = np.where(n1d < 500, 1, 0).astype(np.bool)  

#######################
### Indices 
#######################

# Using the noDataValOut of black fill
indices -outdirID n1i -indirID SRC1_SCUBE -indexIDsFromFile FILE_1 all -noDataValIn -0 -noDataValOut 9999 -deliver

#######################
### Class map
#######################

# Use -rules if want rules file
spec_angle_mapper -outdirID n1m -indirID SRC1_SCUBE -materialIDsFromFile FILE_2 all -defAngThreshRad 0.175 -noDataValIn 0 -noDataValOut 255 -deliver

#######################
### Merge Masks
#######################

### Dark --> 1 
n1s = np.where(n2d, 1, 0).astype(np.uint8) 
### Vegetation --> 2
n2s = np.where(n2v, 2, n1s).astype(np.uint8)
### Water --> 3
n3s = np.where(SRC3_WATER, 3, n2s).astype(np.uint8)
### Cloud --> 4 
n4s = np.where(SRC2_CLOUD, 4, n3s).astype(np.uint8)
### Black fill --> 5
n5s = np.where(n2b, 5, n4s).astype(np.uint8) -deliver

#######################
### Veg Polygons
#######################

polygonize --outdirID n3v --indirID n2v --deliver
```

<!--
***************************************************************************
-->

The above recipe file references the following pair of auxiliary files:

**WV3_mineral_indices_small.exp:**

```shell
# ENVI EXPRESSIONS
B5/B3 : Ferric oxide composition
B11/B13 : Laterite
B11/B5 : Gossan
B11/B7 : Ferric oxide content
(B6 + B9) / B8 : WV3 Ferric Iron, Iron2
B14/B16 : Amphibole
B14/(B15+B16) : WV3 Carbonate Index
```

**WV3_mineral_spectra_small.txt:**

```shell
ENVI ASCII Plot File [Thu Apr 13 22:39:42 2017]
Column 1: X Axis
Column 2: alunite1.spc Alunite GDS84 Na03
Column 3: goethit1.spc Goethite WS222
Column 4: hematit2.spc Hematite GDS27
Column 5: jarosit1.spc Jarosite GDS99 K-y 200C
Column 6: muscovi1.spc Muscovite GDS107
Column 7: kaolini1.spc Kaolinite CM9
Column 8: montmor5.spc Montmorillonite CM27
Column 9: calcite1.spc Calcite WS272
   427.399994  0.487077  0.023342  0.020498  0.148245  0.265378  0.658748  0.570649  0.888164
   481.899994  0.569597  0.037919  0.020564  0.289171  0.440956  0.711892  0.666749  0.932836
   547.099976  0.690354  0.115554  0.033976  0.455857  0.519117  0.750877  0.735990  0.940587
   604.299988  0.779987  0.198295  0.150544  0.571353  0.563403  0.765593  0.758684  0.944833
   660.099976  0.814578  0.207331  0.204799  0.658325  0.602790  0.768714  0.766208  0.946470
   722.700012  0.846923  0.256384  0.292346  0.732752  0.645155  0.775495  0.776951  0.949129
   824.000000  0.857553  0.259180  0.259423  0.545687  0.660149  0.790071  0.776285  0.956332
   913.599976  0.848026  0.227457  0.288944  0.442332  0.657636  0.782465  0.756181  0.958576
  1209.099976  0.861922  0.477551  0.749020  0.595431  0.715096  0.779794  0.762423  0.962938
  1571.599976  0.738906  0.552991  0.833831  0.766949  0.792398  0.791024  0.752381  0.958077
  1661.099976  0.719835  0.534704  0.833675  0.812515  0.798399  0.790810  0.766538  0.955768
  1729.500000  0.637763  0.531958  0.834966  0.804248  0.799671  0.772994  0.753937  0.940535
  2163.699951  0.283338  0.560218  0.822459  0.575042  0.599858  0.363176  0.559239  0.877023
  2202.199951  0.340376  0.545391  0.813539  0.495288  0.425050  0.340700  0.461802  0.881524
  2259.300049  0.521631  0.523693  0.803009  0.439641  0.583838  0.424930  0.537936  0.775606
  2329.199951  0.432153  0.491270  0.788937  0.572383  0.489974  0.355986  0.479090  0.626139
```

<!--
***************************************************************************
-->

To test the workflow on the above DGLayers recipe file, copy the recipe file and its two auxiliary files (create the files using cut and paste out of this document) to your desired recipe directory on S3, set the directory paths in the workflow as appropriate, and run. 















