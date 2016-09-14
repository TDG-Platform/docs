Test Goals/Objectives
Our main test goal for the GBDX tasks is to develop a set of average runtimes for each task.  We will identify a baseline for each task (algorithm) at the atomic task level in GBDX.  A set of applicable calibration images will be utilized for the test.

A secondary objective is to provide a set of python test scripts which will support automated testing of gbdx tasks using gbdxtools.  These scripts will be included in the GitHUB and GBDX university documentation and provide gbdx consumers with examples of how to run a task. 

Definitions
CI environment - is the practice of merging all developer working copies to a shared mainline several times a day.

GAC – Geospatial Big data Algorithm Curation team – Team responsible for curation and documentation of tasks on the GBDX platform.

GBDX – Geospatial Big Data Platform – Digital Globe’s GBDX platform provides customers with a fast and easy way to search, order, and process images and their data. The Digital Globe, Inc. platform or ecosystem is where consumers and producers of geospatial and image based algorithms (Tasks) interact.

GBDX tasks – Algorithms available on the GBDX platform – this refers to a single algorithm and not a string of algorithms which is known as a workflow

GBDX Rest API – You can use GBDX's REST APIs and services to search the catalog, order imagery data, run tasks and workflows, access your AWS S3 bucket, and much more.

gbdxtools – gbdxtools is a package for ordering imagery and launching workflows on Digital Globe’s GBDX platform.  

GBDX University - A library of resources to help you get the most value out of the GBDX platform.	

GBDX- Web App – The web application is a graphical user interface (GUI) where you can define your area of interest, create material sets, and process imagery data.
Areas to be tested
Within GBDX list of tasks tested for correct functionality, the following task categories will be tested:
ENVI tasks
Preprocessing tasks
Image mining/ analytic tasks 
Third party tasks
Each task will be tested with applicable imagery and settings.  The test results will be normalized based on a runtime per geographic area.  These metrics will be reported within each task document in the format shown in Table 1. 

Table 1. Example results of AOP_Strip_Processor task


Sensor     |  Resolution |  Total Pixels |  Total Area k2 | Runtime (Min.Sec)| Runtime (Min/Area k2)
-----------|:-----------:|----------------|---------------|------------------|--------------------
QB   | Pan - 0.61m MS – 2.44m |41,551,668| 312.07|  460.603| 1.48
   | S3 URL | S3 location of input .tif file processed through AOP_Strip
WV01 |  N/A  |     string of index name        |
WV02|
WV02|
WV03|
