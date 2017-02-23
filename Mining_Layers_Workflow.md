# Mining Layers GBDX Workflow Template

This document describes how to modify a supplied Mining Layers GBDX workflow template in order to compute desired mining layers (rasters and polygons) from WV3 DN VNIR and SWIR data with **_Level 3X_** processing. 

The template has two parts: The first part computes a 16-band aligned AComp "supercube" from the 8-band DN VNIR plus 8-band DN SWIR data, as well as pixel-aligned water mask and cloud mask. The second part invokes the DGLayers task on a DGlayers recipe file. The recipe file describes the desired Mining Layers operations and outputs (e.g., indices, SAM classification map, masks, polygons, etc.) 

To learn about the operations that can be called from within a DGLayers recipe file, see the documentation for [DGLayers] 
(https://github.digitalglobe.com/nw002655/dglayers/blob/master/DGLayers-GBDX.md)

<!--
***************************************************************************
-->

**Mining Layers Workflow Template:** 

```shell
import os
from gbdxtools import Interface
gbdx = Interface()

in_base_dir = "s3://gbd-customer-data/58600248-2927-4523-b44b-5fec3d278c09/jm_images/"
out_base_dir = "s3://gbd-customer-data/58600248-2927-4523-b44b-5fec3d278c09/jm_images/Seth_OUT/"

####### INPUTS #######

dn_dir = os.path.join(in_base_dir, "scube_data/")
vnir_dn_dir = os.path.join(dn_dir, "vnir/")
swir_dn_dir = os.path.join(dn_dir, "swir/")

recipe_dir = "s3://gbd-customer-data/58600248-2927-4523-b44b-5fec3d278c09/jm_images/Seth_Temp/Recipes/"
recipe_filename = "mining_layers_dgl_recipe.txt"

####### OUTPUTS (Supercube Processing) #######

out_rgb_dir = os.path.join(out_base_dir, "RGB")
out_scube_dir = os.path.join(out_base_dir, "SCUBE")
out_water_scube_dir = os.path.join(out_base_dir, "WATER")
out_cloud_scube_dir = os.path.join(out_base_dir, "CLOUD")

####### OUTPUTS (DGLayers Processing) #######

out_indices_dir = os.path.join(out_base_dir, "INDICES")
out_classmap_dir = os.path.join(out_base_dir, "CLASSMAP")
out_combo_mask_dir = os.path.join(out_base_dir, "COMBO_MASK")
out_veg_polys_dir = os.path.join(out_base_dir, "VEG_POLYS")

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

####################################################################################
################################## DGLayers ########################################
####################################################################################

# Mining Layers Task 
# SRCXXX is an input symbol in the DGLayers recipe file
layers_task = gbdx.Task("DGLayers_v_3_0", 
                     SRC1_SCUBE = scube_dir, 
                     SRC2_CLOUD = cloud_scube_dir,
                     SRC3_WATER = water_scube_dir,
                     recipe_dir = recipe_dir, 
                     recipe_filename = recipe_filename)

###################################################################################
####################### Write Recipe-Directed Outputs #############################
###################################################################################

# DST_XXX is an output symbol in the DGLayers recipe file
indices_dir = layers_task.outputs.DST_INDICES.value
classmap_dir = layers_task.outputs.DST_CLASSMAP.value
combo_mask_dir = layers_task.outputs.DST_COMBO_MASK.value
veg_polys_dir = layers_task.outputs.DST_VEG_POLYS.value

save_indices_task = gbdx.Task("StageDataToS3",
                          data = indices_dir,
                          destination = out_indices_dir)

save_classmap_task = gbdx.Task("StageDataToS3",
                          data = classmap_dir,
                          destination = out_classmap_dir)

save_combo_mask_task = gbdx.Task("StageDataToS3",
                          data = combo_mask_dir,
                          destination = out_combo_mask_dir)

save_veg_polys_task = gbdx.Task("StageDataToS3",
                          data = veg_polys_dir,
                          destination = out_veg_polys_dir)

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
                          save_cloud_scube_task,
                          layers_task,
                          save_indices_task,
                          save_classmap_task,
                          save_combo_mask_task,
                          save_veg_polys_task])

workflow.execute()
print(workflow.id)
```

<!--
***************************************************************************
-->

The above template should reflect the latest versions of all tasks. Here are the modifications you need to make:
 
* Set **_in_base_dir_** -- this is the top-level S3 input directory that contains your DN data 
* Set **_out_base_dir_** -- this is the top-level S3 output directory
* Set **_dn_dir_**, **_vnir_dn_dir_**, and **_swir_dn_dir_** -- these are the S3 locations of the input DN data that will be AComp'd and Supercube'd
* Set **_recipe_dir_** -- this is the directory containing your DGLayers recipe file **_and any auxiliary text files it refers to_** 
* Set **_recipe_filename_** -- this is the file name of your DGLayers recipe file 

* In the section of the template entitled, **_OUTPUTS (DGLayers Processing)_**, set the output subdirectories that you want in your **_out_base_dir_**. These subdirectories correspond (perhaps in one-to-many fashion) with the output directory symbols in your DGLayers recipe file.

* In the section of the template entitled, **_Write Recipe-Directed Outputs_**, write the save-tasks that correspond to directory output symbols in your DGLayers recipe. These save-tasks will write the the DGlayers output data to S3. 

* Modify the call to *gbdx.Workflow*([...]) so that it calls your save tasks.

<!--
***************************************************************************
-->

The Mining Layers workflow template presently calls the following DGLayers recipe file (but you can make your own):

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
ENVI ASCII Plot File [Wed Aug 24 11:21:49 2016]
Column 1: X Axis
Column 2: alunite1.spc Alunite GDS84 Na03~~2
Column 3: goethit1.spc Goethite WS222~~3
Column 4: gypsum1.spc Gypsum HS333.3B~~4
Column 5: hematit2.spc Hematite GDS27~~5
Column 6: jarosit1.spc Jarosite GDS99 K-y 200C~~6
Column 7: limonite.spc Limonite HS41.3~~7
Column 8: muscovi1.spc Muscovite GDS107~~8
   427.399994  0.487077  0.023342  0.895419  0.020498  0.148245  0.023582  0.265378  0.389181  0.041222  0.055648  0.177140  0.142345  0.265571  0.471871  0.200118  0.658748  0.648114  0.260138  0.340935  0.570649  0.888164  0.780697  0.693244  0.705506
   481.899994  0.569597  0.037919  0.905923  0.020564  0.289171  0.031369  0.440956  0.588914  0.052539  0.062876  0.269411  0.154845  0.326644  0.526917  0.242367  0.711892  0.732614  0.319002  0.389731  0.666749  0.932836  0.807759  0.699244  0.748309
   547.099976  0.690354  0.115554  0.917072  0.033976  0.455857  0.060910  0.519117  0.644921  0.076030  0.090115  0.324034  0.164014  0.376331  0.590195  0.274951  0.750877  0.797609  0.385355  0.457017  0.735990  0.940587  0.840758  0.705941  0.795509
   604.299988  0.779987  0.198295  0.923539  0.150544  0.571353  0.092324  0.563403  0.673246  0.109802  0.196595  0.325179  0.170234  0.367252  0.623303  0.292060  0.765593  0.838528  0.446357  0.537912  0.758684  0.944833  0.861912  0.708092  0.828556
   660.099976  0.814578  0.207331  0.925506  0.204799  0.658325  0.099761  0.602790  0.692656  0.135298  0.260385  0.304228  0.175467  0.337717  0.638282  0.303355  0.768714  0.861047  0.485689  0.570410  0.766208  0.946470  0.875179  0.709690  0.841843
   722.700012  0.846923  0.256384  0.928130  0.292346  0.732752  0.114370  0.645155  0.714574  0.166876  0.326122  0.272294  0.183053  0.307472  0.650707  0.320397  0.775495  0.883248  0.533402  0.603001  0.776951  0.949129  0.884078  0.714398  0.853696
   824.000000  0.857553  0.259180  0.929501  0.259423  0.545687  0.111180  0.660149  0.721669  0.177679  0.285183  0.228578  0.194508  0.316963  0.657145  0.352704  0.790071  0.903059  0.566174  0.623900  0.776285  0.956332  0.889873  0.713725  0.857772
   913.599976  0.848026  0.227457  0.902766  0.288944  0.442332  0.097196  0.657636  0.716115  0.121160  0.310383  0.228897  0.205715  0.313645  0.652819  0.373266  0.782465  0.907327  0.588631  0.637218  0.756181  0.958576  0.872009  0.694795  0.834585
```

<!--
***************************************************************************
-->

To test the Mining Layers workflow template on the above DGLayers recipe file, copy the recipe file and its two auxiliary files (create the files using cut and paste out of this document) to your desired recipe directory on S3, set the directory paths (mentioned above) in the workflow as appropriate, and run. 















