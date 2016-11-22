### Description
Image intersection takes two rasters as input, and it outputs two rasters that cover only the overlapping area of two inputs. If the input rasters have different projections or pixel sizes, one of the output rasters will be reprojected or resampled so that the two output rasters have the same number of samples and lines. File inputs can have standard map projections, can be pixel-based, or can have RPC information.

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
# First Initialize the Environment
from gbdxtools import Interface
gbdx = Interface()

#QB catIDs : 1010010004F8A100,101001000460B200
data1 = "s3://receiving-dgcs-tdgplatform-com/055664619010_01_003"
data2 = "s3://receiving-dgcs-tdgplatform-com/055668601010_01_003"
'''
#WV1 catIDs : 102001001BB4F500, 1020010016585600
#data1 = 's3://receiving-dgcs-tdgplatform-com/055940816010_01_003'
#data2 = 's3://receiving-dgcs-tdgplatform-com/055940817010_01_003'
#WV2 catIDs : 1030050043F8B400,104001001D66F800
data1 = "s3://receiving-dgcs-tdgplatform-com/055690224010_01_003"
data2 = "s3://receiving-dgcs-tdgplatform-com/055438828010_01_003"
#WV3 catIDs : 1040010002965B00,10400E0001DBBA00
data1 = ""
data2 = "s3://receiving-dgcs-tdgplatform-com/055436253010_01_003"
#GE catIDs : 1050410003F75A00,1050410003F7AF00
data1 = "s3://receiving-dgcs-tdgplatform-com/055917898010_01_003"
data2 = "s3://receiving-dgcs-tdgplatform-com/055917899010_01_003"
'''
#aoptask1 = gbdx.Task("AOP_Strip_Processor", data=data1, enable_acomp=True, enable_pansharpen=False, enable_dra=False, bands='MS')
#aoptask2 = gbdx.Task("AOP_Strip_Processor", data=data2, enable_acomp=True, enable_pansharpen=False, enable_dra=False, bands='MS')
#aoptask1 = gbdx.Task("AOP_Strip_Processor", data=data1, enable_acomp=True, enable_pansharpen=False, enable_dra=False, bands='PAN')
#aoptask2 = gbdx.Task("AOP_Strip_Processor", data=data2, enable_acomp=True, enable_pansharpen=False, enable_dra=False, bands='PAN')

envi_II = gbdx.Task("ENVI_ImageIntersection")
envi_II.inputs.file_types = "hdr"
envi_II.inputs.input_raster1 = data1
envi_II.inputs.input_raster2 = data2
envi_II.inputs.output_raster1_uri_filename = "Image1"
envi_II.inputs.output_raster2_uri_filename = "Image2"

workflow = gbdx.Workflow([envi_II])
'''
workflow.savedata(
    aoptask1.outputs.data,
        location='Benchmark/ENVI_ImageIntersection/AOP/QB1'
)
workflow.savedata(
    aoptask2.outputs.data,
        location='Benchmark/ENVI_ImageIntersection/AOP/QB2'
)
'''
workflow.savedata(
    envi_II.outputs.output_raster1_uri,
        location='Benchmark/ENVI_ImageIntersection/II/QS/QB1'
)
workflow.savedata(
    envi_II.outputs.output_raster2_uri,
        location='Benchmark/ENVI_ImageIntersection/II/QS/QB2'
)
workflow.execute()
status = workflow.status["state"]
wf_id = workflow.id
# print wf_id
# print status
```

### Inputs
The following table lists all taskname inputs.
Mandatory (optional) settings are listed as Required = True (Required = False).

  Name  |  Required  |  Default  |  Valid Values  |  Description  
--------|:----------:|-----------|----------------|---------------
file_types|False|None| |GBDX Option. Comma seperated list of permitted file type extensions. Use this to filter input files -- Value Type: STRING[*]
warping_method|False|None| |Specify the warping method to use. -- Value Type: STRING -- Default Value: "Triangulation"
output_raster2_uri_filename|False|None| |Outputor OUTPUT_RASTER2. -- Value Type: ENVIURI
resampling|False|None| |Specify the resampling method.  Nearest Neighbor: Uses the nearest pixel without any interpolation.  Bilinear: Performs a linear interpolation using four pixels to resample, Cubic Convolution: Uses 16 pixels to approximate the sinc function using cubic polynomials to resample the image. -- Value Type: STRING -- Default Value: "Bilinear"
input_raster1|True|None| |Specify a raster to use as the base for computing the intersection. -- Value Type: ENVIRASTER
input_raster2|True|None| |Specify a second raster for computing the intersection. -- Value Type: ENVIRASTER
output_raster1_uri_filename|False|None| |Outputor OUTPUT_RASTER1. -- Value Type: ENVIURI

### Outputs
The following table lists all taskname outputs.
Mandatory (optional) settings are listed as Required = True (Required = False).

  Name  |  Required  |  Default  |  Valid Values  |  Description  
--------|:----------:|-----------|----------------|---------------
task_meta_data|False|None| |GBDX Option. Output location for task meta data such as execution log and output JSON
output_raster2_uri|True|None| |Outputor OUTPUT_RASTER2. -- Value Type: ENVIURI
output_raster1_uri|True|None| |Outputor OUTPUT_RASTER1. -- Value Type: ENVIURI

**Output structure**

Explain output structure via example.


### Advanced
Include example(s) with complicated parameter settings and/or example(s) where the task is used as part of a workflow involving other GBDX tasks.

```python
from gbdxtools import Interface
gbdx = Interface()
#QB catIDs : 1010010004F8A100,101001000460B200
#data1 = "s3://receiving-dgcs-tdgplatform-com/055917900010_01_003"
#data2 = "s3://receiving-dgcs-tdgplatform-com/055917901010_01_003"
'''
#WV1 catIDs : 102001001BB4F500, 1020010016585600
#data1 = 's3://receiving-dgcs-tdgplatform-com/055940816010_01_003'
#data2 = 's3://receiving-dgcs-tdgplatform-com/055940817010_01_003'
#WV2 catIDs : 1030050043F8B400,104001001D66F800
data1 = "s3://receiving-dgcs-tdgplatform-com/055690224010_01_003"
data2 = "s3://receiving-dgcs-tdgplatform-com/055438828010_01_003"
'''
#WV3 catIDs : 1040010002965B00,10400E0001DBBA00
data1 = "s3://receiving-dgcs-tdgplatform-com/055940818010_01_003"
data2 = "s3://receiving-dgcs-tdgplatform-com/055436253010_01_003"
'''
#GE catIDs : 1050410003F75A00,1050410003F7AF00
data1 = "s3://receiving-dgcs-tdgplatform-com/055917898010_01_003"
data2 = "s3://receiving-dgcs-tdgplatform-com/055917899010_01_003"
'''
aoptask1 = gbdx.Task("AOP_Strip_Processor", data=data1, enable_acomp=True, enable_pansharpen=False, enable_dra=False, bands='MS')
aoptask2 = gbdx.Task("AOP_Strip_Processor", data=data2, enable_acomp=True, enable_pansharpen=False, enable_dra=False, bands='MS')
#aoptask1 = gbdx.Task("AOP_Strip_Processor", data=data1, enable_acomp=True, enable_pansharpen=False, enable_dra=False, bands='PAN')
#aoptask2 = gbdx.Task("AOP_Strip_Processor", data=data2, enable_acomp=True, enable_pansharpen=False, enable_dra=False, bands='PAN')

envi_II = gbdx.Task("ENVI_ImageIntersection")
envi_II.inputs.file_types = "hdr"
envi_II.inputs.input_raster1 = aoptask1.outputs.data.value
envi_II.inputs.input_raster2 = aoptask2.outputs.data.value
envi_II.inputs.output_raster1_uri_filename = "Image1"
envi_II.inputs.output_raster2_uri_filename = "Image2"
'''
envi_ndvi1 = gbdx.Task("ENVI_SpectralIndex")
envi_ndvi1.inputs.input_raster = envi_II.outputs.output_raster1_uri.value
envi_ndvi1.inputs.file_types = "hdr"
envi_ndvi1.inputs.index = "Normalized Difference Vegetation Index"
envi_ndvi2 = gbdx.Task("ENVI_SpectralIndex")
envi_ndvi2.inputs.input_raster = envi_II.outputs.output_raster2_uri.value
envi_ndvi2.inputs.file_types = "hdr"
envi_ndvi2.inputs.index = "Normalized Difference Vegetation Index"
'''
workflow = gbdx.Workflow([aoptask1, aoptask2, envi_II])
workflow.savedata(
    aoptask1.outputs.data,
        location='Benchmark/ENVI_ImageIntersection/AOP/WV31'
)
workflow.savedata(
    aoptask2.outputs.data,
        location='Benchmark/ENVI_ImageIntersection/AOP/WV32'
)
workflow.savedata(
    envi_II.outputs.output_raster1_uri,
        location='Benchmark/ENVI_ImageIntersection/II/WV31'
)
workflow.savedata(
    envi_II.outputs.output_raster2_uri,
        location='Benchmark/ENVI_ImageIntersection/II/WV32'
)
workflow.execute()
status = workflow.status["state"]
wf_id = workflow.id
```

### Issues
List known past/current issues with ENVI_ImageIntersection (e.g., version x does not ingest vrt files).


### Background
For background on the development and implementation of ENVI_ImageIntersection see [here](Insert link here).


### Contact
List contact information for technical support.
