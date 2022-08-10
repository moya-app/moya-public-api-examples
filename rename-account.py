from moya.messaging import API
from moya.argtypes import setup_argparse

parser = setup_argparse("Rename an account", include_priority=False, include_deduplicate=False, include_job_id=False)
parser.add_argument("name", help="What to rename it to")
args = parser.parse_args()

api = API(args.token, args.endpoint)
print(api.update(name=args.name))
