# ENVI Task Runner



In general the ENVI task runner is an interface to the ENVI task engine. Part of this interface is to provide support for the various ENVI data types, which are far more complex then the GBDX types (string, directory). This document will cover the more complicated use case of specific ENVI data types, that cannot be covered by the various documents for each ENVI task. The following are the currently supported ENVI data types and their GBDX type:



|        ENVI Data Type        | GBDX Type |
| :--------------------------: | :-------: |
|           ENVIURI            | Directory |
|          ENVIRaster          | Directory |
|          ENVIGCPSet          | Directory |
|           ENVIROI            | Directory |
|     ENVISpectralLibrary      | Directory |
|       ENVITiePointSet        | Directory |
|          ENVIVector          | Directory |
|         ENVICoordSys         |  String   |
|      ENVIGridDefinition      |  String   |
|  ENVIPseudoRasterSpatialRef  |  String   |
| ENVIStandardRasterSpatialRef |  String   |
|         ENVIGeoJson          |  String   |



# Find ENVI Port Type



All of the GBDX task definitions have the ENVI (or IDL) data types in the description of the ports. There are a couple of ways to get the task definition: through API requests (Postman, etc), or through gbdxtools. The easiest is to use [gbdxtools](http://gbdxtools.readthedocs.io/en/latest/), for example:



```python
In [1]: from gbdxtools import Interface
In [2]: gbdx = Interface()
In [3]: task = gbdx.Task("ENVI_QuerySpectralIndices")

In [4]: task.inputs
Out[4]:
input_raster
input_raster_metadata
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



As can be seen from the above, the ENVI type for `task.inputs.input_raster` is `ENVIRASTER`, and the IDL type for `task.inputs.file_types` is `String[*]`.



# ENVI Data Types



## ENVIURI



This data type is a generic file input for ENVI. There is no specific data types that it will accept. The ENVI task engine will also only accept a single file name. So, inorder to use a port of this type, the `file_types` input port must be used. A usage example of this type of port is a follows:



```python
from gbdxtools import Interface
gbdx = Interface()

task = gbdx.Task("ENVI_BuildRasterSeries")
task.inputs.file_types = "dat"
task.inputs.input_raster_uri = "s3://<bucket>/<folder>/"

# rest of script omitted ...
```



## ENVIRaster



> To come



## ENVIGCPSet



> To come



## ENVIROI



> To come



## ENVISpectralLibrary



> To come



## ENVITiePointSet



> To come



## ENVIVector



> To come



## ENVICoordSys



> To come



## ENVIGridDefinition



> To come



## ENVIPseudoRasterSpatialRef



> To come



## ENVIStandardRasterSpatialRef



> To come



## ENVIGeoJson



> To come
