# AOP Strip Processor (Advanced Ortho Product)

The AOP Strip Processor generates large scale, color balanced ortho imagery in a semi-automated fashion.  Level 1B imagery is processed according to defined inputs.  The AOP Strip Processor can be run through a simple Python script using  [gbdxtools](https://github.com/DigitalGlobe/gbdxtools/blob/master/docs/user_guide.rst), which requires some initial setup, or through the [GBDX Web Application](https://gbdx.geobigdata.io/materials/).  Tasks and workflows can be added to AOP (described here in [gbdxtools](https://github.com/DigitalGlobe/gbdxtools/blob/master/docs/running_workflows.rst)) or run separately after the AOP process is completed.

**Example Script:** These basic settings will run orthorectification and DG AComp on an input dataset containing MS + PAN.  See also examples listed under the optional settings below.

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

     
**Example Run in IPython Produces AComp'ed 8-Band + PAN Images:**

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

**Test Datasets for All Sensors (Naples, Italy):**

All sensors have been tested, with the exception of WV03-SWIR imagery.  The S3 locations of the test data are given below.  Script examples for various sensors have been posted:

	10200100423D7A00 = WV01 's3://receiving-dgcs-tdgplatform-com/055250712010_01_003'
	103001004DAFAF00 = WV02 's3://receiving-dgcs-tdgplatform-com/055253506010_01_003'
	104001000E25D700 = WV03 's3://receiving-dgcs-tdgplatform-com/055249130010_01_003'
	1050010001136C00 = GE01 's3://receiving-dgcs-tdgplatform-com/055254039010_01_003'
	101001000F18EA00 = QB02 's3://receiving-dgcs-tdgplatform-com/055269445010_01_003'

**Description of Input Parameters and Options for the "aoptask":**

**REQUIRED SETTINGS AND DEFINITIONS:**

* S3 location of 1B input data:
    * Required = ‘True’
    * type = ‘directory’
    * name = ‘data’
    
* Define the AOP Task:
    * Required = ‘True’
    * aoptask = gbdx.Task("AOP_Strip_Processor,data=data,"opt1”,”opt2”,etc...)

* Define the Output Directory: (a gbd-customer-data location)
    * Required = ‘true’
    * type = ‘directory’
    * name = "destination"

* Define the Output log Directory",
    * Required = true      
    * type = directory
    * name =  "log"

* Define Stage to S3 location:
    * S3task = gbdx.Task("StageDataToS3",data=” ”,destination=” “)

**OPTIONAL SETTINGS: Default = True or Auto**

**The Default setting will run the process or automatically determine the proper value to run the process. It is recommended to use ACOMP for the best image quality, therefore the Default ='True'. The one exception is WV01 or any Panchromatic-only processed Imagery from other sensors, where ACOMP should be set to 'False'. For Panchromatic Imagery, you can only run the ortho-rectification process. An example is given below. Please contact us for assitance if you have any questions regarding the processesing of Panchromatic Imagery.**

**Example aoptask for WV01:**This produces an orthorectified panchromatic image.

	aoptask = gbdx.Task("AOP_Strip_Processor", data=data, enable_acomp=False, enable_pansharpen=False, enable_dra=False)

* Enable/disable AComp. Choices are 'true' or 'false'. 
    * Default = ‘true’
    * Required = ‘false’
    * type = ‘string’
    * name = ‘enable_acomp’

* Enable/disable pan sharpening. Choices are 'true' or 'false'. 
    * Default = 'true'
    * Required = ‘false’
    * Type = ‘string’
    * name = ‘enable_pansharpen’

* Enable/disable dynamic range adjustment (DRA). Choices are 'true' or 'false'. DRA should be disabled, if you want to run AOP on both PAN+MS simultaneously without PanSharpening. 
    * Default = ‘true’
    * Required = ‘false’
    * type = ‘string’
    * name = ‘enable_dra’

**Script Example PanSharpen & DRA All Bands:**This will produce an AComp'ed, Pansharpened, RGB Image

	aoptask = gbdx.Task("AOP_Strip_Processor", data=data, enable_acomp=True, enable_pansharpen=True, enable_dra=True)


* Bands to process. Choices are 'PAN+MS', 'PAN', 'MS', 'Auto'. 
    * Default = 'Auto', which searches for band IDs in IMD files
    * Required = false
    * type = "string"
    * name = "bands"

**Script Example to Produce MS Bands Only:**When only 8-band output is required.

    aoptask = gbdx.Task("AOP_Strip_Processor", data=data, enable_acomp=True, enable_pansharpen=False, bands='MS', enable_dra=False)

**OPTIONAL SETTINGS: Default = False or a specified Valued that can be changed (e.g. changing the projection from the default WGS84 to UTM).**

* Enable/disable output tiling. Choices are 'true' or 'false'. 
    * Default = 'false'. If 'true', the 'ortho_tiling_scheme' input must be set.",
    * Required = ‘false’
    * type": "string"
    * Name = "enable_tiling"

* Set Input for 'ortho_tiling_scheme'. This consists of Comma-separated list of numeric strip parts to process. 
    * Default = process all strip parts
    * Required = false,
    * Type = "string",
    * Name = "parts"
    
* Ortho EPSG projection. String "UTM" is also allowed. Specify along with ortho_pixel_size. Overridden by ortho_tiling_scheme if specified. 
    * Default = 'EPSG:4326'  
    * Required = false
    * type = "string"
    * name = "ortho_epsg"

**Script Example Reproject to UTM**

	aoptask = gbdx.Task("AOP_Strip_Processor", data=data, enable_acomp=True, enable_pansharpen=False, enable_dra=False, ortho_epsg="EPSG:32633") # specify UTM Zone
    
    aoptask = gbdx.Task("AOP_Strip_Processor", data=data, enable_acomp=True, enable_pansharpen=False, enable_dra=False, ortho_epsg="UTM") # Will automatically determine the UTM Zone

* Ortho pixel size in meters. Specify along with ortho_epsg. Overridden by ortho_tiling_scheme when specified. 
    * Default = 'Auto', which uses the pixel size of the input data.",
    * Required = false,
    * type = "string"
    * Name = "ortho_pixel_size"

**Script Example Changing Ortho Output Pixel Size**  (Default for non-pansharpened MS=2 meters); make sure both PanSharpen and DRA are disabled. Caveat: You are changing the PAN pixel size (Default = 0.50m) and the MS pixel size will be downsampled proportionally.

	aoptask = gbdx.Task("AOP_Strip_Processor", data=data, enable_acomp=True, enable_pansharpen=False, enable_dra=False, ortho_pixel_size="3")
    
* Set inputs for 'ortho tiling scheme'. This is a tiling scheme and zoom level, e.g. 'DGHalfMeter:18'. Overrides ortho_epsg and ortho_pixel_size.
    * Required = false,
    * type = "string".
    * name = "ortho_tiling_scheme"

* Designate 'parts' of the strip to be processed.  This consists of a comma-separated list of numeric strip parts.
	*Default = process the entire strip
	*Required = false
	*Type ="string"
	*Name = "parts"

* Ortho DEM specifier. Options are 'NED', 'SRTM30', 'SRTM90'. 
    * Default = 'SRTM90'
    * Required = false
    * Type = "string"
    * Name = "ortho_dem_specifier"


**Script Example Change DEM to SRTM30**

	aoptask = gbdx.Task("AOP_Strip_Processor", data=data, enable_acomp=True, enable_pansharpen=False, enable_dra=False, ortho_dem_specifier="SRTM30")

* Ortho pixel interpolation type. Options are 'Nearest', 'Bilinear', 'Cubic'. 
    * Default is 'Cubic’
    * Required": false,
    * type = "string",
    * name = "ortho_interpolation_type"

**Script to Change Interpolation method to Bilinear**

	aoptask = gbdx.Task("AOP_Strip_Processor", data=data, enable_acomp=True, enable_pansharpen=False, enable_dra=False, ortho_interpolation_type="Bilinear")

**The Dynamic Range Adjustment Mode (DRA) should be run using the default setting 'enable_dra=True', which will be adequate for most imagery.  The adjustments described below should only be used in special cases as discussed at the end of this document.**

* Dynamic Range Adjustment mode. Options are 'IntensityAdjust', 'BaseLayerMatch'. 
    * Default is 'IntensityAdjust' 
        * 'BaseLayerMatch' is currently only compatible with EPSG:4326.",
    * Required = false,
    * type = "string",
    * name = "dra_mode"

* Dynamic range adjustment low cutoff percentage. Range is from 0 to 100. 
    * Default is 0.5. Only used for 'IntensityAdjust' mode.","
    * Required": false,
    * type = "string"
    * Name = "dra_low_cutoff"

* Dynamic range adjustment high cutoff percentage. Range is from 0 to 100. 
    * Default is 99.95. Only used for 'IntensityAdjust' mode
    * Required = false
    * type = "string"
    * name = "dra_high_cutoff"
    
* Dynamic range adjustment gamma value. 
    * Default = 1.25. Only used for 'IntensityAdjust' mode.
    * Required = false
    * type = "string"
    * name = "dra_gamma"

* Dynamic range adjustment output bit depth. Choices are 8 or 16. 
    * Default = 8. Only used for 'IntensityAdjust' mode.
    * Required = false
    * type = "string"
    * name = "dra_bit_depth"

* Zoom level (i.e. size) of output tiles if tiling is enabled. 
    * Default = 12.
    * Required = false
    * type = "string",
    * name = "tiling_zoom_level"



**Data Structure for Expected Outputs:**

Your Processed Imagery will be written to your specified S3 Customer Location (e.g.  s3://gbd-customer-data/unique customer id/named directory/).  When you open the 'named directory' your files should look like this:

![First Directory](https://lh3.googleusercontent.com/-YzyRjMprZ54/VyJqnZjA7oI/AAAAAAAAJaw/hqIopdghThsz9eU9uEN4sUpz8iA7WoscQCLcB/s0/datastructure1.PNG "datastructure1.PNG")

There will be a *standard error file* (###.stderr) and a *standard output file* (###.stdout). These files track the progress of the process and can be downloaded and reviewed, especially if the task has failed to produce a final output.  You must include example lines [323], [324] and [328] in your script to record this output. The *workorder_'SOLI'.xml* file details the input parameters applied to the AOP Strip Processor.  

Click on the Folder at the bottom of the list identified by the 'Sales Order Line Item' (SOLI). Inside this directory you will find the processed imagery output (e.g. below).  The .IMD and .XML files describe the spectral and physical characteristics of the Imagery Product.  The *assembly_MS.tif* and *assembly_PAN.tif* are the imagery files that can be viewed in standard GIS and Remote Sensing Software.  the .vrt files are GDAL virtual raster format that allows viewing of the complete image without making a mosaic.




![Second Directory](https://lh3.googleusercontent.com/-_lAVdacJf2c/VyJqZp78PAI/AAAAAAAAJao/1Px_21rWHBQEjbqyi_orY-BnTiH0-ZtGACLcB/s0/datastructure2.PNG "datastructure2.PNG")

**Notes on Special DRA Settings:**

**Dynamic range adjustment mode** – IntensityAdjust is for standalone, individual images that are not going to be mosaicked together. BaseLayerMatch uses a global base layer for color matching and helps maintain consistency when mosaicking. The base layer started out as color-balanced and mosaicked Landsat imagery but may have started incorporating higher-res imagery also.

**Dynamic range adjustment low cutoff percentage** – Sets the black point in the histogram. Adjusting this will change the point in the histogram that is considered “black” and will darken and lighten the low end of the histogram. Setting the number lower (<0.5) will brighten the darker color tones and make the overall image lighter. Setting the number higher will saturate more of the darker color tones and make the overall image darker. Could start to lose detail in the darker areas if too heavy-handed. A light touch can make a huge difference so be careful.

**Dynamic range adjustment high cutoff percentage** – Sets the white point in the histogram. Same general idea as the low cutoff percentage but operates on the brightest color tones to adjust what is considered saturated “white”. Setting this number lower (<99.95) will brighten the image while setting the number higher will darken the image. Again, a light touch is mandatory to keep things looking “normal”.

**Dynamic range adjustment gamma value** – Adjusts the curvature of the transfer function from input to output. When gamma=1, that is a straightforward, linear transfer from input to output. When gamma>1, the image will get overall brighter. Conversely, the image will get overall darker when gamma<1. Works in conjunction with the histogram cutoff values but is a completely independent parameter. Operates like a root stretch but with much finer adjustment settings. All three parameters, low cutoff, high cutoff, and gamma, work together to adjust the overall brightness, contrast, and dynamic range of the image. They’re all independent and will affect the final DRAed image in similar, but different, ways. Setting these is more an art than a science and it’s highly recommended to NOT mess with these unless the image is one of those special cases and is totally screwed up. Then the art comes into play.

**Dynamic range adjustment output bit depth** – Should NEVER be set to anything other than 8. DRA is valid and makes sense ONLY for 8bit output imagery. Running DRA to get a 16bit DRAed image will get you nothing since you still have to scale the image to 8bits/band for display purposes anyway.


For background on the development and implementation of AOP refer to the [Advanced Ortho Processor PDF.](http://tu00aopapp006:8102/job/AOP-Docs/ws/build/latex/AOP-AdvancedOrthoProcessor.pdf)


