import argparse
from moya.messaging import API
from moya.argtypes import number_or_file, setup_argparse
from moya.timing import Timer

parser = setup_argparse("Bulk send messages to moya users")
parser.add_argument("numbers", type=number_or_file(), help="The number or file of numbers to send to")
parser.add_argument("message", type=argparse.FileType('r'), help="A file containing the message to send")
args = parser.parse_args()

api = API(args.token, args.endpoint)

message_text = args.message.read()

print(f"Job ID: {args.job_id}")

timer = Timer()

try:
    for numbers in args.numbers:
        api.send_message(numbers, message_text, job_id=args.job_id, priority=args.priority)
        timer.add_call(len(numbers))
        print(f"Sent up to number {numbers[-1]}")
except KeyboardInterrupt:
    # Don't kill the whole process, exit cleanly
    pass
except Exception as e:
    print(e)

timer.end()
print("")
print("Queued %d messages in %0.1f seconds and %d calls. %d/s" % (timer.items_processed, timer.duration, timer.api_calls, timer.items_processed / timer.duration))
