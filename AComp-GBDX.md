# AComp GBDX task

The AComp GBDX task performs atmospheric compensation on 
satellite imagery collected from DigitalGlobe sensors as well as other sources. Atmospheric compensation is the process 
of converting image Digital Number (DN) counts to surface reflectance. This removes:

* Variation due to different illumination conditions
* Variation due to different viewing geometries
* Atmospheric effects

The AComp GBDX task operates on a variety of input data:

* DG Level 2A images
* DG Level 1B images (orthorectification is automatically applied first)
* Landsat8 images

Input imagery must at least contain the VNIR multispectral bands, and optionally may also include panchromatic and/or SWIR data.

### Table of Contents
 * [Quickstart](#quickstart) - Get started!
 * [Inputs](#inputs) - Required and optional task inputs.
 * [Outputs](#outputs) - Task outputs and example contents.
 * [Advanced Options](#advanced-options) - Additional information for advanced users.

### Quickstart

The AComp GBDX task can be run through a simple Python script using  [gbdxtools](https://github.com/DigitalGlobe/gbdxtools/blob/master/docs/user_guide.rst), which requires some initial setup, or through the [GBDX Web Application](https://gbdx.geobigdata.io/materials/).  Tasks and workflows can be added (described here in [gbdxtools](https://github.com/DigitalGlobe/gbdxtools/blob/master/docs/running_workflows.rst)) or run separately after the AComp process is completed.

**Example Script:** These basic settings will run AComp on a Landsat8 image.  See also examples listed under the [Advanced Options](#advanced-options).

    # Run atmospheric compensation on Landsat8 data
    from gbdxtools import Interface
    gbdx = Interface()
    import json
    acomp = gbdx.Task('AComp_0.23.2.1', data='s3://landsat-pds/L8/033/032/LC80330322015035LGN00')
    workflow = gbdx.Workflow([acomp])
    workflow.savedata(acomp.outputs.data, location='acomp_output_folder')
    workflow.execute()
           
    print workflow.id
    print workflow.status
     
**Example Run in IPython:**

    In [1]: from gbdxtools import Interface
    In [2]: gbdx = Interface()
    2016-06-06 10:53:09,026 - gbdxtools - INFO - Logger initialized
    In [3]: acomp = gbdx.Task('AComp_0.23.2.1', data='s3://landsat-pds/L8/033/032/LC80330322015035LGN00')
    In [4]: workflow = gbdx.Workflow([acomp])
    In [5]: workflow.savedata(acomp.outputs.data, location='acomp_output_folder')
    In [6]: workflow.execute()
    Out[6]: u'4349739083145886153'
    In [7]: print workflow.id
    4349739083145886153
    In [8]: print workflow.status
    2016-06-06 10:53:41,301 - gbdxtools - DEBUG - Get status of workflow: 4349739083145886153
    {u'state': u'pending', u'event': u'submitted'}
    In [9]:

**Test Datasets for Tracy, California**

  Sensor |  Catalog ID      | S3 URL
:-------:|:----------------:|--------
   WV02  |  10400100076AB300  |  s3://receiving-dgcs-tdgplatform-com/055168976010_01_003
   WV03  | 10400100076AB300 | s3://receiving-dgcs-tdgplatform-com/055442993010_01_003
   GE01  |  1050410013233600  |  s3://receiving-dgcs-tdgplatform-com/055385387010_01_003
   QB02  |  101001000B3E9F00  |  s3://receiving-dgcs-tdgplatform-com/055168847010_01_003
   
   
   

### Inputs

To use this task, set the "data" input parameter (described below) to point at an S3 bucket containing the image data to process. Note that this
task will search through the given bucket to locate the input data and process the data it finds. In order to process VNIR or VNIR + PAN data, simply point the "data" input parameter at the directory within the bucket containing the VNIR or VNIR + PAN data for a single catalog ID. If SWIR data is to also be processed, the process is slightly different. Since SWIR data is normally ordered separately from VNIR in GBDX and therefore has a different catalog ID, in order to process VNIR+SWIR or VNIR+PAN+SWIR, it is necessary to point the "data" input parameter at a parent directory containing both a single VNIR (or VNIR+PAN) catalog ID directory and also a single corresponding SWIR catalog ID directory. Note that the SWIR data must intersect the VNIR data and be "acquired during the same overpass" in order to obtain valid results. SWIR data acquired during the same overpass will have a catalog ID that is differentiated from the VNIR catalog ID solely by having an "A" in the 4th position of the catalog ID. For example, the SWIR catalog ID 104A010008437000 was acquired during the same overpass as the the VNIR catalog ID 1040010008437000.



**Description of Input Parameters and Options for the AComp GBDX task**

The following table lists the AComp-GBDX inputs. All inputs are optional with default values, with the exception of 'data' which specifies the task's input data location and output data location.

Name                     |       Default         |        Valid Values             |   Description
-------------------------|:---------------------:|---------------------------------|-----------------
data (in)      |   N/A   | S3 URL                                | S3 location of 1B input data.
data (out)     |   N/A   | S3 URL                                | S3 gbd-customer-data location
exclude_bands  |   Off	 |  'P', 'MS1', 'Multi', 'All-S'         | Comma-separated list of bands to exclude; excluded bands are not processed. 
bit_depth      |   16    |  16 or 32                             |


### Outputs

On completion, the processed imagery will be written to your specified S3 Customer Location (e.g.  s3://gbd-customer-data/unique customer id/named directory/).   The AComp output files will be located Within the 'named directory'. The specific layout and names of the output files will depend on the specific input files and the options selected. 


### Advanced Options


**Script Example specifying alternate AOD grid size and bit depth**

	acomp = gbdx.Task('AComp_0.23.2.1', data=data, aod_grid_size=15, bit_depth=32 )



