#-*- coding: utf-8 -*-

import os
import csv


def load_csv(fnames):

    users = []

    for f in fnames:

        if not os.path.exists(f):
            continue

        with open(f) as fp:
            reader = csv.DictReader(fp)
            users.extend(list(reader))

    return dict((l['no'], l) for l in users)




