import webbrowser
import json

keys = json.load(open("keys.json"))
tenant_id = keys["tenant"]
client_id = keys["client"]

scopes = ['Files.ReadWrite.All']
request_auth_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize?client_id={client_id}&response_type=code&scope={'%20'.join(scopes)}"

webbrowser.open(request_auth_url)