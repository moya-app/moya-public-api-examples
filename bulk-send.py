import argparse
import uuid
import time
from moya.messaging import API
from moya.argtypes import uuid_type, number_or_file

parser = argparse.ArgumentParser(description="Bulk send messages to moya users")
parser.add_argument("--job-id", "-j", default=uuid.uuid4(), type=uuid_type, help="The job id to use")
parser.add_argument("token", help="API token")
parser.add_argument("numbers", type=number_or_file(), help="The number or file of numbers to send to")
parser.add_argument("message", type=argparse.FileType('r'), help="A file containing the message to send")
args = parser.parse_args()

api = API(args.token)

message_text = args.message.read()

print(f"Job ID: {args.job_id}")

calls = 0
sent = 0
start_time = time.time()

try:
    for numbers in args.numbers:
        api.send_message(numbers, message_text, job_id=args.job_id)
        sent += len(numbers)
        calls += 1
        print(f"Sent up to number {numbers[-1]}")
except KeyboardInterrupt:
    # Don't kill the whole process, exit cleanly
    pass
except Exception as e:
    print(e)

print("")
duration = time.time() - start_time
print("Queued %d messages in %0.1f seconds and %d calls. %d/s" % (sent, duration, calls, sent / duration))
