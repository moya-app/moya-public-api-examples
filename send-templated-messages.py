# Use like python3 send-templated-messages.py <token> test-bulk.csv test-template.j2
import argparse
import uuid
import time

from jinja2 import Environment, FileSystemLoader

from moya.messaging import API
from moya.argtypes import uuid_type
from moya.numbers import csv_reader

parser = argparse.ArgumentParser(description="Bulk send templated messages to moya users")
parser.add_argument("--job-id", "-j", default=uuid.uuid4(), type=uuid_type, help="The job id to use")
parser.add_argument("token", help="API token")
parser.add_argument("csv", type=argparse.FileType('r'), help="A CSV with a header containing the names of the variables with one column called `to` containing the numbers to send to")
parser.add_argument("template", type=str, help="A file containing a j2 template of the message to send")
args = parser.parse_args()

api = API(args.token)

# Setup j2
j2env = Environment(loader=FileSystemLoader("."))

template = j2env.get_template(args.template)

print(f"Job ID: {args.job_id}")

calls = 0
sent = 0
start_time = time.time()

try:
    for items in csv_reader(args.csv):
        messages = [(to, template.render(**variables)) for to, variables in items]

        api.bulk_send_messages(messages, job_id=args.job_id)
        sent += len(items)
        calls += 1
        print(f"Sent up to number {items[-1][0]}")
except KeyboardInterrupt:
    # Don't kill the whole process, exit cleanly
    pass
except Exception as e:
    print(e)

print("")
duration = time.time() - start_time
print("Queued %d messages in %0.1f seconds and %d calls. %d/s" % (sent, duration, calls, sent / duration))
