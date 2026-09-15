import urllib.request

data = b'{"question":"How much has Lagos spent on waterways?"}'

request = urllib.request.Request(
    "http://127.0.0.1:8000/questions/",
    data=data,
    headers={
        "Content-Type": "application/json",
        "Accept": "application/json",
    },
)

response = urllib.request.urlopen(request)

raw = response.read()

print("STATUS:", response.status)
print("CONTENT-TYPE:", response.headers.get("Content-Type"))
print("BYTES:", raw[:1000])