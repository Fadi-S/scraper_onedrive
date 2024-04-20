import json
import time
from azure.identity import InteractiveBrowserCredential, UsernamePasswordCredential


def get_token(from_console=True):
    keys = json.load(open("keys.json"))
    tenant_id = keys["tenant"]
    client_id = keys["client"]
    email = keys["email"]
    password = keys["password"]

    redirect_uri = "http://localhost:8080/auth/callback"
    scopes = ['Files.ReadWrite.All']

    try:
        token = json.load(open("access_token.json"))
        if token["expires_on"] < time.time():
            raise Exception("Token expired")
        return token["token"]
    except:
        if from_console:
            credential = UsernamePasswordCredential(client_id, username=email, password=password, tenant_id=tenant_id)
        else:
            credential = InteractiveBrowserCredential(client_id=client_id, tenant_id=tenant_id, redirect_uri=redirect_uri)
        access_token = credential.get_token(' '.join(scopes))
        with open("access_token.json", "w") as f:
            f.write(json.dumps({"token": access_token.token, "expires_on": access_token.expires_on}))
        return access_token.token
