#!/bin/bash

# Set variables
PROJECT_ID="your-project-id"
INSTANCE_NAME="your-instance-name"

# Get list of disks attached to the instance
DISKS=$(gcloud compute instances describe ${INSTANCE_NAME} --project ${PROJECT_ID} --format="value(disks.deviceName)")

# Loop through each disk and restore from most recent snapshot
for DISK in $DISKS
do
  # Get most recent snapshot for the disk
  SNAPSHOT=$(gcloud compute snapshots list --project ${PROJECT_ID} --filter="sourceDisk=${INSTANCE_NAME}/${DISK} AND status=READY" --sort-by="~creationTimestamp" --format="value(name)" | head -n 1)

  # Restore the disk from the snapshot
  gcloud compute disks create ${DISK} --project ${PROJECT_ID} --source-snapshot ${SNAPSHOT} --zone=us-central1-a --labels restored-from=${SNAPSHOT}

  # Attach the disk to the instance
  gcloud compute instances attach-disk ${INSTANCE_NAME} --disk=${DISK} --project ${PROJECT_ID} --zone=us-central1-a
done

