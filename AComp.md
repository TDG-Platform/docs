# AComp (DG Atmospheric Compensation)

The AComp GBDX task performs atmospheric compensation on
satellite imagery collected from DigitalGlobe sensors as well as other sources. Atmospheric compensation is the process
of converting image Digital Number (DN) counts to surface reflectance. This removes:

* Variation due to different illumination conditions
* Variation due to different viewing geometries
* Atmospheric effects

The AComp GBDX task operates on imagery from Landsat-8 and all DG Sensors (except WorldView-1).  Input imagery must at least contain the VNIR multispectral bands, and optionally may also include panchromatic data and/or SWIR data.

### Table of Contents
 * [Quickstart](#quickstart) - Get started!
 * [Inputs](#inputs) - Required and optional task inputs.
 * [Outputs](#outputs) - Task outputs and example contents.
 * [Advanced Options](#advanced-options) - Examples linking to a second task and running VNIR+SWIR
 * [Known Issues](#known-issues)

### Quickstart

The AComp GBDX task can be run through a simple Python script using  [gbdxtools](https://github.com/DigitalGlobe/gbdxtools/blob/master/docs/user_guide.rst), which requires some initial setup, or through the [GBDX Web Application](https://gbdx.geobigdata.io/materials/).  Tasks and workflows can be added (described here in [gbdxtools](https://github.com/DigitalGlobe/gbdxtools/blob/master/docs/running_workflows.rst)) or run separately after the AComp process is completed.

**Example Script:** These basic settings will run AComp on a Landsat-8 image.  See also examples listed under the [Advanced Options](#advanced-options).

```python
    # Run Atmospheric Compensation (AComp) on Landsat-8 data
    from gbdxtools import Interface
    gbdx = Interface()

    # The data input and lines must be edited to point to an authorized customer S3 location)
    acomp = gbdx.Task('AComp', data='s3://gbd-customer-data/CustomerAccount#/PathToImage/')
    workflow = gbdx.Workflow([acomp])
    #Edit the following line(s) to reflect specific folder(s) for the output file (example location provided)
    workflow.savedata(acomp.outputs.data, location='S3 gbd-customer-data location/<customer account>/output directory')
    workflow.execute()

    print workflow.id
    print workflow.status
```

**Example Run in IPython:**

    In [1]: from gbdxtools import Interface
    In [2]: gbdx = Interface()
    2016-06-06 10:53:09,026 - gbdxtools - INFO - Logger initialized
    In [3]: acomp = gbdx.Task('AComp', data='s3://landsat-pds/<Landsat8 Image ID>')
    In [4]: workflow = gbdx.Workflow([acomp])
    In [5]: workflow.savedata(acomp.outputs.data, location='S3 gbd-customer-data location/<customer account>/output directory')
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
   Landsat-8  | LC80330322015035LGN00    |s3://landsat-pds/L8/033/032/LC80330322015035LGN00

### Inputs

To use this task, set the "data" input parameter (described below) to point at an S3 bucket containing the image data to process. Note, that this task will search through the given bucket to locate the input data and process the data it finds. In order to process VNIR or VNIR + PAN data, simply point the "data" input parameter at the directory within the bucket containing the VNIR or VNIR + PAN data for a single catalog ID.

If SWIR data is to also be processed, the workflow is slightly different. A summary follows here, but refer to [Advanced Options](#advanced-options) for examples. Since SWIR data is normally ordered separately from VNIR in GBDX and therefore has a different catalog ID, in order to process VNIR+SWIR or VNIR+PAN+SWIR, it is necessary to point the "data" input parameter at a parent directory containing both a single VNIR (or VNIR+PAN) catalog ID directory and also a single corresponding SWIR catalog ID directory. Note that the SWIR data must intersect the VNIR data and be "acquired during the same overpass" in order to obtain valid results. SWIR data acquired during the same overpass will have a catalog ID that is differentiated from the VNIR catalog ID solely by having an "A" in the 4th position of the catalog ID. For example, the SWIR catalog ID 104A010008437000 was acquired during the same overpass as the the VNIR catalog ID 1040010008437000.  Please [Contact Us](#contact-us) if you would like us to stage a VNIR+SWIR test dataset for you.

**Description of Input Parameters and Options for the AComp GBDX task**

The following table lists the AComp-GBDX inputs. All inputs are optional with default values, with the exception of 'data' which specifies the task's input data location and output data location.

Name                     |       Default         |        Valid Values             |   Description
-------------------------|:---------------------:|---------------------------------|-----------------
data (in)      |   N/A   | S3 URL                                | S3 location of input data.
data (out)     |   N/A   | S3 URL                                | S3 gbd-customer-data location
exclude_bands  |   Off	 |  'P', 'MS1', 'Multi', 'All-S'         | Comma-separated list of bands to exclude; excluded bands are not processed.
bit_depth      |   16    |  11, 16 or 32                         | Bit depth refers to how many digits the spectral information for each pixel is stored in



**Script Example specifying exclusion of panchromatic bands**

	acomp = gbdx.Task('AComp', exclude_bands='P')

**Script Example specifying alternate bit depth**

	acomp = gbdx.Task('AComp', data=data, bit_depth=32 )

### Outputs

On completion, the processed imagery will be written to your specified S3 Customer Location (e.g.  s3://gbd-customer-data/unique customer id/named directory/).   The AComp output files will be located Within the 'named directory'. The specific layout and names of the output files will depend on the specific input files and the options selected.

**Description of Output Files**

Data Input Type          | Description of Output Files  | Runs FastOrtho to produce Final Output
-------------------------|:------------------------------|------------------------------
Landsat-8                | .TIF                          |  NO   (individual .tif files)
DG Sensors Level 1B      | .TIF, .IMD                    |  YES  (single mosaic .tif)
DG Sensors Level 2 and Level 3 |  .TIF, .TIL, .IMD       |  NO   (individual .tif files)


[Contact Us](#contact-us) If your Customer has questions regarding required inputs, expected outputs and [Advanced Options](advanced-options).

### Advanced Options

#### Running AComp on VNIR+SWIR Imagery from WorldView-3

First the VNIR and SWIR images must be staged to the same parent directory.  An example is given below as a reminder.

```python
	from gbdxtools import Interface
	gbdx = Interface()

	# Stage VNIR and SWIR in the same parent directory
	destination = 's3://gbd-customer-data/<customer account>/your designated parent directory'
	s3task2 = gbdx.Task("StageDataToS3", data='s3://receiving-dgcs-tdgplatform-com/<file directory>', destination=destination) # VNIR image
	s3task2 = gbdx.Task("StageDataToS3", data='s3://receiving-dgcs-tdgplatform-com/<file directory>', destination=destination) # SWIR image)
	workflow = gbdx.Workflow([ s3task1, s3task2 ])
	workflow.execute()

	print workflow.id
	print workflow.status
```

These tasks can be combined, but it works best to stage the data first in a separate task to make sure the imagery has been completely copied before starting the AComp task.

Script Example running AComp on VNIR+SWIR:

```python
	# Runs AComp on corresponding VNIR and SWIR images from WorldView-3
	from gbdxtools import Interface
	gbdx = Interface()

	# Setup AComp Task
	# The data input and output lines must be edited to point to an authorized customer S3 location)
	acompTask = gbdx.Task('AComp', data='s3://gbd-customer-data/CustomerAccount#/PathToImage/')

	# Run AComp Workflow
	workflow = gbdx.Workflow([ acompTask ])
  #Edit the following line(s) to reflect specific folder(s) for the output file (example location provided)
	workflow.savedata(acompTask.outputs.data, location='Acomp/')
	workflow.execute()

	print workflow.id
	print workflow.status
```

[Script Example running AComp on Level 3D Imagery:](#known-issues)

```python
	# Runs AComp on Level 3D images
	# Test Imagery is WV03 Jefferson County, CO - Elk Meadow Park
	from gbdxtools import Interface
	gbdx = Interface()

	# Setup AComp Task; requires full path to input dataset
	# The data input and output lines must be edited to point to an authorized customer S3 location)
	acompTask = gbdx.Task('AComp', data='S3 gbd-customer-data location/<customer account>/input directory')

	# Run Workflow
	workflow = gbdx.Workflow([ acompTask ])
	workflow.savedata(acompTask.outputs.data, location='S3 gbd-customer-data location/<customer account>/output directory')
	workflow.execute()

	print workflow.id
	print workflow.status
```


Script Example linking AComp to [protogenV2LULC](https://github.com/TDG-Platform/docs/blob/master/protogenV2LULC.md):

```python
	# Runs AComp, then sends that data to the protogenV2LULC process
	from gbdxtools import Interface
	gbdx = Interface()

	# Setup AComp Task
	# The data input and output lines must be edited to point to an authorized customer S3 location)
	acompTask = gbdx.Task('AComp', exclude_bands='P', data='s3://gbd-customer-data/CustomerAccount#/PathToImage/')

	# Stage AComp output for the Protogen Task
	pp_task = gbdx.Task("ProtogenPrep",raster=acompTask.outputs.data.value)    

	# Setup ProtogenV2LULC Task
	prot_lulc = gbdx.Task("protogenV2LULC",raster=pp_task.outputs.data.value)

	# Run Combined Workflow
	workflow = gbdx.Workflow([ acompTask, pp_task, prot_lulc ])
 	#Edit the following line(s) to reflect specific folder(s) for the output file (example location provided)
	workflow.savedata(prot_lulc.outputs.data, location='ProtogenLULC/')
	workflow.execute()

	print workflow.id
	print workflow.status
```


### Runtime

The following table lists all applicable runtime outputs.
For details on the methods of testing the runtimes of the task visit the following link:(INSERT link to GBDX U page here)

  Sensor Name  |  Total Pixels  |  Total Area (k2)  |  Time(secs)  |  Time/Area k2
--------|:----------:|-----------|----------------|---------------
WV02|35,872,942|329.87| 591.909 | 1.79 |
WV03|35,371,971|196.27| 390.332 | 1.99 |
GE01| 57,498,000|332.97| 507.664 | 1.52 |
QB02 | 41,551,668 | 312.07 | 395.610  | 1.27  |




###Known Issues

Processing Level 2 or Level 3 imagery will require you to order the imagery outside the platform and upload it to your S3-customer location.

AComp currently does not run end-to-end with ENVI Tasks.

### Contact Us
Tech Owners: [Fabio Pacifici](#fpacific@digitalglobe.com), [Alex Comer](#acomer@digitalglobe.com) & Editor:  [Kathleen Johnson](#kathleen.johnsons@digitalglobe.com)
