from moya.messaging import API
from moya.argtypes import setup_argparse

parser = setup_argparse("Cancel a specific job", include_priority=False, include_deduplicate=False)
args = parser.parse_args()

api = API(args.token, args.endpoint)
api.cancel_job(args.job_id)
