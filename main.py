import csv
import os

from atproto import Client, models
from imageio.v2 import imread


def main():
    client = Client()
    client.login(os.environ.get("BSKY_USER"), os.environ.get("BSKY_PASS"))
    with open("data/movies.csv", mode="r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            text = f"{row["year"]} watch #{row["number"]}: {row["title"]} ({row["release_year"]})\n\n{row["review"]}"
            alt_text = row["alt_text"]
            print(text)
            print(f"\n{alt_text}")
            with open(row["image_path"], "rb") as f:
                img_data = f.read()

            img = imread(row["image_path"])
            print(f"Aspect ratio: {img.shape}")
            post = client.send_image(
                text=text,
                image=img_data,
                image_alt=alt_text,
                image_aspect_ratio=models.AppBskyEmbedDefs.AspectRatio(
                    height=img.shape[0], width=img.shape[1]
                ),
            )
            print(f"\n{post}")


if __name__ == "__main__":
    main()
