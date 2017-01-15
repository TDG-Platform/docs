# ENVI_SpectralIndex

ENVI_SpectralIndex. This task creates a spectral index raster from one pre-defined spectral index. Spectral indices are combinations of surface reflectance at two or more wavelengths that indicate relative abundance of features of interest. This task is used to compute a single index on a combination of multi spectral bands within an image. This task can be used to compute indices such as the Normalized Difference Vegetation Index (NDVI). An index such as NDVI will be passed into the task and a single band raster with the results of the index will be returned as output.
Note:  The wavelength metadata is not available in the correct format from the AOP task. Therefore this task is dependent on the "AOP_ENVI_HDR" task  

### Table of Contents
 * [Quickstart](#quickstart) - Get started!
 * [Inputs](#inputs) - Required and optional task inputs.
 * [Outputs](#outputs) - Task outputs and example contents.
 * [Advanced](#advanced) - Additional information for advanced users.
 * [Runtime](#runtime) - Example estimate of task runtime.
 * [Background](#background) - Background information.
 * [Contact Us](#contact-us) - Contact tech or document owner.

### Quickstart

This script gives the example of ENVI Spectral Index with a single tif file as input.

```python
# Quickstart **Example Script Run in Python using the gbdxTools InterfaceExample producing a single band vegetation mask from a tif file.
# First Initialize the Environment

from gbdxtools import Interface
gbdx = Interface()

#Edit the following path to reflect a specific path to an image
image = 's3://gbd-customer-data/CustomerAccount#/PathToImage/'

envi_ndvi = gbdx.Task("ENVI_SpectralIndex")
envi_ndvi.inputs.input_raster = image
envi_ndvi.inputs.index = "Normalized Difference Vegetation Index"

workflow = gbdx.Workflow([envi_ndvi])
#Edit the following line(s) to reflect specific folder(s) for the output file (example location provided)

workflow.savedata(
   envi_ndvi.outputs.output_raster_uri,
      location='NDVI/output_raster_uri'
)

print workflow.execute()
```

### Inputs
The following table lists all taskname inputs.
Mandatory (optional) settings are listed as Required = True (Required = False).
For details regarding the use of input ports refer to the [ENVI Task Runner](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner.md) documentation.

**Description of Input Parameters and Options for the "ENVI_SpectralIndex":**
This task will work on Digital Globe images with a IMD file located in the S3 location:
Input imagery sensor types include: QuickBird, WorldView 1, WorldView 2, WorldView 3 and GeoEye
The following table lists the Spectral Index task inputs.
All inputs are **required**

Name                     |       Default         |        Valid Values             |   Description
-------------------------|:---------------------:|---------------------------------|-----------------
input_raster             |          N/A          | S3 URL   .TIF and .hdr only     | S3 location of input .tif file processed through AOP_Strip_Processor.
index                    |          N/A          |     string of index name        | Specify a string, or array of strings, representing the pre-defined spectral indices to apply to the input raster.
input_raster_band_grouping| N/A                  | Sensor Specific [See input port documentation](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner.md#ENVIRPCRasterSpatialRef) | Specify band group e.g. "multispectral".  input_raster_band_grouping "panchromatic" will not function in the Spectral Index task.
output_raster_uri_filename | N/A | string name for output e.g. "NDVI" | output raster file name

### Outputs

The following table lists the Spectral Index task outputs.

Name                  |       Default         |        Valid Values             |   Description
----------------------|:---------------------:|---------------------------------|-----------------
output_raster_uri     |          N/A          |  S3 URL   .TIF and .hdr only    | S3 location of input .tif file processed through AOP_Strip_Processor.
task_meta_data|N/A| GBDX Option. Output location for task meta data such as execution log and output JSON

**OPTIONAL SETTINGS: Required = False**


Name                         |       Default         |        Valid Values             |   Description
-----------------------------|:---------------------:|---------------------------------|-----------------
file_types                   |          N/A          |     string of index name        | Specify a string, or array of strings, representing the pre-defined spectral indices to apply to the input raster.
output_raster_uri_filename   |          N/A          | S3 URL   .TIF and .hdr only     | S3 location of input .tif file processed through AOP_Strip_Processor.
task_meta_data               |          N/A          |     string of index name        | Specify a string, or array of strings, representing the pre-defined spectral indices to apply to the input raster.


**Description of Output and options for the "ENVI_SpectralIndex":**
This task will provide a raster of the spectral index output in both an ENVI hdr format and tif format.

**Data Structure for Expected Outputs:**

The processed imagery will be written to the specified S3 Customer Location in a 1 band TIF format(e.g.  s3://gbd-customer-data/unique customer id/named directory/).

### Advanced
To link the workflow of 1 input image into AOP_Strip_Processor and the Spectral Index task, use the following GBDX tools script in python. Updates to the ENVI task runner

```python
#First initialize the environment
#AOP strip processor has input values known to complete the Spectral Index task

from gbdxtools import Interface
gbdx = Interface()

#Edit the following path to reflect a specific path to an image
data = 's3://gbd-customer-data/CustomerAccount#/PathToImage/'
aoptask = gbdx.Task("AOP_Strip_Processor", data=data, enable_acomp=True, enable_pansharpen=False, enable_dra=False, bands='MS')

# Capture AOP task outputs
#orthoed_output = aoptask.get_output('data')

envi_ndvi = gbdx.Task("ENVI_SpectralIndex")
envi_ndvi.inputs.input_raster = aoptask.outputs.data.value
envi_ndvi.inputs.index = "Normalized Difference Vegetation Index"
envi_ndvi.inputs.input_raster_metadata = '{"sensor type": "WORLDVIEW-3"}'

workflow = gbdx.Workflow([aoptask, envi_ndvi])

#Edit the following line(s) to reflect specific folder(s) for the output file (example location provided)

workflow.savedata(
  envi_ndvi.outputs.output_raster_uri,
  location='NDVI/SI/output_raster_uri'
)

print workflow.execute()

```

### Runtime

The following table lists all applicable runtime outputs. (This section will be completed the Algorithm Curation team)
For details on the methods of testing the runtimes of the task visit the following link:(INSERT link to GBDX U page here)

  Sensor Name  | Total Pixels |  Total Area (k2)  |  Time(secs)  |  Time/Area k2
--------|:----------:|-----------|----------------|---------------
QB | 41,551,668 | 312.07 |194.58|0.62    
WV01| 1,028,100,320 |NA |NA
WV02|35,872,942|1,265.14|216.12|0.66
WV03|35,371,971|196.27|1,265.14|6.45
GE| 57,498,000|332.97|185.33|0.56


###Known Issues
1) To run the task in a single workflow with AOP the tif file must first be removed from the AOP folder with the additional python commands listed in Advanced


For background on the development and implementation of Spectral Index refer to the [ENVI Documentation](https://www.harrisgeospatial.com/docs/spectralindices.html)

###Contact Us
Document Owner - Carl Reeder - creeder@digitalglobe.com
