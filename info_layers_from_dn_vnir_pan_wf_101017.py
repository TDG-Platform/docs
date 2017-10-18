import os
import sys
from gbdxtools import Interface
gbdx = Interface()

in_base_dir = "s3://gbd-customer-data/58600248-2927-4523-b44b-5fec3d278c09/seth/"
out_base_dir = os.path.join(in_base_dir, "DGL_OUTPUT/Test_101117_D/") 
print "out_base_dir = " + out_base_dir

####### INPUTS #######
input_data_is_1b = True  
if input_data_is_1b:
    vnir_reproj_res = "2.0"
    pan_reproj_res = "0.5"
dn_data_dir = ""
dn_vnir_dir = "s3://receiving-dgcs-tdgplatform-com/056576499010_01_003/"
print "dn_vnir_dir = " + dn_vnir_dir

# Comma-separated list of contiguous parts to process, e.g., "P001,P002"
# To specify all parts, set to "Auto". 
if input_data_is_1b:
    vnir_parts_str = "Auto"

# DGLayers recipe file.
# Assign these items the empty string "" if you do not want to run DGLayers.
recipe_dir = os.path.join(in_base_dir, "DGL_RECIPES/")
recipe_filename = "recipe_vnir_small_test.txt"
print "recipe_dir = " + recipe_dir
print "recipe_filename = " + recipe_filename

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ DO NOT MODIFY BELOW THIS LINE @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

####### OUTPUTS #######
out_acomp_rc_pan_dir = os.path.join(out_base_dir, "ACOMP_PAN_AT_VNIR_RES")
out_acomp_vnir_dir = os.path.join(out_base_dir, "ACOMP_VNIR")
out_water_vnir_dir = os.path.join(out_base_dir, "WATER_VNIR")
out_cloud_vnir_dir = os.path.join(out_base_dir, "CLOUD_VNIR")
out_layers_dir = os.path.join(out_base_dir, "LAYERS")

###### DEBUG OUTPUTS ################
out_water_vnir_dir_00 = os.path.join(out_base_dir, "WATER_VNIR_00")
out_cloud_vnir_dir_00 = os.path.join(out_base_dir, "CLOUD_VNIR_00")
out_acomp_vnir_dir_00 = os.path.join(out_base_dir, "ACOMP_VNIR_00")
out_acomp_pan_dir = os.path.join(out_base_dir, "ACOMP_PAN")
if input_data_is_1b:
    out_acomp_old_dir = os.path.join(out_base_dir, "UTM_ACompOld")
    out_acomp_new_dir = os.path.join(out_base_dir, "UTM_ACompNew")
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
                        data = dn_vnir_dir,
                        bands = "Multi",         # Only orthorectify the VNIR
                        exclude_bands = "P",     # Exclude Pan from AComp
                        epsg_code = "UTM",
                        parts = vnir_parts_str, 
                        pixel_size_ms = vnir_reproj_res,
                        compute_noise = "false") #<---- Despite this being set to "false", the output is now getting mosaicked! smalitz 10/10/17

else: # ortho
    ############## Just do AComp #############
    print "Starting with Ortho"
    first_task = gbdx.Task("AComp",
                           data = dn_vnir_dir, 
                           exclude_bands = "P",     # Exclude Pan from AComp
                           compute_noise = "false") # <--- "false" yields mosaicked output?

acomp_old_dir = first_task.outputs.data.value

save_acomp_old_task = gbdx.Task('StageDataToS3', 
                    data = acomp_old_dir, 
                    destination = out_acomp_old_dir)

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

water_vnir_dir_00 = water_task.outputs.data.value

save_water_vnir_task_00 = gbdx.Task("StageDataToS3",
                            data = water_vnir_dir_00,
                            destination = out_water_vnir_dir_00)

############# Cloud Mask
# Build a cloud mask boolean raster. cloud = 255; non-cloud = 0
cloud_task = gbdx.Task("protogenV2RAC",
                       raster = acomp_vnir_old_dir)

cloud_vnir_dir_00 = cloud_task.outputs.data.value

save_cloud_vnir_task_00 = gbdx.Task("StageDataToS3",
                            data = cloud_vnir_dir_00,
                            destination = out_cloud_vnir_dir_00)

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#    Build ortho and AComp VNIR and Pan -- use new 2016 AC gain offsets
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# Gain offsets file
acomp_gain_offset_file = "gainOffsetTable_WV3_2016v0.xml" 

# Ughli and AComp -- mixing model on.
if input_data_is_1b:
    ############## Orthorectify 1B and AComp -- ALSO converts to UTM
    second_task = gbdx.Task('ughli', 
                        data = dn_vnir_dir, #<---------- VNIR or VNIR+Pan only
                        bands = "Multi,P", # Ortho the VNIR and PAN                  
                        epsg_code = "UTM",
                        parts = vnir_parts_str, 
                        pixel_size_ms = vnir_reproj_res,
                        pixel_size_pan = pan_reproj_res,
                        gain_offset_file = acomp_gain_offset_file,
                        compute_noise = "false") #<---- Despite this being set to "false", the output is now getting mosaicked! smalitz 10/10/17

else: # ortho
    ############## Just do AComp #############  
    second_task = gbdx.Task("AComp", 
                           data = dn_vnir_dir, #<---------- VNIR or VNR+PAN only    
                           gain_offset_file = acomp_gain_offset_file,
                           compute_noise = "false") #<--- mosaicked output still happening?

acomp_new_dir = second_task.outputs.data.value

save_acomp_new_task = gbdx.Task('StageDataToS3', 
                    data = acomp_new_dir, 
                    destination = out_acomp_new_dir)

############# Move AComp VNIR and ACOMP Pan to their own directories

cmd = "mkdir $outdir/dataP $outdir/dataV; "
cmd += "mv $indir/data/*-M*_ACOMP.TIF $outdir/dataV; "
cmd += "mv $indir/data/*-P*_ACOMP.TIF $outdir/dataP"
move_pan_vnir_new_task = gbdx.Task('gdal-cli-multiplex')
move_pan_vnir_new_task.inputs.data = acomp_new_dir
move_pan_vnir_new_task.inputs.command = cmd
move_pan_vnir_new_task.execution_strategy='runonce'         

acomp_vnir_new_dir = move_pan_vnir_new_task.outputs.dataV.value
acomp_pan_new_dir = move_pan_vnir_new_task.outputs.dataP.value

save_vnir_new_task = gbdx.Task('StageDataToS3', 
                    data = acomp_vnir_new_dir, 
                    destination = out_acomp_vnir_dir_00)

save_pan_new_task = gbdx.Task('StageDataToS3', 
                    data = acomp_pan_new_dir, 
                    destination = out_acomp_pan_dir)

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#      BEGIN -- Pan Texture
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#      END -- Pan Texture
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

############# Resample PAN to VNIR and cut to the overlap.
rc_pan_vnir_task = gbdx.Task("resample_and_cut_001",
                    input_A = acomp_pan_new_dir,
                    input_B = acomp_vnir_new_dir,
                    nodata_A  = '0',
                    r_meth = 'dg_average', #<------------------- max?
                    prefixLen = '34', 
                    osuffA = 'ACOMP_RC',
                    osuffB = 'ACOMP_CUT')

rc_pan_dir = rc_pan_vnir_task.outputs.out_A.value
rc_vnir_dir = rc_pan_vnir_task.outputs.out_B.value

save_rc_vnir_task = gbdx.Task("StageDataToS3",
                            data = rc_vnir_dir,
                            destination = out_acomp_vnir_dir)

save_rc_pan_task = gbdx.Task("StageDataToS3",
                            data = rc_pan_dir,
                            destination = out_acomp_rc_pan_dir)

# ########### Resample Water Mask to VNIR and cut to the overlap.
rc_water_task = gbdx.Task("resample_and_cut_001",
                    input_A = water_vnir_dir_00,
                    input_B = rc_vnir_dir,
                    nodata_A='-1',
                    r_meth='near',
                    prefixLen='34', # Stops prior to part name
                    osuffA='ACOMP_WATER_MASK')

water_vnir_dir = rc_water_task.outputs.out_A.value

save_water_vnir_task = gbdx.Task("StageDataToS3",
                            data = water_vnir_dir,
                            destination = out_water_vnir_dir)

########### Resample Cloud Mask to Supercube and cut to the overlap.
rc_cloud_task = gbdx.Task("resample_and_cut_001",
                    input_A = cloud_vnir_dir_00,
                    input_B = rc_vnir_dir,
                    nodata_A='-1',
                    r_meth='near',
                    prefixLen='34', # Stops prior to part name 
                    osuffA='ACOMP_CLOUD_MASK')

cloud_vnir_dir = rc_cloud_task.outputs.out_A.value

save_cloud_vnir_task = gbdx.Task("StageDataToS3",
                            data = cloud_vnir_dir,
                            destination = out_cloud_vnir_dir)

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#                          Call DGLayers 
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

layers_task = gbdx.Task("DGLayers",  
                        SRC1_VNIR = rc_vnir_dir, 
                        SRC2_CLOUD = cloud_vnir_dir,
                        SRC3_WATER = water_vnir_dir,
                        SRC4_PAN = rc_pan_dir,
                        generate_top_dir = 'True',
                        recipe_dir = recipe_dir, 
                        recipe_filename = recipe_filename)
layers_task.domain = 'r44xlarge'
#layers_task.timeout = 36000 

layers_dir = layers_task.outputs.DST_LAYERS.value

save_layers_task = gbdx.Task("StageDataToS3",
                          data = layers_dir,
                          destination = out_layers_dir)

####################################################################################

task_list = [first_task, # <----------- Call to AComp with default gain offsets
             move_vnir_old_task,
             water_task,
             save_water_vnir_task_00,
             cloud_task,
             save_cloud_vnir_task_00,
             second_task, # <---------- Call to AComp with new gain offsets
             move_pan_vnir_new_task,
             #save_vnir_new_task,
             #save_pan_new_task,
             rc_pan_vnir_task,
             save_rc_vnir_task,
             save_rc_pan_task,
             rc_water_task,
             save_water_vnir_task,
             rc_cloud_task,
             save_cloud_vnir_task]

if recipe_dir and recipe_filename:
    task_list += [layers_task, save_layers_task]

workflow = gbdx.Workflow(task_list) 

#print workflow.generate_workflow_description()
workflow.execute()
print 
print workflow.id