# AComp GBDX task

The AComp GBDX task performs atmospheric compensation on 
satellite imagery collected from DitialGlobe sensors as well as other sources. Atmospheric compensation is the process 
of converting image Digital Number (DN) counts to surface reflectance. This removes:

* Variation due to different illumination conditions
* Variation due to different viewing geometries
* Atmospheric effects

The AComp GBDX task operates on a variety of input data:

* DG Level 2A images
* DG Level 1B images (orthorectification is automatically applied first)
* Landsat8 images

Input imagery must at least contain the VNIR multispectral bands, and optionally may also include panchromatic and/or SWIR data.

To use this task, set the "data" input parameter (described below) to point at an S3 bucket containing the image data to process. Note that this
task will search through the given bucket to locate the input data and process the data it finds. In order to process VNIR or VNIR + PAN data, simply point the "data" input parameter at the directory within the bucket containing the VNIR or VNIR + PAN data for a single catalog ID. If SWIR data is to also be processed, the process is slightly different. Since SWIR data is normally ordered separately from VNIR in GBDX and therefore has a different catalog ID, in order to process VNIR+SWIR or VNIR+PAN+SWIR, it is necessary to point the "data" input parameter at a parent directory containing both a single VNIR (or VNIR+PAN) catalog ID directory and also a single corresponding SWIR catalog ID directory. Note that the SWIR data must intersect the VNIR data and be "acquired during the same overpass" in order to obtain valid results. SWIR data acquired during the same overpass will have a catalog ID that is differentiated from the VNIR catalog ID solely by having an "A" in the 4th position of the catalog ID. For example, the SWIR catalog ID 104A010008437000 was acquired during the same overpass as the the VNIR catalog ID 1040010008437000.

The AComp GBDX task can be run through a simple Python script using  [gbdxtools](https://github.com/DigitalGlobe/gbdxtools/blob/master/docs/user_guide.rst), which requires some initial setup, or through the [GBDX Web Application](https://gbdx.geobigdata.io/materials/).  Tasks and workflows can be added (described here in [gbdxtools](https://github.com/DigitalGlobe/gbdxtools/blob/master/docs/running_workflows.rst)) or run separately after the AComp process is completed.

**Example Script:** These basic settings will run AComp on a Landsat8 image.  See also examples listed under the optional settings below.

    # Run atmospheric compensation on Landsat8 data
    from gbdxtools import Interface
    gbdx = Interface()
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


**Description of Input Parameters and Options for the AComp GBDX task**

**REQUIRED SETTINGS AND DEFINITIONS:**

* S3 location of input data:
    * Required = 'True'
    * type = 'directory'
    * name = 'data'
    
* Define the Output Directory: (a gbd-customer-data location)
    * Required = 'true'
    * type = 'directory'
    * name = 'data'

**OPTIONAL SETTINGS:**

* Comma-separated list of bands to exclude. Use band IDs from IMD file such as 'P', 'MS1', 'Multi', 'All-S', etc. Excluded bands are not processed. 
    * Required = 'false'
    * type = 'string'
    * name = 'exclude_bands'

* AOD grid size in meters per pixel. Default is 10. 
    * Default = '10'
    * Required = 'false'
    * Type = 'string'
    * name = 'aod_grid_size'

* Output bit depth. Choices are 16 or 32. Default is 16.
    * Default = '16'
    * Required = 'false'
    * type = 'string'
    * name = 'bit_depth'

**Script Example specifying alternate AOD grid size and bit depth**

	acomp = gbdx.Task('AComp_0.23.2.1', data=data, aod_grid_size=15, bit_depth=32 )


**Expected Outputs:**

On completion, the processed imagery will be written to your specified S3 Customer Location (e.g.  s3://gbd-customer-data/unique customer id/named directory/).   The AComp output files will be located Within the 'named directory'. The specific layout and names of the output files will depend on the specific input files and the options selected. 
