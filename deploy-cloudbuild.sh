gcloud builds submit --region=us-central1 --config cloudbuild.yaml \
--substitutions=_GCP_PROJECT_ID=$GOOGLE_CLOUD_PROJECT
