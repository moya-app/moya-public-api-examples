import requests
import sys

_, token, to = sys.argv

res = requests.post("https://api.moya.app/v1/message", headers={"Authorization": f"Bearer {token}"}, json={
    "to": to,
    "recipient_type": "individual",
    "type": "text",
    "text": {
        "body": """
```
foo bar
```

fred `test` *bold* 

> bar
        """
    }
})
print(res)
print(res.json())
