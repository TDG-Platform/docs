from gbdxtools import Interface
gbdx = Interface()

# Input data
from gbdxtools import Interface
gbdx = Interface()

WV2 = "s3://gbd-customer-data/7d8cfdb6-13ee-4a2a-bf7e-0aff4795d927/Benchmark/WV2/"
WV3 = "s3://gbd-customer-data/7d8cfdb6-13ee-4a2a-bf7e-0aff4795d927/Benchmark/WV3/"

gluetask2 = gbdx.Task('gdal-cli')
# move aoptask output to root where prototask can find it
gluetask2.inputs.data = WV2
gluetask2.inputs.execution_strategy = 'runonce'
gluetask2.inputs.command = """mv $indir/*/*.tif $outdir/"""

gluetask3 = gbdx.Task('gdal-cli')
# move aoptask output to root where prototask can find it
gluetask3.inputs.data = WV3
gluetask3.inputs.execution_strategy = 'runonce'
gluetask3.inputs.command = """mv $indir/*/*.tif $outdir/"""
'''
protoLULC = gbdx.Task("protogenV2LULC", raster=gluetask2.outputs.data.value)
protoPAN = gbdx.Task("protogenV2PANTEX10", raster=gluetask2.outputs.data.value)
protoRAC = gbdx.Task("protogenV2RAC", raster=gluetask2.outputs.data.value)
protoRAS = gbdx.Task("protogenV2RAS", raster=gluetask2.outputs.data.value)
protoRAV = gbdx.Task("protogenV2RAV", raster=gluetask2.outputs.data.value)
protoRAW = gbdx.Task("protogenV2RAW", raster=gluetask2.outputs.data.value)

'''
protoLULC3 = gbdx.Task("protogenV2LULC", raster=gluetask3.outputs.data.value)
protoPAN3 = gbdx.Task("protogenV2PANTEX10", raster=gluetask3.outputs.data.value)
protoRAC3 = gbdx.Task("protogenV2RAC", raster=gluetask3.outputs.data.value)
protoRAS3 = gbdx.Task("protogenV2RAS", raster=gluetask3.outputs.data.value)
protoRAV3 = gbdx.Task("protogenV2RAV", raster=gluetask3.outputs.data.value)
protoRAW3 = gbdx.Task("protogenV2RAW", raster=gluetask3.outputs.data.value)


workflow = gbdx.Workflow([ gluetask3, protoLULC3, protoPAN3, protoRAC3, protoRAS3, protoRAV3, protoRAW3 ])

'''
workflow.savedata(protoLULC.outputs.data, location="Benchmark/Protogen/LULC")
workflow.savedata(protoPAN.outputs.data, location="Benchmark/Protogen/PAN")
workflow.savedata(protoRAC.outputs.data, location="Benchmark/Protogen/RAC")
workflow.savedata(protoRAS.outputs.data, location="Benchmark/Protogen/RAS")
workflow.savedata(protoRAV.outputs.data, location="Benchmark/Protogen/RAV")
workflow.savedata(protoRAW.outputs.data, location="Benchmark/Protogen/RAW")

'''
workflow.savedata(protoLULC3.outputs.data, location="Benchmark/Protogen/LULC3")
workflow.savedata(protoPAN3.outputs.data, location="Benchmark/Protogen/PAN3")
workflow.savedata(protoRAC3.outputs.data, location="Benchmark/Protogen/RAC3")
workflow.savedata(protoRAS3.outputs.data, location="Benchmark/Protogen/RAS3")
workflow.savedata(protoRAV3.outputs.data, location="Benchmark/Protogen/RAV3")
workflow.savedata(protoRAW3.outputs.data, location="Benchmark/Protogen/RAW3")

workflow.execute()
workflow.status
