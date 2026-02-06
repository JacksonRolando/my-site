import json
import os
import re
import datetime

from PIL import Image

image_regex = re.compile(r".*\.(jpe?g|png|gif|bmp|tiff)$", re.IGNORECASE)
manifest_file = "mediaManifest.json"
media_path = "../server/media"
thumbnail_path = "../server/media/thumbnails"

MAX_PXL_DIM = 1280


def generate_thumbnail(img_path):
    thumbnail = None
    with Image.open(img_path) as img:
        reduce_factor = int(max(1, (max(img.width, img.height) / MAX_PXL_DIM)))
        thumbnail = img.reduce(reduce_factor)

    return thumbnail


def gen_and_save_thumbnails(manifest_path, in_photo_dir, out_dir):
    manifest_obj = {}
    with open(manifest_path) as f:
        try:
            manifest_obj = json.load(f)
        except:
            manifest_obj = {}

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    thumb = None
    out_path = ""
    for img_name, _ in manifest_obj.items():
        out_path = os.path.join(out_dir, "thumbnail_" + img_name)
        if not os.path.exists(out_path):
            thumb = generate_thumbnail(os.path.join(in_photo_dir, img_name))
            thumb.save(out_path)


def update_manifest(manifest_path: str, photo_dir: str):
    manifest_obj = {}
    with open(manifest_path) as f:
        try:
            manifest_obj = json.load(f)
        except:
            manifest_obj = {}

    files = [
        f
        for f in os.listdir(photo_dir)
        if os.path.isfile(os.path.join(photo_dir, f)) and bool(image_regex.match(f))
    ]

    files_modified = 0
    for f in files:
        if not bool(manifest_obj.get(f)):
            files_modified += 1
            manifest_obj[f] = {
                "description": "",
                "altText": "",
                "date": str(
                    datetime.datetime.fromtimestamp(
                        os.path.getmtime(os.path.join(photo_dir, f))
                    )
                ),
                "credit": "",
            }

    with open(manifest_path, "w+") as f:
        json.dump(manifest_obj, f)


def main():
    # update_manifest(manifest_file, media_path)
    gen_and_save_thumbnails(manifest_file, media_path, thumbnail_path)


if __name__ == "__main__":
    main()
