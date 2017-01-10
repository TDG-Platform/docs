# Automated Landuse Landcover Classification (protogenV2LULC)



**Task Description:**		LULC is an un-supervised protocol for computing a coarse class LULC layer from 8 band (optical + VNIR) image data-sets. The LULC layer is an RGB image in which unique colors are assigned to unique classes (See Outputs for description).   you can use [gbdxtools](http://gbdxtools.readthedocs.io/en/latest/user_guide.html) and the following examples script to generate the landuse landcover classification output. If you need to generate the 8-Band MS data required as input for this task see [Advanced Options](#advanced-options).



### Table of Contents
 * [Quickstart](#quickstart) - Get started!
 * [Inputs](#inputs) - Required and optional task inputs.
 * [Outputs](#outputs) - Task outputs and example contents.
 * [Advanced Options](#advanced-options) - Additional information for advanced users.
 * [Runtime](#runtime) - Results of task benchmark tests.
 * [Known Issues](#known-issues) - current or past issues known to exist.
 * [Contact Us](#contact-us)


### QuickStart
This script gives the example of Land Use Land Cover with a single 8-band tif file as input.

```python
# Quickstart Example producing an unsupervised Landuse Landcover Classification from a tif file.
# First Initialize the Environment

from gbdxtools import Interface
gbdx = Interface()

#Edit the following path to reflect a specific path to an image
raster = 's3://gbd-customer-data/CustomerAccount#/PathToImage/'
prototask = gbdx.Task("protogenV2LULC", raster=raster)

workflow = gbdx.Workflow([ prototask ])
#Edit the following line(s) to reflect specific folder(s) for the output file (example location provided)  
workflow.savedata(prototask.outputs.data, location='LULC')
workflow.execute()

print workflow.id
print workflow.status

```
### Inputs
This task will process only WorldView 2 or WorldView 3 multi-spectral imagery (8-band optical and VNIR data sets) that has been atmospherically compensated by the AOP processor. Supported formats are .TIF, .TIL, .VRT, .HDR.

Example 1B Datasets that you can process to generate the 8-Band input and then run the LULC Algorithm:

	Tracy, CA: 	104001001D62F700 = WV03 's3://receiving-dgcs-tdgplatform-com/055382035010_01_003'
	Naples, Italy: 	104001000E25D700 = WV03	's3://receiving-dgcs-tdgplatform-com/055249130010_01_003'

### Outputs

RGB .TIF image of type UINT8x3. The data will be displayed using the following color codes:

 Color |  RGB Value     |Class Description
:-------|:----------------|--------
  Green  | [0,255,0] |All types of vegetation (healthy chlorophyll content)
   Blue  | [0,0,128] | All types of water, excluding flood waters (murky)
  Brown | [128,64,0} | All types of soils, excluding rocks and stone
  Light Blue  | [128,255,255] | All types of clouds excluding smoke
  Purple  | [164,74,164] | Shadows
  Gray | [128,128,128]  |  Unclassified (equivalent to man-made  materials, rock, stone)    
  Black  | [0,0,0]   | No-data   


### Advanced Options
If you need to generate the 8-Band MS data required as input for this task, you can use  and the following example script to preprocess your data. This example runs Fast-Ortho+AComp and Protogen LULC from end to end.  Click on this link for details regarding the the [Advanced Image Preprocessor](https://github.com/TDG-Platform/docs/blob/master/AOP_Strip_Processor.md).

```python
	# This Script runs the AOP Processor; moves the output to a file that is accessible
	# to the Protogen task, and runs the protogenV2LULC Task.
	# First initalize the environment

	from gbdxtools import Interface
	gbdx = Interface()
	import json

	# The data input and output lines must be edited to point to an authorized customer S3 location
	data = 's3://gbd-customer-data/CustomerAccount#/PathToImage/'

	# Run AOP to create acomp'd multispectral image
	aoptask2 = gbdx.Task('AOP_Strip_Processor', data=data, bands='MS', enable_acomp=True, enable_pansharpen=False, enable_dra=False)     

	# Move aoptask output to root where prototask can find it
	gluetask = gbdx.Task('gdal-cli')                                 
	gluetask.inputs.data = aoptask2.outputs.data.value
	gluetask.inputs.execution_strategy = 'runonce'
	gluetask.inputs.command = """mv $indir/*/*.tif $outdir/"""
	prototask = gbdx.Task('protogenV2LULC')
	prototask.inputs.raster = gluetask.outputs.data.value

	workflow = gbdx.Workflow([aoptask2, gluetask, prototask])
  #Edit the following line(s) to reflect specific folder(s) for the output file (example location provided)
	workflow.savedata(prototask.outputs.data, location='LULC')

	workflow.execute()
	workflow.status

```
### Runtime

The following table lists all applicable runtime outputs. (This section will be completed the Algorithm Curation team)
For details on the methods of testing the runtimes of the task visit the following link:(INSERT link to GBDX U page here)

  Sensor Name  |  Total Pixels  |  Total Area (k2)  |  Time(secs)  |  Time/Area k2
--------|:----------:|-----------|----------------|--------------
WV02|35,872,942|329.87|328.19 |0.99|
WV03|35,371,971|196.27| 459.06|2.34 |

### Known issues:

***Vegetation:***  Thin cloud (cloud edges) might be misinterpreted as vegetation.

***Water:***  False positives maybe present due to certain types of concrete roofs or shadows.

***Soils:***  Ceramic roofing material and some types of asphalt may be misinterpreted as soil.

***Clouds:***  Certain types of concrete might be misinterpreted as cloud. Thin cloud areas may be interpreted as soil or vegetation.

**Limitations:**		The layer uses smoothing operators in cross-class interfaces for noise reduction. This might result in loss/misinterpretation of small class patches 8m^2.

### Contact Us
Tech Owner: [Georgios Ouzounis](#gouzouni@digitalglobe.com) & Editor:  [Kathleen Johnson](#kathleen.johnsons@digitalglobe.com)
