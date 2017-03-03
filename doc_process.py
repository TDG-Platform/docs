import os.path
from gbdxtools import Interface
import json


def get_default(description):
    """Find the default value stated in the description.
      If there is no default value, return None
    """
    ind1 = description.find('Default is')
    if ind1 == -1: return
    ind2 = description.find('.', ind1) # Find the first period.
    return description[ind1+len('Default is')+1:ind2]

# This data object will initially contain the names of all of the tasks. Further on, it will load
# the status of the tests, and the content for the markdown document.
# The associated files (markdown and example code) will be named using the task name in this list.
list_of_tasks = [
                    {'name': 'ENVI_ImageBandDifference:0.0.2'}

                ]

list_of_steps = {
                    'create_md': True,
                    'run_tests': True
                }

# This is a list of passing values for the test of the example code.
# If anything else is returned, the test fails and the code is not loaded.
wf_pass_list = ['pending', 'running']

# If the test of the example code fails, this is the text that is loaded into the code block.
# fail_string = '\n# I tried to run, but I failed. So, NO CODE FOR YOU!.\n'

fail_string = """

        Example didn't run?

        You're Code Is Dead To Me...


                       ...
                     ;::::;
                   ;::::; :;
                 ;:::::'   :;
                ;:::::;     ;.
               ,:::::'       ;           OOO
               ::::::;       ;          OOOOO
               ;:::::;       ;         OOOOOOOO
              ,;::::::;     ;'         / OOOOOOO
            ;:::::::::`. ,,,;.        /  / DOOOOOO
          .';:::::::::::::::::;,     /  /     DOOOO
         ,::::::;::::::;;;;::::;,   /  /        DOOO
        ;`::::::`'::::::;;;::::: ,#/  /          DOOO
        :`:::::::`;::::::;;::: ;::#  /            DOOO
        ::`:::::::`;:::::::: ;::::# /              DOO
        `:`:::::::`;:::::: ;::::::#/               DOO
         :::`:::::::`;; ;:::::::::##                OO
         ::::`:::::::`;::::::::;:::#                OO
         `:::::`::::::::::::;'`:;::#                O
          `:::::`::::::::;' /  / `:#
           ::::::`:::::;'  /  /   `#

"""

# The location of the template file.
markdown_template_file_name = '/Users/creeder/Documents/auto-docs/DOCUMENT_TEMPLATE.md'

# Text that is loaded into the markdown after the text from the API for the task description.
description_footer_text = 'This task can be run with Python using ' \
                          '[gbdxtools](https://github.com/DigitalGlobe/gbdxtools) or through the ' \
                          '[GBDX Web Application](https://gbdx.geobigdata.io/materials/)'

# Text that is loaded into the markdown after the section title, but before the code, for the quickstart example.
quickstart_header_test = 'Quick start example.'

# Text that is loaded into the markdown after the section title, but before the code, for the advanced example.
advanced_header_test = 'Include example(s) with complicated parameter settings and/or example(s) where the task is ' \
                       'used as part of a workflow involving other GBDX tasks.'

# Text that is loaded into the markdown after the section title, but before the inputs from the API,
# for the inputs section.
inputs_header = 'The following table lists all taskname inputs.\n' \
                'Mandatory (optional) settings are listed as Required = True (Required = False).\n\n' \
                '  Name  |  Required  |  Default  |  Valid Values  |  Description  \n' \
                '--------|:----------:|-----------|----------------|---------------'

# Text that is loaded into the markdown after the section title, but before the inputs from the API,
# for the outputs section.
outputs_header = 'The following table lists all taskname outputs.\n' \
                 'Mandatory (optional) settings are listed as Required = True (Required = False).\n\n' \
                 '  Name  |  Required  |  Default  |  Valid Values  |  Description  \n' \
                 '--------|:----------:|-----------|----------------|---------------'


# Instantiating the GBDx Tools Interface
gbdx = Interface()

# Getting a list of known tasks on GBDx as we don't want to error when we query for the task description.
known_tasks = gbdx.task_registry.list()
print known_tasks

# Loop through the list of tasks and mark whether the docs/code/GBDx task already exist,
# create the expected file names for easy reference later, and, if the task has a quickstart or an advanced example,
# load that module so we can call the function to test that it passes
for i in list_of_tasks:

    i['markdown'] = False
    i['quickstart'] = False
    i['advanced'] = False
    i['knowntask'] = False

    # Build the expected markdown file name as we need this regardless of whether it already exists
    i['markdown_file_name'] = '%s.md' % i['name']

    # Check to see if the markdown file exists already so we don't overwrite it
    if os.path.isfile(i['markdown_file_name']) is True:
        i['markdown'] = True

    # Check to see if the task is a known task on GBDx
    if i['name'] in known_tasks:
        i['knowntask'] = True

    # Check to see if there is a quickstart python file. If so, build the expected file names and
    # load the module for testing
    if os.path.isfile('%s_qs.py' % i['name']) is True:
        i['quickstart'] = True
        i['quickstart_name'] = '%s_qs' % i['name']
        i['quickstart_file_name'] = '%s_qs.py' % i['name']
        i['quickstart_pass'] = False
        module_obj = __import__(i['quickstart_name'])
        globals()[i['quickstart_name']] = module_obj

    # Check to see if there is an advanced python file. If so, build the expected file names and
    # load the module for testing
    if os.path.isfile('%s_adv.py' % i['name']) is True:
        i['advanced'] = True
        i['advanced_name'] = '%s_adv' % i['name']
        i['advanced_file_name'] = '%s_adv.py' % i['name']
        i['advanced_pass'] = False
        module_obj = __import__(i['advanced_name'])
        globals()[i['advanced_name']] = module_obj

# This section of code will test the python code for quickstart and advanced examples.
if list_of_steps['run_tests'] is True:
    # For each task that has a quickstart or an advanced example, call the function and load the test results
    for i in list_of_tasks:
        for j in ['quickstart', 'advanced']:
            if i[j] is True:

                # Run the function to test the example code
                r = globals()[i['%s_name' % j]].runfunction()

                # Store the workflow id in case we want to run a long running test (did the workflow actually finish)
                i['%s_wfid' % j] = r['wfid']

                # Get the status and check against the list of possible passing values
                i['%s_wfst' % j] = r['wfst']
                if i['%s_wfst' % j] in wf_pass_list:
                    i['%s_pass' % j] = True
# If we don't run the tests, then we simply assume that they passed and populate that value in the data object
else:
    for i in list_of_tasks:
        for j in ['quickstart', 'advanced']:
            if i[j] is True:
                i['%s_wfid' % j] = 1
                i['%s_wfst' % j] = 'pending'
                i['%s_pass' % j] = True


# The remainder of the code is pulling information to load into the markdown and creating th enew markdown file.
# If we are not going to create the markdown, there is no need to run this code
if list_of_steps['create_md'] is True:
    # For each task that has example code and passes the test, read in the example code and store for inclusion in the
    # markdown document
    for i in list_of_tasks:
        for j in ['quickstart', 'advanced']:
            # If there is a quickstart of advanced example, check if the code passed the test
            if i[j] is True:
                # If the test passed, get the code
                if i['%s_pass' % j] is True:

                    with open(i['%s_file_name' % j]) as f:
                        s = f.read()

                    start = s.index('try:') + len('try:')
                    end = s.index('    except:', start)

                    i['%s_text' % j] = s[start:end]

                    # Because this code is within a function and within a try/except, it has two more tabs per line
                    # and a few extra lines than it needs in the displayed example.
                    # This code removes the additional tabs and lines for the code that will be displayed in the markdown.
                    i['%s_text' % j] = i['%s_text' % j].replace('\n        ', '\n')
                    i['%s_text' % j] = i['%s_text' % j].replace('\n\n', '\n')

                # If the test failed, don't load the code into the docs. Load the default failed message.
                else:

                    i['%s_text' % j] = fail_string

    # For each task that is known to exist on GBDx already, hit the API and get the task details
    for i in list_of_tasks:
        if i['knowntask'] is True:
            # retrieve task info and store it in the task data object
            task = gbdx.Task(i['name'])
            i['description'] = task.definition['description']
            i['input_ports'] = task.input_ports
            i['output_ports'] = task.output_ports

        list_of_steps = {
            'create_md': True,
            'run_tests': True
        }

    # Now that we have all of the information we need, we can write it to the markdown file for each task in the list.
    for i in list_of_tasks:
        # We don't create markdowns for tasks that are not on GBDx
        if i['knowntask'] is True:
            # If the markdown file already exists, read it in
            if i['markdown'] is True:
                with open(i['markdown_file_name']) as f:
                    s = f.read()
            # If not, we start with the template
            else:
                with open(markdown_template_file_name) as f:
                    s = f.read()

            # Replace instances of "taskname" in the template with the actual task name
            # Note that this will prepare the document with the correct task name on the first run as it will use the
            # template.
            # On subsequent runs, this will not actually make any changes as the task name will already be in the
            # markdown file and the "taskname" phrase will not.
            s = s.replace('taskname', i['name'])

            # This code will replace anything between the Description and Table of Contents sections with the
            # description text from the tasks API response.
            # Note the use of the footer, which is defined at the start of this code.
            if i['knowntask'] is True:
                start = s.index('### Description') + len('### Description')
                end = s.index('### Table of Contents', start)
                ins_str = '\n%s\n\n%s\n\n' % (i['description'], description_footer_text)
                s = s[:start] + ins_str + s[end:]

            # This code will replace anything between the Inputs and Outputs sections with the inputs from the
            # API response
            # Note the use of the header, which is defined at the start of this code.
            if i['knowntask'] is True:
                start = s.index('### Inputs') + len('### Inputs')
                end = s.index('### Outputs', start)
                port_strings = []
                for p in i['input_ports']:
                    default = get_default(p['description'])
                    if not default:
                        default = 'None'
                    port_strings.append('|'.join([p['name'],
                                                  str(p['required']),
                                                  default,
                                                  ' ',
                                                  p['description']]))
                ins_str = '\n%s\n%s\n\n' % (inputs_header, '\n'.join(port_strings))
                s = s[:start] + ins_str + s[end:]

            # This code will replace anything between the Outputs and Output structure sections with the outputs from the
            # API response
            # Note the use of the header, which is defined at the start of this code.
            if i['knowntask'] is True:
                start = s.index('### Outputs') + len('### Outputs')
                end = s.index('**Output structure**', start)
                port_strings = []
                for p in i['output_ports']:
                    default = get_default(p['description'])
                    if not default:
                        default = 'None'
                    port_strings.append('|'.join([p['name'],
                                                  str(p['required']),
                                                  default,
                                                  ' ',
                                                  p['description']]))
                ins_str = '\n%s\n%s\n\n' % (outputs_header, '\n'.join(port_strings))
                s = s[:start] + ins_str + s[end:]

            # This code will replace anything between the Quickstart and Inputs sections with the quickstart example code
            # Note the use of the header, which is defined at the start of this code.
            if i['quickstart'] is True:
                start = s.index('### Quickstart') + len('### Quickstart')
                end = s.index('### Inputs', start)
                ins_str = '\n%s\n\n%s%s%s\n\n' % (quickstart_header_test, "```python", i['quickstart_text'], "```")
                s = s[:start] + ins_str + s[end:]

            # This code will replace anything between the Advanced and Issues sections with the advanced example code
            # Note the use of the header, which is defined at the start of this code.
            if i['advanced'] is True:
                start = s.index('### Advanced') + len('### Advanced')
                end = s.index('### Issues', start)
                ins_str = '\n%s\n\n%s%s%s\n\n' % (advanced_header_test, "```python", i['advanced_text'], "```")
                s = s[:start] + ins_str + s[end:]

            # This code writes the modified contents to the new markdown file, replacing the old file if it is present.
            with open(i['markdown_file_name'], 'w') as f:
                f.write(s)


# TODO: We should either dump out some JSON here or create a report of what made and what failed
# and output that as a log file. For now, I'm just printing the data object.


report = []

# report = [
#             {
#                 'tasn name one': {
#                             'Markdown generated': True,
#                             'Quickstart esists': True,
#                             'Quickstart passed': False,
#                             'Advanced esists': True,
#                             'Advanced passed': False
#
#                             }
#             },
#             {
#                 'tasn name two': {
#                             'Markdown generated': True,
#                             'Quickstart esists': True,
#                             'Quickstart passed': False,
#                             'Advanced esists': True,
#                             'Advanced passed': False
#
#                         }
#             }
#         ]

for i in list_of_tasks:
    temp = {
        i['name']: {
                    'Markdown generated': True
                    }
    }

    if i['quickstart'] is True:
        temp[i['name']]['Quickstart code esists'] = i['quickstart']
        temp[i['name']]['Quickstart code passed'] = i['quickstart_pass']

    if i['advanced'] is True:
        temp[i['name']]['Advanced code esists'] = i['advanced']
        temp[i['name']]['Advanced code passed'] = i['advanced_pass']

    report.append(temp)


print 'Document Creation Report: \n'
print(json.dumps(report, sort_keys=False, indent=4))

# print(json.dumps(list_of_tasks, sort_keys=False, indent=4))
