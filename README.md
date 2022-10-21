# Pipeline set-up

Currently running with Python version: 3.8.13

Set up a service-account and download its credentials. Give it the following roles:
- Dataflow Admin
- Service Account User
Set application default credentials to `beam-deploy` service account by setting `GOOGLE_APPLICATION_CREDENTIALS`:

```bash
export SA_NAME=beam-deploy
export GCP_ACCOUNT=xxx # Set your GCP username
export GCP_PROJECT=yyy # Set your GCP project
export GOOGLE_APPLICATION_CREDENTIALS=$PWD/key.json
gcloud iam service-accounts create $SA_NAME --account=$GCP_ACCOUNT --project=$GCP_PROJECT
```

```bash
gcloud iam service-accounts keys create $GOOGLE_APPLICATION_CREDENTIALS --iam-account=$SA_NAME@$GCP_PROJECT.iam.gserviceaccount.com --account=$GCP_ACCOUNT
```

```bash
gcloud projects add-iam-policy-binding $GCP_PROJECT --member="serviceAccount:$SA_NAME@$GCP_PROJECT.iam.gserviceaccount.com" --role=roles/dataflow.admin --account=$GCP_ACCOUNT
gcloud projects add-iam-policy-binding $GCP_PROJECT --member="serviceAccount:$SA_NAME@$GCP_PROJECT.iam.gserviceaccount.com" --role roles/iam.serviceAccountUser --account=$GCP_ACCOUNT
```

Launch Dataflow job by executing:
```
python streaming_pipeline.py \
    --output=matthias-sandbox:devfest_demo. \
    --input_subscription=projects/matthias-sandbox/subscriptions/frontend-log \
    --output_subscription=projects/gde-front-end/topics/languages \
    --runner=DataflowRunner \
    --project=matthias-sandbox \
    --region=asia-southeast1 \
    --temp_location=gs://mb-beam-demo/
```