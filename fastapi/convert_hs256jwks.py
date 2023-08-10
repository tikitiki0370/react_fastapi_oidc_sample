import base64


def convert_hs256jwks(secret: str) -> dict:
    return {
        "keys": [
            {
                "kty": "oct",
                "alg": "HS256",
                "k": base64.urlsafe_b64encode(secret.encode('utf-8')).decode('utf-8').rstrip("=")
            }
        ]
    }
