# Use like python3 send-templated-messages.py <token> test-bulk.csv test-template.j2
import argparse
import uuid
import time

from jinja2 import Environment, FileSystemLoader

from moya.messaging import API
from moya.argtypes import setup_argparse
from moya.numbers import csv_reader
from moya.timing import Timer

parser = setup_argparse("Bulk send templated messages to moya users")
parser.add_argument("csv", type=argparse.FileType('r'), help="A CSV with a header containing the names of the variables with one column called `to` containing the numbers to send to")
parser.add_argument("template", type=str, help="A file containing a j2 template of the message to send")
args = parser.parse_args()

api = API(args.token, args.endpoint)

# Setup j2
j2env = Environment(loader=FileSystemLoader("."))
template = j2env.get_template(args.template)

print(f"Job ID: {args.job_id}")

timer = Timer()

try:
    for items in csv_reader(args.csv, dp=args.deduplicate):
        messages = [(to, template.render(**variables)) for to, variables in items]

        api.bulk_send_messages(messages, job_id=args.job_id, priority=args.priority)
        timer.add_call(len(messages))
        print(f"Sent up to number {items[-1][0]}")
except KeyboardInterrupt:
    # Don't kill the whole process, exit cleanly
    pass
except Exception as e:
    print(e)

timer.end()
print("")
print("Queued %d messages in %0.1f seconds and %d calls. %d/s" % (timer.items_processed, timer.duration, timer.api_calls, timer.items_processed / timer.duration))
