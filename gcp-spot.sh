#!/bin/bash

# provision gcp spot instance

gcloud beta compute instances create spot-example \
--provisioning-model=SPOT \
--instance-termination-action=STOP \
--image-project=rocky-linux-cloud \
--image-family=rocky-linux-8 \
--machine-type=e2-micro \
--project=airy-totality-151318

