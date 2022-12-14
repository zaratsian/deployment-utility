# Cloud Shell Deployment Tutorial


## Let's get started!

This guide will details the steps needed to deploy this utility withih your GCP project. 

## Deploy this Utility

Step 1: Deploy the utility via the script provided. This will run a Cloud Build process.

```
./deploy-cloudbuild.sh
```

Step 2: View your running utility
[Cloud Run](https://console.cloud.google.com/run)

Get Cloud Run Endpoint
```
export ENDPOINT=$(gcloud run services describe bqapi --platform managed --region us-central1 --format 'value(status.url)')
```

Issue BQ API Calls

```
# Create Dataset
curl $ENDPOINT/dataset?create=mynewdataset

# Create Table
curl -X POST $ENDPOINT/table -H "Content-Type: application/json" -d '{"dataset":"mynewdataset", "table":"mytable", "payload":{"name":"sam", "value":10}}'

# Insert records into Table
curl -X POST $ENDPOINT/insert -H "Content-Type: application/json" -d '{"dataset":"mynewdataset", "table":"mytable", "payload":{"name":"sam", "value":10}}'

# Query Table
curl -X POST $ENDPOINT/query -H "Content-Type: application/json" -d '{"query":"select * from `$GOOGLE_CLOUD_PROJECT.mynewdataset.mytable`"}'

```

## What is Cloud Shell?

Let's briefly go over what Cloud Shell can do.

Cloud Shell is a personal hosted Virtual Machine which comes pre-loaded with developer tools for Google Cloud products. This interactive shell environment comes with a built-in code editor, persistent disk storage, and web preview functionality. To use command-line access alone, visit [console.cloud.google.com/cloudshell](https://console.cloud.google.com/cloudshell).
