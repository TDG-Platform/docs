# ENVI_ClassificationToShapefile

### Description
The task exports one or more classes to a single shapefile. The vectors include separate records for each polygon.

This task can be run with Python using [gbdxtools](https://github.com/DigitalGlobe/gbdxtools) or through the [GBDX Web Application](https://gbdx.geobigdata.io/materials/)

### Table of Contents
 * [Quickstart](#quickstart) - Get started!
 * [Inputs](#inputs) - Required and optional task inputs.
 * [Outputs](#outputs) - Task outputs and output structure.
 * [Advanced](#advanced) - Additional information for advanced users.
 * [Runtime](#runtime) - Results of task benchmark tests.
 * [Issues](#issues) - Current or past known issues.
 * [Background](#background) - Background information.
 * [Contact](#contact) - Contact information.

### Quickstart
Quick start example.

```python

# Quickstart **Example Script Run in Python using the gbdxTools InterfaceExample producing a single band vegetation mask from a tif file.
# First Initialize the Environment
from gbdxtools import Interface
gbdx = Interface()

isodata = gbdx.Task("ENVI_ISODATAClassification")
isodata.inputs.input_raster = "s3://gbd-customer-data/7d8cfdb6-13ee-4a2a-bf7e-0aff4795d927/Benchmark/WV2/054876618060_01/"
isodata.inputs.file_types = "tif"

shp = gbdx.Task("ENVI_ClassificationToShapefile")
shp.inputs.input_raster = isodata.outputs.output_raster_uri.value
shp.inputs.file_types = "hdr"

workflow = gbdx.Workflow([isodata, shp])

workflow.savedata(
  isodata.outputs.output_raster_uri,
    location="Benchmark/classification/isodata"
    )

workflow.savedata(
  shp.outputs.output_vector_uri,
    location="Benchmark/classification/shp"
)
# print wf_id
# print status
```

### Inputs
The following table lists all taskname inputs.
Mandatory (optional) settings are listed as Required = True (Required = False).

  Name  |  Required  |  Default  |  Valid Values  |  Description  
--------|:----------:|-----------|----------------|---------------
file_types|False|None| .hdr, .tif |GBDX Option. Comma seperated list of permitted file type extensions. Use this to filter input files -- Value Type: STRING
input_raster|True|None| ENVI raster dataset|Specify a classification raster from which to generate a shapefile. -- Value Type: ENVIRASTER
export_class_clrs|False|None|see Description |Set this property to export CLASS_CLRS (class colors) as a shapefile attribute for each polygon. The options are true (default) or false. -- Value Type: BOOL
export_classes|False|None| Must be identical to the classification .hdr file class names|Specify a string array with class names to export to the shapefile. -- Value Type: STRING To edit names of the classes you may manually edit the names in the .hdr output, or use a software package to edit the attribute names.
export_area|False|None| see Description|Set this property to export AREA as a shapefile attribute for each polygon. The options are true (default) or false. -- Value Type: BOOL
output_vector_uri_filename|False|None| string name e.g. "classificationShape"|OUTPUT_VECTOR. -- Value Type: ENVIURI

### Outputs
The following table lists all taskname outputs.
Mandatory (optional) settings are listed as Required = True (Required = False).

  Name  |  Required  |  Default  |  Valid Values  |  Description  
--------|:----------:|-----------|----------------|---------------
task_meta_data|False|None|s3 location for metadata output |GBDX Option. Output location for task meta data such as execution log and output JSON
output_vector_uri|True|None| s3 location for data output |Outputor OUTPUT_VECTOR. -- Value Type: ENVIURI

**Output structure**

The output of this task is a shapefile (.shp) and the supporting file structure for a GIS program such as ArcGIS. The vectors include separate records for each polygon for each class.

### Advanced
Include example(s) with complicated parameter settings and/or example(s) where the task is used as part of a workflow involving other GBDX tasks.

```python

# Quickstart **Example Script Run in Python using the gbdxTools InterfaceExample producing a single band vegetation mask from a tif file.
# First Initialize the Environment
from gbdxtools import Interface
gbdx = Interface()

QB = "s3://receiving-dgcs-tdgplatform-com/PathToImage"

aop = gbdx.Task('AOP_Strip_Processor', data=data, bands='MS', enable_acomp=True, enable_pansharpen=False, enable_dra=False)

isodata = gbdx.Task("ENVI_ISODATAClassification")
isodata.inputs.input_raster = aop.outputs.data.value
isodata.inputs.file_types = "tif"

shp = gbdx.Task("ENVI_ClassificationToShapefile")
shp.inputs.input_raster = isodata.outputs.output_raster_uri.value
shp.inputs.file_types = "hdr"
shp.inputs.output_vector_uri_filename = "ShapefileName"

workflow = gbdx.Workflow([aop, isodata, shp])


workflow.savedata(
  shp.outputs.output_vector_uri,
    location="PathToSHP"
)
workflow.execute()

# print wf_id
# print status
```

### Runtime

The following table lists runtime outputs for applicable sensors.
For details on the methods of testing the runtimes of the task visit the following link:(INSERT link to GBDX U page here)

  Sensor Name  |  Total Pixels  |  Total Area (k2)  |  Time(secs)  |  Time/Area k2
--------|:----------:|-----------|----------------|---------------
QB | 41,551,668 | 312.07 | 1,337.20 | 4.28 |
WV02|35,872,942|329.87| 1,806.83 | 5.48|
WV03|35,371,971|196.27| 18,209.79|92.78|
GE| 57,498,000|332.97|3,012.48| 9.05|


### Issues
NA


### Background
For background on the development and implementation of this task see [here](http://www.harrisgeospatial.com/docs/ENVIClassificationToShapefileTask.html).


### Contact
Document Owner - Carl Reeder - creeder@digitalglobe.com