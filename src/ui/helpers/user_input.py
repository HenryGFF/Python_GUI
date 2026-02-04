from .sort_pathlist import sort_by_date

class UserInput(dict):
    def __init__(self, **kwargs):
        super().__init__()

        if kwargs['form_type'] == 'FormA':
            self['date_interval'] = 'single date'
            self['date'] = kwargs['date'].toPython()

        elif kwargs['form_type'] == 'FormB':
            self['date_interval'] = 'period'
            self['start_date'] = kwargs['start_date'].toPython()
            self['end_date'] = kwargs['end_date'].toPython()

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