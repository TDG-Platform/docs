# Simularity: Automatic Image Anomaly Detection System (aiads)

The algorithm takes a candidate image, and a historical set of images which intersect the candidate and precede it in time, and produces a heat map image of the same dimensions as the candidate, which marks anomalous regions as red and non-anomalous regions as blue or transparent.
Both candidates and historical images must be AComp and DRA corrected, as well as being pan-sharpened. Lower off-nadir angles are preferred, but images with significant off-nadir angles have been successfully processed.
This File documents the use of the GBDX version of AIADS

The Task takes as its input, a directory which is output by the AOP_strip_processor
task (or an equivalent directory structure) and outputs an image file which is a
heat map of anomalies in a "candidate" image.

Automatic Image Anomaly Detection can be run with Python using [gbdxtools](https://github.com/DigitalGlobe/gbdxtools) or through ESRI Analytics.

### Table of Contents
 * [Quickstart](#quickstart) - Get started!
 * [Inputs](#inputs) - Required and optional task inputs.
 * [Outputs](#outputs) - Task outputs and output structure.
 * [Advanced](#advanced) - Additional information for advanced users.
 * [Runtime](#runtime) - Example estimate of task runtime.
 * [Issues](#issues) - Current or past known issues.
 * [Background](#background) - Background information.
 * [Contact](#contact) - Contact information.

### Quickstart

Quick start example.

```python
# AIADS Example Python
# python aiads.py test_directory 10500100077B2A00 1050410011113800 1030010063143700 10300100649F2800 103001003E418400

from gbdxtools import Interface
import inspect
import time
from os.path import join
import subprocess
import sys

gbdx = Interface()

aop = gbdx.Task("AOP_Strip_Processor")
aop.inputs.data = ['s3://receiving-dgcs-tdgplatform-com/056374187010_01_003',
	's3://receiving-dgcs-tdgplatform-com/056380302010_01_003',
	's3://receiving-dgcs-tdgplatform-com/056374186010_01_003',
	's3://receiving-dgcs-tdgplatform-com/056374188010_01_003',
	's3://receiving-dgcs-tdgplatform-com/056374184010_01_003']

aiads = gbdx.Task("aiads")
aiads.inputs.data_in = aop.outputs.data.value
aiads.inputs.method = "euclidean"
aiads.inputs.metric = "variation_dist"
aiads.inputs.scale = "3"
aiads.inputs.threshold = "0.1"
# aiads.inputs.target = target

workflow = gbdx.Workflow([aop, aiads])

# order.timeout = 36000
aop.timeout = 36000
aiads.timeout = 36000
workflow.savedata(aiads.outputs.data_out, location='Akejohnson_Files/SIMILARITY/Test1')
    # execute

workflow.execute()

print workflow.id
print workflow.status
```

### Inputs

The following table lists all taskname inputs.
Mandatory (optional) settings are listed as Required = True (Required = False).

  Name  |  Required  |  Default  |  Valid Values  |  Description  
--------|:----------:|-----------|----------------|---------------
inputshere


### Outputs

The following table lists all taskname outputs.
Mandatory (optional) settings are listed as Required = True (Required = False).

  Name  |  Required  |  Default  |  Valid Values  |  Description
--------|:----------:|-----------|----------------|---------------
outputshere

**Output structure**

Explain output structure via example.


### Advanced
Include example(s) with complicated parameter settings and/or example(s) where
taskname is used as part of a workflow involving other GBDX tasks.



### Issues
List known past/current issues with taskname (e.g., version x does not ingest vrt files).


### Background
For background on the development and implementation of taskname see [here](Insert link here).


### Contact
Tech Owner: [Ray Richardson](ray@simularity.com) @ SIMULARITY

Document Owner: [Kathleen Johnson](kajohnso@digitalglobe.com)



