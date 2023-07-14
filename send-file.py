import argparse
from moya.messaging import API
from moya.argtypes import number_or_file, setup_argparse

parser = setup_argparse("Send file to moya users")
parser.add_argument("file", type=argparse.FileType('rb'), help="The file to send")
parser.add_argument("numbers", nargs='?', type=number_or_file(), help="The number or file of numbers to send to")
args = parser.parse_args()

api = API(args.token, args.endpoint)

file_url = api.upload_file(args.file)
print(f"File uploaded to {file_url}")
if args.numbers:
    for numbers in args.numbers:
        api.send_file(numbers, file_url, job_id=args.job_id, priority=args.priority)
