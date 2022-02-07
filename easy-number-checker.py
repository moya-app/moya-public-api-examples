from moya.messaging import API
from moya.argtypes import number_or_file, setup_argparse

parser = setup_argparse("Check which of the given list of numbers are active on the Moya", include_job_id=False)
parser.add_argument("numbers", type=number_or_file(3000), help="A file containing numbers one per line")
args = parser.parse_args()

api = API(args.token, args.endpoint)

for numbers in args.numbers:
    for number in api.lookup_numbers(numbers):
        print(number)
