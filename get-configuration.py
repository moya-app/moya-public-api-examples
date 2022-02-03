import argparse
from moya.messaging import API

parser = argparse.ArgumentParser(description="Print details about the account's configuration")
parser.add_argument("token", help="API bot token")
args = parser.parse_args()

api = API(args.token)
print(api.get_configuration())
