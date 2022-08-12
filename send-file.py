import argparse
from moya.messaging import API
from moya.argtypes import number_or_file, setup_argparse

parser = setup_argparse("Send file to moya users")
parser.add_argument("numbers", type=number_or_file(), help="The number or file of numbers to send to")
parser.add_argument("file", type=argparse.FileType('rb'), help="The file to send")
args = parser.parse_args()

api = API(args.token, args.endpoint)

file_url = api.upload_file(args.file)
print(f"Image uploaded to {file_url}")
for numbers in args.numbers:
    api.send_file(numbers, file_url, job_id=args.job_id, priority=args.priority)
