# ENVI RX Anomaly Detection (ENVI_RXAnomalyDetection)

This task uses the Reed-Xiaoli Detector (RXD) algorithm to identify the spectral or color differences between a region to test its neighbouring pixels or the entire dataset.

### Table of Contents
 * [Quickstart](#quickstart) - Get started!
 * [Inputs](#inputs) - Required and optional task inputs.
 * [Outputs](#outputs) - Task outputs and example contents.
 * [Advanced](#advanced) - Additional information for advanced users.
 * [Known Issues](#known-issues) - current or past issues known to exist.

### Quickstart

**Example Script:** Run in IPython using the GBDXTools Interface

```python
# Quickstart Example Script Run in Python using the gbdxTools Interface.  The script will produce a single band tif file showing areas of anomaly.
# First Initialize the Environment
    from gbdxtools import Interface 
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
```	

### Inputs
**Description of Input Parameters and Options for the "RXAnomalyDetection":**

The following table lists the ENVI_RXAnomalyDetection task inputs:

Name                                |       Default         |        Valid Values             |   Description
------------------------------------|:---------------------:|---------------------------------|-----------------
gbdx.Task("ENVI_RXAnomalyDetection")|          N/A          | string                          | string of task name "ENVI_RXAnomalyDetection" 
input_raster                        |         true          | Folder name in S3 location      | This will explain the input file location in either the DG 1b format or following the AOP_Strip_Processor

	
### Outputs

The following table lists the ENVI_RXAnomalyDetection task outputs:

Name        | Required |   Description
------------|:--------:|-----------------
destination |     Y    | This will explain the output file location directory and provide the output in .TIF format.
log         |     N    | S3 location where logs are stored.


**OPTIONAL SETTINGS: Required = False**

**The Default setting does not run the specified process. Some of these processes (e.g. "enable_tiling" = “True”) may have dependencies that also require resetting. Some of the dependencies have “Auto” settings.**

Name                         |       Default         |        Valid Values             |   Description
-----------------------------|:---------------------:|---------------------------------|-----------------
file_types                   |          N/A          | string of file types e.g. .TIF  | This will list the file type to use as input into the task
suppress_vegetation          |         False         | string 'true' or 'false'        | Set this property to true to suppress vegetation anomalies in the RXD results. The options are true or false 
mean\_calculation_method’    |           ?           | string                          | Specify one of the values from the CHOICE_LIST, indicating which mean calculation method to use.  Global: Derive the mean spectrum from the full dataset, Local: Derive the mean spectrum from the **KERNEL\_SIZE** around a given pixel
anomaly\_detection_method    |           ?           | string                          | Specify one of the values from the CHOICE_LIST, indicating which method to use. RXD: Standard RXD algorithm, UTD: Uniform Target Detector algorithm, RXD-UTD: Hybrid of the RXD and UTD algorithms
kernel_size                  |           3           | string                          | Specify the kernel size in pixels, around a given pixel that will be used to create a mean spectrum.  Use an odd number. The minimum value is 3, and the maximum value is (number of columns - 1) less than (number of rows - 1).  Specify **KERNEL_SIZE** only when using the 'Local' option for **MEAN\_CALCULATION_METHOD.**
task\_meta_data              |          N/A          | directory                       | Specify an output location for task metadata

### Advanced
Advanced examples for this task are under development
    

###Known Issues
1)To run an extended workflow including the image preprocessing step with AOP_Strip_Processor use the advanced script. 

**Data Structure for Expected Outputs:**

Your Processed Imagery will be written to the specified S3 Customer Location in a 1 band TIF format(e.g.  s3://gbd-customer-data/unique customer id/named directory/).  


For background on the development and implementation of RX Anomaly Detection refer to the [ENVI Documentation](https://www.harrisgeospatial.com/docs/rxanomalydetection.html)

