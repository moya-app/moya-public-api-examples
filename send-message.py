import requests
import sys

_, token, to, message = sys.argv
if not message:
    message = """
```
foo bar
```

fred `test` *bold* 

> bar
        """

res = requests.post("https://api.moya.app/v1/message", headers={"Authorization": f"Bearer {token}"}, json={
    "to": to,
    "recipient_type": "individual",
    "type": "text",
    "text": {
        "body": message
    }
})
print(res)
print(res.json())
