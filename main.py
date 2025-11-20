import argparse
import csv
import os

from atproto import Client, models
from imageio.v2 import imread


def main():
    parser = argparse.ArgumentParser(
        prog="MovieSkeeter",
        description="Skeets a movie review on BlueSky",
    )
    parser.add_argument(
        "-x",
        dest="execute",
        action="store_true",
        help="Actually run, otherwise just print what would be posted.",
    )
    parsed_args = parser.parse_args()

    client = build_bsky_client()

    for row in read_csv_rows("data/movies.csv"):
        body_text = build_body_text(row)
        alt_text = build_alt_text(row)
        image_data, aspect_ratio = build_image_and_aspect_ratio(row)
        if parsed_args.execute:
            send_skeet(client, body_text, image_data, alt_text, aspect_ratio)


def build_bsky_client():
    client = Client()
    client.login(os.environ.get("BSKY_USER"), os.environ.get("BSKY_PASS"))
    return client


def read_csv_rows(filename):
    with open(filename, mode="r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            yield row


def send_skeet(client, body_text, img_data, alt_text, aspect_ratio):
    post = client.send_image(
        text=body_text,
        image=img_data,
        image_alt=alt_text,
        image_aspect_ratio=aspect_ratio,
    )
    print(f"\nPost info: {post}")
    print("---------------------")


def build_body_text(row):
    year = row["year"]
    num = row["number"]
    title = row["title"]
    release_year = row["release_year"]
    review = row["review"].replace("\\n", "\n")
    body_text = f"{year} watch #{num}: {title} ({release_year})\n\n{review}"
    print(body_text)
    l = len(body_text)
    if l <= 300:
        print(f"✅ length OK: {l}")
    else:
        print(f"⛔ too long: {l}")
    return body_text


def build_alt_text(row):
    alt_text = row["alt_text"]
    if alt_text.isspace() or len(alt_text) == 0:
        print(f"⛔ missing ALT text")
    else:
        print(f"✅ ALT text: {alt_text}")
    return alt_text


def build_image_and_aspect_ratio(row):
    with open(row["image_path"], "rb") as f:
        img_data = f.read()
    img = imread(row["image_path"])

    img_size = len(img_data)

    if img_size < 1_000_000:
        print(f"✅ Image size OK: {img_size}")
    else:
        print(f"⛔ Image size must be below 1MB: {img_size}")

    print(f"Aspect ratio: {img.shape[1]}x{img.shape[0]}")

    return img_data, models.AppBskyEmbedDefs.AspectRatio(
        height=img.shape[0], width=img.shape[1]
    )


if __name__ == "__main__":
    main()
