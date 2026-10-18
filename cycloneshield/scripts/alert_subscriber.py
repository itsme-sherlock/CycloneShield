"""
Demo subscriber: prints CycloneShield alerts as they arrive.

    python scripts/alert_subscriber.py --project my-proj --subscription cs-alerts-sub

Filter by district by creating the subscription with a message filter, e.g.:

    gcloud pubsub subscriptions create cs-puri-sub --topic cyclone-alerts \\
        --message-filter='attributes.district = "Puri"'

Uses Application Default Credentials (GOOGLE_APPLICATION_CREDENTIALS or
`gcloud auth application-default login`).
"""

import argparse
import json
from concurrent.futures import TimeoutError as FutureTimeout

from google.cloud import pubsub_v1


def main() -> None:
    """Pull alerts from a subscription and print them until interrupted."""
    parser = argparse.ArgumentParser(description="Print CycloneShield Pub/Sub alerts.")
    parser.add_argument("--project", required=True, help="GCP project id")
    parser.add_argument("--subscription", required=True, help="Subscription id")
    parser.add_argument("--timeout", type=float, default=None, help="Stop after N seconds")
    args = parser.parse_args()

    subscriber = pubsub_v1.SubscriberClient()
    path = subscriber.subscription_path(args.project, args.subscription)

    def on_message(message: pubsub_v1.subscriber.message.Message) -> None:
        attrs = dict(message.attributes)
        print("=" * 60)
        print(f"ALERT  {attrs.get('severity')}  |  {attrs.get('district')}, {attrs.get('state')}")
        print(f"  location_source : {attrs.get('location_source')}")
        print(f"  assessment      : {attrs.get('assessment_source')}")
        print(f"  photo           : {attrs.get('photo_uri')}")
        try:
            body = json.loads(message.data.decode("utf-8"))
            print(f"  damage_type     : {body.get('damage_type')}")
            print(f"  incident_id     : {body.get('incident_id')}")
            if body.get("needs_human_confirmation"):
                print("  ** NEEDS HUMAN CONFIRMATION **")
        except ValueError:
            print(f"  raw: {message.data!r}")
        message.ack()

    print(f"Listening on {path} (Ctrl+C to stop)...")
    future = subscriber.subscribe(path, callback=on_message)
    with subscriber:
        try:
            future.result(timeout=args.timeout)
        except (KeyboardInterrupt, FutureTimeout):
            future.cancel()
            future.result()


if __name__ == "__main__":
    main()
