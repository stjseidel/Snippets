# -*- coding: utf-8 -*-
"""
Created on Mon May 20 21:39:29 2019
Create screenshots from the source code of a website.
Currently takes the source code of the 'Course' tab of an edx-course.
I was unable to use beautiful soup to extract the urls, so the code below
relies on an excel file with the source code pasted into,
then eliminates irrelevant html code und splits the remainder into URLs and
text to use for file names and chapter folders.

In order to use it, you will need to install Firefox and create a user profile.
In the line starting with 'With browser...' enter the path to the profile.
Otherwise, you will not be able to login to the course.
 Possibly, you will need to still log in manually first.
 In that case, enter a longer time delay before the first screenshots.
Retrieve html code from website, then remove html code from text.

Problems:
    - In some cases, the code fails when a unit summary is present.
        Reason unkown, not yet fixed.
        I used 'Single_URL_screenshotting.py' to create those screenshots

To Do:
    - currently need to copy source code by hand into excel file.
      Change to either read source code from page,
      or copy source code and prepare file automatically.
    - Screenshots are saved with 4 random chars and additional '.png'.
      Prevent it, or rename it immediately.
@author: stjseidel
"""

import pandas as pd
import os
import time
import re
from splinter import Browser

# =============================================================================
# url='https://courses.edx.org/courses/course-v1:MITx+6.431x+2T2019/course/'
# =============================================================================
source = pd.read_excel('source.xlsx', header=None)

# remove empty values
source.dropna

base = source.copy()
base_series = base[0]
base_list = list(base_series)


chapter_names = []
unit_names = []
link_names = []
link_list = []
indent = 0
last_was_link_list = False


def is_a_link(text):
    if len(text) < 5:
        return False
    if text[:4] == 'href':
        return True
    else:
        return False


def is_NOT_a_link(text):
    if len(text) < 5:
        return True
    if text[:4] == 'href':
        return False
    else:
        return True


def create_folder(path):
    if not os.path.isdir(path):
        try:
            os.mkdir(path)
        except OSError:
            print("Creation of the directory %s failed" % path)
        else:
            print("Successfully created the directory %s " % path)





# unit headings are formated. remove their formating
# <h3 class="section-title">Unit 1: Probability models and axioms</h3>
for i in range(len(base_list)):
    #     use this for exam chapters
    # =============================================================================
    #     if ">Unit " in base_list[i] or ">Exam " in base_list[i]:
    # =============================================================================
    if ">Unit " in base_list[i]:  # This ignores Exams
        base_list[i] = base_list[i][26:-5]

# search for first relevant entries
notFound = True
i = -1
while notFound and i < len(base_list):
    i += 1
    if is_a_link(base_list[i]):
        notFound = False
base_list = base_list[i-12:]

# filter most tags
for i in range(len(base_list)-1, -1, -1):
    if '<' in base_list[i]:
        del base_list[i]

# filter short entries
base_list = [x for x in base_list if len(x) > 3]

# filter all assignments that are not relevant hrefs
for i in range(len(base_list)-1, -1, -1):
    if not is_a_link(base_list[i]):
        if '="' in base_list[i]:
            del base_list[i]

# filter everything after the last relevant link
notFound = True
i = len(base_list)
while notFound and i > 0:
    i -= 1
    if is_a_link(base_list[i]):
        notFound = False
base_list = base_list[:i+2]

base_list.insert(0, "Unit 0: Overview")

for i in range(len(base_list)):
    if last_was_link_list:
        last_was_link_list = False
        link_names[-1][-1].append(base_list[i])
    elif i < len(base_list) - 3:
        if is_NOT_a_link(base_list[i]) and is_NOT_a_link(base_list[i+1]):
            # this is a new chapter heading
            indent = 1
            unit_names.append(base_list[i])
            link_list.append([])
            link_names.append([])
            chapter_names.append([])
        elif is_NOT_a_link(base_list[i]):
            # this is a subsection
            indent = 2
            chapter_names[-1].append(base_list[i])
            link_list[-1].append([])
            link_names[-1].append([])
        else:
            link_list[-1][-1].append(base_list[i])
            last_was_link_list = True
    else:
        link_list[-1][-1].append(base_list[i])
        last_was_link_list = True


# wd = os.getcwd()
wd = "D:\A_SCRAPING"

for i in range(len(unit_names)):
    unit_names[i] = (re.sub("[:,.?]", "-", unit_names[i]))

base_path = os.path.join(wd, 'Screenshots')
create_folder(base_path)


def create_screenshots(start_unit=0, end_unit=len(unit_names)):
    first = True
    with Browser('firefox', profile='C:/Users/user/AppData/Roaming/Mozilla/Firefox/Profiles/4dr01shn.Panda') as browser:
        for i in range(start_unit, end_unit):
            unit = unit_names[i]
            print("Working on main unit {}".format(unit))
            chapters = chapter_names[i]
            unit_link_list = link_list[i]
            unit_link_names = link_names[i]
            unit = unit.strip()
            print(unit)
            unit = (re.sub("[:,?]", "-", unit))
            # shortened length of unit to 50 characters
            # To undo, remove [:50]
            unit_path = os.path.join(base_path, unit[:50])
            unit_path = unit_path.strip()
            create_folder(unit_path)
            for j in range(len(chapters)):
                chap_name = str(j+1) + ". " + chapters[j]
                chap_name = (re.sub("[:,?]", "-", chap_name))
                # shortened length of chapter to 40 characters
                # To undo, remove [:40]
                chapter_path = os.path.join(unit_path, chap_name[:40])
                chapter_path = chapter_path.strip()
                create_folder(chapter_path)
                print("Working on chapter {}".format(chap_name))
                links = unit_link_list[j]
                names = unit_link_names[j]
                for n, link in enumerate(links):
                    url = link[6:-1]
                    browser.visit(url)
                    if first:
                        # This time delay enables you to log into edx,
                        # if not logged in already
                        time.sleep(15)
                        first = False
                    # shortened length of file to 30 characters.
                    # To undo, remove [:30]
                    file_name = "U{}_C{}_{}.png".format(i, j+1, names[n][:30])
                    file_name = file_name.strip()
                    file_name = (re.sub("[:,?]", "-", file_name))
                    path = os.path.join(chapter_path, file_name)
                    print("Printing {} into {}".format(names[n], path))
                    time.sleep(3)
                    browser.screenshot(path, full=True)


# =============================================================================
# REMEBER TO SAVE THE SOURCE CODE TO EXCEL AND DELETE EMPTY COLUMN AND ROWS
# SOURCE CODE SHOULD START IN CELL A1
# =============================================================================
# To print all units:
# create_screenshots()

# To print unit 2:
# create_screenshots(1)

# To print units 2, 3, 4:
# create_screenshots(1, 4)

# To print the second second-last unit:
# create_screenshots(len(unit_names)-2, len(unit_names)-1)

# To print the last unit:
create_screenshots(len(unit_names)-1)
# =============================================================================
# REMEBER TO SAVE THE SOURCE CODE TO EXCEL AND DELETE EMPTY COLUMN AND ROWS
# SOURCE CODE SHOULD START IN CELL A1
# =============================================================================
