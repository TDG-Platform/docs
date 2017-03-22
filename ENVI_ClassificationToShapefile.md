# ENVI_ClassificationToShapefile

### Description
The task exports one or more classes to a single shapefile. The vectors include separate records for each polygon.

This task can be run with Python using [gbdxtools](https://github.com/DigitalGlobe/gbdxtools) or through the [GBDX Web Application](https://gbdx.geobigdata.io/materials/)

### Table of Contents
 * [Quickstart](#quickstart) - Get started
 * [Inputs](#inputs) - Required and optional task inputs.
 * [Outputs](#outputs) - Task outputs and output structure.
 * [Runtime](#runtime) - Results of task benchmark tests.
 * [Advanced](#advanced) - Additional information for advanced users.
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

#Edit the following path to reflect a specific path to an image
isodata.inputs.input_raster = 's3://gbd-customer-data/CustomerAccount#/PathToImage/'

shp = gbdx.Task("ENVI_ClassificationToShapefile")
shp.inputs.input_raster = isodata.outputs.output_raster_uri.value

workflow = gbdx.Workflow([isodata, shp])

#Edit the following line(s) to reflect specific folder(s) for the output file (example location provided)
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
input_raster|True|None| ENVI raster dataset|Specify a classification raster from which to generate a shapefile. -- Value Type: ENVIRASTER
export_class_clrs|False|None|see Description |Set this property to export CLASS_CLRS (class colors) as a shapefile attribute for each polygon. The options are true (default) or false. -- Value Type: BOOL
export_classes|False|None| Must be identical to the classification .hdr file class names|Specify a string array with class names to export to the shapefile. -- Value Type: STRING To edit names of the classes you may manually edit the names in the .hdr output, or use a software package to edit the attribute names.
export_area|False|None| see Description|Set this property to export AREA as a shapefile attribute for each polygon. The options are true (default) or false. -- Value Type: BOOL
output_vector_uri_filename|False|None| string name e.g. "classificationShape"|OUTPUT_VECTOR. -- Value Type: ENVIURI
ignore_validate      |    False   |   N/A     |     1        |Set this property to a value of 1 to run the task, even if validation of properties fails. This is an advanced option for users who want to first set all task properties before validating whether they meet the required criteria. This property is not set by default, which means that an exception will occur if any property does not meet the required criteria for successful execution of the task.

### Outputs
The following table lists all taskname outputs.
Mandatory (optional) settings are listed as Required = True (Required = False).

  Name  |  Required  |  Default  |  Valid Values  |  Description  
--------|:----------:|-----------|----------------|---------------
task_meta_data|False|None|s3 location for metadata output |GBDX Option. Output location for task meta data such as execution log and output JSON
output_vector_uri|True|None| s3 location for data output |Outputor OUTPUT_VECTOR. -- Value Type: ENVIURI

**Output structure**

The output of this task is a shapefile (.shp) and the supporting file structure for a GIS program such as ArcGIS. The vectors include separate records for each polygon for each class.

### Runtime

The following table lists runtime outputs for applicable sensors.
For details on the methods of testing the runtimes of the task visit the following link:(INSERT link to GBDX U page here)

  Sensor Name  |  Total Pixels  |  Total Area (k2)  |  Time(secs)  |  Time/Area k2
--------|:----------:|-----------|----------------|---------------
QB | 41,551,668 | 312.07 | 1,337.20 | 4.28 |
WV02|35,872,942|329.87| 1,806.83 | 5.48|
WV03|35,371,971|196.27| 18,209.79|92.78|
GE| 57,498,000|332.97|3,012.48| 9.05|



### Advanced
Include example(s) with complicated parameter settings and/or example(s) where the task is used as part of a workflow involving other GBDX tasks.

```python

# Quickstart **Example Script Run in Python using the gbdxTools InterfaceExample producing a single band vegetation mask from a tif file.
# First Initialize the Environment
from gbdxtools import Interface
gbdx = Interface()

#Edit the following path to reflect a specific path to an image
QB = 's3://gbd-customer-data/CustomerAccount#/PathToImage/'

aop = gbdx.Task('AOP_Strip_Processor', data=data, bands='MS', enable_acomp=True, enable_pansharpen=False, enable_dra=False)

isodata = gbdx.Task("ENVI_ISODATAClassification")
isodata.inputs.input_raster = aop.outputs.data.value

shp = gbdx.Task("ENVI_ClassificationToShapefile")
shp.inputs.input_raster = isodata.outputs.output_raster_uri.value
shp.inputs.output_vector_uri_filename = "ShapefileName"

workflow = gbdx.Workflow([aop, isodata, shp])

#Edit the following line(s) to reflect specific folder(s) for the output file (example location provided)
workflow.savedata(
  shp.outputs.output_vector_uri,
    location="PathToSHP"
)
workflow.execute()

# print wf_id
# print status
```


### Issues
None

### Background
For background on the development and implementation of this task see [here](http://www.harrisgeospatial.com/docs/ENVIClassificationToShapefileTask.html).


### Contact
Document Owner - Carl Reeder - creeder@digitalglobe.com
