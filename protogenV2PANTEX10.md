# 8-Band Built-up extent (protogenV2PANTEX10)

PANTEX10 is an un-supervised protocol for computing a built-up expectation layer from 8 band (optical + VNIR) image data-sets. This is a binary image in which intensity 255 indicates that it is likely that a pixel coincides with a built-up area and intensity 0 that a pixel does not coincide with a built-up area.  The building stock defining the built-up areas excludes those with roofs covered with ceramic tiles.


### Table of Contents
 * [Quickstart](#quickstart) - Get started!
 * [Inputs](#inputs) - Required and optional task inputs.
 * [Outputs](#outputs) - Task outputs and example contents.
 * [Advanced](#advanced) - Additional information for advanced users.
 * [Runtime](#runtime) - Results of task benchmark tests.
 * [Known Issues](#known-issues) - current or past issues known to exist.
 * [Contact Us](#contact-us) - Contact tech or document owner.

### Quickstart

**Example Script:** Run in IPython using the [GBDXTools Interface] (https://github.com/DigitalGlobe/gbdxtools)


This script gives the example of Pantex with a single tif file as input.

```python
    from gbdxtools import Interface
    gbdx = Interface()

    #Edit the following path to reflect a specific path to an image
    raster = 's3://gbd-customer-data/CustomerAccount#/PathToImage/'
    prototask = gbdx.Task("protogenV2PANTEX10", raster=raster)

    workflow = gbdx.Workflow([ prototask ])  
    #Edit the following line(s) to reflect specific folder(s) for the output file (example location provided)
    workflow.savedata(prototask.outputs.data, location="protogen/BuiltUpExtent")
    workflow.execute()

    print workflow.id
    print workflow.status
```
### Inputs
**Description of Input Parameters and Options for "protogenV2PANTEX10":**

WorldView 2 or WorldView 3 multi-spectral imagery (8-band optical and VNIR data sets) that has been atmospherically compensated by the AOP processor.  Supported formats are .TIF

Name                     |       Default         |        Valid Values             |   Description
-------------------------|:---------------------:|---------------------------------|-----------------
raster                   |          N/A          | S3 URL   .TIF only              | S3 location of input .tif file processed through AOP_Strip_Processor.

**REQUIRED SETTINGS AND DEFINITIONS:**

### Outputs

The following table lists the Pantex Protogen task outputs.

Name | Required |   Description
-----|:--------:|-----------------
data |     Y    | This will explain the output file location and provide the output in .TIF format.
log  |     N    | S3 location where logs are stored.

**OPTIONAL SETTINGS: Required = False**

* NA - No additional optional settings for this task exist

### Runtime

The following table lists all applicable runtime outputs. (This section will be completed the Algorithm Curation team)
For details on the methods of testing the runtimes of the task visit the following link:(INSERT link to GBDX U page here)

  Sensor Name  |  Total Pixels  |  Total Area (k2)  |  Time(secs)  |  Time/Area k2
--------|:----------:|-----------|----------------|---------------
WV02|35,872,942|329.87|118.36 |0.36|
WV03|35,371,971|196.27| 161.39|0.82 |


**Data Structure for Expected Outputs:**

Your Processed Imagery will be written as Binary .TIF image type UINT8x1 and placed in the specified S3 Customer Location (e.g.  s3://gbd-customer-data/unique customer id/named directory/).  

###Known issues:  Highly granular rock-covered areas might be interpreted as built-up areas.

**Limitations:** Ceramic roofs are not considered.  


For background on the development and implementation of Protogen  [Documentation under development](Insert link here)

###Contact Us
Tech Owner - [Georgios Ouzounis](gouzouni@digitalglobe.com)
Document Owner - [Carl Reeder](creeder@digitalglobe.com)
