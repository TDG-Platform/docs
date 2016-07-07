# ENVI RX Anomaly Detection 

RX Anomaly Detection This task uses the Reed-Xiaoli Detector (RXD) algorithm to identify the spectral or color differences between a region to test its neighboring pixels or the entire dataset.
**Example Script:** Run in IPython using the GBDXTools Interface
	
    from gbdxtools import Interface 
    import json
    gbdx = Interface()
       
    # launch workflow ENVI_RXAnomalyDetection -> S3
    #example data WV02 image of Denver previously processed with AOP strip processor 
	data = "s3://gbd-customer-data/7d8cfdb6-13ee-4a2a-bf7e-0aff4795d927/ENVI/Denver/055026839010_01/055026839010_01_assembly.tif"
	 
	envitask = gbdx.Task("ENVI_RXAnomalyDetection")
	envitask.inputs.task_name='RXAnomalyDetection'
	envitask.inputs.file_types='til'
	envitask.inputs.kernel_size='3'
    envitask.inputs.input_raster=data
	
	workflow = gbdx.Workflow([ envitask ] )
	workflow.savedata(envitask.outputs.task_meta_data, location='envi_task_output')
	workflow.savedata(envitask.outputs.output_raster_uri, location='envi_task_output')
	
	print workflow.execute()
	
	

**Description of Input Parameters and Options for the**** "RXAnomalyDetection":**

**REQUIRED SETTINGS AND DEFINITIONS:**

* S3 location of input data (1B data will process by TIL or a strip run through AOP will be in TIF format):
    * Required = ‘True’
    * type = ‘directory’
    * name = ‘data’
    
* Define the ENVI Task:
    * Required = ‘True’
    * envitask = gbdx.Task("ENVI_RXAnomalyDetection")

* Define the Output Directory: (a gbd-customer-data location)
    * Required = ‘true’
    * type = ‘directory’
    * name = "destination"
* Define the Output log Directory",
    * Required = true      
    * type = directory
    * name =  "log"

* Define Stage to S3 location:
    * S3task = gbdx.Task("StageDataToS3",“data=” ”,destination=”)

**OPTIONAL SETTINGS: Required = False**

**_The Default setting does not run the specified process. Some of these processes (e.g. "enable_tiling" = “True”) may have dependencies that also require resetting. Some of the dependencies have “Auto” settings.**

* Comma-separated list of file type extensions, use this to filter input files 
    * Required = ‘false’
    * type = ‘string’
    * name = ‘file_types’
* Set this property to true to suppress vegetation anomalies in the RXD results. The options are true or false (default). 
    * Default = 'false'
    * Required = ‘false’
    * type = ‘string’
    * name = ‘suppress_vegetation’
* Select the mean calculation method:  Specify one of the values from the CHOICE_LIST, indicating which mean calculation method to use.  Global: Derive the mean spectrum from the full dataset, Local: Derive the mean spectrum from the **KERNEL\_SIZE** around a given pixel.
    * Required = ‘false’
    * type = ‘string’
    * name = ‘mean\_calculation_method’
* Select the RXD method to use.  Specify one of the values from the CHOICE_LIST, indicating which method to use. RXD: Standard RXD algorithm, UTD: Uniform Target Detector algorithm, RXD-UTD: Hybrid of the RXD and UTD algorithms.

    * Required = ‘false’
    * type = ‘string’
    * name = ‘anomaly\_detection_method’
	
 •	Select the kernel size for the analysis. Specify the kernel size in pixels, around a given pixel that will be used to create a mean spectrum.  Use an odd number. The minimum value is 3, and the maximum value is (number of columns - 1) less than (number of rows - 1).  Specify **KERNEL_SIZE** only when using the 'Local' option for **MEAN\_CALCULATION_METHOD.**

    * Default is 3
    * Required = ‘false’
    * type = ‘string’
    * name = ‘kernel_size’
	
 •	Select the kernel size for the analysis. Specify the kernel size in pixels, around a given pixel that will be used to create a mean spectrum.  Use an odd number. The minimum value is 3, and the maximum value is (number of columns - 1) less than (number of rows - 1).  Specify KERNEL_SIZE only when using the 'Local' option for **MEAN\_CALCULATION\_METHOD.**

    * Required = ‘false’
    * type = ‘directory’
    * name = ‘task\_meta_data’


**Sample Output: Test Run 4/27/16, On R&D Cluster**

    [3]: envitask = gbdx.Task("ENVI_RXAnomalyDetection")
    [4]: envitask.inputs.task_name='RXAnomalyDetection'
    [5]: envitask.inputs.file_types='til'
    [6]: envitask.inputs.kernel_size='3'
    [7]: data = "s3://receiving-dgcs-tdgplatform-com/054813633050_01_003/054813633050_01/054813633050_01_P001_MUL/"
    [8]: envitask.inputs.input_raster=data
    [9]: workflow = gbdx.Workflow([ envitask ] )
    [10]: workflow.savedata(envitask.outputs.task_meta_data, location=' s3://gbd-customer-data/7d8cfdb6-13ee-4a2a-bf7e-0aff4795d927/ENVI/')
    [11]: workflow.savedata(envitask.outputs.output_raster_uri, location=' s3://gbd-customer-data/7d8cfdb6-13ee-4a2a-bf7e-0aff4795d927/ENVI/')
    [12]: print workflow.execute()
     
    4320185934977513853 



###Postman status @ 16:22 4/27/16
   "completed_time": null,
   "state": {
    "state": "complete",
    "event": "succeeded"
  },
  "submitted_time": "2016-04-27T17:46:54.537965+00:00",




**Data Structure for Expected Outputs:**

Your Processed Imagery will be written to the specified S3 Customer Location in a 1 band TIF format(e.g.  s3://gbd-customer-data/unique customer id/named directory/).  


For background on the development and implementation of RX Anomaly Detection refer to the [ENVI Documentation](https://www.harrisgeospatial.com/docs/rxanomalydetection.html)

