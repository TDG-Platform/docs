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
file_types|False|None| |GBDX Option. Comma seperated list of permitted file type extensions. Use this to filter input files -- Value Type: STRING
input_raster|True|None| |Specify a 1 band raster on which to perform color slice classification. -- Value Type: ENVIRASTER
color_table_name|False|None| |Specify a string with the name of an IDL color table.  The default value is Rainbow.  Issue the following command to find valid strings: LOADCT, get_name=color_table_names. -- Value Type: STRING
class_colors|False|None| |Specify a (3,n) byte array with the RGB colors for the given ranges, where n is the number of classes.  Use this property in conjunction with CLASS_RANGES. -- Value Type: BYTE[3,]
reverse_color_table|False|None| |Set this property to reverse the color table.  Use this property in conjunction with COLOR_TABLE_NAME property. The options are true or false. -- Value Type: BOOL
data_maximum|False|None| |Specify the maximum value used to calculate data ranges with NUMBER_OF_RANGES.  If this is not set, then the largest value in the INPUT_RASTER band is used. -- Value Type: DOUBLE
class_ranges|False|None| |Specify a (2,n) array of color slice ranges, where n is the number of classes.  In each array element, specify the minimum and maximum data value for the class. -- Value Type: DOUBLE[2,]
range_size|False|None| |Specify the width of each data range to create.  The NUMBER_OF_RANGES is used in conjunction with RANGE_SIZE.  Any data above DATA_MINIMUM+NUMBER_OF_RANGES*RANGE_SIZE will not be classified.  -- Value Type: DOUBLE
data_minimum|False|None| |Specify the minimum value used to calculate data ranges with NUMBER_OF_RANGES or RANGE_SIZE.  If this is not set, then the smallest value in the INPUT_RASTER band is used. -- Value Type: DOUBLE
number_of_ranges|False|None| |Specify the number of data ranges to create.  If RANGE_SIZE is specified, then the ranges are each that width, starting at DATA_MINIMUM and ending at DATA_MINIMUM+NUMBER_OF_RANGES*RANGE_SIZE.  If RANGE_SIZE is not specified, then the ranges are equal width between DATA_MINIMUM and DATA_MAXIMUM. -- Value Type: UINT
output_raster_uri_filename|False|None| |Output OUTPUT_RASTER. -- Value Type: ENVIURI

### Outputs
The following table lists all taskname outputs.
Mandatory (optional) settings are listed as Required = True (Required = False).

  Name  |  Required  |  Default  |  Valid Values  |  Description  
--------|:----------:|-----------|----------------|---------------
task_meta_data|False|None| |GBDX Option. Output location for task meta data such as execution log and output JSON
output_raster_uri|True|None| |Outputor OUTPUT_RASTER. -- Value Type: ENVIURI

**Output structure**

Explain output structure via example.


### Advanced
Include example(s) with complicated parameter settings and/or example(s) where
ENVI_ColorSliceClassification is used as part of a workflow involving other GBDX tasks.

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
List known past/current issues with ENVI_ColorSliceClassification (e.g., version x does not ingest vrt files).


### Background
For background on the development and implementation of ENVI_ColorSliceClassification see [here](http://www.harrisgeospatial.com/docs/ENVIColorSliceClassificationTask.html).


### Contact
List contact information for technical support.
