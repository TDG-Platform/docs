# Information Layers from DN VNIR GBDX Workflow 

Developer of this workflow: Seth Malitz

Description: (TBD polish) If starting from 1B DN VNIR, then orthorectify and AComp. Of starting from ortho DN VNIR, the AComp. In both cases, compute cloud and water, and there is the option to run a DGLayers recipe to produce other derived layers. (Refernce DGLayers link)

**_Workflow:_** 

```shell
import os
import sys
from gbdxtools import Interface
gbdx = Interface()

in_base_dir = "s3://gbd-customer-data/58600248-2927-4523-b44b-5fec3d278c09/seth/"
out_base_dir = os.path.join(in_base_dir, "DGL_OUTPUTS/Test_092517_C/") 
print "out_base_dir = " + out_base_dir

####### INPUTS #######
input_data_is_1b = True  
if input_data_is_1b:
    vnir_reproj_res = "2.0" #<------------------------------------ change to whatever you like
dn_data_dir = os.path.join(in_base_dir, "DGL_DATA/Level_1B/Fullerton/")
dn_vnir_dir = os.path.join(dn_data_dir, "vnir/056518998010_01/")
print "dn_vnir_dir = " + dn_vnir_dir

# Comma-separated list of contiguous parts to process, e.g., "P001,P002"
# To specify all parts, set to "Auto". 
if input_data_is_1b:
    vnir_parts_str = "Auto"

# DGLayers recipe file.
# Assign these items the empty string "" if you do not want to run DGLayers.
recipe_dir = os.path.join(in_base_dir, "DGL_RECIPES/")
recipe_filename = "recipe_cann_092517.txt"
print "recipe_dir = " + recipe_dir
print "recipe_filename = " + recipe_filename

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ DO NOT MODIFY BELOW THIS LINE @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

####### OUTPUTS #######
out_acomp_vnir_dir = os.path.join(out_base_dir, "ACOMP_VNIR")
out_water_vnir_dir = os.path.join(out_base_dir, "WATER_VNIR")
out_cloud_vnir_dir = os.path.join(out_base_dir, "CLOUD_VNIR")
out_layers_dir = os.path.join(out_base_dir, "LAYERS")

###### DEBUG OUTPUTS ################
if input_data_is_1b:
    out_acomp_old_dir = os.path.join(out_base_dir, "Ortho_ACompOld")
    out_acomp_new_dir = os.path.join(out_base_dir, "Ortho_ACompNew")
else:
    out_acomp_old_dir = os.path.join(out_base_dir, "ACOMP_OLD")
    out_acomp_new_dir = os.path.join(out_base_dir, "ACOMP_NEW")

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#     Build Water and Cloud Mask -- use old 2015 (default) AC gain offsets          
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# Ughli and AComp -- mixing model on. 
if input_data_is_1b:
    ############## Orthorectify 1B and AComp -- ALSO converts to UTM
    print "Starting with 1B"
    first_task = gbdx.Task('ughli', 
                        data = dn_vnir_dir, #<---------- VNIR only
                        bands = "Multi",         # Suppress PAN processing in orthorectify and reproject
                        exclude_bands = "P",     # Suppress PAN processing in AComp
                        epsg_code = "UTM",
                        parts = vnir_parts_str, 
                        pixel_size_ms = vnir_reproj_res,
                        compute_noise = "true") #<------- Generates noise files (which we don't need), but usefully mosaics the output

else: # ortho
    ############## Just do AComp #############
    print "Starting with Ortho"
    first_task = gbdx.Task("AComp",
                           data = dn_vnir_dir, #<---------- VNIR only
                           exclude_bands = "P",     # Suppress PAN processing in AComp
                           compute_noise = "true") #<------- Generates noise files (which we don't need), but usefully mosaics the output

acomp_old_dir = first_task.outputs.data.value

"""
save_acomp_old_task = gbdx.Task('StageDataToS3', 
                    data = acomp_old_dir, 
                    destination = out_acomp_old_dir)
"""

############# Move AComp VNIR to its own directory
cmd = "mv $indir/*-M*_ACOMP.TIF $outdir"
move_vnir_old_task = gbdx.Task("gdal-cli",
                      command = cmd,
                      data = acomp_old_dir,
                      execution_strategy = 'runonce')

acomp_vnir_old_dir = move_vnir_old_task.outputs.data.value

############# Water Mask
# Build a water mask boolean raster. water = 255; non-water = 0
water_task = gbdx.Task("protogenV2RAW",
                       raster = acomp_vnir_old_dir)

water_vnir_dir = water_task.outputs.data.value

save_water_vnir_task = gbdx.Task("StageDataToS3",
                            data = water_vnir_dir,
                            destination = out_water_vnir_dir)

############# Cloud Mask
# Build a cloud mask boolean raster. cloud = 255; non-cloud = 0
cloud_task = gbdx.Task("protogenV2RAC",
                       raster = acomp_vnir_old_dir)

cloud_vnir_dir = cloud_task.outputs.data.value

save_cloud_vnir_task = gbdx.Task("StageDataToS3",
                            data = cloud_vnir_dir,
                            destination = out_cloud_vnir_dir)

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#      Build ortho VNIR -- use new 2016 AC gain offsets
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# Gain offsets file
acomp_gain_offset_file = "gainOffsetTable_WV3_2016v0.xml" 

# Ughli and AComp -- mixing model on.
if input_data_is_1b:
    ############## Orthorectify 1B and AComp -- ALSO converts to UTM
    print "Starting with 1B"
    second_task = gbdx.Task('ughli', 
                        data = dn_vnir_dir, #<---------- VNIR only
                        bands = "Multi",                # Suppress PAN and SWIR processing in orthorectify and reproject
                        exclude_bands = "P, All-S",     # Suppress PAN and SWIR processing in AComp
                        epsg_code = "UTM",
                        parts = vnir_parts_str, 
                        pixel_size_ms = vnir_reproj_res,
                        gain_offset_file = acomp_gain_offset_file,
                        compute_noise = "true") #<------- Generates noise files (which we don't need), but usefully mosaics the output

else: # ortho
    ############## Just do AComp #############
    print "Starting with Orth"
    second_task = gbdx.Task("AComp", 
                           data = dn_vnir_dir, #<---------- VNIR only
                           exclude_bands = "P",     # Suppress PAN processing in AComp
                           gain_offset_file = acomp_gain_offset_file,
                           compute_noise = "true")

acomp_new_dir = second_task.outputs.data.value

"""
save_acomp_new_task = gbdx.Task('StageDataToS3', 
                    data = acomp_new_dir, 
                    destination = out_acomp_new_dir)
"""

############# Move AComp VNIR to its own directory
cmd = "mv $indir/*-M*_ACOMP.TIF $outdir"
move_vnir_new_task = gbdx.Task("gdal-cli",
                      command = cmd,
                      data = acomp_new_dir,
                      execution_strategy = 'runonce')

acomp_vnir_new_dir = move_vnir_new_task.outputs.data.value

save_vnir_new_task = gbdx.Task('StageDataToS3', 
                    data = acomp_vnir_new_dir, 
                    destination = out_acomp_vnir_dir)

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#                          Call DGLayers 
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# SRCXXX is an input symbol in the DGLayers recipe 
layers_task = gbdx.Task("DGLayers",  
                     SRC1_VNIR = acomp_vnir_new_dir, 
                     SRC2_CLOUD = cloud_vnir_dir,
                     SRC3_WATER = water_vnir_dir,
                     generate_top_dir = 'True',
                     recipe_dir = recipe_dir, 
                     recipe_filename = recipe_filename)

layers_dir = layers_task.outputs.DST_LAYERS.value

save_layers_task = gbdx.Task("StageDataToS3",
                          data = layers_dir,
                          destination = out_layers_dir)

####################################################################################

task_list = [first_task, # <----------- Call to AComp with default gain offsets
             move_vnir_old_task,
             water_task,
             save_water_vnir_task,
             cloud_task,
             save_cloud_vnir_task,
             second_task, # <---------- Call to AComp with new gain offsets
             move_vnir_new_task,
             save_vnir_new_task]

if recipe_dir and recipe_filename:
    task_list += [layers_task, save_layers_task]

workflow = gbdx.Workflow(task_list) 

#print workflow.generate_workflow_description()
workflow.execute()
print 
print workflow.id
```

<!--
***************************************************************************
-->

Here are the modifications you need to make to the above workflow for your application:
 
* Set **_in_base_dir_** -- this is the top-level S3 input directory that contains your DN input data 
* Set **_out_base_dir_** -- this is your  top-level S3 output directory
* Set **_input_data_is_1b_** -- (True/False) this indicates whether the input DN VNIR data is Level 1B or Orthorectified
* Set **_vnir_reproj_res_** -- these are the target reprojection resolution when converting 1B to UTM
* Set **_dn_vnir_dir_** -- this the S3 locationsof your DN VNIR input data 
* Set **_vnir_parts_str_** -- TBD
* Set **_recipe_dir_** -- TBD
* Set **_recipe_filename_** -- TBD









