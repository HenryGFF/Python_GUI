from .sort_pathlist import sort_by_date
from .bacen_request import get_ptax_single_date, get_ptax_period

class UserInput(dict):
    def __init__(self, **kwargs):
        super().__init__()

        if kwargs['form_type'] == 'FormA':
            self['date_interval'] = 'single date'
            self['date'] = kwargs['date'].toPython()
            self['ptax_diaria'] = get_ptax_single_date(self['date'])

        elif kwargs['form_type'] == 'FormB':
            self['date_interval'] = 'period'
            self['start_date'] = kwargs['start_date'].toPython()
            self['end_date'] = kwargs['end_date'].toPython()
            self['ptax_diaria'] = get_ptax_period(self['start_date'], self['end_date'])

        self['file_lists'] = split_file_fields(kwargs['file_fields'])

def split_file_fields(file_fields):
    file_lists: list[dict] = []
    for field in file_fields.values():
        pathlist: list[str] = field.value()
        pathlist.sort(key=sort_by_date)

        obj: dict = {
            'label': field.label.text(),
            'pathlist': pathlist
        }
        file_lists.append(obj)

    return file_lists