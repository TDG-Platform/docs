from gbdxtools import Interface
gbdx = Interface()

QB = "s3://receiving-dgcs-tdgplatform-com/054876960040_01_003"
WV1 = "s3://receiving-dgcs-tdgplatform-com/054876516120_01_003"
WV2 = "s3://receiving-dgcs-tdgplatform-com/054876618060_01_003"
WV3 = "s3://receiving-dgcs-tdgplatform-com/055605759010_01_003"
GE = "s3://receiving-dgcs-tdgplatform-com/055217125010_01_003"

aoptask1 = gbdx.Task('AOP_Strip_Processor', data=QB, bands='MS', enable_acomp=True, enable_pansharpen=False, enable_dra=False)     # creates acomp'd multispectral image
#aoptask2 = gbdx.Task('AOP_Strip_Processor', data=WV1, bands='PAN', enable_acomp=False, enable_pansharpen=False, enable_dra=False)     # creates acomp'd multispectral image
#aoptask3 = gbdx.Task('AOP_Strip_Processor', data=WV2, bands='MS', enable_acomp=True, enable_pansharpen=False, enable_dra=False)     # creates acomp'd multispectral image
#aoptask4 = gbdx.Task('AOP_Strip_Processor', data=WV3, bands='MS', enable_acomp=True, enable_pansharpen=False, enable_dra=False)     # creates acomp'd multispectral image
#aoptask5 = gbdx.Task('AOP_Strip_Processor', data=GE, bands='MS', enable_acomp=True, enable_pansharpen=False, enable_dra=False)     # creates acomp'd multispectral image



workflow = gbdx.Workflow([aoptask1])

workflow.savedata(
    aoptask1.outputs.data,
        location='Benchmark/QB'
)
'''
workflow.savedata(
    aoptask2.outputs.data,
        location='Benchmark/WV1'
)

workflow.savedata(
    aoptask3.outputs.data,
        location='Benchmark/WV2'
)

workflow.savedata(
    aoptask4.outputs.data,
        location='Benchmark/WV3'
)

workflow.savedata(
    aoptask5.outputs.data,
        location='Benchmark/GE'
)
'''
workflow.execute()
workflow.status
