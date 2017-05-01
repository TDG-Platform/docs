# ENVI NNDiffuse PanSharpening

This task performs Nearest Neighbor Diffuse (NND) Pansharpening using a low-resolution raster and a high-resolution panchromatic raster.  For details regarding the operation of ENVI Tasks on the Platform refer to [ENVI Task Runner](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md) documentation.

NND Pansharpening works best when the spectral response function of each multispectral band has minimal overlap with one another, and the combination of all multispectral bands covers the spectral range of the panchromatic raster.
The following are input raster requirements for running the NND Pansharpening algorithm:

- The pixel size of the low-resolution raster must be an integral multiple of the pixel size of the high-resolution raster. If it is not, then pre-process (resample) the rasters.
- When the rasters have projection information, it must be in the same
   projection. If it is not the same, then reproject the rasters.
- The rasters must be aligned. If the rasters have misalignment, then
   register the rasters.
- Ensure that the rasters line up, particularly in the upper-left
   corner (see the following diagram). When alignment is as little as
   1/2 pixel off between the two, pan sharpening accuracy will be
   affected. If both input rasters have map information, they will be
   automatically subsetted so that they line up. If the rasters do not
   line up and do not have map information, then use spatial subsetting.



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
data_low_res = 's3://gbd-customer-data/CustomerAccount#/PathToImage/'
data_high_res = 's3://gbd-customer-data/CustomerAccount#/PathToImage/'

envi = gbdx.Task("ENVI_NNDiffusePanSharpening")
envi.inputs.input_low_resolution_raster = data_low_res
envi.inputs.input_high_resolution_raster = data_high_res

workflow = gbdx.Workflow([ envi ])

workflow.savedata(
    envi.outputs.output_raster_uri,
    location='NNDPanSharp/output_raster_uri'
)

print workflow.execute()
print workflow.status
# Repeat workflow.status as needed to monitor progress.
```


### Inputs

The following table lists all inputs for this task. For details regarding the use of all ENVI input types refer to the [ENVI Task Runner Inputs]([See ENVIRASTER input type](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md)) documentation.

| Name                                     | Required |                 Default                  |               Valid Values               | Description                              |
| ---------------------------------------- | :------: | :--------------------------------------: | :--------------------------------------: | ---------------------------------------- |
| file_types                               |  False   |                   None                   |                  string                  | GBDX Option. Comma separated list of permitted file type extensions. Use this to filter input files -- Value Type: STRING |
| input_low_resolution_raster              |   True   |                   N/A                    |  A valid S3 URL containing image files.  | Specify a low-resolution raster.         |
| input_low_resolution_raster_format       |  False   |                   None                   | [See ENVIRASTER input type](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md) | Provide the format of the image, for example: landsat-8. -- Value Type: STRING |
| input_low_resolution_raster_band_grouping |  False   |                   None                   | [See ENVIRASTER input type](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md) | Provide the name of the band grouping to be used in the task, ie - panchromatic. -- Value Type: STRING |
| input_low_resolution_raster_filename     |  False   |                   None                   | [See ENVIRASTER input type](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md) | Provide the explicit relative raster filename that ENVI will open. This overrides any file lookup in the task runner. -- Value Type: STRING |
| input_high_resolution_raster             |   True   |                   N/A                    |  A valid S3 URL containing image files.  | Specify a high-resolution panchromatic raster. |
| input_high_resolution_raster_format      |  False   |                   None                   | [See ENVIRASTER input type](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md) | Provide the format of the image, for example: landsat-8. -- Value Type: STRING |
| input_high_resolution_raster_band_grouping |  False   |                   None                   | [See ENVIRASTER input type](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md) | Provide the name of the band grouping to be used in the task, ie - panchromatic. -- Value Type: STRING |
| input_high_resolution_raster_filename    |  False   |                   None                   | [See ENVIRASTER input type](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md) | Provide the explicit relative raster filename that ENVI will open. This overrides any file lookup in the task runner. -- Value Type: STRING |
| intensity_smoothness                     |  False   | value is set adaptively using local similarity |      string float (positive number)      | A positive number that defines the intensity smoothness factor (σ) of the NNDiffuse pan sharpening algorithm. A smaller intensity_smoothness value will restrict diffusion and produce sharper images, but will have more noise.  A larger value is also suggested for panchromatic scenes with high contrast (they require less diffusion sensitivity), and with complex scenes (to reduce the possibility of noise). If not specified, the value is set adaptively using local similarity. -- Value Type: FLOAT |
| spatial_smoothness                       |  False   |         pixel_size_ratio x 0.62          |      string float (positive number)      | A positive number that defines the spatial smoothness factor (σs) of the NNDiffuse pan sharpening algorithm. spatial_smoothness should be set to a value that will resemble a bicubic interpolation kernel. -- Value Type: FLOAT |
| pixel_size_ratio                         |  False   | resolution ratio of the sensor in meters (low-res/high-res) |                string int                | A scalar number that defines the pixel size ratio of the low-resolution raster and the high-resolution raster. The NNDiffuse pan-sharpening algorithm requires that the pixel size ratio be an integer. If this property is not set, the value is determined from the metadata of the input rasters. -- Value Type: UINT |
| output_raster_uri_filename               |  False   |                   None                   |                  string                  | Specify a string with the fully-qualified path and filename for OUTPUT_RASTER. -- Value Type: STRING |



### Outputs

The following table lists all the tasks outputs.

| Name              | Required | Description                              |
| ----------------- | :------: | ---------------------------------------- |
| output_raster_uri |   True   | Output for OUTPUT_RASTER.                |
| task_meta_data    |  False   | GBDX Option. Output location for task meta data such as execution log and output JSON. |

##### Output Structure

The output_raster image file will be written to the specified S3 Customer Account Location in GeoTiff (\*.tif) format, with an ENVI header file (\*.hdr).




### Runtime

The following table lists all applicable runtime outputs. (This section will be completed the Algorithm Curation team). For details on the methods of testing the runtimes of the task visit the following link:(INSERT link to GBDX U page here).

| Sensor Name | Total Pixels | Total Area (k2) | Time(secs) | Time/Area k2 |
| ----------- | :----------: | --------------- | ---------- | ------------ |
| QB          |  41,551,668  | 312.07          | 1242.554   | 3.98         |
| WV02        |  35,872,942  | 329.87          | 4555.128   | 13.81        |
| WV03        |  35,371,971  | 196.27          | 6741.883   | 34.35        |
| GE01        |  57,498,000  | 332.97          | 2286.475   | 6.87         |
| IKONOS      |  29,976,302  | 273.34          | 367.958    | 1.35         |



### Advanced

This task requires that WorldView-2, Worldview-3, GeoEYE-1 and Quickbird imagery has been pre-processed using the [Advanced Image Preprocessor](#https://github.com/TDG-Platform/docs/blob/master/Advanced_Image_Preprocessor.md) for proper orthorectification of both the panchromatic and multispectral images. Use NNDiffuse Pansharpening on imagery from these sensors when you need full multipsectral band (4-band or 8-band) pansharpening.


```python
from gbdxtools import Interface
gbdx = Interface()

# Edit the following path to reflect a specific path to an image
data = 's3://gbd-customer-data/CustomerAccount#/PathToImage/'

aop_low = gbdx.Task("AOP_Strip_Processor") 
aop_low.inputs.data = data
aop_low.inputs.enable_dra = False
aop_low.inputs.bands = 'MS'

aop_high = gbdx.Task("AOP_Strip_Processor") 
aop_high.inputs.data = data
aop_high.inputs.enable_dra = False
aop_high.inputs.bands = 'PAN'

envi = gbdx.Task("ENVI_NNDiffusePanSharpening")
envi.inputs.input_low_resolution_raster = aop_low.outputs.data.value
envi.inputs.input_high_resolution_raster = aop_high.outputs.data.value

workflow = gbdx.Workflow([ envi ])

workflow.savedata(
    envi.outputs.output_raster_uri, 
    location='NNDPanSharp/output_raster_uri' # edit location to suit account
)

print workflow.execute()
print workflow.status
# Repeat workflow.status as needed to monitor progress.
```



### Background

For background on the development and implementation of NND PanSharpening refer to the [ENVI Documentation](https://www.harrisgeospatial.com/docs/classificationtutorial.html)

Additional References:
Sun, W., B. Chen, and D.W. Messinger. "Nearest Neighbor Diffusion Based Pan Sharpening Algorithm for Spectral Images." Optical Engineering 53, no. 1 (2014).



### Contact Us

Document Owner - [Kathleen Johnson](#kajohnso@digitalglobe.com)
