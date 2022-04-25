from moya.messaging import API
from moya.argtypes import setup_argparse

parser = setup_argparse("Look up information about a single user", include_job_id=False, include_priority=False, include_deduplicate=False)
parser.add_argument("item", help="Number or DID")
args = parser.parse_args()

api = API(args.token, args.endpoint)
print(api.lookup_user(args.item))
