import argparse
from moya.messaging import API
from moya.argtypes import setup_argparse

parser = setup_argparse("Print details about the account's configuration", include_job_id=False, include_priority=False)
args = parser.parse_args()

api = API(args.token, args.endpoint)
print(api.get_configuration())
