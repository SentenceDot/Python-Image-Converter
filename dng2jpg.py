import piexif
from PIL import Image
import os

raw_path = ""
jpg_path = ""

import os
files = [os.path.splitext(filename)[0] for filename in os.listdir(raw_path)]

for file in files:

    # Get FILE path
    raw_image_path = f"{raw_path}\{file}.DNG"
    jpg_image_path = f"{jpg_path.lower()}\{file}.jpg"

    # Covert DNG to JPG
    im = Image.open(raw_image_path)
    rgb_im = im.convert('RGB')
    rgb_im.save(jpg_image_path)


    # Load origin EXIF informations from the DNG file 
    raw_exif_dict = piexif.load(raw_image_path)

    # Extract the Exif field
    exif_info = raw_exif_dict['Exif']
    # WORKAROUND: The module "piexif" can not process the negative values, so we delete it from Exif information
    # The Exif tag 37379 means BrightnessValue, the value can in the range of -99.99 to 99.99
    # For more information, refer the following URL:
    # https://www.awaresystems.be/imaging/tiff/tifftags/privateifd/exif/brightnessvalue.html
    del exif_info[37379]

    # Get GPS infomartion from Exif field
    gps_info = raw_exif_dict['GPS']

    # Combine the Exif and GPS information in to a new dict. 
    new_exit_dict = {
        'Exif': exif_info,
        'GPS': gps_info,
    }

    # Dump the new Exif dict to dict_bytes and write it to the jpg files.
    exif_bytes = piexif.dump(new_exit_dict)
    piexif.insert(exif_bytes, jpg_image_path)