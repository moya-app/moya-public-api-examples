import argparse
import os

from cryptography.exceptions import InvalidTag

from moya.aesgcm import download, encrypt, to_aesgcm_url
from moya.argtypes import number_or_file, setup_argparse
from moya.messaging import API

# Uploaded with upload_image (upload_file refuses them) and shown inline in the chat once downloaded;
# any other extension is uploaded and sent as a file
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"}

parser = setup_argparse("Encrypt a file and send it to moya users")
parser.add_argument("--verify", action="store_true", help="Download the upload again and check that it decrypts (proves the upload is intact, not that it was delivered)")
parser.add_argument("file", type=argparse.FileType('rb'), help="The file to encrypt and send")
parser.add_argument("numbers", nargs='?', type=number_or_file(), help="The number or file of numbers to send to")
args = parser.parse_args()

api = API(args.token, args.endpoint)

plaintext = args.file.read()
ciphertext, iv_key = encrypt(plaintext)

# Keep the real extension: the app decides how to show the file from the extension in the URL
filename = os.path.basename(args.file.name)
kind = "image" if os.path.splitext(filename)[1].lower() in IMAGE_EXTENSIONS else "file"
upload = api.upload_encrypted_image if kind == "image" else api.upload_encrypted_file
https_url = upload(filename, ciphertext)
print(f"Encrypted {kind} uploaded to {https_url}")

aesgcm_url = to_aesgcm_url(https_url, iv_key)

if args.verify:
    try:
        intact = download(aesgcm_url) == plaintext
    except InvalidTag:
        intact = False
    if not intact:
        raise SystemExit("Uploaded file did not decrypt to the original")
    print("Upload decrypts correctly")

if args.numbers:
    for numbers in args.numbers:
        api.send_file(numbers, aesgcm_url, job_id=args.job_id, priority=args.priority, type=kind)

# The key is only in this URL: anyone holding it can read the file until it expires, and it will end up in
# your shell history or CI logs if you print it there. Store it like a password if you need to resend the file.
print(f"Encrypted file URL: {aesgcm_url}")
