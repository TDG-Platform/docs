
# ENVI Get Spectrum From Library

This task retrieves the details of a specified material from a spectral library. For details regarding the operation of ENVI Tasks on the Platform refer to [ENVI Task Runner](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md).

### Table of Contents
 * [Quickstart](#quickstart) - Get started!
 * [Runtime](#runtime) - Not Applicable
 * [Inputs](#inputs) - Required and optional task inputs.
 * [Outputs](#outputs) - Task outputs
 * [Advanced](#advanced) - Upload your own spectral files
 * [Contact Us](#contact-us)

### Quickstart

This task requires that you first retrieve the list of available spectral libraries by using the [ENVI_QuerySpectralIndices Task](https://github.com/TDG-Platform/docs/blob/master/ENVI_QuerySpectralIndices.md).  

```python
    	
	from gbdxtools import Interface
	gbdx = Interface()

	# Retrieve the Spectrum Data from the Library
	getspectrum = gbdx.Task("ENVI_GetSpectrumFromLibrary")

	# Edit the following path to reflect a specific path to the Spectral Index File
	getspectrum.inputs.input_spectral_library_filename = 'veg_2grn.sli'
	getspectrum.inputs.spectrum_name = 'Dry Grass' # example from Spectral Index veg_2grn.sli

	# Run Workflow & save the output
	workflow = gbdx.Workflow([ getspectrum ])
	# Edit the following line(s) to reflect specific folder(s) for the output file (example location provided)			workflow.savedata(getspectrum.outputs.task_meta_data, location=location='customer_output_directory/getspectrum/')

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
task_meta_data | True       |.json | file contains the following spectral information: *wavelength, wavelength_units, reflectance_scale_factor, and y_range*

**Data Structure for Expected Outputs:**

The output is a .json file **'task_meta_data'**, which contains the following spectral information.  The example below uses data from ENVI Spectral Library:  *veg_1dry.sli*, spectrum_name = *CDE054: Pinyon Pine (SAP)*

Output Parameters   | Description       |Example Output 
--------------------|-------------------|-------------------
wavelengths      |A double-precision array representing the wavelength values of the spectrum. |   0.4000000059604645, 0.4009999930858612,......., 2.496000051498413, 2.5
wavelength_units   | A string representing the wavelength units of the spectrum. |  "micrometers"
y_range      | The range of spectrum values.  | [0.0,1.0] 
spectrum     |A double-precision array representing the spectrum that matches the input spectrum name.|     0.03869999945163727, 0.03869999945163727,..........,0.0608999989926815, 0.06119999662041664
reflectance_scale_factor  | The scale factor to use for translating the spectrum to reflectance.    |   default = 1.0


**OPTIONAL SETTINGS AND DEFINITIONS:**

Name                 |       Default    | Valid Values |   Description
---------------------|:----------------:|---------------------------------|-----------------
ignore_validate      |          N/A     |     1        |Set this property to a value of 1 to run the task, even if validation of properties fails. This is an advanced option for users who want to first set all task properties before validating whether they meet the required criteria. This property is not set by default, which means that an exception will occur if any property does not meet the required criteria for successful execution of the task.

### Advanced

The advanced script for this task demonstrates loading your own spectrum data to run the task. The Advanced Script example uses the ENVI  *"veg_1dry.sli"* spectral index file and the *CDE054: Pinyon Pine (SAP)* spectrum. If you use your own spectral data, and it is a .sli file, you must create an "HDR" file.

```python
    	
	from gbdxtools import Interface
	gbdx = Interface()

	# Retrieve the Spectrum Data from the Library
	getspectrum = gbdx.Task("ENVI_GetSpectrumFromLibrary")
	
	# Edit the following path to reflect a specific path to the Spectral Index File
	getspectrum.input_spectral_library_filename = "veg_1dry.sli"
	getspectrum.inputs.file_types = "HDR"
	getspectrum.inputs.input_spectral_library = 's3://gbd-customer-data/CustomerAccount#/PathToSpectralLibrary/'
	getspectrum.inputs.spectrum_name = "CDE054: Pinyon Pine (SAP)" # example from Spectral Index veg_1dry.sli

	# Run Workflow & save the output
	workflow = gbdx.Workflow([ getspectrum ])
	# Edit the following line(s) to reflect specific folder(s) for the output file (example location provided)
	workflow.savedata(getspectrum.outputs.task_meta_data, location='customer_output_directory/getspectrum/')

	workflow.execute()
	print workflow.id
	print workflow.status
	
```

For background on the development and implementation of this task refer to the [ENVI Documentation](https://www.harrisgeospatial.com/docs/classificationtutorial.html)



###Contact Us
Document Owner - [Kathleen Johnson](kajohnso@digitalglobe.com)


