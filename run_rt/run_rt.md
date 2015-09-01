## Basic usage

1. The basic way to run roadtracker in gbd is to have a run_config.json file in the same directory as the intended raster file to be extracted. 
2. The ability to run vector update and automated RT are available. 
  1. If you want to run vector update the input shapefile needs to be in the directory too. 
  2. If the input shapefile does not exist the missingfeatures tag needs to be "true" in the run_config.json.  

## Example run_configs for RoadTracker
Along with running RT in gbdx, the same Run_RT.py file can be run locally in Linux or Windows. The only requirement is the run_configs.json file (this can be renamed for local (or clustered) runs).

Example run_configs are in this repository directory (these need to be named run_config.json in the directory for gbd):

1. example_input_gbd.json - typical run for fully automated (could be vector update + fill in missing features if shapefile is there) 

## Different feature modes that RoadTracker can handle

1. Dirt Urban - Clustered areas where the streets are dirt or dirty. This is also good when you don't know any better
2. trails - features that are 10 meters or less in width (unless very low resolution imagery) that are light compared to its background. ability to be more free form.
3. rivers - same as trails except dark compared to background. There is some more filtering here to try and capture dark rivers.
4. suburban - Intended to pick up roads/features that have low textures
5. Oil Fields - intended to pick up dirt roads that access oil fields.
