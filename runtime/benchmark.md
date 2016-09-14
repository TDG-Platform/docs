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
QB   | Pan - 0.61m MS – 2.44m |41,551,668(ms)| 312.07|  460.603| 1.4
WV01 |Pan - 0.5|1,028,100,320(pan)| 351.72| 475.276| 1.35
WV02|Pan - 0.5m MS – 2 m |35,872,942(ms)| 329.87| 651.095| 1.97
WV02|Pan – 0.31.m MS – 1.24m |35,371,971(ms)| 196.27| 655.671| 3.34
WV03|Pan – 0.31.m MS – 1.24m |57,498,000(ms)| 332.97| 560.836| 1.68

6	Features not to be tested
The runtime tests will not be exhaustive tests of all parameters of a task and possible workflow combinations. When possible, default values will be utilized to minimize complexity. The runtime of a single task will be tested and averaged.  Further, the tests will not include external sensors or imagery (e.g. Rapid Eye).

Each task requires different testing types. As the organization and usability of gbdxtools and the Web App evolve, automation will be developed to replace manual testing. However, automated tests cannot cover all user scenarios; hence, manual tests will continue to be executed throughout the GBDX platform lifecycle. 
6.1	Automated Testing
Automation testing is critical to the success of products in the market. Most manual tests have to be re-executed repeatedly during development, so automating these repetitive test cases will save time and money. Specifically, tests should be re-executed whenever source code is modified. By automating these repeated tests, time is given back to GAC engineers to develop more detailed test cases that add to the depth of the testing coverage.

All GBDX tasks will eventually be tested through automated methods.  However, the method of automation and suite of tests require further design and consideration before developing a Continuous Integration test environment.  

The Algorithm Curation team currently has two high-level processes for creating automation test cases: 
•	Simply automating the execution of the gbdxtools scripts running from command-line with pre-defined parameters, configurations, and inputs that are hard-coded into script format for repetitive execution.
•	Developing automated testing through the documentation, whereby scripts within the documentation are run and tested for completion.  This method of automated testing will require additional curation of the task json workflow but will test the task, gbdxtools and the documentation for functionality.

All automated tests for the GBDX tasks can be described in one of these types of tests: 
•	Unit testing 
•	Functional testing 
•	Regression testing
•	Performance testing

Each product requires different testing types. For this release, only manual tests will be executed from only a user-level perspective. No automation tests will be developed since our release timeframe is extremely short.
6.2	Manual Testing
Manual software testing is performed by a human carefully going through the workflow of the product, trying various usage and input combinations, comparing the results to the expected behavior and recording their observations. 

The GAC team will document and execute manual test cases to check functionality of each task within the gbdx archive of tasks. Manual tests will initially cover a wide array of types that include the following:

•	Functional – verifying features work
•	Integration – test products that are integrated into a larger system/platform
•	Regression – seeks to find new defects in already tested, functional areas
•	End-to-End – verifying user scenarios of a product from start to finish
•	Performance – testing how a product performs in terms of runtime

Most of these manual tests will be executed as if we were operators of the product. All tests will be executed within the GBDX Platform. Each manual testing type is described in detail below.
6.2.1	Functional – Verifying features work
This type of manual testing is the most common type of testing the GAC team will execute. A GAC engineer methodically goes through all the actions available to the customer and verifies correct behavior. This type of testing only verifies correct or valid functionality.

Example Functional Test –
Verify that if a task is in GBDX Catalogue, that it can be run on sample imagery with gbdxtools after being processed through AOP_Strip_Processor or Acomp.

6.2.2	GBDX Integration – Test products that are integrated into a platform
Integration testing is the verification of correct interaction between multiple units/components of software that are part of a larger system. This type of manual testing requires the tasks be deployed to GBDX and also requires a fully functional GBDX/IIP environment is functional ready for integration. GAC will verify that our integration is seamless and workflows are stable and easy to run.

For GBDX integration testing, here are some example test cases that will be executed:
	Verify our use of the GBDX Workflow API is working correctly.
	Verify Docker deployments are complete and stable.
	Verify image ordering by catalogue ID from factory.
	Verify images ordered from the factory can be run thru Fastortho and Acomp with the output of those components resulting in a valid file format consumable by the PMP product.
	Verify exports of all output data types out of the GBDX S3 environment are successful.
6.2.3	Regression – Seeks to find new defects in already tested, functional areas
Experience has shown that as releases are produced and software is fixed, the emergence of new and/or reemergence of old issues is common. The purpose of regression testing is to uncover software errors and insure the latest version of a product continues to run successfully.  Also, regression testing provides a general assurance that additional errors were not introduced in the latest build.  

