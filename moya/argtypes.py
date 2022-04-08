import argparse
import uuid
import os
from moya.numbers import file_reader, is_number

def uuid_type(data):
    return uuid.UUID(data)

def setup_argparse(description, include_job_id=True, include_priority=True):
    parser = argparse.ArgumentParser(description="Send image to moya users")
    parser.add_argument("--endpoint", "-e", default="https://api.moya.app", help="The endpoint to use")
    if include_priority:
        parser.add_argument("-p", "--priority", choices=("low", "medium", "high"), default="low", help="The send priority")
    if include_job_id:
        parser.add_argument("--job-id", "-j", default=uuid.uuid4(), type=uuid_type, help="The job id to use")

    # First parameter, token, is always required
    parser.add_argument("token", help="API token")

    return parser

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
