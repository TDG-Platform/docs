# Unsupervised Landuse Landcover Classification (protogenV2LULC)

		
		
**Task Description:**		LULC is an un-supervised protocol for computing a coarse class LULC layer from 8 band (optical + VNIR) image data-sets. The LULC layer is an RGB image in which unique colors are assigned to unique classes. See table below for details.


 Color |  RGB Value     |Class Description
:-------|:----------------|--------
  Green  | [0,255,0] |All types of vegetation (healthy chlorophyll content)
   Blue  | [0,0,128] | All types of water, excluding flood waters (murky)
  Brown | [128,64,0} | All types of soils, excluding rocks and stone
  Light Blue  | [128,255,255] | All types of clouds excluding smoke
  Purple  | [164,74,164] | Shadows
  Gray | [128,128,128]  |  Unclassified (equivalent to man-made  materials, rock, stone)    
  Black  | [0,0,0]   | No-data   






### Table of Contents
 * [Quickstart](#quickstart) - Get started!
 * [Inputs](#inputs) - Required and optional task inputs.
 * [Outputs](#outputs) - Task outputs and example contents.
 * [Advanced](#advanced) - Additional information for advanced users.
 * [Known Issues](#known-issues) - current or past issues known to exist.
 * 
 
**QuickStart**



		

**Known issues:**

***Vegetation:***  Thin cloud (cloud edges) might be misinterpreted as vegetation.

***Water:***  False positives maybe present due to certain types of concrete roofs or shadows.

***Soils:***  Ceramic roofing material and some types of asphalt may be misinterpreted as soil.

***Clouds:***  Certain types of concrete might be misinterpreted as cloud. Thin cloud areas may be interpreted as soil or vegetation.
		
**Limitations:**		The layer uses smoothing operators in cross-class interfaces for noise reduction. This might result in loss/misinterpretation of small class patches (8m^2).
		
**Task input:**		WorldView 2 or WorldView 3 multi-spectral imagery (8-band optical and VNIR data sets) that has been atmospherically compensated by the AOP processor.  Supported formats are .TIF, .TIL, .VRT, .HDR.  
		



**Task output:**		RGB .TIF image of type UINT8x3.
		






		LULC (TASK OUPUT) EXAMPLE
		
RGB view of the input		 
		![enter image description here](https://lh3.googleusercontent.com/-fZLrWWu5KcM/V1cNpe2DDlI/AAAAAAAAJn0/vKFTazNMTSkjW4PVhXggGj4dJXe-OBzGgCLcB/s0/Denver_rgb2_800x600.bmp "Denver_rgb2_800x600.bmp")

LULC layer		 
![enter image description here](https://lh3.googleusercontent.com/-eXo17ewGUGc/V1cM5oeHo2I/AAAAAAAAJnU/FfbcnUbEarARXvvXM9zaigQDijQlAFOJwCLcB/s0/Denver_lulc2_800x600.bmp "Denver_lulc2_800x600.bmp")

Example 1B Datasets that you can process to generate the 8-Band input and then run the LULC Algorithm:

	Tracy, CA: 	104001001D62F700 = WV03 's3://receiving-dgcs-tdgplatform-com/055382035010_01_003'
	Naples, Italy: 	104001000E25D700 = WV03	's3://receiving-dgcs-tdgplatform-com/055249130010_01_003'



If you need to generate the 8-Band MS data required as input for this task, you can use [gbdxtools](http://gbdxtools.readthedocs.io/en/latest/user_guide.html) and the following example script to generate the 8-Bands data. This example runs Fast-Ortho+AComp and Protogen LULC from end to end.  Click on this link for details regarding the the [Advanced Ortho Product Pre-Processing](https://github.com/TDG-Platform/docs/blob/master/AOP%20Strip%20Processor_V3.md).

	# Runs Fast-Ortho+AComp, then feeds that data to the protogenv2LULC process
 	from gbdxtools import Interface 
	import json
	gbdx = Interface()

	data = "s3://receiving-dgcs-tdgplatform-com/054813633050_01_003"
	aoptask = gbdx.Task("AOP_Strip_Processor", data=data, enable_acomp=True, enable_pansharpen=False, enable_dra=False, bands='MS')

	# ProtogenPrep task is used to get AOP output into proper format for protogen task
	pp_task = gbdx.Task("ProtogenPrep",raster=aoptask.outputs.data.value)      
	prot_lulc_task = gbdx.Task("protogenV2LULC", raster=pp_task.outputs.data.value)

	# Run Combined Workflow
	workflow = gbdx.Workflow([ aoptask, pp_task, prot_lulc_task ])
	workflow.savedata(prot_lulc_task.outputs.data.value, location="/kathleen_complex_test2")
	workflow.execute()

	print workflow.id
	print workflow.status

Source Algorithm:		PROTOGEN version 2.0.0, (May 13, 2016)		
Author: 		Georgios Ouzounis,  DigitalGlobe Inc. 
					georgios.ouzounis@digitalglobe.com


> Written with [StackEdit](https://stackedit.io/).
