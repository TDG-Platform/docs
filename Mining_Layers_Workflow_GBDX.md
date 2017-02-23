# Mining Layers GBDX Workflow Template

This document describes how to modify the *mining_layers_TOTAL_wf.py* GBDX workflow template script (part of the current repository) in order compute desired mining layers (raster or polygon) from WV3 DN VNIR+SWIR data that has **Level 3X** processing. 

The workflow template has two parts: The first part computes a 16-band AComped aligned "supercube" from the 8-band DN VNIR and and 8-band DN SWIR data, as well as pixel-aligned water mask and cloud mask. The second part executes the DGLayers GBDX task on a DGlayers recipe file that describes the desired Mining Layers computations (e.g., indices, spectral angle mapper, masks, polygons, etc.) 

To learn about the computations that can be called from a DGLayers recipe file, see the documentation for [DGLayers] 
(https://github.digitalglobe.com/nw002655/dglayers/blob/master/DGLayers-GBDX.md)

In customizing the Mining layers workflow template, the portion of the workflow that computes the supercube, water mask, and cloud mask should not be touched. Only the input and output directories, recipe file and path, and recipe-specific Save Tasks are to be modified. 

The template should reflect the latest versions available for all tasks. 

Here is the process for modifying the template workflow. First save the workflow under a new name on your local machine. Then, inside the workflow, do the following:
 
* Set *in_base_dir* -- this is the top-level S3 input directory that contains your DN data 
* Set *out_base_dir* -- this is the top-level S3 output directory
* Set *dn_dir*, *vnir_dn_dir*, and *swir_dn_dir* -- these are the S3 locations of the input DN data that will be AComped and Supercubed
* Set *recipe_dir* -- this is the directory containing your DGLayers recipe and any of its auxiliary files
* Set *recipe_filename* -- this is the file name of your DGLayers recipe file 

* In the workflow section, *OUTPUTS (DGLayers Processing)*, set the output subdirectories that you want in *out_base_dir*. These subdirectories correspond (perhaps in one-to-many fashion) with the output directory symbols in your DGLayers recipe.

* In the workflow section delimited by the banners, *Custom – BEGIN* and *Custom –End*, write the Save Tasks that correspond to directory output symbols in your DGLayers recipe. These Save Tasks will write the the DGlayers output data to S3. 

* Modify the call to *gbdx.Workflow*([...]) so that it calls your Save Tasks.

To test the template workflow on the DGLayers recipe file, *mining_layers_recipe_generic.txt* (part of the current repository), which mentions auxiliary files  

* _general_minerals_for_testing_simplified_WV3.txt_ 
* _general_minerals_for_testing_simplified_WV3.exp_ 

copy all three files to a your desired recipe directory on S3, set the aforementioned directory paths in the workflow appropriately, and run. 


