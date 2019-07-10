# -*- coding: utf-8 -*-
"""
Created on Thu May  9 17:48:10 2019
takes an excel list as input, then downloads files.
xlsx file must have columns 'Link' with urls and 'File_Names with strings
@author: stjseidel
"""

import urllib.request
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
import shutil

from pathlib import Path
import pandas as pd


def download_file(url, file_name):
    downloaded = Path(file_name)
    if downloaded.is_file():
        print("{} existed already.".format(downloaded))
    else:
        try:
            response = urlopen(url)
        except HTTPError as e:
            # do something
            print('Error code: ', e.code)
            print("{} could not be found.".format(url))
        except URLError as e:
            # do something
            print('Reason: ', e.reason)
            print("{} could not be found.".format(url))
        else:
            with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)
        return None


DF = pd.read_excel('Download_files_from_xlsx.xlsx')
DF.columns
DF.columns
file_names = DF['File_name']
urls = DF['Link']
for i in range(len(file_names)):
    file_name = file_names[i]
    url = urls[i]
    file_name = file_names[i]
    print("downloading {}".format(file_name))
    download_file(url, file_name)
# Download the file from `url` and save it locally under `file_name`:
