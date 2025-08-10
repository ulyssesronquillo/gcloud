#!/usr/bin/env python3

import argparse
import subprocess
import sys
import json

def get_latest_snapshots(disk_name, project=None, limit=5, zone=None):
    # Build the gcloud command
    command = [
        "gcloud", "compute", "snapshots", "list",
        "--filter=name~^{}-".format(disk_name),
        "--format=json"
    ]
    if project:
        command += ["--project", project]
    if zone:
        command += ["--filter=diskZone:{}".format(zone)]

    try:
        # Run the gcloud command and parse output
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE)
        snapshots = json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running gcloud: {e}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON output: {e}", file=sys.stderr)
        sys.exit(1)

    # Sort by creationTimestamp descending (latest first)
    snapshots_sorted = sorted(
        snapshots,
        key=lambda s: s.get("creationTimestamp", ""),
        reverse=True
    )

    # Print the latest 'limit' snapshots
    for snap in snapshots_sorted[:limit]:
        print(f"Name: {snap['name']}")
        print(f"  Status: {snap.get('status')}")
        print(f"  Created: {snap.get('creationTimestamp')}")
        print(f"  Disk Size: {snap.get('diskSizeGb')} GB")
        print(f"  Disk: {snap.get('sourceDisk')}")
        print(f"  Storage Locations: {', '.join(snap.get('storageLocations', []))}")
        print("-" * 40)

def main():
    parser = argparse.ArgumentParser(description="Show latest GCP disk snapshots using gcloud.")
    parser.add_argument("disk", help="Name of the disk to find snapshots for")
    parser.add_argument("--project", help="GCP project ID", default=None)
    parser.add_argument("--zone", help="Compute zone of the disk (optional)", default=None)
    parser.add_argument("--limit", type=int, default=5, help="Number of latest snapshots to show (default: 5)")
    args = parser.parse_args()

    get_latest_snapshots(args.disk, args.project, args.limit, args.zone)

if __name__ == "__main__":
    main()
