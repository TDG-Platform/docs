import json
import os


def export_workflow(gbdx_workflow, filename = "temp.json"):
    """
    Takes an Interface object from gbdxtools
    and builds the workflow json
    """
    if os.path.exists(filename):
	os.remove(filename)
    temp_wf = {"name": gbdx_workflow.name, "tasks": []}

    for task in gbdx_workflow.tasks:
        temp_wf['tasks'].append(task.generate_task_workflow_json())

    with (open(filename,"w")) as ff:
        json.dump(temp_wf, ff, indent = 4, sort_keys=True)
