# AComp VNIR + Cloud + Water from DN VNIR GBDX Workflow 

Developer of this workflow: Seth Malitz

Description: TBD

**_Workflow:_** 

```shell
import os
from gbdxtools import Interface
gbdx = Interface()

# Need trailing slash
in_base_dir = "s3://XXXXXXXXX/"
out_base_dir = "s3://XXXXXXXXXX/"
print out_base_dir

####### INPUTS #######
input_data_is_1b = True  
if input_data_is_1b:
    vnir_reproj_res = "2.0" #<------------------------------------ change to whatever you like
dn_vnir_dir = os.path.join(in_base_dir, "XXXXXXXXXX")

####### OUTPUTS #######
out_acomp_vnir_dir = os.path.join(out_base_dir, "ACOMP_VNIR")
out_water_vnir_dir = os.path.join(out_base_dir, "WATER_VNIR")
out_cloud_vnir_dir = os.path.join(out_base_dir, "CLOUD_VNIR")

###### DEBUG OUTPUTS ################
if input_data_is_1b:
    out_acomp_old_dir = os.path.join(out_base_dir, "Ortho_ACompOld")
    out_acomp_new_dir = os.path.join(out_base_dir, "Ortho_ACompNew")
else:
    out_acomp_old_dir = os.path.join(out_base_dir, "ACOMP_OLD")
    out_acomp_new_dir = os.path.join(out_base_dir, "ACOMP_NEW")

####################################################################################

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#     Build Water and Cloud Mask -- use old (default) AC gain offsets          
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# Ughli and AComp -- mixing model on. 
if input_data_is_1b:
    ############## Orthorectify 1B and AComp -- ALSO converts to UTM
    print "Starting with 1B"
    first_task = gbdx.Task('ughli', 
                        data = dn_vnir_dir, #<---------- VNIR only
                        bands = "Multi",                # Suppress PAN and SWIR processing in orthorectify and reproject
                        exclude_bands = "P, All-S",     # Suppress PAN and SWIR processing in AComp
                        epsg_code = "UTM",
                        pixel_size_ms = vnir_reproj_res,
                        compute_noise = "true") #<------- Generates noise files (which we don't need), but usefully mosaics the output

else: # ortho
    ############## Just do AComp #############
    print "Starting with Ortho"
    first_task = gbdx.Task("AComp",
                           data = dn_vnir_dir, #<---------- VNIR only
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
#      Build ortho VNIR -- use new AC gain offsets
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
                        pixel_size_ms = vnir_reproj_res,
                        gain_offset_file = acomp_gain_offset_file,
                        compute_noise = "true") #<------- Generates noise files (which we don't need), but usefully mosaics the output

else: # ortho
    ############## Just do AComp #############
    print "Starting with Orth"
    second_task = gbdx.Task("AComp", 
                           data = dn_vnir_dir, #<---------- VNIR only
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

####################################################################################

workflow = gbdx.Workflow([first_task, # <----------- Call to AComp with default gain offsets
                          move_vnir_old_task,
                          water_task,
                          save_water_vnir_task,
                          cloud_task,
                          save_cloud_vnir_task,
                          second_task, # <---------- Call to AComp with new gain offsets
                          move_vnir_new_task,
                          save_vnir_new_task]) 

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









