# Input data
from gbdxtools import Interface
gbdx = Interface()

WV2 = "s3://gbd-customer-data/7d8cfdb6-13ee-4a2a-bf7e-0aff4795d927/Benchmark/WV2/"
WV3 = "s3://gbd-customer-data/7d8cfdb6-13ee-4a2a-bf7e-0aff4795d927/Benchmark/WV3/"


prep2 = gbdx.Task('ProtogenPrep')
# ProtogenPrep will move the aoptask output to root where prototask can find it
prep2.inputs.raster = WV2


prep3 = gbdx.Task('ProtogenPrep')
# ProtogenPrep will move the aoptask output to root where prototask can find it
prep3.inputs.raster = WV3

'''
protoLULC = gbdx.Task("protogenV2LULC", raster=gluetask2.outputs.data.value)
protoPAN = gbdx.Task("protogenV2PANTEX10", raster=gluetask2.outputs.data.value)
protoRAC = gbdx.Task("protogenV2RAC", raster=gluetask2.outputs.data.value)
protoRAS = gbdx.Task("protogenV2RAS", raster=gluetask2.outputs.data.value)
protoRAV = gbdx.Task("protogenV2RAV", raster=gluetask2.outputs.data.value)
protoRAW = gbdx.Task("protogenV2RAW", raster=gluetask2.outputs.data.value)

'''
protoLULC3 = gbdx.Task("protogenV2LULC", raster=prep3.outputs.data)
protoPAN3 = gbdx.Task("protogenV2PANTEX10", raster=prep3.outputs.data)
protoRAC3 = gbdx.Task("protogenV2RAC", raster=prep3.outputs.data)
protoRAS3 = gbdx.Task("protogenV2RAS", raster=prep3.outputs.data)
protoRAV3 = gbdx.Task("protogenV2RAV", raster=prep3.outputs.data)
protoRAW3 = gbdx.Task("protogenV2RAW", raster=prep3.outputs.data)


workflow = gbdx.Workflow([ prep3, protoLULC3, protoPAN3, protoRAC3, protoRAS3, protoRAV3, protoRAW3 ])

'''
workflow.savedata(protoLULC.outputs.data, location="Benchmark/Protogen/LULC")
workflow.savedata(protoPAN.outputs.data, location="Benchmark/Protogen/PAN")
workflow.savedata(protoRAC.outputs.data, location="Benchmark/Protogen/RAC")
workflow.savedata(protoRAS.outputs.data, location="Benchmark/Protogen/RAS")
workflow.savedata(protoRAV.outputs.data, location="Benchmark/Protogen/RAV")
workflow.savedata(protoRAW.outputs.data, location="Benchmark/Protogen/RAW")
'''

workflow.savedata(protoLULC3.outputs.data, location="Benchmark/Protogen/prep/LULC3")
workflow.savedata(protoPAN3.outputs.data, location="Benchmark/Protogen/prep/PAN3")
workflow.savedata(protoRAC3.outputs.data, location="Benchmark/Protogen/prep/RAC3")
workflow.savedata(protoRAS3.outputs.data, location="Benchmark/Protogen/prep/RAS3")
workflow.savedata(protoRAV3.outputs.data, location="Benchmark/Protogen/prep/RAV3")
workflow.savedata(protoRAW3.outputs.data, location="Benchmark/Protogen/prep/RAW3")

workflow.execute()
workflow.status
