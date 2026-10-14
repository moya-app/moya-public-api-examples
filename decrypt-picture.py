import argparse

from cryptography.exceptions import InvalidTag

from moya.aesgcm import download

# This tool is to download and decrypt moya app encrypted image urls received from webhooks.
# The documentation can be found here: https://docs.moya.app/#receive-image

parser = argparse.ArgumentParser(description="Download and decrypt an image from a URL")
parser.add_argument("url", type=str, help="The encrypted image URL")
parser.add_argument("--output", type=str, help="The output file name")
args = parser.parse_args()

try:
    # Decrypted with the IV and key in the URL's fragment; a URL without them is saved as downloaded
    decrypted_file = download(args.url)
except (InvalidTag, ValueError) as e:
    print(f"Unable to create cipher output stream: {e}")
else:
    # Save the decrypted file to disk
    with open(args.output, "wb") as f:
        f.write(decrypted_file)
    print("Decrypted file written to disk")
