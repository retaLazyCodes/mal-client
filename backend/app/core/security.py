import secrets
import hashlib
import base64

def generate_code_verifier() -> str:
    """
    Generates a code verifier for PKCE.
    It should be a high-entropy cryptographic random string of 43-128 characters.
    """
    return secrets.token_urlsafe(100)[:128]

def generate_code_challenge(code_verifier: str) -> str:
    """
    Generates a code challenge from the verifier using S256 (SHA256).
    MAL expects this to be URL-safe base64 encoded without padding.
    """
    sha256_hash = hashlib.sha256(code_verifier.encode("ascii")).digest()
    code_challenge = base64.urlsafe_b64encode(sha256_hash).decode("ascii")
    # Remove padding as per RFC 7636
    return code_challenge.replace("=", "")
