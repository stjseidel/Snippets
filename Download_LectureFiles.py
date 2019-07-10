# -*- coding: utf-8 -*-
"""
Created on Thu May  9 17:48:10 2019
adapted from:
https://stackoverflow.com/questions/7243750/download-file-from-web-in-python-3

Downloads all available lecture files from an edx-course
Depends on the files being named consistently
Concats the url names of the videos from fixed parts and loop-created indexes

Does not yet create any folders, simply stores in working directory.
@author: stjseidel
"""

import urllib.request
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
import shutil

from pathlib import Path


base = "https://s3.amazonaws.com/edx-course-videos/mit-6041x/MIT6041XT114-G"
tail = "_100.mp4"

for chap in range(1, 25):
    chapnum = str(chap) if chap >= 10 else '0' + str(chap)
    print("Chapter Number {}".format(chapnum))
    for sect in range(1, 25):

        sectnum = str(sect) if sect >= 10 else '0' + str(sect)
        print("{} sect {}".format(chapnum, sectnum))
        url = base + chapnum + sectnum + tail
        print(url)
        file_name = "Probability_{}_{}.mp4".format(chapnum, sectnum)
# Download the file from `url` and save it locally under `file_name`:
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
                # do something
                with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
                    shutil.copyfileobj(response, out_file)
