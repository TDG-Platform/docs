
# ENVI Get Spectrum From Library*(Editing in Progress)*

This task retrieves the details of a specified material from a spectral library. The QuickStart example uses the *"WorldView Improved Vegetative Index"* which is only applicable to 8-band data (WV02 & WV03).

### Table of Contents
 * [Quickstart](#quickstart) - Get started!
 * [Runtime](#runtime) - Detailed Description of Inputs
 * [Inputs](#inputs) - Required and optional task inputs.
 * [Outputs](#outputs) - Task outputs and example contents.
 * [Advanced](#advanced)
 * [Contact Us](#contact-us)

### Quickstart

This task requires that you first retrieve the list of available spectral libraries by using the ENVI_QuerySpectralIndices Task (ADD LINK).  An example script for this Task is included in the Advanced Options.

    Add QuickStart Script HERE
	


### Runtime

The following table lists all applicable runtime outputs for Classification Smoothing. An estimated Runtime for the Advanced Script example can be derived from adding the result for the two pre-processing steps. For details on the methods of testing the runtimes of the task visit the following link:(INSERT link to GBDX U page here)

  Sensor Name  |  Total Pixels  |  Total Area (k2)  |  Time(secs)  |  Time/Area k2
--------|:----------:|-----------|----------------|---------------
QB02 | 41,551,668 | 312.07 |  |  |
WV02|35,872,942 | 329.87 |  |  |
WV03|35,371,971 | 196.27 |  |  |
GE01| 57,498,000 | 332.97 |  |  |


### Inputs
The following table lists all taskname inputs.
Mandatory (optional) settings are listed as Required = True (Required = False).

  Name       |  Required  |  Description  
-------------|:-----------:|:---------------
input_spectral_library | True       | Specify a spectral library from which to retrieve a particular spectrum.
spectrum_name      | True       | Provide a string with the material spectrum to be retreived.
y_range         |  True    | The range of spectrum values.

### Outputs
The following table lists all taskname outputs.
Mandatory (optional) settings are listed as Required = True (Required = False).

  Name            |  Required  |  Valid Values             | Description  
------------------|:---------: |:------------------------- |---------------
output_raster_uri | True       | s3 URL, .hdr, .tiff, .xml | Specify a string with the fully qualified filename and path of the output raster. If you do not specify this property, the output raster is only temporary. Once the raster has no remaining references, ENVI deletes the temporary file.


**OPTIONAL SETTINGS AND DEFINITIONS:**

Name                 |       Default    | Valid Values |   Description
---------------------|:----------------:|---------------------------------|-----------------
ignore_validate      |          N/A     |     1        |Set this property to a value of 1 to run the task, even if validation of properties fails. This is an advanced option for users who want to first set all task properties before validating whether they meet the required criteria. This property is not set by default, which means that an exception will occur if any property does not meet the required criteria for successful execution of the task.
covariance           |    N/A          |  number     | Specify an array that is the covariance matrix of the input bands. The array size is [number of bands, number of bands].


### Advanced

Included below is a complete end-to-end workflow for 

**Data Structure for Expected Outputs:**

The output is a .json file **'task_meta_data'**, which contains the following spectral information: *wavelength, wavelength_units, reflectance_scale_factor, and y_range*

For background on the development and implementation of XXXXXXXXXX refer to the [ENVI Documentation](https://www.harrisgeospatial.com/docs/classificationtutorial.html)



###Contact Us
Document Owner - [Kathleen Johnson](kajohnso@digitalglobe.com)

> Written with [StackEdit](https://stackedit.io/).