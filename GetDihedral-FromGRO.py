import numpy as np
import math
#import matplotlib.pyplot as plt
import re
import json
# import cPickle as pickle
# get_ipython().magic('matplotlib inline')

iso_fn = "./D1_iso.adjusted.gro"
full_fn = "./D1_full.adjusted.gro"
#out_fn = "hellinger.dat"

def separate_string(s):
    m = re.search('^[\+\-]?[0-9]+', s)
    if m:
        return(s[m.start():m.end()])

def get_coords(frame, P_list, C4_list):
        for line in frame:
            entries = line.strip().split()
#             print(separate_string(entries[0]))
            resid = int(separate_string(entries[0]))
            atomname = entries[1];
            coords = [float(entries[3]), float(entries[4]), float(entries[5])]
            if atomname == "P":
                P_list.append([resid, coords])
            elif atomname == "C4*":
                C4_list.append([resid, coords])
#         return P_list, C4_list

def dihedral(P_0, P_1, P_2, P_3):
    p0 = np.array([float(P_0[0]), float(P_0[1]), float(P_0[2])]);
    p1 = np.array([float(P_1[0]), float(P_1[1]), float(P_1[2])]);
    p2 = np.array([float(P_2[0]), float(P_2[1]), float(P_2[2])]);
    p3 = np.array([float(P_3[0]), float(P_3[1]), float(P_3[2])]);
    
    b0 = -1*(p1 - p0);
    b1 = p2 - p1;
    b2 = p3 - p2;
    
    b0xb1 = np.cross(b0, b1);
    b1xb2 = np.cross(b2, b1);
    
    b0xb1_x_b1xb2 = np.cross(b0xb1, b1xb2);
    
    y = np.dot(b0xb1_x_b1xb2, b1)*(1.0/np.linalg.norm(b1));
    x = np.dot(b0xb1, b1xb2);
    
    dih = np.degrees(np.arctan2(y, x))
    
    if dih < 0:
        return 360+dih
    else:
        return dih

def theta(dic_C4, dic_P, theta_dic):
    for i in dic_P:
        if ((int(i)-1) in dic_C4 and i in dic_C4 and (int(i)+1) in dic_P):
            theta_dic.setdefault(i, []).append(dihedral(dic_C4[int(i)-1], dic_P[i], dic_C4[i], dic_P[int(i)+1]));
        else:
            continue


def eta(dic_C4, dic_P, eta_dic):
    for i in dic_P:
        if (i in dic_C4 and (int(i)+1) in dic_C4 and (int(i)+1) in dic_P):
            eta_dic.setdefault(i, []).append(dihedral(dic_P[i], dic_C4[i], dic_P[int(i)+1], dic_C4[int(i)+1]));
        else:
            continue

def delta_sq(iso, full):
    delta_sq_dic = {}
    for i in iso.keys():
        find = False
        if i in full.keys():
            find = True
        if find:
            delta_t = np.abs(iso[i]-full[i])
        if delta_t > 180:
            delta_2 = (360 - delta_t)**2
        else:
            delta_2 = delta_t**2
        delta_sq_dic[i] = delta_2
    return delta_sq_dic

def analyze_frame(frame, theta_val, eta_val):
    input_P = []
    input_C4 = []
    input_theta_dic = {}
    input_eta_dic = {}
    
    get_coords(frame, input_P, input_C4)
    
    input_P_dic = {input_P[i][0]:input_P[i][1] for i in range(len(input_P))}
    input_C4_dic = {input_C4[i][0]:input_C4[i][1] for i in range(len(input_C4))}
    
    theta(input_C4_dic, input_P_dic, theta_val)
    eta(input_C4_dic, input_P_dic, eta_val)

def read_frame(filename, theta_out, eta_out):
    with open(filename, 'r') as file_in:
        in_frame = False
        num_frame = 0
        
        for line in file_in:
            entries = line.strip().split()
            #if num_frame > 10000:
            #    break
            if entries[0] == "Generated":
                frame = []
                theta_frame = {}
                eta_frame = {}
                num_frame += 1
                if num_frame > 999 and num_frame % 1000 == 0:
                    print(num_frame)
                continue
            elif len(entries) == 6:
                frame.append(line)
            elif len(entries) == 3:
                analyze_frame(frame, theta_out, eta_out)
    return theta_out
    return eta_out

def wrtie_dic_to_file(dic, filenm):
    with open(filenm, 'w') as fo:
        fo.write(json.dumps(dic))

iso_theta_out = {}
iso_eta_out = {}
full_theta_out = {}
full_eta_out = {}

read_frame(iso_fn, iso_theta_out, iso_eta_out)
read_frame(full_fn, full_theta_out, full_eta_out)

dic_name = {'iso_theta': iso_theta_out,
           'iso_eta': iso_eta_out,
           'full_theta': full_theta_out,
           'full_eta': full_eta_out}

for i in ['iso', 'full']:
    for j in ['theta', 'eta']:
        fn = "./%s_%s.txt" %(i, j)
        dic = '%s_%s' %(i, j)
        wrtie_dic_to_file(dic_name[dic], fn)

