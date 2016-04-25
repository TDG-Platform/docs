# AOP Strip Processor (Advanced Ortho Product)

The AOP Strip Processor generates large scale, color balanced ortho mosaics in a semi-automated fashion.  Level 1B imagery is processed according to defined inputs. PAN, 4-Band and 8-Band Imagery have been tested and can be run successfully. The AOP Strip Processor can be run through a simple Python script using the [GBDXTools Interface](http://gbdxtools.readthedocs.org/en/latest/user_guide.html), which requires some initial setup, or through the [GBDX Web Application](https://gbdx.geobigdata.io/materials/).  Tasks and workflows can be added to AOP (described in Part II) or run separately after the AOP process is completed.

**Example Script: Run in IPython using the GBDXTools Interface**

pip install git+https://github.com/DigitalGlobe/gbdxtools@feature-simpleworkflows

**_The Script can be found here:_**
https://github.com/DigitalGlobe/gbdxtools/blob/feature-simpleworkflows/examples/launch_simple_workflow.py




    from gbdxtools import Interface
	import json
    
    gbdx = Interface()
    
    data = "s3://receiving-dgcs-tdgplatform-com/054813633050_01_003" # WV02 Image over San Francisco
    aoptask = gbdx.Task("AOP_Strip_Processor", data=data, enable_acomp=False, enable_pansharpen=False)
    
    destination = 's3://gbd-customer-data/nate_test/asdf123'
    s3task = gbdx.Task("StageDataToS3", data=aoptask.outputs.data.value, destination=destination)
    
    workflow = gbdx.Workflow([ s3task, aoptask ]) 
    workflow.execute()`



 




**Description of Input Parameters and Options for the**** "aoptask":**

**REQUIRED SETTINGS AND DEFINITIONS:**

* S3 location of 1B input data:
    * Required = ‘True’
    * type = ‘directory’
    * name = ‘data’
* Define the AOP Task:
    * Required = ‘True’
    * aoptask = gbdx.Task("AOP_Strip_Processor,data=data,"opt1”,”opt2”,etc...)
* Define the Output Directory: (a gbd-customer-data location)
    * Required = ‘True’
    * type = ‘directory’
    * name = "destination"
* Define the Output log Directory",
    * Required = 'True '     
    * type = directory
    * name =  "log"
* Define Stage to S3 location:
    * S3task = gbdx.Task("StageDataToS3",data=” ”,destination=” “)

**OPTIONAL SETTINGS: Default = True or Auto**

**_The Default setting will run the process or automatically determine the proper value to run the process._**

* Enable/disable AComp. Choices are 'true' or 'false'. 
    * Default = ‘True’
    * Required = false
    * type = ‘string’
    * name = ‘enable_acomp’
* Enable/disable pan sharpening. Choices are 'true' or 'false'. 
    * Default = 'true'
    * Required = ‘false’
    * Type = ‘string’
    * name = ‘enable_pansharpen’
* Enable/disable dynamic range adjustment (DRA). Choices are 'true' or 'false'. 
    * Default = ‘true’
    * Required = ‘false’
    * type = ‘string’
    * name = ‘enable_dra’
* Bands to process. Choices are 'PAN+MS', 'PAN', 'MS', 'Auto'. 
    * Default = 'Auto', which searches for band IDs in IMD files
    * Required = false
    * type = "string"
    * name = "bands"

**OPTIONAL SETTINGS: Default = False, Auto or a Specified Default Valued**

**_The Default setting does not run the specified process. Some of these processes (e.g. "enable_tiling" = “True”) may have dependencies that also require resetting. Some of the dependencies have “Auto” settings._**

* Enable/disable output tiling. Choices are 'true' or 'false'. 
    * Default = "False".  If 'true the 'ortho_tiling_scheme' input must be set.
    * Required = false
    * type": "string"
    * Name = "enable_tiling"
* Comma-separated list of numeric strip parts to process. 
    * Default = process all strip parts
    * Required = false,
    * Type = "string",
    * Name = "parts"
* Ortho EPSG projection. String 'UTM' is also allowed. Specify along with ortho_pixel_size. Overridden by ortho_tiling_scheme if specified. 
    * Default = 'EPSG:4326'  
    * Required = false
    * type = "string"
    * name = "ortho_epsg"
* Ortho pixel size in meters. Specify along with ortho_epsg. Overridden by ortho_tiling_scheme if specified. 
    * Default = 'Auto', which uses the pixel size of the input data.",
    * Required = false,
    * type = "string"
    * Name = "ortho_pixel_size"
* Ortho tiling scheme and zoom level, e.g. 'DGHalfMeter:18'. Overrides ortho_epsg and ortho_pixel_size.
    * Required = false,
    * type = "string"
    * name  "ortho_tiling_scheme"
* Ortho DEM specifier. Options are 'NED', 'SRTM30', 'SRTM90'. 
    * Default = 'SRTM90'
    * Required = false
    * Type = "string"
    * Name = "ortho_dem_specifier"
* Ortho pixel interpolation type. Options are 'Nearest', 'Bilinear', 'Cubic'. 
    * Default is 'Cubic’
    * Required": false,
    * type = "string",
    * name = "ortho_interpolation_type"
* AComp AOD grid size in meters per pixel.
    * Default is 10.
    * Required = false,
    * type = "string",
    * name = "acomp_aod_grid_size"
* Dynamic range adjustment mode. Options are 'IntensityAdjust', 'BaseLayerMatch'. 
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

**_Sample Output: Test Run 4/14/16, On R&D Cluster_**

    In [1]: from gbdxtools import Interface
    
    In [2]: import json
    
    In [3]: gbdx = Interface()
    
    2016-04-14 19:49:39,914 - gbdxtools - INFO - Logger initialized
    
    In [4]: data = "s3://receiving-dgcs-tdgplatform-com/055212180010_01_003"
    
    In [5]: aoptask = gbdx.Task("AOP_Strip_Processor", data=data, enable_acomp=True, enable_pansharpen=False)
    
    In [6]: log = aoptask.get_output('log')
    
    In [7]: orthoed_output = aoptask.get_output('data')
    
    In [8]: destination = ' s3://gbd-customer-data/7d8cfdb6-13ee-4a2a-bf7e-0aff4795d927/kathleen_SimpleToolsTest'
    
    In [9]: s3task = gbdx.Task("StageDataToS3", data=orthoed_output, destination=destination)
    
    In [10]: s3task2 = gbdx.Task("StageDataToS3", data=log, destination=destination)
    
    In [11]: workflow = gbdx.Workflow([ s3task, s3task2, aoptask ])  # the ordering doesn't matter here.
    
    In [12]: workflow.execute()
    
    Out[12]: u'4311415112750049799'
    
    In [13]: 
    
    In [13]: print workflow.id
    
    4311415112750049799
    
    In [14]: print workflow.status
    
    2016-04-14 19:52:40,758 - gbdxtools - DEBUG - Get status of workflow: 4311415112750049799
    
    {u'state': u'pending', u'event': u'submitted'}

For background on the development and implementation of AOP refer to the [Advanced Ortho Processor PDF.](http://tu00aopapp006:8102/job/AOP-Docs/ws/build/latex/AOP-AdvancedOrthoProcessor.pdf)

