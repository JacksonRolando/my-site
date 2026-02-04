import json
import os
import re
import datetime

image_regex = re.compile(r".*\.(jpe?g|png|gif|bmp|tiff)$", re.IGNORECASE)


def update_manifest(manifest_path: str, photo_dir: str):
    manifest_obj = {}
    with open(manifest_path) as f:
        try:
            manifest_obj = json.load(f)
        except:
            manifest_obj = {}
        print(manifest_obj)

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
    update_manifest("mediaData.json", "../server/media")


if __name__ == "__main__":
    main()
