from datetime import datetime
from collections import namedtuple

_START_STATE = 'running'
_END_STATE = 'complete'
_STATES = {_START_STATE: 'start', _END_STATE: 'end'}


def timedelta(start, end):
    """
    Return Runtime in seconds.

    Timestamp format:  2017-04-27T17:33:57.395030+00:00
    * Remove timezone, not required
    """
    fmt = '%Y-%m-%dT%H:%M:%S.%f'
    starttime = datetime.strptime(start.split('+')[0], fmt)
    endtime = datetime.strptime(end.split('+')[0], fmt)
    if endtime > starttime:
        return (endtime - starttime).total_seconds()
    else:
        raise ValueError('Start time is greater than end time.')


def convert(dictionary):
    return namedtuple('GenericDict', dictionary.keys())(**dictionary)


def get_task_runtime(events, taskname):
    """Run time for a single task."""
    events = filter(
        lambda x: taskname in x['task'] and x['state'] in _STATES.keys(),
        events
    )

    timestamps = {_STATES[e['state']]: e['timestamp'] for e in events}

    runt = timedelta(**timestamps)
    print('Runtime for task %s: %s seconds' % (taskname, runt))
    return runt


def runtime(workflow_obj, task_name=None):
    # Check Status
    wf_status = convert(workflow_obj.status)
    if wf_status.state == 'running' or wf_status.event == 'failed':
        print('Workflow is either not complete or failed')
        return None

    events = workflow_obj.events

    if task_name:
        # Return single runtime
        return get_task_runtime(events, task_name)
    else:
        # Return runtime for all tasks
        task_names = [t.name for t in workflow_obj.tasks]
        runtimes = {}
        for task in task_names:
            runtimes[task] = get_task_runtime(events, task)
        return runtimes
