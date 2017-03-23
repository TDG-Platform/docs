# ENVI_SpectralIndex

ENVI_SpectralIndex. This task creates a spectral index raster from one pre-defined spectral index. Spectral indices are combinations of surface reflectance at two or more wavelengths that indicate relative abundance of features of interest. This task is used to compute a single index on a combination of multi spectral bands within an image. This task can be used to compute indices such as the Normalized Difference Vegetation Index (NDVI). An index such as NDVI will be passed into the task and a single band raster with the results of the index will be returned as output.

### Table of Contents
* [Quickstart](#quickstart) - Get started!
* [Inputs](#inputs) - Required and optional task inputs.
* [Outputs](#outputs) - Task outputs and example contents.
* [Runtime](#runtime) - Example estimate of task runtime.
* [Advanced](#advanced) - Additional information for advanced users.
* [Contact Us](#contact-us) - Contact tech or document owner.

### Quickstart

Example Script: Run in a python environment (i.e. - IPython) using the gbdxtools interface.

```python
from gbdxtools import Interface
gbdx = Interface()

# Edit the following path to reflect a specific path to an image
image = 's3://gbd-customer-data/CustomerAccount#/PathToImage/'

envi_ndvi = gbdx.Task("ENVI_SpectralIndex")
envi_ndvi.inputs.input_raster = image
envi_ndvi.inputs.index = "Normalized Difference Vegetation Index"

workflow = gbdx.Workflow([envi_ndvi])

workflow.savedata(
   envi_ndvi.outputs.output_raster_uri,
      location='NDVI/output_raster_uri' # edit location to suit account
)

print workflow.execute()
print workflow.status
# Repeat workflow.status as needed to monitor progress.
```

### Inputs
The following table lists all inputs for this task. For details regarding the use of all ENVI input types refer to the [ENVI Task Runner Inputs]([See ENVIRASTER input type](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md)) documentation.

| Name                       | Required | Default | Valid Values                             | Description                              |
| -------------------------- | :------: | :-----: | ---------------------------------------- | ---------------------------------------- |
| file_types                 |  False   |  None   | string                                   | GBDX Option. Comma separated list of permitted file type extensions. Use this to filter input files -- Value Type: STRING |
| input_raster               |   True   |  None   | A valid S3 URL containing image files.   | Specify a raster from which to run the task. -- Value Type: ENVIRASTER |
| input_raster_format        |  False   |  None   | [See ENVIRASTER input type](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md) | Provide the format of the image, for example: landsat-8. -- Value Type: STRING |
| input_raster_band_grouping |  False   |  None   | [See ENVIRASTER input type](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md) | Provide the name of the band grouping to be used in the task, ie - panchromatic. -- Value Type: STRING |
| input_raster_filename      |  False   |  None   | [See ENVIRASTER input type](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md) | Provide the explicit relative raster filename that ENVI will open. This overrides any file lookup in the task runner. -- Value Type: STRING |
| index                      |   True   |  None   | string                                   | Specify a string, or array of strings, representing the pre-defined spectral indices to apply to the input raster. -- Value Type: STRING |
| output_raster_uri_filename |  False   |  None   | string                                   | Specify a string with the fully-qualified path and filename for OUTPUT_RASTER. -- Value Type: STRING |

### Outputs

The following table lists the Spectral Index task outputs.

| Name              | Required | Description                              |
| ----------------- | :------: | ---------------------------------------- |
| output_raster_uri |   True   | Output for OUTPUT_RASTER.                |
| task_meta_data    |  False   | GBDX Option. Output location for task meta data such as execution log and output JSON. |

##### Output Structure

The index image file will be written to the specified S3 Customer Account Location in GeoTiff (\*.tif) format, with an ENVI header file (\*.hdr).



### Runtime

The following table lists all applicable runtime outputs. (This section will be completed the Algorithm Curation team). For details on the methods of testing the runtimes of the task visit the following link:(INSERT link to GBDX U page here)

| Sensor Name | Total Pixels  | Total Area (k2) | Time(secs) | Time/Area k2 |
| ----------- | :-----------: | --------------- | ---------- | ------------ |
| QB          |  41,551,668   | 312.07          | 194.58     | 0.62         |
| WV01        | 1,028,100,320 | NA              | NA         |              |
| WV02        |  35,872,942   | 1,265.14        | 216.12     | 0.66         |
| WV03        |  35,371,971   | 196.27          | 1,265.14   | 6.45         |
| GE          |  57,498,000   | 332.97          | 185.33     | 0.56         |

### 

### Advanced

To link the workflow of 1 input image into AOP_Strip_Processor and the Spectral Index task, use the following GBDX tools script in python.

```python
from gbdxtools import Interface
gbdx = Interface()

# Edit the following path to reflect a specific path to an image
data = 's3://gbd-customer-data/CustomerAccount#/PathToImage/'

aoptask = gbdx.Task("AOP_Strip_Processor") 
aoptask.inputs.data = data
aoptask.inputs.enable_dra = False
aoptask.inputs.bands = 'MS'

envi_ndvi = gbdx.Task("ENVI_SpectralIndex")
envi_ndvi.inputs.input_raster = aoptask.outputs.data.value
envi_ndvi.inputs.index = "Normalized Difference Vegetation Index"
envi_ndvi.inputs.input_raster_format = 'ikonos'

workflow = gbdx.Workflow([aoptask, envi_ndvi])

workflow.savedata(
  envi_ndvi.outputs.output_raster_uri,
  location='AOP_NDVI/output_raster_uri' # edit location to suit account
)

print workflow.execute()
print workflow.status
# Repeat workflow.status as needed to monitor progress.
```


###Known Issues

For background on the development and implementation of Spectral Index refer to the [ENVI Documentation](https://www.harrisgeospatial.com/docs/spectralindices.html), or ENVI's documentation for this task [here](https://www.harrisgeospatial.com/docs/ENVISpectralIndexTask.html).

###Contact Us
Document Owner - Carl Reeder - creeder@digitalglobe.com
