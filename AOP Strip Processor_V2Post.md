# AOP Strip Processor (Advanced Ortho Product)

The AOP Strip Processor generates large scale, color balanced ortho mosaics in a semi-automated fashion.  Level 1B imagery is processed according to defined inputs.  The AOP Strip Processor can be run through a simple Python script using  [gbdxtools](https://github.com/DigitalGlobe/gbdxtools/blob/master/docs/user_guide.rst), which requires some initial setup, or through the [GBDX Web Application](https://gbdx.geobigdata.io/materials/).  Tasks and workflows can be added to AOP (described here in [gbdxtools](https://github.com/DigitalGlobe/gbdxtools/blob/master/docs/running_workflows.rst)) or run separately after the AOP process is completed.

**Example Script:**

     from gbdxtools import Interface 
     import json
     gbdx = Interface()
       
     # WV03 Image over Naples, Italy 
     # Make sure DRA is disabled if you are processing both the PAN+MS files
       
     data = "s3://receiving-dgcs-tdgplatform-com/055249130010_01_003"
     aoptask = gbdx.Task("AOP_Strip_Processor", data=data,
     enable_acomp=True, enable_pansharpen=False, enable_dra=False)
     
    # Capture AOP task outputs log = aoptask.get_output('log') orthoed_output = aoptask.get_output('data')
        
    destination = 's3://kathleen_Naples_WV03_Test1' 
    s3task = gbdx.Task("StageDataToS3", data=orthoed_output, destination=destination) 
    s3task2 = gbdx.Task("StageDataToS3", data=log, destination=destination)

    workflow = gbdx.Workflow([ s3task, s3task2, aoptask ])  # the ordering
    doesn't matter here. workflow.execute()
           
    print workflow.id
    print workflow.status
     
**Example Run in IPython:**

    In [316]: from gbdxtools import Interface
    In l317]: import json
    In [318]: gbdx = Interface()
    In [319]: # WV03 Image over Naples, Italy
    In [320]: # Make sure DRA is disabled if you are processing both the PAN+MS files
    In [321]: data = "s3://receiving-dgcs-tdgplatform-com/055249130010_01_003"
    In [322]: aoptask = gbdx.Task("AOP_Strip_Processor", data=data, enable_acomp=True, enable_pansharpen=False, enable_dra=False)
    In [323]: # Capture AOP task outputs
    In [324]: log = aoptask.get_output('log')
    In [325]: orthoed_output = aoptask.get_output('data')
    In [326]: destination = 's3://kathleen_Naples_WV03_Test1'
    In [327]: s3task = gbdx.Task("StageDataToS3", data=orthoed_output, destination=destination)
    In [328]: s3task2 = gbdx.Task("StageDataToS3", data=log, destination=destination)
    In [329]: workflow = gbdx.Workflow([ s3task, s3task2, aoptask ])  # the ordering doesn't matter here.
    In [330]: workflow.execute()
    Out[330]: u'4321584012718856899'
    In [331]: print workflow.id
    4321584012718856899

**Test Datasets for All Sensors (Naples, Italy):**

All sensors have been tested.  The S3 locations of the test data are given below.  Only script examples for WorldView-3 have been posted:

	10200100423D7A00 = WV01 's3://receiving-dgcs-tdgplatform-com/055250712010_01_003'
	103001004DAFAF00 = WV02 's3://receiving-dgcs-tdgplatform-com/055253506010_01_003'
	104001000E25D700 = WV03 's3://receiving-dgcs-tdgplatform-com/055249130010_01_003'
	1050010001136C00 = GE01 's3://receiving-dgcs-tdgplatform-com/055254039010_01_003'
	101001000F18EA00 = QB02 's3://receiving-dgcs-tdgplatform-com/055269445010_01_003'

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

**_The Default setting will run the process or automatically determine the proper value to run the process. It is recommended to use ACOMP for the best image quality, therefore the Default ='True'. The one exception is WV01, where ACOMP should be set to 'False'. ACOMP for WV01 requires custom processing by out Team.  Please contact us for assitance.  _**

Example aoptask for WV01:

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

* Enable/disable dynamic range adjustment (DRA). Choices are 'true' or 'false'. DRA should be disabled, if you want to run AOP on both PAN+MS simultaneously without PanSharpening. In order to apply DRA with a successful output to MS bands only with no Pansharpening, you must set "bands"=MS.
    * Default = ‘true’
    * Required = ‘false’
    * type = ‘string’
    * name = ‘enable_dra’

**Script Example PanSharpen & DRA All Bands:**

aoptask = gbdx.Task("AOP_Strip_Processor", data=data, enable_acomp=True, enable_pansharpen=True, enable_dra=True)

**Script Example DRA MS Bands Only:**

    aoptask = gbdx.Task("AOP_Strip_Processor", data=data, enable_acomp=True, enable_pansharpen=False, bands=MS, enable_dra=True)

* Bands to process. Choices are 'PAN+MS', 'PAN', 'MS', 'Auto'. 
    * Default = 'Auto', which searches for band IDs in IMD files
    * Required = false
    * type = "string"
    * name = "bands"


**OPTIONAL SETTINGS: Default = False or a specified Valued**

**_The Default setting does not run the specified process. Some of these processes (e.g. "enable_tiling" = “True”) may have dependencies that also require resetting. Some of the dependencies have “Auto” settings._**

* Enable/disable output tiling. Choices are 'true' or 'false'. 
    * Default = 'false'. If 'true', the 'ortho_tiling_scheme' input must be set.",
    * Required = ‘false’
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

**Script Example Reproject to UTM**

 

	aoptask = gbdx.Task("AOP_Strip_Processor", data=data, enable_acomp=True, enable_pansharpen=False, enable_dra=False, ortho_epsg="EPSG:32633") # specify UTM Zone
    
    aoptask = gbdx.Task("AOP_Strip_Processor", data=data, enable_acomp=True, enable_pansharpen=False, enable_dra=False, ortho_epsg="UTM") # Will automatically determine the UTM Zone

* Ortho pixel size in meters. Specify along with ortho_epsg. Overridden by ortho_tiling_scheme if specified. 
    * Default = 'Auto', which uses the pixel size of the input data.",
    * Required = false,
    * type = "string"
    * Name = "ortho_pixel_size"
* Ortho tiling scheme and zoom level, e.g. 'DGHalfMeter:18'. Overrides ortho_epsg and ortho_pixel_size.
    * Required = false,
    * type = "string",",
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

**Example Code Run in IPython:**


**Data Structure for Expected Outputs:**

Your Processed Imagery will be written to your specified S3 Customer Location (e.g.  s3://gbd-customer-data/unique customer id/named directory/).  When you open the 'named directory' your files should look like this:

![First Directory](https://lh3.googleusercontent.com/-YzyRjMprZ54/VyJqnZjA7oI/AAAAAAAAJaw/hqIopdghThsz9eU9uEN4sUpz8iA7WoscQCLcB/s0/datastructure1.PNG "datastructure1.PNG")

There will be a *standard error file* (###.stderr) and a *standard output file* (###.stdout). These files track the progress of the process and can be downloaded and reviewed, epsecially if the task has failed to produce a final output.  The *workorder_'SOLI'.xml* file details the input parameters applied to the AOP Strip Processor.  

Click on the Folder at the bottom of the list identified by the 'Sales Order Line Item' (SOLI). Inside this directory you will find the processed imagery output (e.g. below).  The .IMD and .XML files describe the spectral and physical characteristics of the Imagery Product.  The *assembly_MS.tif* and *assembly_PAN.tif* are the imagery files that can be viewed in standard GIS and Remote Sensing Software.  the .vrt files are GDAL virtual raster format that allows viewing of the complete image without making a mosaic.




![Second Directory](https://lh3.googleusercontent.com/-_lAVdacJf2c/VyJqZp78PAI/AAAAAAAAJao/1Px_21rWHBQEjbqyi_orY-BnTiH0-ZtGACLcB/s0/datastructure2.PNG "datastructure2.PNG")



For background on the development and implementation of AOP refer to the [Advanced Ortho Processor PDF.](http://tu00aopapp006:8102/job/AOP-Docs/ws/build/latex/AOP-AdvancedOrthoProcessor.pdf)


