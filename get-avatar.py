import argparse
from requests import HTTPError
from moya.messaging import API
from moya.argtypes import setup_argparse

parser = setup_argparse("Save the accounts avatar to a file", include_job_id=False, include_priority=False)
parser.add_argument("output", type=argparse.FileType('wb'), help="Path to save to")
args = parser.parse_args()

api = API(args.token, args.endpoint)
try:
    image = api.get_avatar()
    args.output.write(image)
    print("Avatar written to file")
except HTTPError as e:
    if e.response.status_code == 404:
        print("Avatar not set for this account")
    else:
        raise e
