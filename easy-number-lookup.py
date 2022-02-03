from moya.messaging import API
import sys

# May be DID or number
_, token, lookup = sys.argv
api = API(token)
print(api.lookup_user(lookup))
