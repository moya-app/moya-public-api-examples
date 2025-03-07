import argparse
from moya.messaging import API
from moya.argtypes import number_or_file, setup_argparse
from moya.timing import Timer

## Example Usage:
# python bulk-send-message-image.py -p high <API-TOKEN> number_list.txt image.png message.txt

TOTAL_NUMBER_MESSAGES = 10000
BATCH_SIZE = 3000

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

parser = setup_argparse("Bulk send messages to users", include_no_merge=True)
parser.add_argument("numbers", type=number_or_file(batch_size=TOTAL_NUMBER_MESSAGES), help="The number or file of numbers to send to")
parser.add_argument("image", type=argparse.FileType('rb'), help="The image to send")
parser.add_argument("message", type=argparse.FileType('r'), help="A file containing the message to send")
args = parser.parse_args()

api = API(args.token, args.endpoint)

# Upload the image and get its URL
image_url = api.upload_image(args.image)
print(f"Image uploaded to {image_url}")

numbers_list = list(args.numbers)
if numbers_list and isinstance(numbers_list[0], list):
    numbers_list = numbers_list[0]

message_text = args.message.read()

print(f"Job ID: {args.job_id}")

try:
    with open("batch_count.txt", "a") as batch_file:
        batch_file.write(f"Job ID: {args.job_id}\n")
        for batch_count, batch in enumerate(chunks(numbers_list, BATCH_SIZE), start=1):
            timer = Timer()
            print(f"Processing batch #{batch_count} with {len(batch)}")
            batch_file.write(f"Batch #{batch_count}: {batch}\n")
            api.send_image(batch, image_url, job_id=args.job_id, priority=args.priority)
            timer.add_call(len(batch))
            api.send_message(batch, message_text, job_id=args.job_id, priority=args.priority, allow_merge=not args.no_merge)
            timer.end()
            print("Queued %d messages in %0.1f seconds and %d calls. %d/s" % (timer.items_processed, timer.duration, timer.api_calls, timer.items_processed / timer.duration))
except KeyboardInterrupt:
    # Exit cleanly on a keyboard interrupt
    pass
except Exception as e:
    print(e)
