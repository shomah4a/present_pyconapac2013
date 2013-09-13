#-*- coding: utf-8 -*-

import sys
import argparse


from present import loader, server


def main(args=sys.argv[1:]):

    members = loader.load_csv(args)
    server.serve(members)



if __name__ == '__main__':
    main()






