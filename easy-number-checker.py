import argparse
from moya.messaging import API
from moya.argtypes import number_or_file

parser = argparse.ArgumentParser(description="Check which of the given list of numbers are active on the Moya")
parser.add_argument("token", help="API token")
parser.add_argument("numbers", type=number_or_file(3000), help="A file containing numbers one per line")
args = parser.parse_args()

api = API(args.token)

for numbers in args.numbers:
    for number in api.lookup_numbers(numbers):
        print(number)
