"""
AES-256-GCM encryption for Moya file shares (the `aesgcm://` URL scheme).

The file is encrypted with a fresh 16-byte IV and 32-byte key, and the 16-byte GCM tag is appended
to the ciphertext. The IV and key travel in the URL fragment as lowercase hex, so a URL looks like
aesgcm://<host>/<path>#<32 hex IV><64 hex key>. decrypt-picture.py is the inverse of this.
"""
import secrets

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def encrypt(plaintext: bytes) -> tuple[bytes, str]:
    """Return (ciphertext with the tag appended, hex IV+key for the URL fragment)."""
    iv = secrets.token_bytes(16)
    key = secrets.token_bytes(32)
    return AESGCM(key).encrypt(iv, plaintext, None), (iv + key).hex()


def decrypt(ciphertext: bytes, iv_key: str) -> bytes:
    """Inverse of encrypt(). Raises cryptography's InvalidTag if the data was altered."""
    raw = bytes.fromhex(iv_key)
    if len(raw) != 48:
        raise ValueError("Expected 96 hex characters: a 16-byte IV followed by a 32-byte key")
    return AESGCM(raw[16:]).decrypt(raw[:16], ciphertext, None)


def to_aesgcm_url(https_url: str, iv_key: str) -> str:
    """https://host/path -> aesgcm://host/path#<iv_key>"""
    if not https_url.startswith("https://"):
        raise ValueError(f"Expected an https:// URL, got {https_url}")
    return "aesgcm://" + https_url[len("https://"):] + "#" + iv_key
