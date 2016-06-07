# 8-Band Vegetation Mask (protogenV2RAV)

RAV is an un-supervised protocol for computing vegetation masks from 8 band (optical + VNIR) image data-sets. The vegetation mask is a binary image in which intensity 255 indicates the presence of vegetation and intensity 0 the absence of vegetation. Vegetation is defined as any type of flora with healthy chlorophyll content. 

**Example Script:** Run in IPython using the [GBDXTools Interface] (https://github.com/DigitalGlobe/gbdxtools)


    from gbdxtools import Interface 
    import json
    gbdx = Interface()
    raster = 's3://gbd-customer-data/7d8cfdb6-13ee-4a2a-bf7e-0aff4795d927/PathToImage/image.tif'
    prototask = gbdx.Task("protogenV2RAV", raster=raster)

    workflow = gbdx.Workflow([ prototask ])  
    workflow.savedata(prototask.outputs.data, location="protogen/RAV")
    workflow.execute()

    print workflow.id
    print workflow.status
	

**Description of Input Parameters and Options for the**** "protogenV2RAV":**

WorldView 2 or WorldView 3 multi-spectral imagery (8-band optical and VNIR data sets) that has been atmospherically compensated by the AOP processor.  Supported formats are .TIF, .TIL, .VRT, .HDR.

**REQUIRED SETTINGS AND DEFINITIONS:**

* Define the Task:
    * Required = ‘true’
    * gbdxtask = gbdx.Task("protogenV2RAV")

* S3 location of input data 'raster'(Must be run through AOP_strip_processor to have ortho-rectification and atmospheric compensation. Formats.TIF, .TIL, .VRT, .HDR.   ):
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



###Postman status @ 06/07/16

**Successful run with Tif file.  Testing additional input formats still in progress.  .VRT is currently not functioning (6/7/2016)**



**Data Structure for Expected Outputs:**

Your Processed Imagery will be written as Binary .TIF image type UINT8x1 and placed in the specified S3 Customer Location (e.g.  s3://gbd-customer-data/unique customer id/named directory/).  


For background on the development and implementation of  Protogen  [Protogen Documentation](Insert link here)

