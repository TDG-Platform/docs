### Description
This task performs a difference analysis on a specific band in two images.

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
# Quickstart example for ENVI_ImageBandDifference:0.0.2.  

from gbdxtools import Interface
gbdx = Interface()
raster = 's3://gbd-customer-data/PathToImage/image.tif'
ENVI_ImageBandDifference:0.0.2 = gbdx.Task('ENVI_ImageBandDifference:0.0.2', raster=raster)

workflow = gbdx.Workflow([ENVI_ImageBandDifference:0.0.2])  
workflow.savedata(ENVI_ImageBandDifference:0.0.2.outputs.data, location='ENVI_ImageBandDifference:0.0.2')
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
input_raster1|True|None| |Specify a single-band raster on which to perform an image difference of input band. -- Value Type: ENVIRASTER
input_raster1_metadata|False|None| |Provide a dictionary of attributes for overriding the raster metadata. -- Value Type: DICTIONARY
input_raster1_band_grouping|False|None| |Provide the name of the band grouping to be used in the task, ie - panchromatic. -- Value Type: STRING
input_raster1_filename|False|None| |Provide the explicit relative raster filename that ENVI will open. This overrides any file lookup in the task runner. -- Value Type: STRING
input_raster2|True|None| |Specify a second single-band raster on which to perform an image difference of input band. -- Value Type: ENVIRASTER
input_raster2_metadata|False|None| |Provide a dictionary of attributes for overriding the raster metadata. -- Value Type: DICTIONARY
input_raster2_band_grouping|False|None| |Provide the name of the band grouping to be used in the task, ie - panchromatic. -- Value Type: STRING
input_raster2_filename|False|None| |Provide the explicit relative raster filename that ENVI will open. This overrides any file lookup in the task runner. -- Value Type: STRING
output_raster_uri_filename|False|None| |Specify a string with the fully-qualified path and filename for OUTPUT_RASTER. -- Value Type: STRING

### Outputs
The following table lists all taskname outputs.
Mandatory (optional) settings are listed as Required = True (Required = False).

  Name  |  Required  |  Default  |  Valid Values  |  Description  
--------|:----------:|-----------|----------------|---------------
task_meta_data|False|None| |GBDX Option. Output location for task meta data such as execution log and output JSON
output_raster_uri|True|None| |Output for OUTPUT_RASTER. -- Value Type: ENVIURI

**Output structure**

Explain output structure via example.


### Advanced
Include example(s) with complicated parameter settings and/or example(s) where
ENVI_ImageBandDifference:0.0.2 is used as part of a workflow involving other GBDX tasks.

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
List known past/current issues with ENVI_ImageBandDifference:0.0.2 (e.g., version x does not ingest vrt files).


### Background
For background on the development and implementation of ENVI_ImageBandDifference:0.0.2 see [here](Insert link here).


### Contact
List contact information for technical support.
