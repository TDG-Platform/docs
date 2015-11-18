## Basic usage

1. Their are two basic usages of the RoadTracker tasks in GBDX. The first usage is to produce support files so that the 
resulting files can be used by the client ArcMap/QGIS plugin for digitization. The second usage is to produce a fully 
automated extraction or update of specified features. 
  * To run the automated extraction task you need to first have the support files built. If the support files are not 
already built, they can be built in conjunction by running a workflow with both tasks.    

## Here are some example workflows

* Example workflow to build support files for all of the features for every tif file that is in the input directory.
(Notice the filename field is set to False.)

[example_workflow_supportfilesAll.json](example_workflow_supportfilesAll.json)

* Example workflow to build support files for all of the features for a specified input file.
(Notice the filename field is set to filename.)

[example_workflow_supportfilesOne.json](example_workflow_supportfilesOne.jsone)

* Example workflow to build support files for one feature for all the tifs in the input directory.
(Notice the featuretype field.)

[example_workflow_supportfilesOneFeature.json](example_workflow_supportfilesOneFeature.jsons)

* Example workflow for an automated run filling in missing features (base run if no vectors exist in the beginning).

[example_workflow_automatedDU.json](example_workflow_automatedDU.json)

* Example workflow for a combined support generation and automated run.

[example_workflow_automatedDU.json](example_workflow_automatedDU.json)

## Different feature modes that RoadTracker can handle

1. Dirt Urban - Clustered areas where the streets are dirt or dirty. This is also good when you don't know any better
2. trails - features that are 10 meters or less in width (unless very low resolution imagery) that are light compared to its background. ability to be more free form.
3. rivers - same as trails except dark compared to background. There is some more filtering here to try and capture dark rivers.
4. suburban - Intended to pick up roads/features that have low textures
5. Oil Fields - intended to pick up dirt roads that access oil fields.

