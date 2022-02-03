import uuid
import os
from moya.numbers import file_reader, is_number

def uuid_type(data):
    return uuid.UUID(data)

def number_or_file(batch_size=10000):
    def fn(item):
        """
        If item is a file, open it for batch processing, otherwise if it is a number then return it.
        """
        if os.path.exists(item):
            fh = open(item, 'r')
            return file_reader(fh, batch_size)
        elif is_number(item):
            return [[item]]

        raise Exception(f"{item} is neither a number nor a file of numbers")

    return fn
