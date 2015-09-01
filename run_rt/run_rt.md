The basic way to run roadtracker in gbd is to have a run_config.json file in the same directory as the intended raster file to be extracted. The ability to run vector update and automated RT are available. If you want to run vector update the input shapefile needs to be in the directory too. If the input shapefile does not exist the missingfeatures tag needs to be "true" in the run_config.json.  

Example run_configs are in this directory (these need to be named run_config.json in the directory): 
example_input_gbd.json - typical run for fully automated (could be vector update + fill in missing features if shapefile is there) 
example_input_gbd_full.json - all options that are available now


The different features you can have are
Dirt Urban
trails
rivers
suburban
Oil Fields
