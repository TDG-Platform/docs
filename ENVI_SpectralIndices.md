# ENVI_SpectralIndices

### Description
This task creates a spectral index raster with one or more bands, where each band represents a different spectral index. Spectral indices are combinations of surface reflectance at two or more wavelengths that indicate relative abundance of features of interest.

This task can be run with Python using [gbdxtools](https://github.com/DigitalGlobe/gbdxtools) or through the [GBDX Web Application](https://gbdx.geobigdata.io/materials/)

### Table of Contents

- [Quickstart](#quickstart) - Get started!
- [Inputs](#inputs) - Required and optional task inputs.
- [Outputs](#outputs) - Task outputs and example contents.
- [Runtime](#runtime) - Example estimate of task runtime.
- [Advanced](#advanced) - Additional information for advanced users.
- [Contact Us](#contact-us) - Contact tech or document owner.

### Quickstart
Example Script: Run in a python environment (i.e. - IPython) using the gbdxtools interface.

```python
from gbdxtools import Interface
gbdx = Interface()

# Edit the following path to reflect a specific path to an image
image = 's3://gbd-customer-data/CustomerAccount#/PathToImage/'

envi = gbdx.Task("ENVI_SpectralIndices")
envi.inputs.input_raster = image
envi.inputs.index = '["Normalized Difference Vegetation Index", "WorldView Soil Index"]'

workflow = gbdx.Workflow([envi])

workflow.savedata(
   envi.outputs.output_raster_uri,
   location='ENVI_SIS/output_raster_uri' # edit location to suit account
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

### 

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
| QB          |  41,551,668   | 312.07          | 184.23     | 0.59         |
| WV01        | 1,028,100,320 | 351.72          | NA         | NA           |
| WV02        |  35,872,942   | 329.87          | 215.81     | 0.65         |
| WV03        |  35,371,971   | 196.27          | 247.30     | 1.26         |
| GE          |  57,498,000   | 332.97          | 216.80     | 0.65         |

### 


### Advanced
For advanced parameters and a full list of indices compatible with this task refer to the following link:
http://www.harrisgeospatial.com/docs/alphabeticallistspectralindices.html

Example of workflow with Spectral Indices including preprocessing steps in gbdxtools

```python
from gbdxtools import Interface
gbdx = Interface()

# Edit the following path to reflect a specific path to an image
data = 's3://gbd-customer-data/CustomerAccount#/PathToImage/'

aoptask = gbdx.Task("AOP_Strip_Processor") 
aoptask.inputs.data = data
aoptask.inputs.enable_dra = False
aoptask.inputs.bands = 'MS'

envi = gbdx.Task("ENVI_SpectralIndices")
envi.inputs.input_raster = aop2task.outputs.data.value
envi.inputs.index = '["Normalized Difference Vegetation Index", "WorldView Built-Up Index", "WorldView Non-Homogeneous Feature Difference", "WorldView Water Index", "WorldView Soil Index"]'

workflow = gbdx.Workflow([aoptask, envi])

workflow.savedata(
   envi.outputs.output_raster_uri,
   location='AOP_ENVI_SIS/output_raster_uri'
)

print workflow.execute()
print workflow.status
# Repeat workflow.status as needed to monitor progress.
```


### Issues
Currently the advanced task in the Web App 2.0 will process an image with Normalized Difference Vegetation Index, WorldView Built-Up Index, WorldView Non-Homogeneous Feature Difference, WorldView Water Index, WorldView Soil Index (Aug 8th, 2016). However, custom workflows with gbdxtools may include any of the indices compatible with the task (see link in Advanced section)

### Background

For background on the development and implementation of Spectral Index refer to the [ENVI Documentation](https://www.harrisgeospatial.com/docs/spectralindices.html)


### Contact
Document Owner - Carl Reeder - creeder@digitalglobe.com
