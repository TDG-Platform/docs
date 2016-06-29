# AOP Strip Processor (Advanced Ortho Product)

The AOP_Strip_Processor (AOP) produces orthorectified imagery from raw (level 1B) imagery.  There are many additional processing options including atmospheric compensation (always recommended), pansharpening and dynamic range adjustment (DRA).  The AOP Strip Processor can be run through a simple Python script using  [gbdxtools](https://github.com/DigitalGlobe/gbdxtools/blob/master/docs/user_guide.rst), which requires some initial setup, or through the [GBDX Web Application](https://gbdx.geobigdata.io/materials/).  Tasks and workflows can be added to AOP (described here in [gbdxtools](https://github.com/DigitalGlobe/gbdxtools/blob/master/docs/running_workflows.rst)) or run separately after the AOP process is completed.

**1.0 QUICKSTART EXAMPLES**

**1.1 Example Script:** Here is a quick example that uses the AOP Strip Processor to produce an orthorectified and atmospherically compensated dataset of Multispectral and Panchromatic output from a WorldView-3 image over Naples, Italy.  The output will be saved to a user-specified location under s3://bucket/prefix. 

    # Quickstart Example producing an Orthorectified and Acomp output for MS + PAN
    # First Initialize the Environment
    from gbdxtools import Interface
    import json
    gbdx = Interface()

    # WV03 Image over Naples, Italy
    # Make sure Both Pansharpen and DRA is disabled if you are processing both the PAN+MS files
    data = "s3://receiving-dgcs-tdgplatform-com/055249130010_01_003"
    aoptask = gbdx.Task("AOP_Strip_Processor", data=data, enable_acomp=True, enable_pansharpen=False, enable_dra=False)
    workflow = gbdx.Workflow([ aoptask ])  
    workflow.savedata(aoptask.outputs.data, location='kathleen_Naples_WV03_QuickStart3')

    workflow.execute()

    print workflow.id
    print workflow.status

     
**1.2 Example Run in IPython Produces Orthorectified and Atmospherically Compensated 8-Band + PAN Images:**

    In [1]: # Quickstart Example producing an Orthorectified and Acomp output for MS + PAN
    In [2]: # First Initialize the Environment
    In [3]: from gbdxtools import Interface
    In [4]: import json
    In [5]: gbdx = Interface()
      2016-06-24 16:29:53,856 - gbdxtools - INFO - Logger initialized
    In [6]: # WV03 Image over Naples, Italy
    In [7]: # Make sure Both Pansharpen and DRA is disabled if you are processing both the PAN+MS files
    In [8]: data = "s3://receiving-dgcs-tdgplatform-com/055249130010_01_003"
    In [9]: aoptask = gbdx.Task("AOP_Strip_Processor", data=data, enable_acomp=True, enable_pansharpen=False, enable_dra=False)
    In [10]: workflow = gbdx.Workflow([ aoptask ])  
    In [11]: workflow.savedata(aoptask.outputs.data, location='kathleen_Naples_WV03_QuickStart3')
    In [12]: workflow.execute()
    Out[12]: u'4362772047134837472'
    In [13]: print workflow.id
      4362772047134837472

**1.3 Test Datasets for All Sensors (Naples, Italy):**

All sensors have been tested, with the exception of WV03-SWIR imagery.  The S3 locations of the test data are given below.  Script examples for various sensors have been posted:

	10200100423D7A00 = WV01 's3://receiving-dgcs-tdgplatform-com/055250712010_01_003'
	103001004DAFAF00 = WV02 's3://receiving-dgcs-tdgplatform-com/055253506010_01_003'
	104001000E25D700 = WV03 's3://receiving-dgcs-tdgplatform-com/055249130010_01_003'
	1050010001136C00 = GE01 's3://receiving-dgcs-tdgplatform-com/055254039010_01_003'
	101001000F18EA00 = QB02 's3://receiving-dgcs-tdgplatform-com/055269445010_01_003'

**2.0 SUMMARY OF AOP OUTPUT PRODUCTS:** Examples of the script changes required are given below.

	2.1-Pansharpened and DRA RGB Image with atmospheric compensation
	2.2-Multispectral image only (8-band or 4-band) with atmospheric compensation
	2.3-Multispectral + Panchromatic with atmospheric compensation
	2.4-Orthorectified Panchromatic Image (no spectral options available)

**2.1 Example: Pansharpened and DRA RGB Image with atmospheric compensation:**

	aoptask = gbdx.Task("AOP_Strip_Processor", data=data, enable_acomp=True, enable_pansharpen=True, enable_dra=True)
	
**2.2 Example: Multispectral image with atmospheric compensation:**

	 aoptask = gbdx.Task("AOP_Strip_Processor", data=data, enable_acomp=True, bands='MS', enable_pansharpen=False, enable_dra=False)
	
**2.3 Example: Multispectral + Panchromatic Images with atmospheric compensation** (Same as line [9] in the example script):

	 aoptask = gbdx.Task("AOP_Strip_Processor", data=data, enable_acomp=True, enable_pansharpen=False, enable_dra=False)
	
**2.4 Example: Orthorectified Panchromatic Image:**

	aoptask = gbdx.Task("AOP_Strip_Processor", data=data, enable_acomp=False, enable_pansharpen=False, enable_dra=False)


**NOTE:**  The default ouput is an atmospherically compensated RGB image unless the options are set as shown in the examples.  ** YOU MUST** specify 'enable_pansharpen=False' AND 'enable_dra=False' to get multispectral output. Panchromatic images can be orthorectified using AOP, but all spectral options must be set to "false' or the process will not run.  Following example #4, if the source s3 bucket contains both multispectral and panchromatic images, both will be orthorectified, but not atmospherically compensated. 

**3.0 REVIEW OF REQUIRED SETTINGS AND DEFINITIONS:**

| Action       | Required       | Type  |  Name       | 
| ------------- |:-------------| :-----| :------------- |
| S3 location of 1B input image    | True | directory |data   |
| Define the aoptask     | True   | script |  aoptask = gbdx.Task ("AOP_Strip_Processor,data=data,"opt1”,”opt2”,etc...  ) |
| Define output directory | True   | directory | workflow.savedata = (aoptask.outputs.data, location='customer's s# bucket'  ) | 



**4.0 FILE STRUCTURE FOR EXPECTED OUTPUTS:**

Your Processed Imagery will be written to your specified S3 Customer Location (e.g.  s3://gbd-customer-data/unique customer id/named directory/).  When you open the 'named directory' your files should look like this:

![First Directory](https://lh3.googleusercontent.com/-YzyRjMprZ54/VyJqnZjA7oI/AAAAAAAAJaw/hqIopdghThsz9eU9uEN4sUpz8iA7WoscQCLcB/s0/datastructure1.PNG "datastructure1.PNG")

There will be a *standard error file* (###.stderr) and a *standard output file* (###.stdout). These files track the progress of the process and can be downloaded and reviewed, especially if the task has failed to produce a final output.  To create these log files see *Define Output Log* under the advaced settings . The *workorder_'SOLI'.xml* file details the input parameters applied to the AOP Strip Processor.  

Click on the Folder at the bottom of the list identified by the 'Sales Order Line Item' (SOLI). Inside this directory you will find the processed imagery output (e.g. below).  The .IMD and .XML files describe the spectral and physical characteristics of the Imagery Product.  The *assembly_MS.tif* and *assembly_PAN.tif* are the imagery files that can be viewed in standard GIS and Remote Sensing Software.  the .vrt files are GDAL virtual raster format that allows viewing of the complete image without making a mosaic.




![Second Directory](https://lh3.googleusercontent.com/-_lAVdacJf2c/VyJqZp78PAI/AAAAAAAAJao/1Px_21rWHBQEjbqyi_orY-BnTiH0-ZtGACLcB/s0/datastructure2.PNG "datastructure2.PNG")



**5.0 OPTIONAL SETTINGS FOR ADVANCED USERS ONLY: Description of Input Parameters and Options for the "aoptask"** Advanced users may choose to modify the spectral spatial processes run in the aoptask by setting these options.  Examples are given for the options most often applied.


| Action       | Required       | Default | Type  |  Name       | 
| ------------- |:-------------| :-----| :------------- | :-----------|
| Define the output log directory | False | None | directory | log = aoptask.get_output('log')|
|Enable/disable AComp | False | True | string | enable_acomp |
|Enable/disable pan sharpening | False | True | string | enable_pansharpen|
| Enable/disable dynamic range adjustment (DRA) | False | True | string | enable_dra |
| Select Bands to process ('PAN+MS', 'PAN', 'MS', 'Auto') |False | None | string | bands|
| Enable/disable output tiling | False | None | string | enable_tiling|
|Zoom level (tiling is enabled)| False | 12 | string |tiling_zoom_level |
| Process part of the image | False | Process Entire Image | string | parts |
|Ortho EPSG projection (UTM is also allowed) | False | EPSG:4326 | string | ortho_epsg |
| Ortho pixel size in meters | False | Input pixel size | string | ortho_pixel_size |
| Ortho pixel interpolation ('Nearest', 'Bilinear', 'Cubic') | False | Cubic | String | ortho_interpolation_type |
|Specify Ortho DEM ('NED', 'SRTM30', 'SRTM90') | False | SRTM90 | string | ortho_dem_specifier |
|Dynamic Range Adjustment (DRA) mode ('IntensityAdjust', 'BaseLayerMatch')| False | 'IntensityAdjust' | string | dra_mode |
| DRA low cutoff percentage (range: 0-100) | False | 0.5 | string | dra_low_cutoff |
|DRA high cutoff percentage (range: 0-100) | False | 99.95 | string | dra_high_cutof |
|DRA gamma value | False | 1.25 | string | dra_gamma |
| DRA output bit depth (8 or 16) | False | 8 | string | dra_bit_depth |







**6.0 EXAMPLES FOR COMMON OPTION CHANGES**

**6.1 Script Example Reproject to UTM**

	aoptask = gbdx.Task("AOP_Strip_Processor", data=data, enable_acomp=True, enable_pansharpen=False, enable_dra=False, ortho_epsg="EPSG:32633") # specify UTM Zone
    
    aoptask = gbdx.Task("AOP_Strip_Processor", data=data, enable_acomp=True, enable_pansharpen=False, enable_dra=False, ortho_epsg="UTM") # Will automatically determine the UTM Zone



**6.2 Script Example Changing Ortho Output Pixel Size**  (Default for non-pansharpened MS=2 meters); make sure both PanSharpen and DRA are disabled. Caveat: You are changing the PAN pixel size (Default = 0.50m) and the MS pixel size will be downsampled proportionally.

	aoptask = gbdx.Task("AOP_Strip_Processor", data=data, enable_acomp=True, enable_pansharpen=False, enable_dra=False, ortho_pixel_size="3")
    

**6.3 Script Example Change DEM to SRTM30**

	aoptask = gbdx.Task("AOP_Strip_Processor", data=data, enable_acomp=True, enable_pansharpen=False, enable_dra=False, ortho_dem_specifier="SRTM30")


**6.4 Script to Change Interpolation method to Bilinear**

	aoptask = gbdx.Task("AOP_Strip_Processor", data=data, enable_acomp=True, enable_pansharpen=False, enable_dra=False, ortho_interpolation_type="Bilinear")


**NOTES ON SPECIAL DRA SETTINGS:**

**6.5 The Dynamic Range Adjustment Mode (DRA) should be run using the default setting 'enable_dra=True', which will be adequate for most imagery. ** 

**6.5.1 Dynamic range adjustment mode** – IntensityAdjust is for standalone, individual images that are not going to be mosaicked together. BaseLayerMatch uses a global base layer for color matching and helps maintain consistency when mosaicking. The base layer started out as color-balanced and mosaicked Landsat imagery but may have started incorporating higher-res imagery also.

**6.5.2 Dynamic range adjustment low cutoff percentage** – Sets the black point in the histogram. Adjusting this will change the point in the histogram that is considered “black” and will darken and lighten the low end of the histogram. Setting the number lower (<0.5) will brighten the darker color tones and make the overall image lighter. Setting the number higher will saturate more of the darker color tones and make the overall image darker. Could start to lose detail in the darker areas if too heavy-handed. A light touch can make a huge difference so be careful.

**6.5.3 Dynamic range adjustment high cutoff percentage** – Sets the white point in the histogram. Same general idea as the low cutoff percentage but operates on the brightest color tones to adjust what is considered saturated “white”. Setting this number lower (<99.95) will brighten the image while setting the number higher will darken the image. Again, a light touch is mandatory to keep things looking “normal”.

**6.5.4 Dynamic range adjustment gamma value** – Adjusts the curvature of the transfer function from input to output. When gamma=1, that is a straightforward, linear transfer from input to output. When gamma>1, the image will get overall brighter. Conversely, the image will get overall darker when gamma<1. Works in conjunction with the histogram cutoff values but is a completely independent parameter. Operates like a root stretch but with much finer adjustment settings. All three parameters, low cutoff, high cutoff, and gamma, work together to adjust the overall brightness, contrast, and dynamic range of the image. They’re all independent and will affect the final DRAed image in similar, but different, ways. Setting these is more an art than a science and it’s highly recommended to NOT mess with these unless the image is one of those special cases and is totally screwed up. Then the art comes into play.

**6.5.6 Dynamic range adjustment output bit depth** – Should NEVER be set to anything other than 8. DRA is valid and makes sense ONLY for 8bit output imagery. Running DRA to get a 16bit DRAed image will get you nothing since you still have to scale the image to 8bits/band for display purposes anyway.


For background on the development and implementation of AOP refer to the [Advanced Ortho Processor PDF.](http://tu00aopapp006:8102/job/AOP-Docs/ws/build/latex/AOP-AdvancedOrthoProcessor.pdf)


