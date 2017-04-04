
# ENVI Get Spectrum From Library

This task retrieves the details of a specified material from a spectral library. For details regarding the operation of ENVI Tasks on the Platform refer to [ENVI Task Runner](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md).

### Table of Contents

- [Quickstart](#quickstart) - Get started!
- [Inputs](#inputs) - Required and optional task inputs.
- [Outputs](#outputs) - Task outputs and example contents.
- [Runtime](#runtime) - Example estimate of task runtime.
- [Advanced](#advanced) - Additional information for advanced users.
- [Contact Us](#contact-us) - Contact tech or document owner.](#contact-us)



### Quickstart

Example Script: Run in a python environment (i.e. - IPython) using the gbdxtools interface.

```python
from gbdxtools import Interface
gbdx = Interface()

envi = gbdx.Task("ENVI_GetSpectrumFromLibrary")
envi.inputs.input_spectral_library_filename = 'veg_2grn.sli'
envi.inputs.spectrum_name = 'Dry Grass' # example from Spectral Index veg_2grn.sli

workflow = gbdx.Workflow([ getspectrum ])
	
workflow.savedata(
    envi.outputs.task_meta_data,
    location=location='GetSpecLib/task_meta_data'
)

print workflow.execute()
print workflow.status
# Repeat workflow.status as needed to monitor progress.
```



### Inputs

The following table lists all inputs for this task. For details regarding the use of all ENVI input types refer to the [ENVI Task Runner Inputs]([See ENVIRASTER input type](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md)) documentation.

| Name                            | Required | Default |               Valid Values               | Description                              |
| ------------------------------- | :------: | :-----: | :--------------------------------------: | ---------------------------------------- |
| input_spectral_library          |  False   |  None   |              A valid S3 URL              | Specify a spectral library from which to retrieve a particular spectrum. This may be an ENVI library or a library that you have uploaded.  It is required if you are using a custom library. — Value Type: [ENVISPECTRALLIBRARY](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md#envispectrallibrary) |
| input_spectral_library_filename |  False   |  None   | string name (see ENVI software for available libraries) | String name of the ENVI spectral library file .sli -- Value Type: STRING [(See Task Runner details)](https://github.com/TDG-Platform/docs/blob/master/ENVI_Task_Runner_Inputs.md#envispectrallibrary) |
| spectrum_name                   |   True   |   N/A   |                  string                  | Provide a string with the material spectrum to be retreived. |



### Outputs

The following table lists all the tasks outputs.

| Name                     | Required | Description                              |
| ------------------------ | :------: | ---------------------------------------- |
| task_meta_data           |  False   | GBDX Option. Output location for task meta data such as execution log and output JSON. |
| wavelengths              |   True   | A double array representing the wavelength values of the spectrum. -- Value Type: DOUBLE[*] |
| wavelength_units         |   True   | A string representing the wavelength units of the spectrum. -- Value Type: STRING |
| y_range                  |   True   | The range of spectrum values. -- Value Type: DOUBLE[*] |
| spectrum                 |   True   | A double array representing the spectrum that matches the input spectrum name. -- Value Type: DOUBLE[*] |
| reflectance_scale_factor |   True   | Scale factor to be used in converting spectra to reflectance. -- Value Type: DOUBLE |

##### Output Structure

The output are string values that can be passed to another chained task. The values are also written to an `output.json` in the `task_meta_data` port. 



### Advanced

The advanced script for this task demonstrates loading your own spectrum data to run the task. The Advanced Script example uses the ENVI  *"veg_1dry.sli"* spectral index file and the *CDE054: Pinyon Pine (SAP)* spectrum. If you use your own spectral data, and it is a .sli file, you must create an "HDR" file.

```python
from gbdxtools import Interface
gbdx = Interface()

# Ikonos
wavelengths = '[480.00000, 552.00000, 666.00000, 803.00000]'
wavelength_units = 'Nanometers'

getspec = gbdx.Task("ENVI_GetSpectrumFromLibrary")
getspec.input_spectral_library_filename = "veg_1dry.sli"
getspec.inputs.input_spectral_library = 
getspec.inputs.spectrum_name = "CDE054: Pinyon Pine (SAP)"

resample = gbdx.Task("ENVI_ResampleSpectrum")
resample.inputs.input_spectrum = task1.outputs.spectrum.value
resample.inputs.input_wavelengths = task1.outputs.wavelengths.value
resample.inputs.input_wavelength_units = task1.outputs.wavelength_units.value
resample.inputs.resample_wavelengths = wavelengths
resample.inputs.resample_wavelength_units = wavelength_units

workflow = gbdx.Workflow([ getspec, resample ])

workflow.savedata(
    resample.outputs.task_meta_data, 
    location='GetSpecLib/task_meta_data'
)

print workflow.execute()
print workflow.status
# Repeat workflow.status as needed to monitor progress.
```



### Background

For background on the development and implementation of this task refer to the [ENVI Documentation](https://www.harrisgeospatial.com/docs/ENVIGetSpectrumFromLibraryTask.html), and Resample Spectrum [here](https://www.harrisgeospatial.com/docs/ENVIResampleSpectrumTask.html)



###Contact Us
Document Owner - [Kathleen Johnson](kajohnso@digitalglobe.com)


