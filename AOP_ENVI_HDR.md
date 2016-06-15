# AOP output to ENVI HDR 

**AOP_ENVI_HDR** This task builds an ENVI .hdr file for each .tif file found in a folder. This task is used to pass wavelength metadata into .hdr format for use in subsequent tasks, such as "ENVI_Spatial_Index".  Currently the .hdr file will only explain wavelength metadata, but additional metadata will be added with updated versions.  
**Example Script:** Run in IPython using the GBDXTools Interface
	
    from gbdxtools import Interface
    gbdx = Interface()
    
    aop2envi = gbdx.Task("AOP_ENVI_HDR")
    aop2envi.inputs.image = 's3://receiving-dgcs-tdgplatform-com/055249130010_01_003'
    
    workflow = gbdx.Workflow([aop2envi])
    workflow.savedata(
       aop2envi.outputs.output_data,
       location='aop2envi_test1/output_data'
    )
    
    print workflow.execute()
	
	
**Description of Input Parameters and Options for the**** "AOP_ENVI_HDR":**

This task will function on Digital Globe images with an XML or IMD file located in the S3 location.  The input imagery may be either an AOP output folder or an order in 1B image format.
Input imagery sensor types include: QuickBird, WorldView 1, WorldView 2, WorldView 3 and GeoEye

**REQUIRED SETTINGS AND DEFINITIONS:**

* S3 location of input data (1B data will process by TIL or a strip run through AOP will be in TIF format):
    * Required = ‘True’
    * type = ‘directory’
    * name = ‘image’
    
* Define the Task:
    * Required = ‘True’
    * envitask = gbdx.Task("AOP_ENVI_HDR")

* Define the Output Directory: (a gbd-customer-data location)
    * Required = ‘true’
    * type = ‘directory’
	* description = The original AOP image data with the ENVI .hdr file
    * name = "output_data"
	
**OPTIONAL SETTINGS: Required = False**
Currently additional options for this task are not available.  Updates to this task may provide options to add various metadata attributes to the .hdr file.  

**Sample Output: Test Run 4/27/16, On R&D Cluster**

  
###Postman status @ 16:22 6/14/16
completed_time": null,
  "state": {
    "state": "complete",
    "event": "succeeded"
  },
  "submitted_time": "2016-06-15T17:09:34.572641+00:00",
 

**Data Structure for Expected Outputs:**

Your processed imagery will be written to the specified S3 Customer Location in TIF format as well as the ENVI format (e.g. s3://gbd-customer-data/unique customer id/named directory/Image.tif).  


For background on the development and implementation of geoIO and this task, please refer to the GitHub documentation [Adding geoIO Documentation](https://github.com/TDG-Platform/docs)

