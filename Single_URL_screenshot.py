# -*- coding: utf-8 -*-
"""
Created on Mon May 20 21:39:29 2019
to create a single screenshot of a target url:
    update user profile for the selected browser, if needed.
    enter url to visit
    enter file name for the screenshot
    enter the chapter_path where you want to save it
@author: stjseidel
"""

import os
import time
import re


from splinter import Browser

url = 'https://courses.edx.org/courses/course-v1:MITx+6.431x+2T2019/jump_to/block-v1:MITx+6.431x+2T2019+type@vertical+block@ch9-s8-tab1'
file_name = "U6_C8_01. Unit Summary.png"
file_name = (re.sub("[:,?]", "-", file_name)).strip()  # filter forbidden chars
chapter_path = "D:\\A_SCRAPING\\Screenshots\\Unit 6- Further topics on random variables\\8. Unit Summary"
path = os.path.join(chapter_path, file_name)

# with Browser('firefox') as browser:
with Browser('firefox', profile='C:/Users/user/AppData/Roaming/Mozilla/Firefox/Profiles/4dr01shn.Panda') as browser:
    browser.visit(url)
    print("Printing {} into {}".format(file_name, path))
    time.sleep(3)  # wait time so ensure all elements are correctly loaded
    screenshot_path = browser.screenshot(path, full=True)
