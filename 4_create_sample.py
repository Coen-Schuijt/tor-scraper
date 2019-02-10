#!/usr/bin/env python3

import os
import sys
import random
import argparse

def parse_args():
    """
    Parses the arguments from the command line.
    Defaults to './parsed/'
    """
    parser = argparse.ArgumentParser(description='Script to generate a list of random samples from the complete list with onion addresses.')
    parser.add_argument('--in-file','-i', required=True, type=str, help='Relative path to file with urls to parse')
    parser.add_argument('--out-file','-o', required=True, type=str, help='Relative path to file to put samples in')
    parser.add_argument('--count','-c', required=True, type=str, help='Relative path to file with urls to parse')
    args = parser.parse_args()
    f = args.in_file
    o = args.out_file
    c = args.count
    print('[ INFO  ] : Using {} as seed file'.format(f))
    return f,o,c

def return_samples(in_file,count):
    complete_set = []
    with open(in_file, 'r') as f_read:
        data = f_read.readlines()
        for line in data:
            clean_line = line.rstrip('\n')
            complete_set.append(clean_line)
    samples = random.sample(complete_set, int(count))
    return samples
    
def main():
    in_file,out_file,count = parse_args()
    samples = return_samples(in_file,count)
    #fn = './sample.lst'
    with open(out_file, 'w') as f_write:
        for sample in samples:
            print('[ INFO  ] : Writing {s} to {fn}'.format(s=sample,fn=out_file))
            f_write.writelines(sample+'\n')

if __name__ == '__main__':
    main()
