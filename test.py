import json
import subprocess

command = [
    "grpcurl",
    "-H",
    "Authorization: Bearer {}".format(token),
    "-d",
    '{"query": {"semantic_query": "what is the boundary value analysis?"}, "count": 5}',
    "--proto",
    "./chunks.proto",
    "--proto",
    "./Search.proto",
    "grpc.staging.redactive.ai:443",
    "redactive.grpc.v1.Search/QueryChunks"
]

process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()

if process.returncode == 0:
    print("Command executed successfully. Output:")
    output_json = stdout.decode()
    data = json.loads(output_json)
    chunk_body = data['relevantChunks'][0]['chunkBody']
    print(chunk_body)
else:
    print("Error executing command:")
    print(stderr.decode())
