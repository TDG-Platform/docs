# ENVI Color Slice Classification

This task creates a classification raster by thresholding on select data ranges and colors to highlight areas of a raster.  By default, 16 classes are generated with the first 16 colors of the 'Rainbow' color table.

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
#  - Image must be a single band
data = 's3://gbd-customer-data/CustomerAccount#/PathToImage/'

envi = gbdx.Task('ENVI_ColorSliceClassification')
envi.inputs.input_raster = data

workflow = gbdx.Workflow([envi])

workflow.savedata(
    envi.outputs.output_raster_uri, 
    location='Benchmark/ENVI_ColorSliceClassification/WV1'
)

print workflow.execute()
print workflow.status
# Repeat workflow.status as needed to monitor progress.
```



### Inputs

The following table lists all inputs for this task. For details regarding the use of all ENVI input types refer to the [ENVI Task Runner Inputs]([See ENVIRASTER input type](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md)) documentation.

| Name                       | Required | Default | Valid Values                             | Description                              |
| -------------------------- | :------: | ------- | ---------------------------------------- | ---------------------------------------- |
| file_types                 |  False   | None    | string                                   | GBDX Option. Comma separated list of permitted file type extensions. Use this to filter input files -- Value Type: STRING |
| input_raster               |   True   | None    | A valid S3 URL containing image files.   | Specify a raster from which to run the task. -- Value Type: ENVIRASTER |
| input_raster_format        |  False   | None    | [See ENVIRASTER input type](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md) | Provide the format of the image, for example: landsat-8. -- Value Type: STRING |
| input_raster_band_grouping |  False   | None    | [See ENVIRASTER input type](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md) | Provide the name of the band grouping to be used in the task, ie - panchromatic. -- Value Type: STRING |
| input_raster_filename      |  False   | None    | [See ENVIRASTER input type](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md) | Provide the explicit relative raster filename that ENVI will open. This overrides any file lookup in the task runner. -- Value Type: STRING |
| color_table_name           |  False   | None    | string, see IDL command [LOADCT](http://www.harrisgeospatial.com/docs/loadct_procedure.html) for a full list of options. | Specify a string with the name of an IDL color table.  The default value is Rainbow.  Issue the following IDL command to find valid strings: LOADCT. -- Value Type: STRING |
| class_colors               |  False   | None    | i.e. - '[[255,0,0], [0,0,200], [0,200,0]]' | Specify a (3,n) byte array with the RGB colors for the given ranges, where n is the number of classes.  Use this property in conjunction with CLASS_RANGES. -- Value Type: BYTE[3, *] |
| reverse_color_table        |  False   | None    | True/False                               | Set this property to reverse the color table.  Use this property in conjunction with COLOR_TABLE_NAME property. The options are true or false. -- Value Type: BOOL |
| data_maximum               |  False   | None    | Varies depending on raster values        | Specify the maximum value used to calculate data ranges with NUMBER_OF_RANGES.  If this is not set, then the largest value in the INPUT_RASTER band is used. -- Value Type: DOUBLE |
| class_ranges               |  False   | None    | i.e. - '[[min_0, max)0], …, [min_n, max_n]]' | Specify a (2,n) array of color slice ranges, where n is the number of classes.  In each array element, specify the minimum and maximum data value for the class. -- Value Type: DOUBLE |
| range_size                 |  False   | None    | string                                   | Specify the width of each data range to create.  The NUMBER_OF_RANGES is used in conjunction with RANGE_SIZE.  Any data above DATA_MINIMUM+NUMBER_OF_RANGES*RANGE_SIZE will not be classified.  -- Value Type: DOUBLE |
| data_minimum               |  False   | None    | Varies depending on raster values        | Specify the minimum value used to calculate data ranges with NUMBER_OF_RANGES or RANGE_SIZE.  If this is not set, then the smallest value in the INPUT_RASTER band is used. -- Value Type: DOUBLE |
| number_of_ranges           |  False   | None    | dependent on minimum and maximum         | Specify the number of data ranges to create.  If RANGE_SIZE is specified, then the ranges are each that width, starting at DATA_MINIMUM and ending at DATA_MINIMUM+NUMBER_OF_RANGES*RANGE_SIZE.  If RANGE_SIZE is not specified, then the ranges are equal width between DATA_MINIMUM and DATA_MAXIMUM. -- Value Type: UINT |
| output_raster_uri_filename |  False   | None    | string                                   | Output OUTPUT_RASTER. -- Value Type: ENVIURI |



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

| Sensor Name | Average runtime | Total Area (k2) | Time(min) | Time/Area k2 |
| ----------- | :-------------: | --------------- | --------- | ------------ |
| QB          |   41,551,668    | 312.07          | 171.94    | 0.55         |
| WV01        |  1,028,100,320  | 351.72          | 288.61    | 0.82         |
| WV02        |   35,872,942    | 329.87          | 194.22    | 0.59         |
| WV03        |   35,371,971    | 196.27          | 203.28    | 1.04         |
| GE          |   57,498,000    | 332.97          | 192.33    | 0.58         |



### Advanced
This task may be used to stratify and symbolize values within a single band raster.  The color slice raster output will highlight variation of values across a raster. Advanced parameter inputs such as number of classes, class colors, and range sizes may be set by the user.  In this advanced example the task is chained together with ENVI_SpectralIndex to demonstrate the use of the task on the Normalized Difference Vegetation Index (NDVI).  

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
envi_ndvi.inputs.input_raster = aop2task.outputs.data.value
envi_ndvi.inputs.index = "Normalized Difference Vegetation Index"

envi_color = gbdx.Task('ENVI_ColorSliceClassification') 
envi_color.inputs.input_raster = envi_ndvi.outputs.output_raster_uri.value
envi_color.inputs.color_table_name = 'CB-RdYlGn'
envi_color.inputs.number_of_ranges = 15

workflow = gbdx.Workflow([aoptask, envi_ndvi, envi_color])

workflow.savedata(
  envi_color.outputs.output_raster_uri,
  location='Test_color_slice'
)

workflow.execute()

print workflow.execute()
print workflow.id
print workflow.status
```

**Sample Output:**

***AOP_Strip_Processor Output***

![AOP_Strip_Processor](colorslice_imgs/rgb.tiff)

***NDVI Output***

![ndvi](colorslice_imgs/ndvi.tiff)

***Color Slice Output***

![colorslice](colorslice_imgs/colorslice.tiff)


### Background
For background on the development and implementation of ENVI Color Slice Classification see [here](http://www.harrisgeospatial.com/docs/ENVIColorSliceClassificationTask.html).


### Contact
Document Owner - Carl Reeder - creeder@digitalglobe.com
