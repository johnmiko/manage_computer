import os
import zipfile

folder = 'D:/Users/johnm/OneDrive/misc/photos and videos/google drive/google_drive_photos/'
content = os.listdir(folder)
zips = []
for f in content:
    if '.zip' in f:
        zips.append(f)
for zip in zips:
    with zipfile.ZipFile(folder + zip, 'r') as zip_ref:
        print('extracting ' + zip)
        zip_ref.extractall(folder)
