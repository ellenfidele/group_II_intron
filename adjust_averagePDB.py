#!/usr/bin/env python
# coding: utf-8

import numpy as np
import argparse


parser = argparse.ArgumentParser(description='Adjust residue indices in PDB files of group II intron (both iso and full)')
parser.add_argument('--iso_input', type=str, help='input file name of group II intron D1 iso')
parser.add_argument('--iso_output', type=str, help='output file name of group II intron D1 iso')
parser.add_argument('--full_input', type=str, help='input file name of group II intron D1 from full structure')
parser.add_argument('--full_output', type=str, help='output file name of group II intron D1 from full structure')
args = parser.parse_args()


iso_in = args.iso_input
iso_out = args.iso_output
s = [-4, 1, 2, 7, 9, 12]

full_in = args.full_input
full_out = args.full_output


with open(iso_in, 'r') as fin:
    fot = open(iso_out, 'w')
    resid = 0;
    
    for line in fin:
        entries = line.strip().split()

#             print(line)
        resid = int(entries[4])
        if resid < 5:
            fot.write(line.replace("   %d   " %resid, "   %d   " %(resid+s[0])))
        elif resid < 82:
            fot.write(line.replace("   %d   " %resid, "   %d   " %(resid+s[1])))
        elif resid < 101:
            fot.write(line.replace("   %d   " %resid, "   %d   " %(resid+s[2])))
        elif resid < 200:
            fot.write(line.replace("   %d   " %resid, "   %d   " %(resid+s[3])))
        elif resid < 226:
            fot.write(line.replace("   %d   " %resid, "   %d   " %(resid+s[4])))
        else:
            fot.write(line.replace("   %d   " %resid, "   %d   " %(resid+s[5])))


with open(full_in, 'r') as f_in:
    f_out = open(full_out, 'w')
    resid = 0;
    
    for line in f_in:
        entries = line.strip().split()
        resid = int(entries[4])
        f_out.write(line.replace("   %d   " %resid, "   %d   " %(resid-5)))




