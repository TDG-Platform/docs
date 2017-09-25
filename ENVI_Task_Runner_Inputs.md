# ENVI Task Runner Inputs



In general the ENVI task runner is a GBDX execution interface for the ENVI**®** Engine. Part of this interface is to provide support for the various [ENVI data types](https://www.harrisgeospatial.com/docs/supporteddatatypes.html). This document will cover the more complicated use cases of specific ENVI data types, that cannot be covered by the various documents for each ENVI task. The following are the currently supported ENVI data types and their GBDX type:



|              ENVI Data Type              | GBDX Type |
| :--------------------------------------: | :-------: |
|        [ENVIRaster](#enviraster)         | Directory |
|           [ENVIURI](#enviuri)            | Directory |
| [ENVISpectralLibrary](#envispectralLibrary) | Directory |
|           [ENVIROI](#enviroi)            | Directory |
|        [ENVIGCPSet](#envigcpset)         | Directory |
|   [ENVITiePointSet](#envitiepointset)    | Directory |
|        [ENVIVector](#envivector)         | Directory |
|      [ENVICoordSys](#envicoordsys)       |  String   |
| [ENVIGridDefinition](#envigriddefinition) |  String   |
|    [ENVISpatialRef](#envispatialref)     |   None    |
| [ENVIPseudoRasterSpatialRef](#envipseudorasterspatialref) |  String   |
| [ENVIStandardRasterSpatialRef](#envistandardrasterspatialref) |  String   |
| [ENVIRPCRasterSpatialRef](#envirpcrasterspatialref) |  String   |
|       [ENVIGeoJson](#envigeojson)        |  String   |



# Find ENVI Port Type



All of the GBDX task definitions have the ENVI (or IDL) data types in the description of the ports. There are a couple of ways to get the task definition: through API requests (Postman, etc), or through gbdxtools. The easiest and recommended is to use [gbdxtools](http://gbdxtools.readthedocs.io/en/latest/), for example (ipython):



```javascript
In [1]: from gbdxtools import Interface
In [2]: gbdx = Interface()
In [3]: task = gbdx.Task("ENVI_QuerySpectralIndices")

In [4]: task.inputs
Out[4]:
input_raster
input_raster_format
input_raster_filename
file_types
input_raster_band_grouping

In [5]: task.inputs.input_raster
Out[5]:
Port input_raster:
	type: directory
	description: Specify a raster to query for available spectral indices. -- Value Type: ENVIRASTER
	multiplex: False
	required: True
	Value: None
        
In [6]: task.inputs.file_types
Out[6]:
Port file_types:
	type: string
	description: GBDX Option. Comma seperated list of permitted file type extensions. Use this to filter input files -- Value Type: STRING[*]
	multiplex: False
	required: False
	Value: None
```



As can be seen from the above, the ENVI type for `task.inputs.input_raster` is `ENVIRASTER`, and the IDL type for `task.inputs.file_types` is `String[*]`, meaning a one dimension array of strings.



# ENVI Data Types

Here are descriptions for the various GBDX supported ENVI data types and their varying usage examples. ENVI data types can be complex, which means some require multiple GBDX input ports to be adequately configured in the task_runner. These ports are described below.



## ENVIRaster

### Input Ports

| Example Input Ports          | GBDX Type | Required | Description                              |
| ---------------------------- | --------- | -------- | ---------------------------------------- |
| *input_raster*               | Directory | See Task | Directory containing the files required for the a task. |
| *input_raster_format*        | String    | False    | A string for selecting the raster format (non-DG format). Please refer to Supported Datasets table below for a list of valid values for currently supported image data products. |
| *input_raster_filename*      | String    | False    | A string with the filename of the raster for ENVI to open. This overrides any file discovery. |
| *input_raster_band_grouping* | String    | False    | A string name indentify which band grouping to use for the task. |

> Note: the example names in the table above are for demonstrating the typical set of ports used to configure an input raster. The names for the input rasters can vary by task (ie - input_low_resolution_raster), but the set of supplemental input ports will always be standard. 

### Description

ENVI can open many different datasets from different sensors, the full list can be seen [here](https://www.harrisgeospatial.com/docs/supportedformats.html). However, the ENVI task engine requires a JSON object which includes a single file name for the raster dataset. As can be seen from the list of supported sensors, this file is different for each sensor. So the task runner has built in file discovery for datasets supported by GBDX. The default file discovery is suitable for all DigitalGlobe's  Worldview sensors, as it discovers `*.til` first, then `*.tif`, for example:



```python
...
task = gbdx.Task('ENVI_QuerySpectralIndices')
task.inputs.input_raster = 's3://<bucket>/<folder>/'
...
```



To configure the task runner to switch the file discovery logic, use the `*_format` input port to specify the a supported input raster format. Currently the task runner supports all standard DigitalGlobe formats plus `IKONOS`, and `Landsat 8`. The following is an example:

```python
...
task = gbdx.Task('ENVI_QuerySpectralIndices')
task.inputs.input_raster = 's3://<bucket>/<folder>/'
task.inputs.input_raster_format = 'landsat-8'
...
```

> Note: See the ***Supported Datasets*** table below for the acceptable *input_raster_format* names. Also, majority of use cases will also require the *_band_grouping port as ENVI loads all the bands as different indexes. 



Alternately a user can overide all file discovery logic by using the `*_filename` input port. This passes the relative file name directly to the ENVI task engine. It also supports Python's glob style patterns for file discovery. An example is as follows:

```python
...
task = gbdx.Task('ENVI_QuerySpectralIndices')
task.inputs.input_raster = 's3://<bucket>/<folder>/'
task.inputs.input_raster_filename = 'landsat8_MTL.txt'
...
```

This port is particularily useful for use cases where a user has a dataset supported by ENVI, but the task runner doesn't have built in support for it. Also note, depending on how ENVI opens the raster, the `*_band_grouping` port may be required to select an appropriate index for a group of bands.



#### Raster Band Grouping Selection

When ENVI opens standardized raster data products distributed by various geospatial data providers, ENVI has built-in intelligence to open rasters with special metadata assignment and groups certain imagery bands together as individual raster datasets. For example, a typical IKONOS dataset is opened as two raster band groupings, *multispectral* and *panchromatic*. See the table below for datasets currently supported by the GBDX ENVI task runner and the specific band grouping names that can be specified. Even though the band grouping names for DigitalGlobe products (WorldView-\*, QuickBird, GeoEye-1) are provided in the table below, they are not required as the format has seperate images for each grouping. The following are examples of using `*_band_grouping` continued from above:



```python
# For IKONOS
...
task.inputs.input_raster_band_grouping = 'multispectral'
...
```

> Note: When using non-Worldview datasets, the ports `*_format` and `*_band_grouping` must be used together. 



See the below table for support datasets and the specific band grouping names.



##### Supported Datasets

|      Dataset Name      |           Band Grouping Names            | Format Input String |
| :--------------------: | :--------------------------------------: | :-----------------: |
| WorldView-1 (see note) |               panchromatic               |     worldview-1     |
| WorldView-2 (see note) |       multispectral, panchromatic        |     worldview-2     |
| WorldView-3 (see note) |    multispectral, panchromatic, swir     |     worldview-3     |
|  GeoEye-1 (see note)   |       multispectral, panchromatic        |      geoeye-1       |
|  QuickBird (see note)  |       multispectral, panchromatic        |      quickbird      |
|         IKONOS         |       multispectral, panchromatic        |       ikonos        |
|       Landsat 8        | multispectral, panchromatic, cirrus, thermal, quality |      landsat-8      |
|       Sentinel-2       |    M1-10m, M2-20m, M3-60m     |     sentinel-2      |

> Note: Band grouping names do not apply for standard format DG products where the a typical input_raster would have to point to a folder with a multispectral or panchromatic in it. Having both would cause an error with the task runner.



### ENVI DEM Rasters



There are tasks in the ENVI catalogue that require DEM rasters as inputs, which are implemented as *Special Case ENVIRasters*. These can be considered a subset of ENVIRaster except they allow for using DEM Rasters that are already part of the ENVI software distribution, as well as user provided DEM rasters. Also, the ports `*_format` and `*_band_grouping ` are not applicable for these types of rasters. 



#### Input Ports

| Example Input Ports   | GBDX Type | Required | Description                              |
| --------------------- | --------- | -------- | ---------------------------------------- |
| *dem_raster*          | Directory | False    | Directory containing the DEM files required for the a task. |
| *dem_raster_filename* | String    | False    | Special case of ENVI Raster filename. A string with the filename of the raster for ENVI to open. This overrides any file discovery. It also allows for using ENVI built in DEM raster. See below for details. |

> Note: the example names in the table above are for demonstrating the typical set of ports used to configure an input raster. The names for the input rasters can vary by task (ie - input_dem_raster). 



Usage example for a user provided DEM raster is as follows:

```python
...
task = gbdx.Task('ENVI_RPCOrthorectification')
task.inputs.input_raster = 's3://<bucket>/<folder>/<raster>'
task.inputs.dem_raster = 's3://<bucket>/<folder>/<dem>'
...
```



However, ENVI comes with the GMTED2010 DEM raster which is at 30 arc-seconds. And the Docker image for the ENVI task runner includes a 7.5 arc-second version of [GMTED2010](http://www.harrisgeospatial.com/Company/PressRoom/Blogs/ImagerySpeaksDetail/TabId/901/ArtMID/2927/ArticleID/14401/Upgrading-the-GMTED2010-global-elevation-data-included-with-ENVI.aspx). These two rasters can be sumarized as follows:



| Filename            | Resolution     | Notes                          |
| ------------------- | -------------- | ------------------------------ |
| GMTED2010.jp2       | 7.5 arc-second | Excludes Greenland & Antarctic |
| GMTED2010_polar.jp2 | 30 arc-second  | Global Coverage                |



To use these files, the port `*_filename` can be used to specify the which of the above files to use as the DEM file for the task. The following is an example:



```python
# Use the 30 arc-second DEM
...
task = gbdx.Task('ENVI_RPCOrthorectification')
task.inputs.input_raster = 's3://<bucket>/<folder>/<raster>'
task.inputs.dem_raster_filename = 'GMTED2010_polar.jp2'
...
```

> Note: The dem_raster port is optional, and if it is missing, the task runner will use the GMTED2010.jp2 DEM file.



## ENVIURI

### Input Ports

| Example Input Ports       | GBDX Type | Required | Description of Use Case                  |
| ------------------------- | --------- | -------- | ---------------------------------------- |
| *input_raster_uri*        | Directory | See Task | Directory containing the files required for the task. |
| *input_raster_uri_filter* | String    | False    | A single string or list of strings used to filter the input directory. Supports Python glob2 syntax. See below for more details. |



### Description

This input port is a generic file input for the ENVI task runner. The data type has no specific file type(s). The However, the ENVI task engine will only accept a single file name. By default, the task runner will search the input directory for any [supported file type](https://www.harrisgeospatial.com/docs/supportedformats.html). Which can result in multiple files being found by the task runner, which will cause an error. So, in order to use a port of this type, the task runner must be told which files to search for. This is done using the `*_filter` input port, which is prefixed with the name of the ENVIURI port. A usage example of this type of port is as follows:



```python
from gbdxtools import Interface
gbdx = Interface()

task = gbdx.Task("ENVI_BuildRasterSeries")
task.inputs.input_raster_uri = "s3://<bucket>/<folder>/"
task.inputs.input_raster_uri_filter = "*.dat"
...
```



The `*_filter` port needs to be a single string filter, each filter string must be a Python [globe2](https://docs.python.org/2/library/glob.html) style pattern. For example, a single string like `"**/*_MTL.txt"` will recursively look for files ending in `_MTL.txt`, or a string like `*.dat` will non-recursively look for files ending in `.dat`.   



## ENVISpectralLibrary

### Input Ports

| Example Input Ports               | GBDX Type | Required | Description                              |
| --------------------------------- | --------- | -------- | ---------------------------------------- |
| *input_spectral_library*          | Directory | False    | Directory containing the files required for the task. |
| *input_spectral_library_filename* | String    | False    | String name of the ENVI spectral library file. |

> Note: Both ports above are shown as not required, however one of the two is required. The task runner will return an error if none of them are provided.



### Description

This data type has two ports for two different use cases: providing the task runner with a spectral library file (S3 location), or using one of the spectral library files that is bundled with ENVI. When providing a spectral library file, the task runner will search the input directory for a file with the `*.sli` extension. The following example shows this use case:

```python
...
task = gbdx.Task('ENVI_GetSpectrumFromLibrary')
task.inputs.input_spectral_library = 's3://<bucket>/<folder>/'
task.inputs.spectrum_name = '<spectrum_name>'
...
```

> Note: when providing a *.sli file, an ENVI header (*.hdr) is also required. The creation of this file is left to the user.



To use one of the spectral library files bundled with the ENVI software, only the file name is required. The following example shows this use case:

```python
...
task = gbdx.Task('ENVI_GetSpectrumFromLibrary')
task.inputs.input_spectral_library_filename = 'veg_2grn.sli'
task.inputs.spectrum_name = 'Dry Grass'
...
```

> Note: Use the ENVI desktop application to find an appropriate *.sli file name. 



## ENVIROI

### Input Ports

| Example Input Ports | GBDX Type | Required | Description                              |
| ------------------- | --------- | -------- | ---------------------------------------- |
| *input_roi*         | Directory | See Task | Directory containing the files required for the task. |



### Description

This input port allows a user to provide an S3 location for the region of interest input files. The task runner will search the input directory for a `*.xml` file. The following is an example:

```python
...
task = gbdx.Task("ENVI_ROIToClassification")
task.inputs.input_roi = 's3://<bucket>/<folder>/'
...
```





## ENVIGCPSet

### Input Ports

| Example Input Ports | GBDX Type | Required | Description                              |
| ------------------- | --------- | -------- | ---------------------------------------- |
| *input_gcp*         | Directory | See Task | Directory containing the files required for the task. |



### Description

This input port allows a user to provide an S3 location for the ground control point input files. The task runner will search the input directory for a `*.pts` file. The following is an example:

```python
...
task = gbdx.Task("ENVI_RPCOrthorectification")
task.inputs.input_gcp = 's3://<bucket>/<folder>/'
...
```



## ENVITiePointSet

### Input Ports

| Example Input Ports | GBDX Type | Required | Description                              |
| ------------------- | --------- | -------- | ---------------------------------------- |
| *input_tiepoints*   | Directory | See Task | Directory containing the files required for the task. |



### Description

This input port allows a user to provide an S3 location for the tie points input files. The task runner will search the input directory for a `*.pts` file. The following is an example:

```python
...
task = gbdx.Task("ENVI_GenerateGCPsFromTiePoints")
task.inputs.input_tiepoints = 's3://<bucket>/<folder>/'
...
```



## ENVIVector

### Input Ports

| Example Input Ports | GBDX Type | Required | Description                              |
| ------------------- | --------- | -------- | ---------------------------------------- |
| *input_vector*      | Directory | See Task | Directory containing the files required for the task. |



### Description

This input port allows a user to provide an S3 location for the vector input files. The task runner will search the input directory for a `*.shp` file. The following is an example:

```python
...
task = gbdx.Task("ENVI_VectorAttributeToROIs")
task.inputs.input_vector = 's3://<bucket>/<folder>/'
...
```



## ENVICoordSys

Harris documentation Reference: https://www.harrisgeospatial.com/docs/envicoordsys.html 

### Input Attributes

| Attribute Name   | Required | Description                              |
| ---------------- | -------- | ---------------------------------------- |
| *factory*        | True     | Sting value of ` CoordSys`               |
| *coord_sys_code* | False    | An integer indicating the geographic or projected coordinate system code to use. |
| *coord_sys_str*  | False    | A string indicating the geographic or projected coordinate system string. |

> Note: The coord_sys_code and coord_sys_string keys are mutually exclusive.



### Description

This input port uses a string json object and it's attributes to describe a coordinate system. The following is an example:

```python
...
task = gbdx.Task("ENVI_ReprojectRaster")
task.inputs.coord_sys = '{"factory": "CoordSys", "coord_sys_code": 00000}'
...
```



## ENVIGridDefinition

Harris documentation Reference: http://www.harrisgeospatial.com/docs/ENVIGridDefinition.html

### Input Attributes

| Attribute Name | Required | Description                              |
| -------------- | -------- | ---------------------------------------- |
| *factory*      | True     | Sting value of ` GridDefinition`         |
| *coord_sys*    | True     | An `ENVICoordSys` object that indicates the coordinate system of the grid definition |
| *extents*      | True     | The geographic extent of the grid.       |
| *nrows*        | True     | Number of rows in the grid.              |
| *ncolumns*     | True     | Number of columns in the grid            |

### Description

This input port uses a string json object and it's attributes to describe a grid definition. The following is an example:

```python
...
task = gbdx.Task("ENVI_RegridRaster")
task.inputs.grid_definition = '''{
  "factory": "GridDefinition",
  "coord_sys": {"factory": "CoordSys", "coord_sys_code": 00000},
  "extents": [0.0, 0.0, 0.0, 0.0],
  "nrows": 0,
  "ncolumns": 0
}
'''
...
```



## ENVISpatialRef

This type may be identified as `_ENVISPATIALREF` in the GBDX task definitions, and is a wrapper (abstract type) for similar ENVI spatial reference objects. The sub types are as follows:

- [ENVIPseudoRasterSpatialRef](#ENVIPseudoRasterSpatialRef)
- [ENVIStandardRasterSpatialRef](#ENVIStandardRasterSpatialRef)
- [ENVIRPCRasterSpatialRef](#ENVIRPCRasterSpatialRef)

This means any of these sub types can be used for the parent type `_ENVISPATIALREF`. See the below sections for descriptions of each.



## ENVIPseudoRasterSpatialRef

Harris Documentation Reference: http://www.harrisgeospatial.com/docs/envipseudorasterspatialref.html

### Input Attributes

| Attribute Name       | Required | Description                              |
| -------------------- | -------- | ---------------------------------------- |
| *factory*            | True     | Sting value of `PseudoRasterSpatialRef`  |
| *pseudo_geo_point_1* | True     | A four-element array [*X Pixel*, *Y Pixel*, *Longitude*, *Latitude*] specifying a geographic corner for a non-georeferenced file. |
| *pseudo_geo_point_2* | True     | A four-element array [*X Pixel*, *Y Pixel*, *Longitude*, *Latitude*] specifying a geographic corner for a non-georeferenced file. |
| *pseudo_geo_point_3* | True     | A four-element array [*X Pixel*, *Y Pixel*, *Longitude*, *Latitude*] specifying a geographic corner for a non-georeferenced file. |
| *pseudo_geo_point_4* | True     | A four-element array [*X Pixel*, *Y Pixel*, *Longitude*, *Latitude*] specifying a geographic corner for a non-georeferenced file. |



### Description

This input port uses a string json object and it's attributes to describe a pseudo taster spatial reference . The following is an example :

```python
...
task.inputs.spatial_reference = '''{
  "factory": "PseudoRasterSpatialRef",
  "pseudo_geo_point_1": [1.0, 1.0, -117.07201, 32.893801],
  "pseudo_geo_point_2": [1000.0, 1.0, -116.95856, 32.873647],
  "pseudo_geo_point_3": [1.0, 1000.0, -117.09961 32.806283],
  "pseudo_geo_point_4": [1000.0, 1000.0, -116.98626, 32.786154],
}'''
...
```



## ENVIStandardRasterSpatialRef

Harris Documentation Reference: http://www.harrisgeospatial.com/docs/envistandardrasterspatialref.html

### Input Attributes

| Attribute Name   | Required | Description                              |
| ---------------- | -------- | ---------------------------------------- |
| *factory*        | True     | Sting value of `StandardRasterSpatialRef` |
| *coord_sys_code* | False    | An integer indicating the geographic or projected coordinate system code to use. |
| *coord_sys_str*  | False    | A string indicating the geographic or projected coordinate system string. |
| pixel_size       | True     | A two-element double-precision array with the [x,y] pixel size in the same units as the associated coordinate system. |
| rotation         | False    | A double-precision floating-point value indicating the rotation of the image, degrees clockwise from North. |
| tie_point_pixel  | False    | A two-element double-precision array with the pixel coordinates of the tie point. If you do not set this key. DEFAULT: [0,0] |
| tie_point_map    | True     | A two-element double-precision array with the map coordinates of the tie_point_pixel location. Must be in the same units as the coordinate system. |

>  Note: The coord_sys_code and coord_sys_string keys are mutually exclusive.



### Description

This input port uses a string json object and it's attributes to describe a standard raster spatial reference. The following is an example:

```python
...
task.inputs.input_ = '''{
  "factory": "StandardRasterSpatialRef",
  "coord_sys_code": [1.0, 1.0, -117.07201, 32.893801],
  "pixel_size": [9.186, 9.186],
  "tie_point_pixel": [0.0, 0.0],
  "tie_point_map": [3075299.7946,1246937.9905],
}'''
...
```



## ENVIRPCRasterSpatialRef

Harris Documentation Reference: http://www.harrisgeospatial.com/docs/envirpcrasterspatialref.html

### Input Attributes

| Attribute Name       | Required | Description                              |
| -------------------- | -------- | ---------------------------------------- |
| *factory*            | True     | Sting value of `RPCRasterSpatialRef`     |
| *rpc_offsets*        | True     | A five-element, double-precision array that specifies the *Line_Offset*, *Sample_Offset*, *Latitude_Offset*, *Longitude_Offset*, and *Height_Offset* values |
| *rpc_scales*         | True     | A five-element, double-precision array that specifies the *Line_Scale*, *Sample_Scale*, *Latitude_Scale*, *Longitude_Scale*, and *Height_Scale* values. |
| *rpc_line_num_coeff* | True     | A 20-element, double-precision array of RPC line numerator coefficients. |
| *rpc_line_den_coeff* | True     | A 20-element, double-precision array of RPC line denominator coefficients. |
| *rpc_samp_num_coeff* | True     | A 20-element, double-precision array of RPC sample numerator coefficients. |
| *rpc_samp_den_coeff* | True     | A 20-element, double-precision array of RPC sample denominator coefficients. |



### Description

This input port uses a string json object and it's attributes to describe a RPC raster spatial reference. The following is an example:

```python
...
task.inputs.input_ = '''{
  "factory": "StandardRasterSpatialRef",
  "coord_sys_code": [1.0, 1.0, -117.07201, 32.893801],
  "pixel_size": [9.186, 9.186],
  "tie_point_pixel": [0.0, 0.0],
  "tie_point_map": [3075299.7946,1246937.9905],
}'''
...
```



## ENVIGeoJson

Harris Documentation Reference: https://harrisgeospatial.com/docs/envigeojson.html

Harris ENVIGeoJSONToROITask Documentation Reference: https://harrisgeospatial.com/docs/envigeojsontoroitask.html

### Description

This input port supports valid GeoJson, and will accept the GeoJson as a string. A detailed example can be seen on the Above referenced Harris documentation for `ENVIGeoJSONToROITask`. There are some constraints on the contents of the GeoJson:

- ENVI currently supports GeometryCollection type objects. These objects can only contain one or more MultiPolygon type geometries.
- The crs tag is not required. If the code contains this tag, ENVI converts it to a string. Otherwise, it uses a default value of wgs84.
- You can add name and color properties to each MultiPolygon object.

For example:

```python
...
task = gbdx.Task("ENVI_GeoJSONToROI")
task.inputs.input_geojson = ''' {
  "type": "GeometryCollection",
  "geometries": [
    {"type": "MultiPolygon",
  ...
} # See the Harris code example for more details.
'''
...
```

