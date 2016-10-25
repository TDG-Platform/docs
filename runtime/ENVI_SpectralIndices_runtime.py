from gbdxtools import Interface
gbdx = Interface()

QB = "s3://gbd-customer-data/7d8cfdb6-13ee-4a2a-bf7e-0aff4795d927/Benchmark/QB"
WV1 = "s3://receiving-dgcs-tdgplatform-com/054876516120_01_003"
WV2 = "s3://gbd-customer-data/7d8cfdb6-13ee-4a2a-bf7e-0aff4795d927/Benchmark/WV2"
WV3 = "s3://gbd-customer-data/7d8cfdb6-13ee-4a2a-bf7e-0aff4795d927/Benchmark/WV3"
GE = "s3://gbd-customer-data/7d8cfdb6-13ee-4a2a-bf7e-0aff4795d927/Benchmark/GE/055217125010_01"


aop2envi = gbdx.Task("AOP_ENVI_HDR")
aop2envi.inputs.image = GE
envi_ndvi = gbdx.Task("ENVI_SpectralIndices")
envi_ndvi.inputs.input_raster = aop2envi.outputs.output_data.value
envi_ndvi.inputs.file_types = "hdr"
# Specify a string/list of indicies to run on the input_raster variable.  The order of indicies wi
envi_ndvi.inputs.index = '["Normalized Difference Vegetation Index", "Simple Ratio"]'

workflow = gbdx.Workflow([aop2envi, envi_ndvi])
'''
workflow.savedata(
	       envi_ndvi.outputs.output_raster_uri,
	          location='Benchmark/spectralindices/QB'
)

workflow.savedata(
	       envi_ndvi.outputs.output_raster_uri,
	          location='Benchmark/spectralindices/WV2'
)

workflow.savedata(
	       envi_ndvi.outputs.output_raster_uri,
	          location='Benchmark/spectralindices/WV3'
)
'''
workflow.savedata(
	       envi_ndvi.outputs.output_raster_uri,
	          location='Benchmark/spectralindices/GE'
)

workflow.execute()
status = workflow.status["state"]
wf_id = workflow.id
