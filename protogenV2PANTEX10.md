# 8-Band Built-up extent (protogenV2PANTEX10)

PANTEX10 is an un-supervised protocol for computing a built-up expectation layer from 8 band (optical + VNIR) image data-sets. This is a binary image in which intensity 255 indicates that it is likely that a pixel coincides with a built-up area and intensity 0 that a pixel does not coincide with a built-up area.  The building stock defining the built-up areas excludes those with roofs covered with ceramic tiles.

**Example Script:** Run in IPython using the [GBDXTools Interface] (https://github.com/DigitalGlobe/gbdxtools)


    from gbdxtools import Interface 
    import json
    gbdx = Interface()
    raster = 's3://gbd-customer-data/7d8cfdb6-13ee-4a2a-bf7e-0aff4795d927/PathToImage/image.tif'
    prototask = gbdx.Task("protogenV2PANTEX10", raster=raster)

    workflow = gbdx.Workflow([ prototask ])  
    workflow.savedata(prototask.outputs.data, location="protogen/BUE")
    workflow.execute()

    print workflow.id
    print workflow.status
	

**Description of Input Parameters and Options for "protogenV2PANTEX10":**

WorldView 2 or WorldView 3 multi-spectral imagery (8-band optical and VNIR data sets) that has been atmospherically compensated by the AOP processor.  Supported formats are .TIF, .TIL, .HDR.

**REQUIRED SETTINGS AND DEFINITIONS:**

* Define the Task:
    * Required = ‘true’
    * gbdxtask = gbdx.Task("protogenV2PANTEX10")

* S3 location of input data 'raster'(Must be run through AOP_strip_processor to have ortho-rectification and atmospheric compensation. Formats.TIF, .TIL, .HDR.   ):
    * Required = ‘true’
    * type = ‘directory’
    * name = ‘raster’
    
* Define the Output Directory: The output directory of text file(a gbd-customer-data location)
    * Required = ‘true’
    * type = ‘output’
    * name = "data"

* Define Stage to S3 location:
    * workflow.savedata(prototask.outputs.data, location="S3Location/")

**OPTIONAL SETTINGS: Required = False**

* NA - No additional optional settings for this task exist



###Postman status @ 06/09/16

**Successful run with Tif file.  Testing additional input formats still in progress.  .VRT is currently not functioning (6/7/2016)**



**Data Structure for Expected Outputs:**

Your Processed Imagery will be written as Binary .TIF image type UINT8x1 and placed in the specified S3 Customer Location (e.g.  s3://gbd-customer-data/unique customer id/named directory/).  

**Known issues:**  Highly granular rock-covered areas might be interpreted as built-up areas.

**Limitations:** Ceramic roofs are not considered.  


For background on the development and implementation of  Protogen  [Documentation under development](Insert link here)

