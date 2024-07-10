import secrets, base64

print(base64.b64encode(secrets.token_bytes(32)))
