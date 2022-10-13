from moya.messaging import API
from moya.argtypes import setup_argparse

parser = setup_argparse("Show token info", include_job_id=False, include_priority=False, include_deduplicate=False)
args = parser.parse_args()

api = API(args.token, args.endpoint)
print(api.token_info())
