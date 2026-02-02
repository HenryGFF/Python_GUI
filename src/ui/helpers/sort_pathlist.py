from datetime import datetime
import os

def sort_by_date(pathname):
    filename = os.path.basename(pathname)  # remove diretórios
    name, _ = os.path.splitext(filename)  # remove extensão

    parts = name.split("_")
    day, month, year = parts[-3:]

    return datetime(int(year), int(month), int(day))