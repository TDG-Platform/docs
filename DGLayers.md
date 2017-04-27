# DGLayers GBDX Task

The DGLayers GBDX task is a general-purpose recipe-driven workflow engine that is useful 
for generating a wide variety of derived layers from input raster data (**_TIFF only_**). Output layers can be raster 
layers or polygon vector layers. A DGLayers recipe is a text file that describes a sequence of layer functions 
participating a flow graph without loops. 

A DGLayers recipe can call almost any Python array function in the numpy and scipy libraries. It can also call any of 
roughly two dozen built-in functions, including: a fast polygonize (much faster than gdal_polygonize), morphological 
cleaning operations, spectral indices, spectral angle mapper, class coalesce 
in a thematic map, dynamic range adjustment, high-quality edge computation, etc. 

Building a recipe and running DGLayers on that recipe should be considered an alternative to using the gdal-cli and gdal-cli-multiplex GBDX tasks, or building a new GBDX task, or building a GBDX workflow that chains together GBDX tasks. Here's why:

* Compared to gdal_cli and gdal-cli-multiplex, which allow numpy calls via gdal_calc, the DGLayers task additionally allows for calls to other Python libraries (e.g., scipy). Additionally, DGLayers recipe syntax is more user-friendly than gdal_calc syntax.

* DGLayers better supports rapid prototyping than gdal_cli and gdal_cli_multiplex. (Additionally, if DG internal, you can pull docker from docker hub and prototype locally.)


* Each GBDX task in a GBDX workflow incurs I/O between an EC2 machine and S3, whereas each function call in a DGLayers recipe incurs I/O only from the EC2 to the EC2 

* Building a new recipe for DGLayers does not involve the overhead associated with building a new GBDX task (Docker, JSON, registration, Github, etc.)   

* DGLayers, when run in "batch mode", can deliver parallelism across the cores of an EC2 instance

* DGLayers automatically names intermediate files and output files

Input rasters can be single band or multi-band, and of any data type. **_Input raster files 
can be arbitrarily large_**. DGLayers will decompose large rasters into strips for processing and 
then reassemble at the end. **_Input raster files must have .tif or .TIF endings_**.

Input raster data is presented to DGLayers in one or more input directories, each with one or more raster files.
If there are multiple input directories, each with a single raster, then those rasters must be 
**_consistent_** with each other, that is to say, they must be pixel-aligned, same resolution, same extent, 
but do not have to have the same number of bands. 
If there are multiple input directories, each with multiple rasters, then the same number of rasters 
must be in each directory and there must be a correspondence of the following kind across the directories: Suppose 
there are three input directors, A, B, C. Then with respect to the **_lexicographic ordering_** of the files in 
each directory, the first file A1 in A is consistent with the first file B1 in B which is consistent with
the first file C1 in C. Similarly, this must hold for the second file of A, the third file of
A, and so on. The association {A1, B1, C1} is a **_raster group_**. Similarly, {A2, B2, C2} is an
input raster group, and so on. Raster outputs for a raster group are consistent with the rasters in that group. 

There might be one output directory or multiple output directories. The number of files (raster or shape) in each 
output directory is the same as the number of files in each input directory. 
  
The DGLayers GBDX task can be run through a simple Python script using  
[gbdxtools](https://github.com/DigitalGlobe/gbdxtools/blob/master/docs/user_guide.rst), 
which requires some initial setup, 
or through the [GBDX Web Application](https://gbdx.geobigdata.io/materials/).  
Tasks and workflows can be added (described here in 
[gbdxtools](https://github.com/DigitalGlobe/gbdxtools/blob/master/docs/running_workflows.rst)) 
or run separately after the DGLayers process is completed.

<!--
***************************************************************************
-->

**Example DGLayers Workflow:** 

```shell
	from gbdxtools import Interface
	gbdx = Interface()

	# In this example SRC1, SRC2, and SRC3 are input port/directory symbols that appear in the 
	# DGLayers recipe file. Each of these input directories must have the same number of 
	# TIFF raster files. In the lexicographic ordering: "SRC1" < "SRC2" < "SRC3". So the 
	# file names in directory SRC1 will be used to name the output files. 
	dgl_task = gbdx.Task("DGLayers", 
					 SRC1 = 's3://my_dir/my_indir_1/', 
					 SRC2 = 's3://my_dir/my_indir_2/', 
					 SRC3 = 's3://my_dir/my_indir_3/', 
					 recipe_dir = 's3://my_dir/my_recipes/', 
					 recipe_filename = 'my_recipe.txt',
					 generate_top_dir = 'False') 
					 
	workflow = gbdx.Workflow([dgl_task])

	# DST_1 and DST_2 are output port/directory symbols that appears in the DGLayers recipe file.  	
	workflow.savedata(dgl_task.outputs.DST_1.value, location='my_outdir_1')
	workflow.savedata(dgl_task.outputs.DST_2.value, location='my_outdir_2')

	# The LOGS symbol does not appear in the DGLayers recipe file. It denotes a
	# generated output directory of log files that is created by default.	
	workflow.savedata(dgl_task.outputs.LOGS.value, location='my_outdir_logs')	

	workflow.execute()
	print workflow.id
```	

**Example DGLayers Workflow:** 

```shell
	from gbdxtools import Interface
	gbdx = Interface()

	# In this example SRC1, SRC2, and SRC3 are input directory symbols that appear in the 
	# DGLayers recipe file. Each of these input directories must have the same number of 
	# TIFF raster files. In the lexicographic ordering: "SRC1" < "SRC2" < "SRC3". So the 
	# file names in directory SRC1 will be used to name the output files. 
	dgl_task = gbdx.Task("DGLayers", 
					 SRC1 = 's3://my_dir/my_indir_1/', 
					 SRC2 = 's3://my_dir/my_indir_2/', 
					 SRC3 = 's3://my_dir/my_indir_3/', 
					 recipe_dir = 's3://my_dir/my_recipes/', 
					 recipe_filename = 'my_recipe.txt',
					 generate_top_dir = 'True')	#<---------------------- Note
					 
	workflow = gbdx.Workflow([dgl_task])

	# Because the argument "generate_top_dir" was set to 'True' in the above call to dgl_task,
	# a single top-level output port/directory, DST_LAYERS, will be created that contains 
	# subdirectories corresponding to the output symbols in the DGLayers recipe file. These 
	# sub-directories will not have output ports of their own. The advantage of a top-level 
	# DST_LAYERS port is that the workflow does not need to know what output
	# subdirectories are specified by the recipe file. This workflow is thus completely 
	# decoupled from the recipe file. 
	workflow.savedata(dgl_task.outputs.DST_LAYERS.value, location='my_outdir')

	workflow.execute()
	print workflow.id
```

The following is an associated recipe file 
for the above workflows. In this recipe, it is assumed that SRC2 and SRC3 contain single-band 
0/1 TIFF files and SRC1 is an arbitrary single-band TIFF file. 

**Example Recipe File:** 

```shell
	#########################################################################
	###################   DGLayers Recipe File    ###########################
	#########################################################################

	BEGIN_RENAME_OUTPUTS
	PREFIX_LEN 31
	n0 DST_1 union_mask
	n5 DST_2 burn
	END_RENAME_OUTPUTS

	n0 = np.logical_or(SRC2, SRC3) --deliver
	n5 = np.where(n0, 255, SRC1) --deliver
```	
 
<!--
***************************************************************************
-->

**REQUIRED SETTINGS AND DEFINITIONS:**

* One or more directory locations that contain input TIFF data: 
	* required: 'True' 
	* type: 'directory'	
    * name: 'SRC' (or any name that begins with 'SRC', e.g., 'SRC', 'SRC1', 'SRC2_vnir')
	
* Directory containing the recipe file and **_all auxiliary files it mentions_**:
	* required: 'True' 
	* type: 'directory' 
    * name: 'recipe_dir' 

* Name of the recipe file:
	* required: 'True' 
	* type: 'string' 
    * name: 'recipe_filename' 
	
* Create just one output port, DST_LAYERS, that contains subdirectories ('True' or 'False')? If 'False' then an output port is created for each symbol beginning "DST" in the recipe file:
	* required: 'True' 
	* type: 'string' 
    * name: 'generate_top_dir' 	

**OPTIONAL SETTINGS:**

* Number of processing cores to use on EC2 machine (beneficial only with multiple raster groups):	
	* required: 'False' 
	* type: 'string'	
    * name: 'num_cpus'
	
<!--
***************************************************************************
-->

## Recipe File 

A DGLayers recipe file mentions symbols (directory IDs) and commands (layer operations). 
Symbols that begin with "SRC" represent input raster (source) directories.
Symbols that begin with "DST" represent output (destination) directories.
Symbols that begin "Nx" or "nx", where x is a digit, represent derived directories 
that are local to the EC2 instance. Symbols can be viewed as nodes in a flow graph. 
Each command can be viewed as a many-to-one "funnel-arc" from one or more input nodes to 
a single output node. The resulting flow graph must not contain cycles. 

Other aspects of recipe syntax:

* Comment lines begin with "#". White space lines are ignored. 

* All source (input) directory ID's must begin with "SRC". Examples: SRC, SRC1, SRC2_DSM. Suppose your source symbols are SRC1_fred, SRC2_bill, SRC3_ted. Since "SRC1_fred" is the first symbol in the lexicographic ordering of the symbols, its file names will be used in the naming of the output files generated by DGLayers. 

* All derived directory ID's must begin with 'Nx' or 'nx' where "x" **_is a digit_**. Examples include: N2, n35A, n4_tree_mask. **_However, double underscore in the ID is not allowed_**.

* All persistent output directory ID's must be renamed so as to begin with "DST". Examples: DST, DST_2, DST33, DST_NDVI 

* Putting the "--deliver" option after any command indicates that the output node represents a persistent (deliverable) output directory. If you do not specifying this option, the directory is not available for output and will be erased.

* To indicate that all derived directories are to be deliverable, use the DELIVER_ALL tag prior the command sequence

* To suppress a passage of the recipe, bracket the passage between tags BEGIN_IGNORE and END_IGNORE 

* To exit the recipe early, put the EXIT tag at the desired location

Further illustrations of recipe syntax are shown in the examples below.

<!--
***************************************************************************
-->

**Example Recipe File:** 

```shell
#########################################################################
###################   DGLayers Recipe File    ###########################
#########################################################################

# Big White Stuff (cloud finding)
# Assumes the following input symbols:
#		SRC - directory of RGB images of USHORT data type

#------------------------------------------------------------------------
#	Rename output directories and files.
# 	Use sandwiched pair: BEGIN_RENAME_OUTPUTS, END_RENAME_OUTPUTS
#   PREFIX_LEN <j>: means preserve the first j characters of SRC input 
#       file names to use in the names of corresponding output files. 
#   Triplets of form: <outdir_id> <outdir_name> <suffix>. Indicates 
#   	that directory <outdir_id> is to be renamed <outdir_name> and 
#		that the file names will involve the suffix string <suffix>
#------------------------------------------------------------------------

BEGIN_RENAME_OUTPUTS
PREFIX_LEN 31
n3 DST_CLOUD cloud
n4 DST_CLOUD_POLY cloud_poly
END_RENAME_OUTPUTS

#------------------------------------------------------------------------
#             				Process Flow 
#------------------------------------------------------------------------

###### Compute the mean across the bands 
n1 = np.mean(SRC, axis=0).astype(np.uint16)

###### Threshold for bright: True for x > 50; False otherwise.
n2 = np.where(n1 > 50, True, False).astype(np.bool) 

###### Binary closure on True 
n3 = binary_closing_dgl(n2, rad_mtrs=20) --deliver

###### Polygonize
polygonize --outdirID n4 --indirID n3 --deliver
```

<!--
***************************************************************************
-->

**Example Recipe File:** 

```shell
#########################################################################
####################   DGLayers Recipe File    ##########################
#########################################################################

# Create Mining Layers -- Indices, SAM class map, and combination mask
# Assumes the following input symbols:
# 	SRC1_SCUBE -- AComp'd supercube 0-10000 uint16 image
# 	SRC2_CLOUD -- cloud mask with 255 = cloud, 0 = non-cloud
# 	SRC3_WATER -- water mask with 255 = water, 0 = non-water

#------------------------------------------------------------------------
#          Optional file symbols must begin with "FILE_" 
#------------------------------------------------------------------------

FILE_1 = WorldView3_mineral_indices_20150424_SMmods.exp
FILE_2 = general_minerals_for_testing_simplified_WV3.txt

#------------------------------------------------------------------------
#	Rename output directories and files.
# 	Use sandwiched pair: BEGIN_RENAME_OUTPUTS, END_RENAME_OUTPUTS
#   PREFIX_LEN <j>: means preserve the first j characters of SRC input 
#       file names to use in the names of corresponding output files. 
#   Triplets of form: <outdir_id> <outdir_name> <suffix>. Indicates 
#   	that directory <outdir_id> is to be renamed <outdir_name> and 
#		that the file names will involve the suffix string <suffix>
#------------------------------------------------------------------------

BEGIN_RENAME_OUTPUTS
PREFIX_LEN 31
n1i DST_INDICES indices
n1m DST_CLASSMAP classmap
n5s DST_COMBO_MASK comboMask
END_RENAME_OUTPUTS

#------------------------------------------------------------------------
#                             Process Flow 
#------------------------------------------------------------------------

##### black fill
subset_bands --outdirID n1b --indirID SRC1_SCUBE -bands 9
n2b = np.where(n1b == 0, 1, 0).astype(np.bool) 

##### veg mask 
indices -outdirID n1v -indirID SRC1_SCUBE -indexIDandExp NDVI (B7-B5)/(B7+B5) -noDataValIn 0 -noDataValOut 0 
n2v = np.where(n1v > 0.3, 1, 0).astype(np.bool) 

##### Dark mask 
indices -outdirID n1d -indirID SRC1_SCUBE -indexIDandExp AVG (B2+B3+B5)/3 -noDataValIn 0 -noDataValOut 0 
n2d = np.where(n1d < 500, 1, 0).astype(np.bool)  

##### Indices 
indices -outdirID n1i -indirID SRC1_SCUBE -indexIDsFromFile FILE_1 all -noDataValIn -0 -noDataValOut 9999 -deliver

##### Class map
spec_angle_mapper -outdirID n1m -indirID SRC1_SCUBE -materialIDsFromFile FILE_2 all -defAngThreshRad 0.175 -rules -noDataValIn 0 -noDataValOut 255 -deliver

################
### Merge Masks
################

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
```

<!--
***************************************************************************
-->

**Example Recipe File:** 

```shell
#########################################################################
###################   DGLayers Recipe File    ##########################
#########################################################################
#
# Create 2m Tree Digital Height Model (TDHM) for PSMA from 
# 2m DSM, 2m DTM, and 2m LULC.
# Assumes the following input symbols:
# 	SRC1_lulc -- LULC, 2m, 8-bit
# 	SRC2_dsm  -- DSM, 2m, 32-bit, no_data = -9999
# 	SRC3_dtm  -- DTM, 2m, 32-bit, no_data = -8888

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
PREFIX_LEN 18
n5_tree_dhm DST TREE_DHM
END_RENAME_OUTPUTS

#------------------------------------------------------------------------
#                             Process Flow 
#------------------------------------------------------------------------

# False == Tree; True otherwise. tree_label=5
n1_tree_mask = np.where(SRC1_lulc != 5, True, False).astype(np.bool) 

# False == valid DSM; True otherwise. no_data_dsm = -9999
n2_dsm_mask = np.where(SRC2_dsm == -9999, True, False).astype(np.bool)

# False == valid trees and DSM; True otherwise  
n3_umask = np.logical_or(n1_tree_mask, n2_dsm_mask) 

# Digital height model
n4_dhm = SRC2_dsm - SRC3_dtm

# Tree-masked digital height model. no_data_out = -8888
n5_tree_dhm = np.where(n3_umask, -8888, n4_dhm) --deliver
```

<!--
***************************************************************************
-->

## Python-like recipe commands
In a DGLayers recipe you can call virtually any Python function (from numpy
or scipy libraries) that goes from one or more numpy arrays (of same row-column dimension) 
to a new numpy array of the same row-column dimension. The functions you see below are
some examples that satisfy the property. See Internet for descriptions.
```shell				
# In the recipe, use the syntax: <node_id> = <library>.<function>(<arguments>) 
# For numpy functions, <library> equals "np" rather than "numpy"

np.where()
np.average()
np.mean()
np.sum()
np.prod()
np.invert()
np.logical_and()
np.logical_or()
np.logical_xor()
np.digitize()
np.amin()
np.amax()
np.argmin()
np.argmax()
scipy.ndimage.<function>()
scipy.signal.<function>()
scipy.ndimage.filters.<function>()
scipy.ndimage.morphology.<function>()
skimage.morphology.skeletonize() (<--- coming soon)
skimage.morphology.medial_axis() (<--- coming soon)

And arithmetic expressions: (e.g., n3 = 5*(n1[1,:,:] + n2[0,:,:]))
```

## Built-in recipe commands 
```shell
# Argmin and Argmax 
classmap_argmin (plus text legend)		
classmap_argmax	(plus text legend)

# Binary morphology
binary_8_conn_to_4_conn
binary_dilation_dgl
binary_erosion_dgl
binary_opening_dgl
binary_closing_dgl
binary_open_and_reconstruct
binary_close_and_reconstruct
binary_erase_fat_ones
binary_erase_fat_zeros
binary_erase_thin_ones
binary_erase_thin_zeros
binary_erase_small_blobs_ones			
binary_erase_small_blobs_zeros	
	
# Contrast stretch
dra_single_band 
stdev_stretch (<------ coming soon)

# Filters
convolve_3x3 (<------ coming soon)
median_3x3 (<------ coming soon)
min & max (<------ coming soon)
edge_nb

# Miscellaneous 
coalesce_classmap (plus text legend)
indices (plus text legend)
mask_burn
posterize (plus text legend)				
rgb_to_hsv
skeletonize (<---- coming soon)
spec_angle_mapper (plus text legend) 
other_class_algs (<------ coming soon from J. Shafer)

# Polygonize
polygonize	
		
# Threshold
thresh_minmax_the_band	(plus text legend)
thresh_minmax_the_stack (plus text legend)	

# Utilities		
stack_bands	
subset_bands	
```

<!--
***************************************************************************
-->

### argmin and argmax (plus text legend)
```shell
classmap_argmin -outdirID <node_id> -indirID <node_id>  -noDataVal <val>

# Related: 
classmap_argmax
```
The above command takes as input a multi-band raster and returns a single-band UCHAR raster. For each multi-band input pixel, this function determines which band has the minimum value and writes that band index to the corresponding output pixel. Band indexing begins at 1. If the multi-band pixel contains a <no_data_val>, then 0 is written to the output pixel. If the input stack is accompanied by a text legend that was generated by DGLayers, a text legend (README.txt) will be generated for the output raster. **_DONE_**

### Binary morphology 
**_Command:_**
```shell
<node_id> = do_8_conn_to_4_conn(<node_id>) 
```
The above command takes as input a single-band 0-1 UCHAR raster and returns a single-band 0-1 UCHAR raster. This function adds 1's as necessary to create 4-connected regions of 1's from 8-connected regions of 1's. **_DONE_**

**_Command:_**
```shell
<node_id> = binary_dilation_dgl(<node_id>, <rad_pix|rad_mtrs> = <int>) 

# Examples:
	n5 = binary_dilation_dgl(n4, rad_pix=2)
	n5 = binary_dilation_dgl(n3, rad_mtrs=2)

# Related: 
	binary_erosion_dgl, binary_opening_dgl, binary_closing_dgl,
	binary_open_and_reconstruct, binary_close_and_reconstruct,
	binary_erase_fat_ones, binary_erase_fat_zeros, 	
	binary_erase_thin_ones, binary_erase_thin_zeros
```
The above command takes as input a single-band 0-1 UCHAR raster and returns a single-band 0-1 UCHAR raster. This function dilates the 1's by a disc of the specified radius in specified units. Edge effects are handled correctly. All the related commands listed have the same interface. **_DONE_**

**_Command:_**
```shell
binary_erase_small_blobs_ones --outdirID <node_id> --indirID <node_id>  --maxWidth <int> --maxLength <int> -units <pixels|meters> 

# Related: 
	binary_erase_small_blobs_zeros
```
The above command takes as input a single-band 0-1 UCHAR raster and returns a single-band 0-1 UCHAR raster. This function erases any blob of 1's that fits inside a rectangle (not assumed axis-aligned) of the specified dimensions in the specified units. **_DONE_**

### Contrast stretch 
```shell
dra_single_band --outdirID <node_id> --indirID <node_id> 
```
The above command takes as input a single-band raster of USHORT 11-bit (0-2047) and returns a single-band raster of USHORT 11-bit (0-2047). This function performs a data-driven dynamic range adjustment of the input raster. **_DONE_**

### Filters
**_Command:_**
```shell
<node_id> = convolve_3x3(<node_id>) 
```
The above command takes as input a multi-band raster of any data type and returns a multi-band raster of the same data type and with the same number of bands. Each band of the output raster is the convolution of the 3x3 equal-weights averaging kernel and the corresponding band of the input raster.   **_DONE_**

**_Command:_**
```shell
<node_id> = median_3x3(<node_id>) 
```
The above command takes as input a multi-band raster of any data type and returns a multi-band raster of the same data type and with the same number of bands. Each band of the output raster is obtained by applying the 3x3 median filter kernel to the corresponding band of the input raster. **_DONE_**

**_Command:_**
```shell
edge_nb --outdirID <node_id> --indirID <node_id> 
```
The above command takes as input a single-band raster of USHORT 11-bit (0-2047) and returns a single-band raster of USHORT 11-bit (0-2047). This function computes "edge-strength" using the legacy GeoEye implementation of Navatia-Babu edge detection. This function would typically be called on a "prepared" input raster, one that has been dynamically range adjusted (via a call to built-in command "dra_single_band") and smoothed (via call to built-in command "convolve_3x3"). Then "edges" can be obtained by thresholding this edge-strength raster. **_DONE_**

### Miscellaneous
**_Command:_**
```shell
coalesce_classmap -outdirID <node_id> -indirID <node_id> -coalesceFile <file_symbol>
```
Example coalesce file:
```shell
	# Class Remapping
	0 : Unknown : 0
	1 : Flat Concrete : 11, 12, 18, 19
	2 : Fibreglass/Plastic : 27, 28, 30
	3 : Metal : 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 13, 14, 15
	4 : Tile : 16, 17, 20, 21, 22, 23, 24, 25, 26
	5 : Mineral : 
	6 : Unknown Label 1 : 29
```
The above command takes as input a single-band UCHAR raster and returns a single-band UCHAR raster. The specified coalesce-file tells this function which old class labels of the input raster are to be mapped to which new class labels of the output raster. Every old class label must be assigned to a new class label. This coalesce-file must begin with a single header line. Each subsequent line must be of the form (new label) : (name) : (list of old labels). The latter list can be empty. **_DONE_**

**_Command:_**
```shell
indices -outdirID <node_id> -indirID <node_id> -indexIDandExp <index_name> <band_math> -noDataValIn <val> -noDataValOut <val>

# Example:
	indices -outdirID n4 -indirID n2 -indexIDandExp NDVI (b7-b5)/(b7+b5) -noDataValIn 0 -noDataValOut 9999
```
The above command takes as input a multi-band raster of any data type and returns a multi-band raster of FLOAT32 and a text legend (README.txt). The band math expression can involve parentheses, arithmetic operations, exponent (carrot), numbers, log, and sqrt, **_but not spaces_**. Designate bands with B1, B2, B3,... or b1, b2, b3,.... **_DONE_**

**_Command:_**
```shell
indices --outdirID <node_id> --indirID <node_id> --indexIDsFromFile <file_symbol> <(index_names)|all> --noDataValIn <val> -noDataValOut <val>

# Examples:
	indices --outdirID n4 --indirID SRC --indexIDsFromFile FILE_1 Laterite Gossan --noDataValIn 0 -noDataValOut 9999
	indices --outdirID n4 --indirID n2 --indexIDsFromFile FILE_1 all --noDataValIn 0 -noDataValOut 9999 
```
Example index file:
```shell
	# ENVI EXPRESSIONS
	B5/B3 : Ferric oxide composition
	(B13/B7) + (B3/B5) : Ferrous, Fe2+
	B11/B13 : Laterite
	B11/B5 : Gossan
	B13/B11 : Ferrous iron index
```
The above command takes as input a multi-band raster of any data type and returns a multi-band raster of FLOAT32 and a text legend (README.txt). This function builds an index raster stack according to the band math expressions contained in an index file. Command syntax allows the user to reference specific indices within the file or reference all indices within the file. The file may contain any number of comment lines that begin with "#" and blank lines -- these will ignored. Each non-ignored line must be of the form (band_math) : (index_name). The (band_math) can involve spaces, parentheses, arithmetic operations, exponent (carrot), numbers, log, and sqrt. The (index_name) can be any string, and may contain spaces, commas, and so on, but not colons. **_If the user is referencing a subset of the file indices, then every index name in the file must be a string without spaces_**. The bands in the band math expressions must be labelled B1, B2, B3,.... or b1, b2, b3,.... If the user references an ordered subset of indices in the file, then the ordering of the output bands corresponds to the ordered subset. If the user references all the indices in the file, then the ordering of the output bands corresponds to the file ordering. **_DONE_**

**_Command:_**
```shell
mask_burn --outdirID <node_id> --indirID <node_id> --indirMaskID <node_id> -maskVal <val>
```
The above command takes as input a multi-band "source" raster of any data type and a single-band "mask" raster, and returns a multi-band raster identical to the source raster except that wherever the mask raster is True, the value for "-maskVal" is burned through all the layers of the source raster. **_DONE_**

**_Command:_**
```shell
posterize --outdirID <node_id> --indirID <node_id> --cutoffs <val_1> <val_2> ...

# Example:
	posterize --outdirID n2 --indirID n1 --cutoffs 0.3 0.5 0.6 
```
The above command takes as input a single-band raster of any data type and returns a single-band raster of UCHAR and a text legend (README.txt). In the example above, the output raster has value 0 where input raster in (-infinity, 0.3], value 1 where input raster in (0.3, 0.5], value 2 where input raster in (0.5, 0.6], and so on. **_DONE_**

**_Command:_**
```shell
rgb_to_color_space --outdirID <node_id> --indirID <node_id> -rgb <r_band> <g_band> <b_band> -colorSpace HSV 
```
The above command takes as input a multi-band AComp'd reflectance raster of USHORT (0-10000) and returns a 3-band raster of UCHAR. It converts specified RGB layers to HSV (see Wikipedia), in that order. The "-rgb" option identifies which three bands of the input raster comprise R, G, B, in that order. Band indexing begins at 1. **_DONE_**

**_Command:_**
```shell
spec_angle_mapper --outdirID n1 --indirID SRC -materialIDsFromFile <file_symbol> <(materials)|all> -noDataValIn <val> -noDataValOut <val>
	[-rules] [-defAngThreshRad <ang_rad>] [-angThresholdsRad <pairs>] [-angThreshRadFile <file_symbol>]
	
# Examples:
	spec_angle_mapper --outdirID n2 --indirID SRC --materialIDsFromFile FILE_1 all --defAngThreshRad 0.175 
		-angThresholdsRad (alunite1.spc, 0.2) (goethit1.spc, 0.15) --noDataValIn 0 --noDataValOut 0 
	spec_angle_mapper --outdirID n2 --indirID SRC --materialIDsFromFile FILE_1 alunite1.spc gypsum1.spc -angThreshRadFile FILE_2
		--noDataValIn 0 --noDataValOut 0 
```
Example spectral library file:
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
Example angle threshold file:
```shell
	# Angle thresholds (rad)
	alunite1.spc : 0.20
	gypsum1.spc : 0.18
```
The above command takes as input a multi-band AComp'd reflectance raster of USHORT (0-10000) and returns a single-band "class map" raster of UCHAR, an optional multi-band "rules" ("angles") raster of USHORT, and a text legend (README.txt) accompanying each. This function applies the usual Spectral Angle Mapping calculation to produce the rasters. The "rules" raster will only be generated when the "-rules" option is invoked. The "rules" raster is computed as the integer part of "angle(radians) x 10000". Depending on input file size and the number of materials specified, the "rules" raster can be a very large file. The number of bands in the "rules" raster is the same as the number of materials referenced by the user, and the ordering of the bands corresponds to the ordering in the material list referenced by the user. If the user references all the materials in the spectral library, then the ordering of the output bands follows the file order of materials. 

The spectral library file must be the text file equivalent of an ENVI spectral library file. The first line is a header. The second line is "Column 1: X Axis". That is followed by one line per material. In turn, that is followed by the material spectra in column format. The first "material spectrum" is associated with "Column 1: X Axis".

TBD: Describe format of angle thresholds file. 

TBD: What material name in file has spaces in it? 

The "-defAngThreshRad" option allows the user to set a universal default threshold angle (radians) such that, for any pixel and any material, if the spectral angle between pixel and material is greater than the default, the material is disqualified from being explanatory for the pixel. The "-angThresholdsRad" option allows the user to set threshold angles on a per-material basis. Alternatively, the "-angThreshRadFile" option can be used to set threshold angles on a per-material basis. **_DONE_**

### Polygonize 
```shell
polygonize  --indirID <node_id> --outdirID <node_id> 
```
The above command takes as input a single-band raster of UCHAR, and returns an ESRI shapefile of polygons corresponding to the regions of non-zeroes. This function calls Chris Padwick's fast polygonize code, which is orders of magnitude faster than gdal_polygonize and "pulls back" where polygons would otherwise self-touch. (Some GIS software doesn't handle self-touching polygons.) Polygons with holes (multi-polygons) are correctly handled. **_DONE_**

### Threshold 
**_Command:_**
```shell
thresh_minmax_the_stack -outdirID <node_id> -indirID <node_id> -minmaxPairs <threshold_pairs>

# Example:
	thresh_minmax_the_stack -outdirID n5 -indirID n4 -minmaxPairs (*, 0.5) (0.3, 0.4)  
```
The above command takes as input a multi-band raster of any data type and a threshold pair for each band, and returns a multi-band 0-1 raster of UCHAR and an accompanying text legend (README.txt). The output raster has the same number of bands as the input raster. The "star" in ("star", X) means minus infinity. The "star" in (X, "star") means plus infinity. In the example, it is assumed that the input raster has two bands. The first band in the output raster is 1 wherever the first band of the input raster is between minus infinity and 0.5, and 0 otherwise. The second band in the output raster is 1 wherever the second band of the input raster is between 0.3 and 0.4, and 0 otherwise. **_DONE_**

**_Command:_**
```shell
thresh_minmax_the_band -outdirID <node_id> -indirID <node_id> -minmaxPairs <threshold_pairs>  

# Example:
	thresh_minmax_the_band -outdirID n5 -indirID n4  -minmaxPairs (*, 0.5) (0.3, 0.4)  
```
The above command takes as input a single-band raster of any data type and a sequence of threshold pairs, and returns a multi-band 0-1 raster of UCHAR and an accompanying text legend (README.txt). The output raster has the same number of bands as there are pairs in the sequence. The "star" in ("star", X) means minus infinity. The "star" in (X, "star") means plus infinity. In the example, the first band in the output raster is 1 wherever the input raster is between minus infinity and 0.5, and 0 otherwise. The second band in the output raster is 1 wherever the input raster is between 0.3 and 0.4, and 0 otherwise. **_DONE_**

### Utilities 
**_Command:_**            
```shell
stack_bands --outdirID <node_id> --indirIDs <(node_id, band) (node_id, band) ...> 

#Example:
	stack_bands --outdirID n7 --indirIDs (n5, *) (n2, 7) (n2, 6) (n3, 4)  
```
The above command takes as input a sequence of pairs of the for (multi-band raster, band) and returns a new multi-band raster consisting of the specified bands in the specified order. The input rasters must all be of the same data type. The symbol * means include all bands from the corresponding input raster. Band indexing starts at 1. **_DONE_**

**_Command:_**
```shell
subset_bands --outdirID <node_id> --indirID <node_id> -bands <idx1 idx2 ...>
 
# Example:
	subset_bands --outdirID n3 --indirID n1 -bands 2 5 1 7 
```
The above command takes as input a multi-band raster and a sequence of bands indices, and returns a new multi-band raster consisting of the specified bands in the specified order. Band indexing starts at 1. **_DONE_**

## Known Issues

* "saveData" task might not be working with DGLayers. For now, may have to call "StageDataToS3" task
* polygonize does not presently work on multi-band 0-1 input rasters
* polygonize [-thematic] option does not presently work on spectral_angle_mapper output class map because polygonize is expecting README.TXT instead of README_CLASSMAP.TXT
* polygonize [-geojson] option does not work. This option is supposed to output a polygon geojson in addition to polygon shapefile.
* Sometimes when polygon would otherwise be self-touching, Chris Padwick's algorithm is a little aggressive in the "pull back".





