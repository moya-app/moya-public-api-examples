from moya.messaging import API
from moya.argtypes import setup_argparse

parser = setup_argparse("Cancel a specific job")
args = parser.parse_args()

api = API(args.token, args.endpoint)
api.cancel_job(args.job_id)
