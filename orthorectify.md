# orthorectify

The orthorectify GBDX task performs orthorectification on DigitalGlobe 1B images using the CSMv6 camera model.

orthorectify can be run with Python using [gbdxtools](https://github.com/DigitalGlobe/gbdxtools) or through the [GBDX Web Application](https://gbdx.geobigdata.io/materials/).  

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

This example demonstrates orthorectifying a DigitalGlobe 1B image 

```python
# Quickstart example for taskname.  

from gbdxtools import Interface
gbdx = Interface()

#Edit the following line to reflect a specific path to a DG 1B image
input1B = 's3://gbd-customer-data/CustomerAccount#/PathTo1BImage/'
ortho = gbdx.Task('orthorectify', data=input1B)

workflow = gbdx.Workflow([ortho])
  
#Edit the following line(s) to reflect specific folder(s) for the output file (example location provided)
workflow.savedata(ughli.outputs.data, location='ortho-output')
workflow.execute()

print workflow.id
print workflow.status
```

### Inputs

The following table lists all taskname inputs.
Mandatory (optional) settings are listed as Required = Yes.

  Name                  |  Required  |  Default              |  Valid Values       |  Description  
------------------------|------------|-----------------------|---------------------|-----------------------------------------------
data                    |  Yes       |  N/A                  |  S3 bucket location |  Location of DG 1B product containing PAN/VNIR
swir                    |  No        |  None                 |  S3 bucket location |  Location of DG 1B product containing associated SWIR
epsg_code               |  No        |  EPSG:4326            |  EPSG:epsg-code     |  EPSG code, e.g.: "EPSG:4326". Set to "UTM" for automatic UTM zone selection 
pixel_size_ms           |  No        |  2.0                  |  Real number        |  DG pixel size for MS parts in meters. Requires epsg_code to also be specified. Automatically determined from metadata if not specified. Set to "auto" to have MS pixel size computed from PAN pixel size. 
pixel_size_pan          |  No        |  0.5                  |  Real Number        |  DG pixel size for PAN parts in meters. Requires epsg_code to also be specified. Automatically determined from metadata if not specified.
pixel_size_swir         |  No        |  7.5                  |  Real number        |  DG pixel size for SWIR parts in meters. Requires epsg_code to also be specified. Automatically determined from metadata if not specified.
tiling_spec_ms          |  No        |  DGHALFMETER:16       |  DG tiling spec     |  DG tiling spec for MS parts. Not allowed if epsg_code is specified.
tiling_spec_pan         |  No        |  DGHALFMETER:18       |  DG tiling spec     |  DG tiling spec for PAN parts. Not allowed if epsg_code is specified.
tiling_spec_swir        |  No        |  DG750Centimeter:14   |  DG tiling spec     |  DG tiling spec for SWIR parts. Not allowed if epsg_code is specified.
parts                   |  No        |  Auto                 |  e.g.: P001,P002    |  Comma separated list of parts to process. All parts are processed if not specified.
swir_parts              |  No        |  Auto                 |  e.g.: P001,P002    |  Comma separated list of SWIR parts to process. All parts are processed if not specified.
bands                   |  No        |  Auto                 |  Auto, Multi, P     |  Comma separated list of bands to process
interpolation_technique |  No        |  BL                   |  BL, CC, NN         |  Specified interpolation technique for ortho generations. BL=Bilinear, CC=Cubic Convolution, NN=Nearest Neighbor

### Outputs

The following table lists all ughli outputs.
Mandatory (optional) settings are listed as Required = True (Required = False).

  Name  |  Required  |  Default  |  Valid Values  |  Description
--------|------------|-----------|----------------|---------------
data    |  Yes       |  N/A      |  Any           |  Location where output is stored


**Output structure**

The output directory port "data" contains the orthorectified imagery with a structure similar to the 1B input structure. VNIR imagery is output into 
the "vnir" folder. If SWIR imagery is also processed, SWIR output is placed into the "swir" folder. Within each such folder there will be a subfolder for each given 
strip that is further divided into subfolders for each part, as well as a "GIS_FILES" subfolder that contains vector shapefiles relevant to each strip. A manifest.json file is also produced cataloging the salient output files, which can be useful for identifying output files of interest. For example:

    ./vnir
    ./vnir/056459669040_01
    ./vnir/056459669040_01/056459669040_01_P001_PAN
    ./vnir/056459669040_01/056459669040_01_P001_PAN/14OCT07033342-P1BS-056459669040_01_P001.TIF
    ./vnir/056459669040_01/056459669040_01_P001_PAN/14OCT07033342-P1BS-056459669040_01_P001.IMD
    ./vnir/056459669040_01/056459669040_01_P001_MUL
    ./vnir/056459669040_01/056459669040_01_P001_MUL/14OCT07033342-M1BS-056459669040_01_P001.TIF
    ./vnir/056459669040_01/056459669040_01_P001_MUL/14OCT07033342-M1BS-056459669040_01_P001.IMD
    ./vnir/056459669040_01/GIS_FILES
    ./vnir/056459669040_01/GIS_FILES/056459669040_01_ORDER_SHAPE.dbf
    ./vnir/056459669040_01/GIS_FILES/056459669040_01_ORDER_SHAPE.prj
    ./vnir/056459669040_01/GIS_FILES/056459669040_01_ORDER_SHAPE.shp
    ./vnir/056459669040_01/GIS_FILES/056459669040_01_ORDER_SHAPE.shx
    ./vnir/056459669040_01/GIS_FILES/056459669040_01_PRODUCT_SHAPE.dbf
    ./vnir/056459669040_01/GIS_FILES/056459669040_01_PRODUCT_SHAPE.prj
    ./vnir/056459669040_01/GIS_FILES/056459669040_01_PRODUCT_SHAPE.shp
    ./vnir/056459669040_01/GIS_FILES/056459669040_01_PRODUCT_SHAPE.shx
    ./vnir/056459669040_01/GIS_FILES/056459669040_01_STRIP_SHAPE.dbf
    ./vnir/056459669040_01/GIS_FILES/056459669040_01_STRIP_SHAPE.prj
    ./vnir/056459669040_01/GIS_FILES/056459669040_01_STRIP_SHAPE.shp
    ./vnir/056459669040_01/GIS_FILES/056459669040_01_STRIP_SHAPE.shx
    ./vnir/056459669040_01/GIS_FILES/056459669040_01_TILE_SHAPE.dbf
    ./vnir/056459669040_01/GIS_FILES/056459669040_01_TILE_SHAPE.prj
    ./vnir/056459669040_01/GIS_FILES/056459669040_01_TILE_SHAPE.shp
    ./vnir/056459669040_01/GIS_FILES/056459669040_01_TILE_SHAPE.shx
    ./vnir/056459669040_01/GIS_FILES/14OCT07033342-M1BS-056459669040_01_P001_PIXEL_SHAPE.dbf
    ./vnir/056459669040_01/GIS_FILES/14OCT07033342-M1BS-056459669040_01_P001_PIXEL_SHAPE.prj
    ./vnir/056459669040_01/GIS_FILES/14OCT07033342-M1BS-056459669040_01_P001_PIXEL_SHAPE.shp
    ./vnir/056459669040_01/GIS_FILES/14OCT07033342-M1BS-056459669040_01_P001_PIXEL_SHAPE.shx
    ./vnir/056459669040_01/GIS_FILES/14OCT07033342-P1BS-056459669040_01_P001_PIXEL_SHAPE.dbf
    ./vnir/056459669040_01/GIS_FILES/14OCT07033342-P1BS-056459669040_01_P001_PIXEL_SHAPE.prj
    ./vnir/056459669040_01/GIS_FILES/14OCT07033342-P1BS-056459669040_01_P001_PIXEL_SHAPE.shp
    ./vnir/056459669040_01/GIS_FILES/14OCT07033342-P1BS-056459669040_01_P001_PIXEL_SHAPE.shx
    ./manifest.json


### Advanced
The following more complicated example performs orthorectification on associated VNIR and SWIR strips, 
processing only MS+SWIR (skipping PAN), and projects the output into the appropriate UTM zone. The desired MS and SWIR pixel pixel sizes are explicitly specified.

    swir_1b_s3_location = "s3://gbd-customer-data/CustomerAccount#/PathToVNIR1BImage/"
    vnir_1b_s3_location = "s3://gbd-customer-data/CustomerAccount#/PathToSWIR1BImage/"
   
    gbdx = Interface()
    
    ortho = gbdx.Task('orthorectify', data=vnir_1b_s3_location, swir=swir_1b_s3_location, 
                    bands = "Multi,All-S",    # Suppress PAN processing in orthorectify
                    epsg_code = "UTM", 
                    pixel_size_ms = "2.0",
                    pixel_size_swir = "7.5")

    workflow = gbdx.Workflow([ortho])
    workflow.savedata(ortho.outputs.data, location='ortho-output')
    workflow.execute()


### Runtime

The following table lists all applicable runtime outputs. (This section will be completed the Algorithm Curation team)
For details on the methods of testing the runtimes of the task visit the following link:(INSERT link to GBDX U page here)

  Sensor Name  | Total Pixels |  Total Area (k2)  |  Time(secs)  |  Time/Area k2
--------|:----------:|-----------|----------------|---------------
QB | 41,551,668 | 312.07 |  |  
WV01| 1,028,100,320 |351.72 | |
WV02|35,872,942|329.87| |
WV03|35,371,971|196.27| |
GE| 57,498,000|332.97| |

### Issues
Only DigitalGlobe 1B images are accepted as input.

### Contact
If you have any questions or issues with this task, please contact gbdx-support@digitalglobe.com .

