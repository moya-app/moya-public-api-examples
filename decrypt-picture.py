import argparse
import re
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from io import BytesIO
from urllib.parse import urlparse
import requests

# This tool is to download and decrypt moya app encrypted image urls received from webhooks.
# The documentation can be found here: https://docs.moya.app/#receive-image

# Regular expression to match valid IV and key combinations
IV_KEY_REGEX = re.compile(r"([A-Fa-f0-9]{2}){48}|([A-Fa-f0-9]{2}){44}")


def get_key_and_iv(key_iv_combo) -> (bytes, bytes):
    """
    Extracts the AES key and IV from the provided key/IV combination.
    """
    if len(key_iv_combo) == 48:
        aes_key = key_iv_combo[16:]
        iv = key_iv_combo[:16]
    elif len(key_iv_combo) == 44:
        aes_key = key_iv_combo[12:]
        iv = key_iv_combo[:12]
    elif len(key_iv_combo) >= 32:
        aes_key = key_iv_combo[:32]
        iv = bytes(
            [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f]
        )
    else:
        raise ValueError("Invalid key/iv combo")
    return aes_key, iv


def download_image(encrypted_image_url: str) -> BytesIO | None:
    """
    Downloads and decrypts an image from the provided URL.
    """
    parsed_url = urlparse(encrypted_image_url)
    reference = parsed_url.fragment

    # Replace the custom scheme with HTTPS and download the file
    file_url = encrypted_image_url.replace("aesgcm://", "https://")
    response = requests.get(file_url, stream=True)
    is_stream = BytesIO(response.content)

    # Check if the reference is a valid IV and key combination
    if not reference or not IV_KEY_REGEX.match(reference):
        return is_stream
    try:
        # Extract the key and IV from the reference
        aes_key, iv = get_key_and_iv(bytes.fromhex(reference))

        # Get the downloaded content as bytes
        encrypted_content = is_stream.getvalue()

        # Last 16 bytes are the tag
        tag = encrypted_content[-16:]

        # The rest is the encrypted data
        encrypted_data = encrypted_content[:-16]

        # Create a Cipher object for decryption
        cipher = Cipher(algorithms.AES(aes_key), modes.GCM(iv, tag), backend=default_backend())
        decryptor = cipher.decryptor()

        # Decrypt the content and return as a BytesIO stream
        return BytesIO(decryptor.update(encrypted_data) + decryptor.finalize())
    except Exception as e:
        print(f"Unable to create cipher output stream: {e}")
        return None


parser = argparse.ArgumentParser(description="Download and decrypt an image from a URL")
parser.add_argument("url", type=str, help="The encrypted image URL")
parser.add_argument("--output", type=str, help="The output file name")
args = parser.parse_args()

decrypted_file = download_image(args.url)

if decrypted_file:
    # Save the decrypted file to disk
    with open(args.output, "wb") as f:
        f.write(decrypted_file.getvalue())
    print("Decrypted file written to disk")
