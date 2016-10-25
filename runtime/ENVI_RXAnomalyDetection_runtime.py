from gbdxtools import Interface
gbdx = Interface()

QB = "s3://gbd-customer-data/7d8cfdb6-13ee-4a2a-bf7e-0aff4795d927/Benchmark/QB"
WV1 = "s3://receiving-dgcs-tdgplatform-com/054876516120_01_003"
WV2 = "s3://gbd-customer-data/7d8cfdb6-13ee-4a2a-bf7e-0aff4795d927/Benchmark/WV2"
WV3 = "s3://gbd-customer-data/7d8cfdb6-13ee-4a2a-bf7e-0aff4795d927/Benchmark/WV3"
GE = "s3://gbd-customer-data/7d8cfdb6-13ee-4a2a-bf7e-0aff4795d927/Benchmark/GE/055217125010_01"


envi_task = gbdx.Task("ENVI_RXAnomalyDetection")
envi_task.inputs.file_types='til'
envi_task.inputs.kernel_size='3'
envi_task.inputs.input_raster=WV3

workflow = gbdx.Workflow([ envi_task ] )
workflow.savedata(envi_task.outputs.task_meta_data, location='envi_task_output')
workflow.savedata(envi_task.outputs.output_raster_uri, location='envi_task_output')



'''
workflow.savedata(
  envi_task.outputs.task_meta_data,
    location='Benchmark/RX/QB'
)

workflow.savedata(
  envi_task.outputs.task_meta_data,
    location='Benchmark/RX/WV1'
)


workflow.savedata(
  envi_task.outputs.task_meta_data,
    location='Benchmark/RX/WV2'
)

workflow.savedata(
  envi_task.outputs.task_meta_data,
    location='Benchmark/RX/WV3'
)
'''
workflow.savedata(
  envi_task.outputs.task_meta_data,
    location='Benchmark/RX/GE'
)


workflow.execute()
status = workflow.status["state"]
wf_id = workflow.id
