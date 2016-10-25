from gbdxtools import Interface
gbdx = Interface()

QB = "s3://gbd-customer-data/7d8cfdb6-13ee-4a2a-bf7e-0aff4795d927/Benchmark/QB"
WV1 = "s3://receiving-dgcs-tdgplatform-com/054876516120_01_003"
WV2 = "s3://gbd-customer-data/7d8cfdb6-13ee-4a2a-bf7e-0aff4795d927/Benchmark/WV2"
WV3 = "s3://gbd-customer-data/7d8cfdb6-13ee-4a2a-bf7e-0aff4795d927/Benchmark/WV3"
GE = "s3://gbd-customer-data/7d8cfdb6-13ee-4a2a-bf7e-0aff4795d927/Benchmark/GE/055217125010_01"

#aoptask = gbdx.Task('AOP_Strip_Processor', data=QB, bands='MS', enable_acomp=True, enable_pansharpen=False, enable_dra=False)     # creates acomp'd multispectral image
#aoptask = gbdx.Task('AOP_Strip_Processor', data=WV1, bands='PAN', enable_acomp=False, enable_pansharpen=False, enable_dra=False)     # creates acomp'd multispectral image
#aoptask = gbdx.Task('AOP_Strip_Processor', data=WV2, bands='MS', enable_acomp=True, enable_pansharpen=False, enable_dra=False)     # creates acomp'd multispectral image
#aoptask = gbdx.Task('AOP_Strip_Processor', data=WV3, bands='MS', enable_acomp=True, enable_pansharpen=False, enable_dra=False)     # creates acomp'd multispectral image
#aoptask = gbdx.Task('AOP_Strip_Processor', data=GE, bands='MS', enable_acomp=True, enable_pansharpen=False, enable_dra=False)     # creates acomp'd multispectral image

isodata = gbdx.Task("ENVI_ISODATAClassification")
isodata.inputs.input_raster = GE
isodata.inputs.file_types = "tif"

sieve = gbdx.Task("ENVI_ClassificationSieving")
sieve.inputs.input_raster = isodata.outputs.output_raster_uri.value
sieve.inputs.file_types = "hdr"

clump = gbdx.Task("ENVI_ClassificationClumping")
clump.inputs.input_raster = sieve.outputs.output_raster_uri.value
clump.inputs.file_types = "hdr"

workflow = gbdx.Workflow([isodata, sieve, clump])

'''
workflow.savedata(
	clump.outputs.output_raster_uri,
		location='Benchmark/clump/QB'
)


workflow.savedata(
    clump.outputs.output_raster_uri,
        location='Benchmark/clump/WV2'
)

workflow.savedata(
    clump.outputs.output_raster_uri,
        location='Benchmark/clump/WV3'
)
'''

workflow.savedata(
    clump.outputs.output_raster_uri,
        location='Benchmark/clump/GE'
)


workflow.execute()
workflow.status
