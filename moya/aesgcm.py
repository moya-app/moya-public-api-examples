"""
AES-256-GCM encryption for Moya file shares (the `aesgcm://` URL scheme).

The file is encrypted with a fresh 16-byte IV and 32-byte key, and the 16-byte GCM tag is appended
to the ciphertext. The IV and key travel in the URL fragment as lowercase hex, so a URL looks like
aesgcm://<host>/<path>#<32 hex IV><64 hex key>. download() fetches and decrypts such a URL, which is
how decrypt-picture.py reads the files that users send.
"""
import re
import secrets
from urllib.parse import urlsplit, urlunsplit

import requests
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Regular expression to match valid IV and key combinations: a 16-byte IV (or a 12-byte one, 88 hex
# characters) followed by the 32-byte key
IV_KEY_REGEX = re.compile(r"([A-Fa-f0-9]{2}){48}|([A-Fa-f0-9]{2}){44}")


def encrypt(plaintext: bytes) -> tuple[bytes, str]:
    """Return (ciphertext with the tag appended, hex IV+key for the URL fragment)."""
    iv = secrets.token_bytes(16)
    key = secrets.token_bytes(32)
    return AESGCM(key).encrypt(iv, plaintext, None), (iv + key).hex()


def decrypt(ciphertext: bytes, iv_key: str) -> bytes:
    """
    Inverse of encrypt(). Also accepts a 12-byte IV (88 hex characters). Raises cryptography's InvalidTag
    if the data was altered.
    """
    raw = bytes.fromhex(iv_key)
    if len(raw) not in (44, 48):
        raise ValueError("Expected 96 hex characters: a 16-byte IV (or a 12-byte one, 88 hex) followed by a 32-byte key")
    return AESGCM(raw[-32:]).decrypt(raw[:-32], ciphertext, None)


def to_aesgcm_url(https_url: str, iv_key: str) -> str:
    """https://host/path -> aesgcm://host/path#<iv_key>"""
    if not https_url.startswith("https://"):
        raise ValueError(f"Expected an https:// URL, got {https_url}")
    return "aesgcm://" + https_url[len("https://"):] + "#" + iv_key


def from_aesgcm_url(url: str) -> tuple[str, str | None]:
    """
    aesgcm://host/path#<iv_key> -> (https://host/path, iv_key), the inverse of to_aesgcm_url(). iv_key is
    None when the fragment does not start with an IV and key, as for a plain https:// file. Like urlsplit(),
    this ignores leading whitespace and any tabs or line breaks, as in a URL pasted from a wrapped line.
    """
    scheme, netloc, path, query, fragment = urlsplit(url)
    if scheme == "aesgcm":
        scheme = "https"
    https_url = urlunsplit((scheme, netloc, path, query, ""))
    return https_url, fragment if IV_KEY_REGEX.match(fragment) else None


def download(url: str, timeout: float = 60) -> bytes:
    """
    Download the file at a URL from a Moya message, decrypting it if the URL carries an IV and key.
    Raises cryptography's InvalidTag if the data was altered, or ValueError if the IV and key are malformed.
    A failed download of an encrypted URL (a 404, say) also surfaces as InvalidTag, and a plain URL returns
    the response body as it is, whatever the status.
    """
    https_url, iv_key = from_aesgcm_url(url)
    content = requests.get(https_url, timeout=timeout).content
    return decrypt(content, iv_key) if iv_key else content
