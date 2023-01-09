#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import requests
from PIL import Image
import imagehash

print(sys.argv[-1])
format = "png"
url = f"https://www.web2pdfconvert.com/api/convert/web/to/{format}?storefile=true&filename=someurl-com"
headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "sec-ch-ua": '"Not?A_Brand";v="8", "Chromium";v="108"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-requested-with": "XMLHttpRequest",
}
form = {
    "url": (None, sys.argv[-1]),
    "pricing": (None, "monthly"),
    "ConversionDelay": (None, 0),
    "CookieConsentBlock": (None, True),
    "Zoom": (None, 1),
    "ParameterPreset": (None, "Custom"),
    "JavaScript": (None, False),
    "ImageWidth": (None, 1360),
}
response = requests.post(url, files=form, headers=headers)
print(response.status_code)
print(response.text)
data = response.json()
image_url = data["Files"][0]["Url"]
r = requests.get(image_url, timeout=300, stream=True)
with open(f"image.{format}", "wb") as fh:
    for chunk in r.iter_content(1024 * 1024):
        fh.write(chunk)
image_data = Image.open(f"image.{format}")
hash_i = imagehash.average_hash(image_data, hash_size=12)
print(hash_i)
