# AComp 1.0

The AComp GBDX task performs atmospheric compensation on 
satellite imagery collected from DigitalGlobe sensors as well as other sources. Atmospheric compensation is the process 
of converting image Digital Number (DN) counts to surface reflectance. This removes:

* Variation due to different illumination conditions
* Variation due to different viewing geometries
* Atmospheric effects

The AComp GBDX task operates on a variety of input imagery types:

* DG Level 1B (orthorectification is automatically applied first)
* DG Level 2 ([requires special handling](#known-issues))
* DG Level 3 ([requires special handling](#known-issues))
* Landsat8 images

Input imagery must at least contain the VNIR multispectral bands, and optionally may also include panchromatic and/or SWIR data.

### Table of Contents
 * [Quickstart](#quickstart) - Get started!
 * [Inputs](#inputs) - Required and optional task inputs.
 * [Outputs](#outputs) - Task outputs and example contents.
 * [Advanced Options](#advanced-options) - Examples linking to a second task and running VNIR+SWIR
 * [Known Issues](#known-issues)

### Quickstart

The AComp GBDX task can be run through a simple Python script using  [gbdxtools](https://github.com/DigitalGlobe/gbdxtools/blob/master/docs/user_guide.rst), which requires some initial setup, or through the [GBDX Web Application](https://gbdx.geobigdata.io/materials/).  Tasks and workflows can be added (described here in [gbdxtools](https://github.com/DigitalGlobe/gbdxtools/blob/master/docs/running_workflows.rst)) or run separately after the AComp process is completed.

**Example Script:** These basic settings will run AComp on a Landsat8 image.  See also examples listed under the [Advanced Options](#advanced-options).

    # Run atmospheric compensation on Landsat8 data
    from gbdxtools import Interface
    gbdx = Interface()
    import json
    acomp = gbdx.Task('AComp_1.0', data='s3://landsat-pds/L8/033/032/LC80330322015035LGN00')
    workflow = gbdx.Workflow([acomp])
    workflow.savedata(acomp.outputs.data, location='S3 gbd-customer-data location')
    workflow.execute()
           
    print workflow.id
    print workflow.status
     
**Example Run in IPython:**

    In [1]: from gbdxtools import Interface
    In [2]: gbdx = Interface()
    2016-06-06 10:53:09,026 - gbdxtools - INFO - Logger initialized
    In [3]: acomp = gbdx.Task('AComp_1.0', data='s3://landsat-pds/L8/033/032/LC80330322015035LGN00')
    In [4]: workflow = gbdx.Workflow([acomp])
    In [5]: workflow.savedata(acomp.outputs.data, location='S3 gbd-customer-data location')
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
task will search through the given bucket to locate the input data and process the data it finds. In order to process VNIR or VNIR + PAN data, simply point the "data" input parameter at the directory within the bucket containing the VNIR or VNIR + PAN data for a single catalog ID. 

If SWIR data is to also be processed, the workflow is slightly different. A summary follows here, but refer to [Advanced Options](#advanced-options) for examples. Since SWIR data is normally ordered separately from VNIR in GBDX and therefore has a different catalog ID, in order to process VNIR+SWIR or VNIR+PAN+SWIR, it is necessary to point the "data" input parameter at a parent directory containing both a single VNIR (or VNIR+PAN) catalog ID directory and also a single corresponding SWIR catalog ID directory. Note that the SWIR data must intersect the VNIR data and be "acquired during the same overpass" in order to obtain valid results. SWIR data acquired during the same overpass will have a catalog ID that is differentiated from the VNIR catalog ID solely by having an "A" in the 4th position of the catalog ID. For example, the SWIR catalog ID 104A010008437000 was acquired during the same overpass as the the VNIR catalog ID 1040010008437000.

**Description of Input Parameters and Options for the AComp GBDX task**

The following table lists the AComp-GBDX inputs. All inputs are optional with default values, with the exception of 'data' which specifies the task's input data location and output data location.

Name                     |       Default         |        Valid Values             |   Description
-------------------------|:---------------------:|---------------------------------|-----------------
data (in)      |   N/A   | S3 URL                                | S3 location of input data.
data (out)     |   N/A   | S3 URL                                | S3 gbd-customer-data location
exclude_bands  |   Off	 |  'P', 'MS1', 'Multi', 'All-S'         | Comma-separated list of bands to exclude; excluded bands are not processed. 
bit_depth      |   16    |  11, 16 or 32                         | Bit depth refers to how many digits the spectral information for each pixel is stored in



**Script Example specifying exclusion of panchromatic bands**

	acomp = gbdx.Task('AComp_1.0', exclude_bands='P')

**Script Example specifying alternate bit depth**

	acomp = gbdx.Task('AComp_1.0', data=data, bit_depth=32 )

### Outputs

On completion, the processed imagery will be written to your specified S3 Customer Location (e.g.  s3://gbd-customer-data/unique customer id/named directory/).   The AComp output files will be located Within the 'named directory'. The specific layout and names of the output files will depend on the specific input files and the options selected. 

[Contact Us](#contact-us) If your Customer has questions regarding required inputs, expected outputs and Advanced Options.

### Advanced Options


[Script Example running AComp on Level 3D Imagery:](#known-issues)

	# Runs AComp_1.0 on Level 3D images
	# Test Imagery is WV03 Jefferson County, CO - Elk Meadow Park
	from gbdxtools import Interface 
	import json
	gbdx = Interface()

	# Setup AComp Task; requires full path to input dataset
	acompTask = gbdx.Task('AComp_1.0', data='S3 gbd-customer-data location-input')

	# Run Workflow
	workflow = gbdx.Workflow([ acompTask ])
	workflow.savedata(acompTask.outputs.data.value, location='S3 gbd-customer-data location-output')
	workflow.execute()

	print workflow.id
	print workflow.status



Script Example running AComp on VNIR+SWIR:

	# Runs AComp_1.0 on corresponding VNIR and SWIR images
	# Test Imagery is WV03 VNIR+SWIR for the NorCal AOI
	from gbdxtools import Interface 
	import json
	gbdx = Interface()

	# Stage VNIR and SWIR in the same parent directory
	destination = 's3://gbd-customer-data/7d8cfdb6-13ee-4a2a-bf7e-0aff4795d927/kathleen_AComp3'
	s3task1 = gbdx.Task("StageDataToS3", data='s3://receiving-dgcs-tdgplatform-com/055427378010_01_003', destination=destination) # VNIR image
	s3task2 = gbdx.Task("StageDataToS3", data='s3://receiving-dgcs-tdgplatform-com/055486759010_01_003', destination=destination) # SWIR image)
	workflow = gbdx.Workflow([ s3task1, s3task2 ]) # needs to excute and complete this workflow first

	# Setup AComp Task
	acompTask = gbdx.Task('AComp_1.0', data='s3://receiving-dgcs-tdgplatform-com/s3task_output')

	# Run AComp Workflow
	workflow = gbdx.Workflow([ acompTask ])
	workflow.savedata(acompTask.outputs.data.value, location='S3 gbd-customer-data location--')
	workflow.execute()

	print workflow.id
	print workflow.status



Script Example linking AComp to [protogenV2LULC](https://github.com/TDG-Platform/docs/blob/master/protogenV2LULC.md):

	# Runs AComp_1.0, then sends that data to the protogenV2LULC process
	from gbdxtools import Interface 
	import json
	gbdx = Interface()
	
	# Test Imagery for Tracy, CA: WV02
	# Setup AComp Task
	acompTask = gbdx.Task('AComp_1.0', exclude_bands='P', data='s3://receiving-dgcs-tdgplatform-com/055168976010_01_003')

	# Stage AComp output for the Protogen Task
	pp_task = gbdx.Task("ProtogenPrep",raster=acompTask.outputs.data.value)    
	
	# Setup ProtogenV2LULC Task
	prot_lulc = gbdx.Task("protogenV2LULC",raster=pp_task.outputs.data.value)

	# Run Combined Workflow
	workflow = gbdx.Workflow([ acompTask, pp_task, prot_lulc ])
	workflow.savedata(prot_lulc.outputs.data.value, location='S3 gbd-customer-data location')
	workflow.execute()
	
	print workflow.id
	print workflow.status



###Known Issues

*Processing Level 2 or Level 3 imagery  will require you to order the imagery outside the platform and upload it to your S3-customer location.

*AComp_1.0 currently does not run end-to-end with ENVI Tasks.  A "glueTask" to link these processes is under development.

*There may be alignment problems between VNIR and SWIR output.  A resolution to this problem is expected soon.  In the meantime, if you encounter a problem, please contact us.


### Contact Us
Tech Owners: [Fabio Pacifici](#fpacific@digitalglobe.com), [Alex Comer](#acomer@digitalglobe.com) & Editor:  [Kathleen Johnson](#kathleen.johnsons@digitalglobe.com)

