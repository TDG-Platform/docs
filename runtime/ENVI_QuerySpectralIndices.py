from gbdxtools import Interface
gbdx = Interface()

QB = "s3://gbd-customer-data/7d8cfdb6-13ee-4a2a-bf7e-0aff4795d927/Benchmark/QB"
WV1 = "s3://receiving-dgcs-tdgplatform-com/054876516120_01_003"
WV2 = "s3://gbd-customer-data/7d8cfdb6-13ee-4a2a-bf7e-0aff4795d927/Benchmark/WV2"
WV3 = "s3://gbd-customer-data/7d8cfdb6-13ee-4a2a-bf7e-0aff4795d927/Benchmark/WV3"
GE = "s3://gbd-customer-data/7d8cfdb6-13ee-4a2a-bf7e-0aff4795d927/Benchmark/GE/055217125010_01"


aop2envi = gbdx.Task("AOP_ENVI_HDR")
#aop2envi.inputs.image = QB
#aop2envi.inputs.image = WV2
#aop2envi.inputs.image = WV3
aop2envi.inputs.image = GE

envi_query = gbdx.Task("ENVI_QuerySpectralIndices")
envi_query.inputs.input_raster = aop2envi.outputs.output_data.value
envi_query.inputs.file_types = "hdr"

workflow = gbdx.Workflow([aop2envi, envi_query])

'''
workflow.savedata(
  envi_query.outputs.task_meta_data,
    location='Benchmark/QSI/QB'
)

workflow.savedata(
  envi_query.outputs.task_meta_data,
    location='Benchmark/QSI/WV2'
)

workflow.savedata(
  envi_query.outputs.task_meta_data,
    location='Benchmark/QSI/WV3'
)
'''
workflow.savedata(
  envi_query.outputs.task_meta_data,
    location='Benchmark/QSI/GE'
)


workflow.execute()
status = workflow.status["state"]
wf_id = workflow.id
