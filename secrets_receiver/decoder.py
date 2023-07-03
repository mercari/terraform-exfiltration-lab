import base64
import sys

from pathlib import Path

store = dict()


def decode_chunk(secrets_dir, method, info):
    (cid, ctotal, cidx, chunk) = info.split("-", 4)

    cid = int(cid)
    ctotal = int(ctotal)
    cidx = int(cidx)
    chunk = base64.b64decode(chunk)

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


def decode_file(input_file, output_dir):
    with open(input_file, "r") as input:
        for line in input.readlines():
            cid, complete = decode_chunk(output_dir, "access-logs", line)
            if complete:
                print(f"processed secret gcp access log exfil: {cid}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Please specify input and output files")
        print("Usage: decoder.py <inputfile> <outputdir>")
        sys.exit()
    decode_file(sys.argv[1], sys.argv[2])
