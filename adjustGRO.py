#!/usr/bin/env python
# coding: utf-8

import numpy as np
import re
import argparse


parser = argparse.ArgumentParser(description='Adjust residue indices in trajectory gro files of group II intron (both iso and full)')
parser.add_argument('--iso_input', type=str, help='input file name of group II intron D1 iso')
parser.add_argument('--iso_output', type=str, help='output file name of group II intron D1 iso')
parser.add_argument('--full_input', type=str, help='input file name of group II intron D1 from full structure')
parser.add_argument('--full_output', type=str, help='output file name of group II intron D1 from full structure')
args = parser.parse_args()


def separate_string(s):
    m = re.search('^[0-9]+', s)
    if m:
        return(s[m.start():m.end()])


iso_in = args.iso_input
iso_out = args.iso_output
s = [-4, 1, 2, 7, 9, 12]

full_in = args.full_input
full_out = args.full_output


with open(iso_in, 'r') as fin:
    fot = open(iso_out, 'w')
    resid = 0
    frame = 0
    
    for line in fin:
        entries = line.strip().split()
        if len(entries) == 6:
            resid = int(separate_string(entries[0]))
            if resid < 5:
                fot.write(line.replace("  %d" %resid, "  %d" %(resid+s[0]), 1))
            elif resid < 82:
                fot.write(line.replace("  %d" %resid, "  %d" %(resid+s[1]), 1))
            elif resid < 101:
                fot.write(line.replace("  %d" %resid, "  %d" %(resid+s[2]), 1))
            elif resid < 200:
                fot.write(line.replace("  %d" %resid, "  %d" %(resid+s[3]), 1))
            elif resid < 226:
                fot.write(line.replace("  %d" %resid, "  %d" %(resid+s[4]), 1))
            else:
                fot.write(line.replace("  %d" %resid, "  %d" %(resid+s[5]), 1))
        elif entries[0] == "Generated":
            fot.write(line)
            frame +=1;
            if frame % 1000 == 0:
                print('%d' %frame)
        else:
            fot.write(line)
            


with open(full_in, 'r') as f_in:
    f_out = open(full_out, 'w')
    resid = 0;
    frame_full = 0
    
    for line in f_in:
        entries = line.strip().split()
        if len(entries) == 6:
            resid = int(separate_string(entries[0]))
            f_out.write(line.replace("  %d" %resid, "  %d" %(resid-5), 1))
        elif entries[0] == "Generated":
            f_out.write(line)
            frame_full +=1;
            if frame_full % 1000 == 0:
                print('%d' &frame_full)
        else:
            f_out.write(line)


with open(iso_in, 'r') as fin:
    fot = open(iso_out, 'w')
    resid = 0
    ain = 0
    in_frame = False
    no_frame = 0
    
    for line in fin:
#         print(line)
        entries = line.strip().split();
        if no_frame > 1:
            break
        if entries[0] == "Generated":
            frame = []
            continue
        elif len(entries) == 1:
            ain = entries[0]
            continue
        elif len(entries) == 6:
            in_frame = True
            if ain:
                frame.append(line)
            else:
                continue
        elif len(entries) == 3:
            no_frame += 1
            ain = 0
            continue




