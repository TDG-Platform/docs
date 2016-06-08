

		
		
**Task Description:**		LULC is an un-supervised protocol for computing a coarse class LULC layer from 8 band (optical + VNIR) image data-sets. The LULC layer is an RGB image in which unique colors are assigned to unique classes. See table below for details.
		

![enter image description here](https://lh3.googleusercontent.com/iyUmINzySFb28juMhXs3H5Dsq5CDe8l691fO8_FuZ5ioRp4TckGuPJjmq1tuNFYjrVT8PVP0=s0 "Class_Descriptions.PNG")

		

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

If you need to generate the 8-Band MS data required as input for this task, use the following example script.

add SCRIPT HERE FOR 8-BAND AOP

Source Algorithm:		PROTOGEN version 2.0.0, (May 13, 2016)		
Author: 		Georgios Ouzounis,  DigitalGlobe Inc. 
					georgios.ouzounis@digitalglobe.com


> Written with [StackEdit](https://stackedit.io/).