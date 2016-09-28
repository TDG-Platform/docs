from gbdxtools import Interface
gbdx = Interface()

test = "s3://receiving-dgcs-tdgplatform-com/055777190010_01_003"
QB = "s3://receiving-dgcs-tdgplatform-com/054876960040_01_003"
WV1 = "s3://receiving-dgcs-tdgplatform-com/054876516120_01_003"
WV2 = "s3://receiving-dgcs-tdgplatform-com/054876618060_01_003"
WV3 = "s3://receiving-dgcs-tdgplatform-com/055605759010_01_003"
GE = "s3://receiving-dgcs-tdgplatform-com/055217125010_01_003"

aoptask1 = gbdx.Task('AOP_Strip_Processor', data=test, bands='MS', enable_acomp=True, enable_pansharpen=False, enable_dra=False)     # creates acomp'd multispectral image
#aoptask2 = gbdx.Task('AOP_Strip_Processor', data=WV1, bands='PAN', enable_acomp=False, enable_pansharpen=False, enable_dra=False)     # creates acomp'd multispectral image
#aoptask3 = gbdx.Task('AOP_Strip_Processor', data=WV2, bands='MS', enable_acomp=True, enable_pansharpen=False, enable_dra=False)     # creates acomp'd multispectral image
#aoptask4 = gbdx.Task('AOP_Strip_Processor', data=WV3, bands='MS', enable_acomp=True, enable_pansharpen=False, enable_dra=False)     # creates acomp'd multispectral image
#aoptask5 = gbdx.Task('AOP_Strip_Processor', data=GE, bands='MS', enable_acomp=True, enable_pansharpen=False, enable_dra=False)     # creates acomp'd multispectral image


envitask = gbdx.Task("ENVI_ISODATAClassification")
envitask.inputs.file_types = 'tif'
envitask.inputs.input_raster = aoptask1.outputs.data.value
envitask.outputs.output_raster = "ENVI"


shptask = gbdx.Task("ENVI_ClassificationToShapefile")
shptask.inputs.input_raster = envitask.outputs.output_raster_uri
shptask.inputs.file_types = "hdr"

workflow = gbdx.Workflow([aoptask1, envitask, shptask])

workflow.savedata(
	       shptask.outputs.output_vector_uri,
	          location='Benchmark/ENVI/SHP'
)

workflow.savedata(
	envitask.output.output_raster_uri,
		location='Benchmark/SHP/test/ISO'
)

'''

workflow.savedata(
    shptask.outputs.data,
        location='Benchmark/SHP/WV2'
)

workflow.savedata(
    shptask.outputs.data,
        location='Benchmark/SHP/WV3'
)


workflow.savedata(
    shptask.outputs.data,
        location='Benchmark/SHP/GE'
)

'''
workflow.execute()
workflow.status
