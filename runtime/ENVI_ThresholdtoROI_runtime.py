from gbdxtools import Interface
gbdx = Interface()

QB = "s3://gbd-customer-data/7d8cfdb6-13ee-4a2a-bf7e-0aff4795d927/Benchmark/QB"
WV1 = "s3://receiving-dgcs-tdgplatform-com/054876516120_01_003"
WV2 = "s3://gbd-customer-data/7d8cfdb6-13ee-4a2a-bf7e-0aff4795d927/Benchmark/WV2"
WV3 = "s3://gbd-customer-data/7d8cfdb6-13ee-4a2a-bf7e-0aff4795d927/Benchmark/WV3"
GE = "s3://gbd-customer-data/7d8cfdb6-13ee-4a2a-bf7e-0aff4795d927/Benchmark/GE/055217125010_01"


# Capture AOP task outputs
#orthoed_output = aoptask.get_output('data')

task = gbdx.Task("ENVI_ImageThresholdToROI")
task.inputs.input_raster=WV1
task.inputs.file_types = "tif"
task.inputs.roi_name = "[\"Water\"]"
task.inputs.roi_color = "[[0,255,0]"
task.inputs.threshold = "[[138]"
task.inputs.output_roi_uri_filename = "roi.xml"

workflow = gbdx.Workflow([ task ])
'''
workflow.savedata(
    task.outputs.output_roi_uri,
        location='Benchmark/ImgToROI/QB'
)
'''
workflow.savedata(
    task.outputs.output_roi_uri,
        location='Benchmark/ImgToROI/WV1'
)
'''
workflow.savedata(
    task.outputs.output_roi_uri,
        location='Benchmark/ImgToROI/WV2'
)

workflow.savedata(
    task.outputs.output_roi_uri,
        location='Benchmark/ImgToROI/WV3'
)
'''
workflow.savedata(
    task.outputs.output_roi_uri,
        location='Benchmark/ImgToROI/QE'
)

workflow.execute()
status = workflow.status["state"]
wf_id = workflow.id
