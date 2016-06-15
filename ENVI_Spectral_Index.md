# ENVI_Spectral_Index

ENVI_Spectral_Index. This task creates a spectral index raster from one pre-defined spectral index. Spectral indices are combinations of surface reflectance at two or more wavelengths that indicate relative abundance of features of interest. This task is used to compute a single index on a combination of multi spectral bands within an image. This task can be used to compute indices such as the Normalized Difference Vegetation Index (NDVI). An index such as NDVI will be passed into the task and a single band raster with the results of the index will be returned as output.
Note:  The wavelength metadata is not available in the correct format from the AOP task. Therefore this task is dependent on the "AOP_ENVI_HDR" task  

**Example Script:** Run in IPython using the GBDXTools Interface
	
    from gbdxtools import Interface
    gbdx = Interface()
    
    aop2envi = gbdx.Task("AOP_ENVI_HDR")
    aop2envi.inputs.image = 's3://gbd-customer-data/a157fdce-bb1d-42b3-96a9-66942896a787/denver_aop'
    
	envi_ndvi = gbdx.Task("ENVI_SpectralIndex")
    envi_ndvi.inputs.input_raster = aop2envi.outputs.output_data.value
    envi_ndvi.inputs.task_name = "SpectralIndex"
    envi_ndvi.inputs.file_types = "hdr"
    envi_ndvi.inputs.index = "Normalized Difference Vegetation Index"

    workflow = gbdx.Workflow([aop2envi, envi_ndvi])
    workflow.savedata(
       aop2envi.outputs.output_data,
       location='NDVI/output_data'
    )
    workflow.savedata(
       envi_ndvi.outputs.output_raster_uri,
       location='NDVI/output_raster_uri'
    )

    print workflow.execute()
	
	

**Description of Input Parameters and Options for the "ENVI_Spectral_Index":**
This task will work on Digital Globe images with a IMD file located in the S3 location: 
Input imagery sensor types include: QuickBird, WorldView 1, WorldView 2, WorldView 3 and GeoEye
	
**REQUIRED SETTINGS AND DEFINITIONS:**

* Define the index",
    * Required = true      
    * type = "string"
    * name =  "index"

* S3 location of input data (1B data will process by TIL or a strip run through AOP will be in TIF format):
    * Required = true
    * type = ‘directory’
    * name = ‘input_raster’

* Define the Output Directory: (a gbd-customer-data location)
    * Required = true
    * type = ‘directory’
    * name = "output_raster_uri_filename"


**OPTIONAL SETTINGS AND DEFINITIONS:**

* Define the File Types",
    * Required = false 
	* Description = specify file types as input (eg. hdr)
    * type = 'string'
    * name =  "file_types"

* Define the Output log Directory",
    * Required = false 
	* Description = Output location for task meta data such as execution log and output JSON
    * type = directory
    * name =  "task_meta_data"

###Postman status @ 13:07 6/15/16
  "completed_time": "2016-06-15T18:31:02.876281+00:00",
  "state": {
    "state": "complete",
    "event": "succeeded"
  },
  "submitted_time": "2016-06-15T18:08:16.235596+00:00",


**Data Structure for Expected Outputs:**

Your Processed Imagery will be written to the specified S3 Customer Location in a 1 band TIF format(e.g.  s3://gbd-customer-data/unique customer id/named directory/).  


For background on the development and implementation of Spectral Index refer to the [ENVI Documentation](https://www.harrisgeospatial.com/docs/spectralindices.html)

