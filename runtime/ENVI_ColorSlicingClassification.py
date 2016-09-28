from gbdxtools import Interface
gbdx = Interface()


QB = "s3://receiving-dgcs-tdgplatform-com/054876960040_01_003"
WV1 = "s3://receiving-dgcs-tdgplatform-com/054876516120_01_003"
WV2 = "s3://receiving-dgcs-tdgplatform-com/054876618060_01_003"
WV3 = "s3://receiving-dgcs-tdgplatform-com/055605759010_01_003"
GE = "s3://receiving-dgcs-tdgplatform-com/055217125010_01_003"

aoptask = gbdx.Task("AOP_Strip_Processor", data=QB, enable_acomp=True, enable_pansharpen=False, enable_dra=False, bands='MS')

# Capture AOP task outputs
#orthoed_output = aoptask.get_output('data')

aop2envi = gbdx.Task("AOP_ENVI_HDR")
aop2envi.inputs.image = aoptask.outputs.data.value

#hdr file used to compute spectral index

envi_ndvi = gbdx.Task("ENVI_SpectralIndex")
envi_ndvi.inputs.input_raster = aop2envi.outputs.output_data.value
envi_ndvi.inputs.file_types = "hdr"
envi_ndvi.inputs.index = "Normalized Difference Vegetation Index"

#spectral index file used in color slice classification task

envi_color = gbdx.Task('ENVI_ColorSliceClassification', input_raster=envi_ndvi.outputs.output_raster_uri.value)
envi_color.file_types = 'hdr'


workflow = gbdx.Workflow([aoptask, aop2envi, envi_ndvi, envi_color])

workflow.savedata(
  envi_ndvi.outputs.output_raster_uri,
  location='Benchmark/color_slice/QB/NDVI'
)

workflow.savedata(
  envi_color.outputs.output_raster_uri,
  location='Benchmark/color_slice/QB/Color16'
)

workflow.execute()

print workflow.execute()
print workflow.id
print workflow.status
