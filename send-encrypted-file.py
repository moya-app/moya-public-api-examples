import argparse
import os

import requests

from moya.aesgcm import decrypt, encrypt, to_aesgcm_url
from moya.argtypes import number_or_file, setup_argparse
from moya.messaging import API

# Shown inline in the chat once downloaded; any other extension is sent as a file
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
https_url = api.upload_encrypted_file(filename, ciphertext)
print(f"Encrypted file uploaded to {https_url}")

if args.verify:
    if decrypt(requests.get(https_url, timeout=60).content, iv_key) != plaintext:
        raise SystemExit("Uploaded file did not decrypt to the original")
    print("Upload decrypts correctly")

aesgcm_url = to_aesgcm_url(https_url, iv_key)

if args.numbers:
    kind = "image" if os.path.splitext(filename)[1].lower() in IMAGE_EXTENSIONS else "file"
    for numbers in args.numbers:
        api.send_file(numbers, aesgcm_url, job_id=args.job_id, priority=args.priority, kind=kind)

# The key is only in this URL: anyone holding it can read the file until it expires, and it will end up in
# your shell history or CI logs if you print it there. Store it like a password if you need to resend the file.
print(f"Encrypted file URL: {aesgcm_url}")
