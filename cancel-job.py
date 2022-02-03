import argparse
from moya.messaging import API
from moya.argtypes import uuid_type

parser = argparse.ArgumentParser(description="Cancel a specific job")
parser.add_argument("token", help="API token")
parser.add_argument("jobid", type=uuid_type, help="The job id to use")
args = parser.parse_args()

api = API(args.token)
api.cancel_job(args.jobid)
