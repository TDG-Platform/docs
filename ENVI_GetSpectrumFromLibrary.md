
# ENVI Get Spectrum From Library

This task retrieves the details of a specified material from a spectral library. The QuickStart example uses the ENVI  *"veg_1dry.sli"* spectral index file and the *CDE054: Pinyon Pine (SAP)* spectrum.

### Table of Contents
 * [Quickstart](#quickstart) - Get started!
 * [Runtime](#runtime) - Not Applicable
 * [Inputs](#inputs) - Required and optional task inputs.
 * [Outputs](#outputs) - Task outputs
 * [Advanced](#advanced) Not Applicable
 * [Contact Us](#contact-us)

### Quickstart

This task requires that you first retrieve the list of available spectral libraries by using the [ENVI_QuerySpectralIndices Task](https://github.com/TDG-Platform/docs/blob/master/ENVI_QuerySpectralIndices.md).  An example script for this Task is included in the Advanced Options.

```python
    	
	from gbdxtools import Interface
	gbdx = Interface()

	# Retrieve the Spectrum Data from the Library
	getspectrum = gbdx.Task("ENVI_GetSpectrumFromLibrary")
	
	# Edit the following path to reflect a specific path to the Spectral Index File
	getspectrum.inputs.input_spectral_library = 's3://gbd-customer-data/CustomerAccount#/PathToSpectralLibrary/'
	getspectrum.inputs.spectrum_name = "CDE054: Pinyon Pine (SAP)" # example from Spectral Index veg_1dry.sli

	# Run Workflow & save the output
	workflow = gbdx.Workflow([ getspectrum ])
	# Edit the following line(s) to reflect specific folder(s) for the output file (example location provided)
	workflow.savedata(getspectrum.outputs.task_meta_data, location='customer_output_directory')

	workflow.execute()
	print workflow.id
	print workflow.status
	
```


### Inputs
The following table lists all taskname inputs.
Mandatory (optional) settings are listed as Required = True (Required = False).

  Name       |  Required  |  Description  
-------------|:-----------:|:---------------
input_spectral_library | True       | Specify a spectral library from which to retrieve a particular spectrum.
spectrum_name      | True       | Provide a string with the material spectrum to be retreived.

### Outputs
The following table lists all taskname outputs.
Mandatory (optional) settings are listed as Required = True (Required = False).

  Name            |  Required  |  Valid Values             | Description  
------------------|:---------: |:------------------------- |---------------
[task_meta_data[(#data-structure-for-expected-outputs) | True       |.json | file contains the following spectral information: *wavelength, wavelength_units, reflectance_scale_factor, and y_range*


**OPTIONAL SETTINGS AND DEFINITIONS:**

Name                 |       Default    | Valid Values |   Description
---------------------|:----------------:|---------------------------------|-----------------
ignore_validate      |          N/A     |     1        |Set this property to a value of 1 to run the task, even if validation of properties fails. This is an advanced option for users who want to first set all task properties before validating whether they meet the required criteria. This property is not set by default, which means that an exception will occur if any property does not meet the required criteria for successful execution of the task.

### Advanced

This task will normally be included in the Advanced Script for the ENVI Ace Processor or other ENVI tasks that require spectral data. Therefore no Advanced Script is included here.

**Data Structure for Expected Outputs:**

The output is a .json file **'task_meta_data'**, which contains the following spectral information: *wavelength, wavelength_units, reflectance_scale_factor, and y_range*

For background on the development and implementation of XXXXXXXXXX refer to the [ENVI Documentation](https://www.harrisgeospatial.com/docs/classificationtutorial.html)



###Contact Us
Document Owner - [Kathleen Johnson](kajohnso@digitalglobe.com)


