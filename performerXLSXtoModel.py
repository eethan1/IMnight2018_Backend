#!/usr/bin/env python
from openpyxl import load_workbook

filepath = 'performer.xlsx'
wb = load_workbook(filepath)

sheets = wb.get_sheet_names()
sheet1 = sheets[1]
ws = wb.get_sheet_by_name(sheet1)

rows = ws.rows
columns = ws.columns

import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "IMnight.im_settings")
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth.models import Group

performers_group = Group.objects.get(name='Performers')

unenvolved_user = []
for i, row in enumerate(rows):
    # skip titile row
    if i == 0 :
        continue

    line = [col.value for col in row]

    # check if not None
    if line[0]:
        username = line[0]
        job = line[1]
        job_description = line[2]
        bio = line[3]
        user = User.objects.filter(username=username)
        if user:
            user = user.first()
            user.profile.job = job
            user.profile.job_description = job_description
            user.profile.bio = bio
            user.groups.add(performers_group)
            user.save()
            print("====== Finish modify user %s ======" % username)
        else:
            unenvolved_user.append(username)

for username in unenvolved_user:
    print(username)
