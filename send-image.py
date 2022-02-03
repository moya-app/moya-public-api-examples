import argparse
import uuid
from moya.messaging import API
from moya.argtypes import uuid_type, number_or_file

parser = argparse.ArgumentParser(description="Send image to moya users")
parser.add_argument("--job-id", "-j", default=uuid.uuid4(), type=uuid_type, help="The job id to use")
parser.add_argument("token", help="API token")
parser.add_argument("numbers", type=number_or_file(), help="The number or file of numbers to send to")
parser.add_argument("image", type=argparse.FileType('rb'), help="The image to send")
args = parser.parse_args()

api = API(args.token)

image_url = api.upload_image(args.image)
print(f"Image uploaded to {image_url}")
for numbers in args.numbers:
    api.send_image(numbers, image_url, job_id=args.job_id)
