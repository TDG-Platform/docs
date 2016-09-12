# AOP_Strip_Processor

This task runs the Advanced Ortho Processing (AOP) algorithm to produce orthorectified imagery from raw (level 1B) imagery.  There are many additional processing options including atmospheric compensation (ACOMP) (which is always recommended), pansharpening and dynamic range adjustment (DRA).  

AOP_Strip_Processor can be run with Python using   [gbdxtools](https://github.com/DigitalGlobe/gbdxtools) or through the [GBDX Web Application](https://gbdx.geobigdata.io/materials/).  

### Table of Contents
 * [Quickstart](#quickstart) - Get started!
 * [Inputs](#inputs) - Required and optional task inputs.
 * [Outputs](#outputs) - Task outputs and example contents.
 * [Advanced Options](#advanced-options) - Additional information for advanced users.
 * [Runtime](#runtime) - Results of task benchmark tests to find average runtimes.
 * [Contact Us ](#contact-us) - Contact information.


### Quickstart

This script uses AOP_Strip_Processor to produce orthorectified and atmospherically compensated multispectral and panchromatic images from a raw WorldView-3 (WV03) image over Naples, Italy.

```python
# Quickstart Example producing an Orthorectified and AComp output for MS + PAN
# First Initialize the Environment
from gbdxtools import Interface
gbdx = Interface()

# WV03 Image over Naples, Italy
# Make sure both pan sharpening and DRA are disabled in order to get separate PAN and MS outputs.
data = "s3://receiving-dgcs-tdgplatform-com/055249130010_01_003"
aoptask = gbdx.Task('AOP_Strip_Processor', data=data, enable_pansharpen=False, enable_dra=False)
workflow = gbdx.Workflow([ aoptask ])
workflow.savedata(aoptask.outputs.data, location='Naples_WV03_QuickStart')

workflow.execute()

print workflow.id
print workflow.status
```

The `data` variable specifies the S3 URL of the raw image.
The `gbdx.Task()` call creates the `aoptask` instance and specifies its desired input values.
The `workflow.savedata()` call specifies that the task output will be saved in
[gbd-customer-data/prefix/Naples_WV03_Quickstart](http://gbdxdocs.digitalglobe.com/docs/s3-storage-service-course).

Running the script in an IPython session produces these results:
```
In [1]: # Quickstart Example producing an Orthorectified and AComp output for MS + PAN
In [2]: # First Initialize the Environment
In [3]: from gbdxtools import Interface
In [4]: gbdx = Interface()
  2016-06-24 16:29:53,856 - gbdxtools - INFO - Logger initialized
In [5]: # WV03 Image over Naples, Italy
In [6]: # Make sure both pan sharpening and DRA are disabled in order to get separate PAN and MS outputs.
In [7]: data = "s3://receiving-dgcs-tdgplatform-com/055249130010_01_003"
In [8]: aoptask = gbdx.Task('AOP_Strip_Processor', data=data, enable_pansharpen=False, enable_dra=False)
In [9]: workflow = gbdx.Workflow([ aoptask ])  
In [10]: workflow.savedata(aoptask.outputs.data, location='Naples_WV03_QuickStart')
In [11]: workflow.execute()
Out[12]: u'4362772047134837472'
In [13]: print workflow.id
  4362772047134837472
```

The following table lists additional datasets over Naples, Italy, for various DigitalGlobe sensors (WV is WorldView, GE is GeoEye, QB is QuickBird). Substitute the S3 URL for the `data` variable in the previous example script.

  Sensor |  Catalog ID      | S3 URL
:-------:|:----------------:|--------
   WV01  | 10200100423D7A00 | s3://receiving-dgcs-tdgplatform-com/055250712010_01_003
   WV02  | 103001004DAFAF00 | s3://receiving-dgcs-tdgplatform-com/055253506010_01_003
   WV03  | 104001000E25D700 | s3://receiving-dgcs-tdgplatform-com/055249130010_01_003
   GE01  | 1050010001136C00 | s3://receiving-dgcs-tdgplatform-com/055254039010_01_003
   QB02  | 101001000F18EA00 | s3://receiving-dgcs-tdgplatform-com/055269445010_01_003


### Inputs
The following table lists the AOP_Strip_Processor inputs.
All inputs are **optional** with default values, with the exception of `data` which specifies the task's input data location. Click on the name for a more detailed description of the use case.

Name                     |       Default         |        Valid Values             |   Description
-------------------------|:---------------------:|---------------------------------|-----------------
data                     |          N/A          | S3 URL                          | S3 location of 1B input data.
[enable_acomp](#run-dg-acomp)             |         true          | true, false                     | Run atmospheric compensation.
[enable_pansharpen](#pansharpening)   |         true          | true, false                     | Pan sharpen multispectral data.
[enable_dra](#dynamic-range-adjustment) |         true          | true, false                     | Apply dynamic range adjustment.
[enable_tiling](#set-tiling)           |         false         | true, false                     | Tile output images according to the `ortho_tiling_scheme` input.
[bands](#select-bands-to-process)   |         Auto          | PAN+MS, PAN, MS, Auto           | Bands to process. `Auto` inspects input data for band info.
[parts](#specifying-strip-parts)                    |       All Parts       | Comma-separated part numbers    | List of strip parts to include in processing.
[ortho_epsg](#change-projection) |       EPSG:4326      | EPSG codes, UTM                 | EPSG code of projection for orthorectification. `UTM` automatically determines EPSG code from strip coordinates.
[ortho_pixel_size](#set-pixel-size) |         Auto          | Pixel size in meters, Auto      | Pixel size of orthorectified output. `Auto` inspects input data for collected pixel size.
[ortho_tiling_scheme](#set-ortho-tiling-scheme)      |          N/A          | Ex: DGHalfMeter:18              | Tiling scheme and zoom level for orthorectification. Overrides `ortho_epsg` and `ortho_pixel_size`.
[ortho_dem_specifier](#specify-dem)      |        SRTM90         | NED, SRTM30, SRTM90             | DEM identifier for orthorectification.
[ortho_interpolation_type](#specify-interpolation-method) |         Cubic         | Nearest, Bilinear, Cubic        | Pixel interpolation type for orthorectification.
[dra_mode](#using-dynamic-range-adjustment)                 |    IntensityAdjust    | IntensityAdjust, BaseLayerMatch | Dynamic range adjustment type. `BaseLayerMatch` only supported for geographic projection (EPSG:4326).
[dra_low_cutoff](#using-dynamic-range-adjustment)           |          0.5          | 0.0 - 100.0                     | Low cutoff percentage for `dra_mode` == `IntensityAdjust`.
[dra_high_cutoff](#using-dynamic-range-adjustment)          |         99.95         | 0.0 - 100.0                     | High cutoff percentage for `dra_mode` == `IntensityAdjust`.
[dra_gamma](#using-dynamic-range-adjustment)                |          1.25         | Nonzero float value             | Gamma value for `dra_mode` == `IntensityAdjust`.
[dra_bit_depth](#using-dynamic-range-adjustment)            |           8           | 8, 16                           | Output bit depth for `dra_mode` == `IntensityAdjust`.
[dra_baselayer_prefix](#using-dynamic-range-adjustment)     | s3://dg-baselayer/v2/ | S3 URL                          | S3 location of base layer for `dra_mode` == `BaseLayerMatch`. Base layer must be tiled to tiling scheme DGHalfMeter:9.
[tiling_zoom_level](tiling-zoom-level)        |          12           | Integer (see tiling scheme)     | Zoom level (i.e. size) of output tiles for `enable_tiling` == `true`.


The AOP task inputs can be set in various combinations to generate several different types of output imagery:

 * Pansharpened and DRA 8-bit RGB image with atmospheric compensation
  * Default behavior, no need to change inputs
  ```python
  aoptask = gbdx.Task('AOP_Strip_Processor', data=data)
  ```
 * Multispectral image only (4-band or 8-band, depending on sensor) with ACOMP
  * `bands` = `MS`
  * `enable_pansharpen` = `false`
  * `enable_dra` = `false`
  ```python
  aoptask = gbdx.Task('AOP_Strip_Processor', data=data, bands='MS', enable_pansharpen=False, enable_dra=False)
  ```
 * Multispectral and panchromatic images (separate) with ACOMP
  * `enable_pansharpen` = `false`
  * `enable_dra` = `false`
  ```python
  aoptask = gbdx.Task('AOP_Strip_Processor', data=data, enable_pansharpen=False, enable_dra=False)
  ```
 * Panchromatic image only (ACOMP not available)
  * `bands` = `PAN`
  * `enable_acomp` = `false`
  * `enable_pansharpen` = `false`
  * `enable_dra` = `false`
  ```python
  aoptask = gbdx.Task('AOP_Strip_Processor', data=data, bands='PAN', enable_acomp=False, enable_pansharpen=False, enable_dra=False)
  ```

Please pay attention to the following **important** notes.

 * To get separate PAN and MS outputs:
  * `data` must include both PAN and MS bands.
  * `enable_pansharpen` must be `false` to skip combining of PAN and MS data.
  * `enable_dra` must be `false` because it relies on pansharpening to run first.
  * `bands` must be set to either `PAN+MS` or `Auto`.
 * `enable_tiling` can only be `true` when `ortho_tiling_scheme` is set.
 * `ortho_epsg` can be set to `UTM` which automatically determines the correct EPSG code for the UTM zone at the center of the input data.
 * When set, `ortho_tiling_scheme` overrides `ortho_epsg` and `ortho_pixel_size`.
 * `ortho_dem_specifier` currently doesn't include any DEMs that cover the globe north of +60 degrees latitude. Additional non-standard DEMs may be available upon request.
 * When `dra_mode` is set to `BaseLayerMatch`, a geographic projection must be used. Either `ortho_epsg` must be set to `EPSG:4326`, or `ortho_tiling_scheme` must be set to use DGHalfMeter at some zoom level.
 * For WorldView-1, `enable_acomp`, `enable_pansharpen`, and `enable_dra` must all be set to `false` since that sensor only produces panchromatic data.


### Outputs

The AOP_Strip_Processor outputs are the following.

Name | Required |   Description
-----|:--------:|-----------------
data |     Y    | S3 location where output is stored
log  |     N    | S3 location where logs are stored

##### `data`

The `data` output port contains the location where the AOP_Strip_Processor output is stored. Contents may vary slightly depending on the input settings. The following listing  
is from the [AWS CLI](https://aws.amazon.com/cli/), with columns for the creation date, time, file size, and file name. `PRE` in the size column indicates an S3 prefix, similar to a subdirectory. This is a typical result from running AOP_Strip_Processor with default settings. The sequence of characters "055421455010_01" is called a SOLI (Sales Order Line Item) and is an artifact of the image ordering system.

```
                           PRE 055421455010_01/
2016-06-22 15:41:53         16 processed_strips.txt
2016-06-22 15:41:53       4200 workorder_055421455010_01.xml
```

 * `055421455010_01/`: Subdirectory containing the processing results.
 * `processed_strips.txt`: File containing a list of the images that were processed.
 * `workorder_055421455010_01.xml`: File containing the inputs that were used by the AOP workflow system.

This is a listing of the contents of the `055421455010_01/` subdirectory:

```
                           PRE GIS_FILES/
2016-06-22 15:41:26       4948 055421455010_01_assembly.IMD
2016-06-22 15:41:26     895166 055421455010_01_assembly.XML
2016-06-22 15:41:26  984030964 055421455010_01_assembly.tif
```

 * `GIS_FILES/`: Subdirectory copied from input data that contains various shapefiles describing the input image.
 * `055421455010_01_assembly.IMD`: IMD file (image metadata) copied from one part (scene) of the input data. Currently, no attempt is made to update this file to reflect the processed output.
 * `055421455010_01_assembly.XML`: XML file (additional metadata) copied form one part (scene) of the input data. Currently, no attempt is made to update this file to reflect the processed output.
 * `055421455010_01_assembly.tif`: The output image in GeoTIFF format.

You can also preview the results of AOP_Strip_Processor using the [s3 browser](http://s3browser-env.elasticbeanstalk.com/login.html).

##### `log`
The `log` output port contains the location where a trace of log messages generated during processing is stored. This can be useful for debugging. A typical run would produce a listing similar to the one below.

```
2016-06-22 15:40:54          0 055421455010_01.stderr
2016-06-22 15:40:54     117469 055421455010_01.stdout
```

 * `055421455010_01.stderr`: Captured stderr stream from processing.
 * `055421455010_01.stdout`: Captured stdout stream from processing.



### Advanced Options 

#### Run DG AComp
  * The 'enable_acomp' option runs the DG Atmospheric Compensation Process.  The default setting is on (True).  This will remove haze and provide the best surface reflectance output for spectral analysis of imagery. 

#### Pansharpening
  * The 'enable_pansharpen' output is a high-resolution RGB image.  The process merges the lower resolution multispectral image with the higher resolution panchromatic image to produce a high resolution multispectral image (RGB). The default is to run pansharpening.  It must be set to 'False' if you want preserve the full 8-band or 4-band image from the input image.

#### Dynamic Range Adjustment
  * The default for 'enable_dra' is on (True) and it must be set to 'False' to produce a 4-band or 8-band image (+/- panchromatic band). For all other Dynamic Range Adjustment Settings:  [see below](#using-dynammic-range-adjustment)

#### Set Tiling
  * The 'enable_tiling' setting allows the image to be rendered according to a specified grid size.  Tiling is used to improve performance of subsequent image processing steps in the workflow, especially when computing resources are limited. The default setting is off.

#### Select Bands to Process
  * 'bands' allows you to select the bands to be processes for further applications.  The default is 'Auto', which will process all of the bands (including panchromatic) that are in the S3 input data location.  Other options are PAN+MS, PAN, MS. Use when the next application of algorithm in your workflow requires specific band inputs.

#### Specifying Strip Parts
  * The `parts` input can be used to limit processing to a subset of an input strip. This requires advance knowledge of the layout of a strip order. One way to get this information is by looking in the input strip's `GIS_FILES` directory at the *_PRODUCT_SHAPE.shp vectors. That particular file shows the boundaries of each part (scene) of a strip. Once those numeric values are known, set `parts` to a comma-separated list, e.g. `2, 3, 4`.

#### Change Projection
  * The 'ortho_epsg' The default is EPSG:4326 which is WGS84 geographic coordinates.  For some cases, such as for change detection, square pixel are required so you must reproject the image to a UTM grid.  You can specify the EPSG code if you know it, or set ortho_epsg='UTM' and the AOP processor will select the appropriate UTM zone.
  
#### Set Pixel Size
  * The output image pixel size can be specified in meters. The default setting is the same as the input pixel size ('Auto'). 
  
#### Set Tiling Scheme
  * A custom tiling scheme can be specified that overrides 'ortho_epsg' and 'ortho_pixel_size'

#### Specify DEM
  * The default DEM (digital elevation model) used in the orthorectification process is SRTM90 (Shuttle Radar Topography Mission).  Other options include [SRTM30](#http://www2.jpl.nasa.gov/srtm/) and [NED](#http://nationalmap.gov/elevation.html).

#### Specify Interpolation Method
  * This sets the resampling method applied during the AOP process. The default setting is ortho_interpolation_type='Cubic'. Other options are Bilinear and Nearest Neighbor.  However, for spectral analysis Bilinear is preferred because it affects the spectral DN the least.

#### Tiling Zoom Level
  * The output zoom-level for viewing can be set when enable_tiling ='True'.  The default is 12m.  

#### Using Dynamic Range Adjustment
The included DRA algorithm has several inputs that affect the final 8-bit RGB result. Please read all of the options carefully before making any adjustments.  The default DRA setting will work best for most cases.

 * `dra_mode` - IntensityAdjust is for standalone, individual images that are not going to be mosaicked together. BaseLayerMatch uses a global base layer for color matching and helps maintain consistency when mosaicking. The base layer started out as color-balanced and mosaicked Landsat imagery but may have started incorporating higher-res imagery also.

 * `dra_low_cutoff` - Sets the black point in the histogram. Adjusting this will change the point in the histogram that is considered “black” and will darken and lighten the low end of the histogram. Setting the number lower (<0.5) will brighten the darker color tones and make the overall image lighter. Setting the number higher will saturate more of the darker color tones and make the overall image darker. Could start to lose detail in the darker areas if too heavy-handed. A light touch can make a huge difference so be careful.

 * `dra_high_cutoff` - Sets the white point in the histogram. Same general idea as the low cutoff percentage but operates on the brightest color tones to adjust what is considered saturated “white”. Setting this number lower (<99.95) will brighten the image while setting the number higher will darken the image. Again, a light touch is mandatory to keep things looking “normal”.

 * `dra_gamma` - Adjusts the curvature of the transfer function from input to output. When gamma=1, that is a straightforward, linear transfer from input to output. When gamma>1, the image will get overall brighter. Conversely, the image will get overall darker when gamma<1. Works in conjunction with the histogram cutoff values but is a completely independent parameter. Operates like a root stretch but with much finer adjustment settings. All three parameters, low cutoff, high cutoff, and gamma, work together to adjust the overall brightness, contrast, and dynamic range of the image. They’re all independent and will affect the final DRAed image in similar, but different, ways. Setting these is more an art than a science and it’s highly recommended to NOT mess with these unless the image is one of those special cases and is totally screwed up. Then the art comes into play.

 * `dra_bit_depth` - Typically it only makes sense to apply dynamic range adjustment to convert imagery to 8-bit. The 16-bit option is available mainly for debugging purposes, but isn't useful in normal situations.

### Runtime

The following table lists all applicable runtime outputs. 
For details on the methods of testing the runtimes of the task visit the following link:(INSERT link to GBDX U page here)

  Sensor Name  |  Average runtime  |  Total Area (k2)  |  Time(min)  |  Time/Area k2
--------|:----------:|-----------|----------------|---------------
QB | 41,551,668 | 312.07 | 460.603 | 1.48 |
WV01| 1,028,100,320 |351.72 |475.276 | 1.35|
WV02|35,872,942|329.87|651.095 | 1.97|
WV03|35,371,971|196.27|655.671 | 3.34|
GE| 57,498,000|332.97|560.836 | 1.68|


#### Contact Us   
If your customer is having a specific problem. Tech Owner: [Tim Harris](Tim.Harris@digitalglobe.com) & Editor: [Kathleen Johnson](kajohnso@digitalglobe.com)

