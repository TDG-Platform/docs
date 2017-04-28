# ENVI RPC Orthorectification
This task orthorectifies an image georeferenced with RPCs using a DEM and optional GCPs. For more information on RPCOrthorectification see [Background on RPC Orthorectification](http://www.harrisgeospatial.com/docs/rpcbackground.html)

This task can be run with Python using [gbdxtools](https://github.com/DigitalGlobe/gbdxtools) or through the [GBDX Web Application](https://gbdx.geobigdata.io/materials/)

### Table of Contents

- [Quickstart](#quickstart) - Get started!
- [Inputs](#inputs) - Required and optional task inputs.
- [Outputs](#outputs) - Task outputs and example contents.
- [Runtime](#runtime) - Example estimate of task runtime.
- [Advanced](#advanced) - Additional information for advanced users.
- [Known Issues](#known-issues) - Recommended Orthorectification Options for WorldView Imagery
- [Contact Us](#contact-us) - Contact tech or document owner.

### Quickstart
Example Script: Run in a python environment (i.e. - IPython) using the gbdxtools interface.

```python
from gbdxtools import Interface
gbdx = Interface()

# Edit the following path to reflect a specific path to an image
data = 's3://gbd-customer-data/CustomerAccount#/PathToImage/'

# Note: The dem_raster port is optional, and if it is not included, the task runner will use the GMTED2010.jp2 as the default.
envi_RPCO = gbdx.Task("ENVI_RPCOrthorectification")
envi_RPCO.inputs.input_raster = data
envi_RPCO.inputs.input_raster_band_grouping = 'multispectral'

workflow = gbdx.Workflow([envi_RPCO])

workflow.savedata(
    envi_RPCO.outputs.output_raster_uri,
    location='ENVI_RPCO/output_raster_uri' # edit location to suit account
)

print workflow.execute()
print workflow.status
# Repeat workflow.status as needed to monitor progress.
```

### Inputs
The following table lists all inputs for this task. For details regarding the use of all ENVI input types refer to the [ENVI Task Runner Inputs](https://gbdxdocs.digitalglobe.com/docs/envi-task-runner-inputs) documentation.

| Name                          | Required |  Default   |               Valid Values               | Description                              |
| ----------------------------- | :------: | :--------: | :--------------------------------------: | ---------------------------------------- |
| file_types                    |  False   |    None    |                  string                  | GBDX Option. Comma separated list of permitted file type extensions. Use this to filter input files -- Value Type: STRING |
| input_raster                  |   True   |    None    |  A valid S3 URL containing image files.  | Specify a raster from which to run the task. -- Value Type: ENVIRASTER |
| input_raster_format           |  False   |    None    | [See ENVIRASTER input type](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md) | Provide the format of the image, for example: landsat-8. -- Value Type: STRING |
| input_raster_band_grouping    |  False   |    None    | [See ENVIRASTER input type](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md) | Provide the name of the band grouping to be used in the task, ie - panchromatic. -- Value Type: STRING |
| input_raster_filename         |  False   |    None    | [See ENVIRASTER input type](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md) | Provide the explicit relative raster filename that ENVI will open. This overrides any file lookup in the task runner. -- Value Type: STRING |
| dem_is_height_above_ellipsoid |  False   |    None    |                True/False                | Set this property to true if the DEM is already expressed as the height above the ellipsoid and no geoid offset is required. -- Value Type: BOOL |
| output_subset                 |  False   |    None    |             string int array             | Use this property to define a spatial subset from the input image that will apply to the output from ENVIRPCOrthorectificationTask. The output will be a rectangular subset that encompasses the the extent of the input subset. If you set this property, the output extent will be larger than that of the input subset, but the output may contain background pixels. Also, you do not need to specify the ENVIGCPSet::ApplyOffset method to adjust the position of ground control points (GCPs). Set this property to a four-element array expressing the spatial range (in pixels) of the input image. The array is of the form [x1, y1, x2, y2]. Pixel coordinates are zero-based. -- Value Type: INT[4] |
| input_gcp                     |  False   |    None    | [See ENVIGCPSET input type](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md) | A set of ground control points (GCPs). -- Value Type: ENVIGCPSET |
| grid_spacing                  |  False   |    None    |                string int                | Grid spacing to use. -- Value Type: INT -- Default Value: 10 |
| dem_raster                    |  False   |    None    |   A valid S3 URL containing DEM files.   | Specify a digital elevation model (DEM) raster. It must have valid map information and the same spatial extent as INPUT_RASTER. Without elevation information from a DEM, RPCs only give an approximate geographic location.  -- Value Type: ENVIRASTER |
| dem_raster_filename           |  False   |    None    | [See ENVIRASTER input type](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md) | Provide the explicit relative raster filename that ENVI will open. This overrides any file lookup in the task runner. -- Value Type: STRING |
| geoid_offset                  |  False   |    None    |              string double               | Set this property to a floating-point value (in meters) of a geoid offset if the DEM is referenced to mean sea level. -- Value Type: DOUBLE |
| resampling                    |  False   | 'Bilinear' | 'Bilinear', 'Nearest Neighbor', 'Cubic Convolution', | Specify the resampling method.  Nearest Neighbor: Uses the nearest pixel without any interpolation.  Bilinear: Performs a linear interpolation using four pixels to resample, Cubic Convolution: Uses 16 pixels to approximate the sinc function using cubic polynomials to resample the image. -- Value Type: STRING |
| output_pixel_size             |  False   |    None    |           string double array            | Set this property to a two-element array indicating the output X and Y pixel size, in meters. The default value is the pixel size of the input image. -- Value Type: DOUBLE[2] |
| output_raster_uri_filename    |  False   |    None    |        s3 location with the name         | Specify a string with the fully-qualified path and filename for OUTPUT_RASTER. -- Value Type: STRING |

### Outputs
The following table lists all the tasks outputs.

| Name              | Required | Description                              |
| ----------------- | :------: | ---------------------------------------- |
| output_raster_uri |   True   | Output for OUTPUT_RASTER.                |
| task_meta_data    |  False   | GBDX Option. Output location for task meta data such as execution log and output JSON. |



##### Output Structure

The output_raster image file will be written to the specified S3 Customer Account Location in GeoTiff (\*.tif) format, with an ENVI header file (\*.hdr).



### Runtime

To Come...




### Advanced
Include example(s) with complicated parameter settings and/or example(s) where the task is used as part of a workflow involving other GBDX tasks.

```python
from gbdxtools import Interface
gbdx = Interface()

# Edit the following path to reflect a specific path to an image
data = 's3://gbd-customer-data/CustomerAccount#/PathToImage/'

aoptask = gbdx.Task("AOP_Strip_Processor") 
aoptask.inputs.data = data
aoptask.inputs.enable_dra = False
aoptask.inputs.bands = 'MS'

envi_RPCO = gbdx.Task("ENVI_RPCOrthorectification")
envi_RPCO.inputs.input_raster = aop2task.outputs.data.value
envi_RPCO.inputs.dem_raster_filename = 'GMTED2010.jp2'

workflow = gbdx.Workflow([aoptask, envi_RPCO])

workflow.savedata(
    envi_RPCO.outputs.output_raster_uri,
    location='ENVI_RPCO/output_raster_uri'
)

print workflow.execute()
print workflow.status
# Repeat workflow.status as needed to monitor progress.
```

### Known Issues:  
Not recommended for use with WorldView (includes WV01, WV02, WV03, WV04) GeoEye-1 (GE01) or QuickBird (QB02) level 1B imagery.  See background information for details on RPCOrthorectification limitations.  For Level 1B DG Sensor Imagery, Orthorectification using the [Advanced Image Preprocessor](https://github.com/TDG-Platform/docs/blob/master/Advanced_Image_Preprocessor.md) is recommended. RPCOrthorectifcation may be used with IKONOS Imagery, which is ordered through the Platform as a Level 2A product.

### Background
For background on the development and implementation of ENVI_RPCOrthorectification see [here](http://www.harrisgeospatial.com/docs/RPCOrthorectification.html).


### Contact
Document owner - Carl Reeder creeder@digitalglobe.com
