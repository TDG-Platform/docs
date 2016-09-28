### Description
This task creates a classification raster by thresholding on select data ranges and colors to highlight areas of a raster.  By default, 16 classes are generated with the first 16 colors of the 'Rainbow' color table.

This task can be run with Python using [gbdxtools](https://github.com/DigitalGlobe/gbdxtools) or through the [GBDX Web Application](https://gbdx.geobigdata.io/materials/)

### Table of Contents
 * [Quickstart](#quickstart) - Get started!
 * [Inputs](#inputs) - Required and optional task inputs.
 * [Outputs](#outputs) - Task outputs and output structure.
 * [Advanced](#advanced) - Additional information for advanced users.
 * [Runtime](#runtime) - Example estimate of task runtime.
 * [Issues](#issues) - Current or past known issues.
 * [Background](#background) - Background information.
 * [Contact](#contact) - Contact information.

### Quickstart

Quick start example.

```python
# Quickstart example for ENVI_ColorSliceClassification.  

from gbdxtools import Interface
gbdx = Interface()
raster = 's3://gbd-customer-data/PathToImage/image.tif'
ENVI_ColorSliceClassification = gbdx.Task('ENVI_ColorSliceClassification', raster=raster)

workflow = gbdx.Workflow([ENVI_ColorSliceClassification])  
workflow.savedata(ENVI_ColorSliceClassification.outputs.data, location='ENVI_ColorSliceClassification')
workflow.execute()

print workflow.id
print workflow.status
```

### Inputs
The following table lists all taskname inputs.
Mandatory (optional) settings are listed as Required = True (Required = False).

  Name  |  Required  |  Default  |  Valid Values  |  Description  
--------|:----------:|-----------|----------------|---------------
file_types|False|None| .hdr, .tif|GBDX Option. Comma seperated list of permitted file type extensions. Use this to filter input files -- Value Type: STRING
input_raster|True|None|ENVI raster dataset |Specify a 1 band raster on which to perform color slice classification. -- Value Type: ENVIRASTER
color_table_name|False|None|[LOADCT] (http://www.harrisgeospatial.com/docs/loadct_procedure.html)|Specify a string with the name of an IDL color table.  The default value is Rainbow.  Issue the following command to find valid strings: LOADCT, get_name=color_table_names. -- Value Type: STRING
class_colors|False|None| |Specify a (3,n) byte array with the RGB colors for the given ranges, where n is the number of classes.  Use this property in conjunction with CLASS_RANGES. -- Value Type: BYTE
reverse_color_table|False|None| true, false |Set this property to reverse the color table.  Use this property in conjunction with COLOR_TABLE_NAME property. The options are true or false. -- Value Type: BOOL
data_maximum|False|None| Varies depending on raster values|Specify the maximum value used to calculate data ranges with NUMBER_OF_RANGES.  If this is not set, then the largest value in the INPUT_RASTER band is used. -- Value Type: DOUBLE
class_ranges|False|None| e.g. NUMBER_OF_RANGES = 5|Specify a (2,n) array of color slice ranges, where n is the number of classes.  In each array element, specify the minimum and maximum data value for the class. -- Value Type: DOUBLE
range_size|False|None| |Specify the width of each data range to create.  The NUMBER_OF_RANGES is used in conjunction with RANGE_SIZE.  Any data above DATA_MINIMUM+NUMBER_OF_RANGES*RANGE_SIZE will not be classified.  -- Value Type: DOUBLE
data_minimum|False|None|Varies depending on raster values |Specify the minimum value used to calculate data ranges with NUMBER_OF_RANGES or RANGE_SIZE.  If this is not set, then the smallest value in the INPUT_RASTER band is used. -- Value Type: DOUBLE
number_of_ranges|False|None| dependent on minimum and maximum |Specify the number of data ranges to create.  If RANGE_SIZE is specified, then the ranges are each that width, starting at DATA_MINIMUM and ending at DATA_MINIMUM+NUMBER_OF_RANGES*RANGE_SIZE.  If RANGE_SIZE is not specified, then the ranges are equal width between DATA_MINIMUM and DATA_MAXIMUM. -- Value Type: UINT
output_raster_uri_filename|False|None|  |Output OUTPUT_RASTER. -- Value Type: ENVIURI

### Outputs
The following table lists all taskname outputs.
Mandatory (optional) settings are listed as Required = True (Required = False).

  Name  |  Required  |  Default  |  Valid Values  |  Description  
--------|:----------:|-----------|----------------|---------------
task_meta_data|False|None| |GBDX Option. Output location for task meta data such as execution log and output JSON
output_raster_uri|True|None| Folder name in S3 location|Outputor OUTPUT_RASTER. -- Value Type: ENVIURI

**Output structure**

Explain output structure via example.


### Advanced
Include example(s) with complicated parameter settings and/or example(s) where
ENVI_ColorSliceClassification is used as part of a workflow involving other GBDX tasks.

```python
#AOP strip processor has input values known to complete the Spectral Index task
from gbdxtools import Interface
gbdx = Interface()


data = 's3://receiving-dgcs-tdgplatform-com/054876618060_01_003'

aoptask = gbdx.Task("AOP_Strip_Processor", data=data, enable_acomp=True, enable_pansharpen=False, enable_dra=False, bands='MS')

# Capture AOP task outputs
#orthoed_output = aoptask.get_output('data')

aop2envi = gbdx.Task("AOP_ENVI_HDR")
aop2envi.inputs.image = aoptask.outputs.data.value

#hdr file used to compute spectral index

envi_ndvi = gbdx.Task("ENVI_SpectralIndex")
envi_ndvi.inputs.input_raster = aop2envi.outputs.output_data.value
envi_ndvi.inputs.file_types = "hdr"
envi_ndvi.inputs.index = "Normalized Difference Vegetation Index"

#spectral index file used in color slice classification task

envi_color = gbdx.Task('ENVI_ColorSliceClassification', input_raster=envi_ndvi.outputs.output_raster_uri.value)
envi_color.file_types = 'hdr'


workflow = gbdx.Workflow([aoptask, aop2envi, envi_ndvi, envi_color])

workflow.savedata(
  envi_ndvi.outputs.output_raster_uri,
  location='Benchmark/color_slice/NDVI'
)

workflow.savedata(
  envi_color.outputs.output_raster_uri,
  location='Benchmark/color_slice/Color16'
)

workflow.execute()

print workflow.execute()
print workflow.id
print workflow.status

```

### Runtime

The following table lists all applicable runtime outputs. (This section will be completed the Algorithm Curation team)
For details on the methods of testing the runtimes of the task visit the following link:(INSERT link to GBDX U page here)

  Sensor Name  |  Average runtime  |  Total Area (k2)  |  Time(min)  |  Time/Area k2
--------|:----------:|-----------|----------------|---------------
QB | 41,551,668 | 312.07 |  |  |
WV01| 1,028,100,320 |351.72 | | |
WV02|35,872,942|329.87| | |
WV03|35,371,971|196.27| | |
GE| 57,498,000|332.97| | |

### Issues
Requires a single band raster as input.


### Background
For background on the development and implementation of ENVI_ColorSliceClassification see [here](http://www.harrisgeospatial.com/docs/ENVIColorSliceClassificationTask.html).


### Contact
Document Owner - Carl Reeder - creeder@digitalglobe.com
