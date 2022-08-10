import argparse
from requests import HTTPError
from moya.messaging import API
from moya.argtypes import setup_argparse

parser = setup_argparse("Modify the accounts profile picture", include_job_id=False, include_priority=False, include_deduplicate=False)
parser.add_argument("avatar", type=argparse.FileType('rb'), help="Path to new image")
args = parser.parse_args()

api = API(args.token, args.endpoint)
# TODO: Detect png/webp/jpg appropriately
api.set_avatar(args.avatar, 'image/jpeg')
