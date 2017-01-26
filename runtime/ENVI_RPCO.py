'''
from gbdxtools import Interface
gbdx = Interface()

#Insert correct path to image in S3 location
#image = "s3://ikonos-product/po_1018080"

data1 = 's3://gbd-customer-data/CustomerAccount#/PathToImage1/'
data2 = 's3://gbd-customer-data/CustomerAccount#/PathToImage2/'


envi_II = gbdx.Task("ENVI_ImageIntersection")
envi_II.inputs.file_types = "hdr"
envi_II.inputs.input_raster1 = data1
envi_II.inputs.input_raster2 = data2
envi_II.inputs.output_raster1_uri_filename = "Image1"
envi_II.inputs.output_raster2_uri_filename = "Image2"

workflow = gbdx.Workflow([envi_II, envi_RPCO])

workflow.savedata(
    envi_II.outputs.output_raster1_uri,
        location='ENVI_ImageIntersection/image1'
)
workflow.savedata(
    envi_II.outputs.output_raster2_uri,
        location='ENVI_ImageIntersection/image2'
)
workflow.execute()
status = workflow.status["state"]
wf_id = workflow.id

from gbdxtools import Interface
gbdx = Interface()
'''

from gbdxtools import Interface
gbdx = Interface()
image = "s3://gbd-customer-data/7d8cfdb6-13ee-4a2a-bf7e-0aff4795d927/Benchmark/RPCOrtho/image1"
dem = "s3://gbd-customer-data/7d8cfdb6-13ee-4a2a-bf7e-0aff4795d927/Benchmark/RPCOrtho/DEM/image1"


envi_RPCO = gbdx.Task("ENVI_RPCOrthorectification")
envi_RPCO.inputs.input_raster_metadata = '{"sensor type": "IKONOS"}'
envi_RPCO.inputs.input_raster_band_grouping = 'multispectral'
envi_RPCO.inputs.input_raster = image
envi_RPCO.inputs.dem_raster = dem



workflow = gbdx.Workflow([envi_RPCO])

workflow.savedata(
    envi_RPCO.outputs.output_raster_uri,
        location='Benchmark/ENVI_RPCO/results'
)

workflow.execute()

status = workflow.status["state"]
wf_id = workflow.id
