#!/usr/bin/env python3

import os
import argparse
import itertools

def parse_args():
    """
    Parses the arguments from the command line.
    Defaults to './parsed/'
    """
    parser = argparse.ArgumentParser(description='Script to parse the onion files generated by the onion_scraper script.')
    parser.add_argument('--parsed-directory','-p', required=True, type=str, help='Relative path to file with urls to parse')
    args = parser.parse_args()
    if not args.parsed_directory.endswith('/'):
        args.parsed_directory += '/'
        if not args.parsed_directory.startswith('./'):
            args.parsed_directory = './' + args.parsed_directory 
    print('[ INFO  ] : Using [{}] as parsed_directory'.format(args.parsed_directory))
    return args.parsed_directory

def check_directory(parsed_dir):
    """
    Checks if the given directory exists.
    If not, raises an error and exits.
    """
    cwd = os.getcwd()
    print('[ INFO  ] : Current directory [{}]'.format(cwd))
    print('[ INFO  ] : Checking existence of [{}]'.format(parsed_dir))
    if os.path.exists(parsed_dir):
        print('[ INFO  ] : Directory [{}] exists'.format(parsed_dir))
    else:
        print('[ ERROR ] : Directory [{}] does not exsist.'.format(parsed_dir))
        sys.exit(1)
    return

def create_domain_list(directory):
    """
    Creates a list of unique domain names from parsed directory.
    """
    print('[ INFO  ] : Generating list of unique domains for [{d}]'.format(d=directory))
    domain_list = []
    for parsed_file in os.listdir(directory):
        domain = parsed_file.split('_')[1]
        if domain == 'github.com':
            domain = domain + '_' + parsed_file.split('_')[2]
        if not domain in domain_list:
            domain_list.append(domain)
    return domain_list

def group_domains(domain_list,directory):
    """
    Creates a set for each domain name.
    Adds the files for same domain with different dates to that set.
    """
    print('[ INFO  ] : Creating sets of files with same domain name')
    grouped_domain_list = []
    for domain in domain_list:
        domain_set = set()
        for parsed_file in os.listdir(directory):
            if domain in parsed_file:
                domain_set.add(parsed_file)
        grouped_domain_list.append(domain_set)
    return grouped_domain_list

def generate_unique_sets(domain_sets,directory):
    """
    Creates a list with unique domains for each onion list.
    """
    unique_lists = []
    list_lengths = []
    for domain_set in domain_sets:
        unique_sublist = []
        for parsed_file in domain_set:
            with open(directory+parsed_file,'r') as f_read:
                data = f_read.readlines()
                for line in data:
                    line = line.rstrip('\n')
                    if not line in unique_sublist:
                        unique_sublist.append(line)
        unique_lists.append(unique_sublist)
        list_lengths.append(len(unique_sublist))
    return unique_lists,list_lengths

def display_lengths(domain_list,list_lengths):
    for e,domain in enumerate(domain_list):
        print('[ INFO  ] : {} has length {}'.format(domain,list_lengths[e]))

def combinations(iterable, r):
    # combinations('ABCD', 2) --> AB AC AD BC BD CD
    # combinations(range(4), 3) --> 012 013 023 123
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = list(range(r))
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        yield tuple(pool[i] for i in indices)

def map_combinations(unique_lists):
    iter_string = ''
    for e,unique_list in enumerate(unique_lists):
        iter_string += str(e)

    #    possibilities = combinations(iter_string,3)
    poss = []
    for L in range(2, len(unique_lists)+1):
        for subset in itertools.combinations(iter_string, L):
            poss.append(subset)
    return list(poss)
   
def measure_overlap(combinations,unique_lists,domain_list):
    for combination in combinations:
        parsed_comb = list(combination)
        int_comb = []
        list_comb = []
        name_comb = ''
        for item in parsed_comb:
            int_comb.append(int(item))
        for e,unique_list in enumerate(unique_lists):
            if e in int_comb:
                list_comb.append(unique_list)
        
        overlap_count = len(set.intersection(*map(set,list_comb)))
        
        for n,domain in enumerate(domain_list):
            if n in int_comb:
                name_comb += '{ide}:'.format(ide=n+1)
#                name_comb += '{}:{} and '.format(n+1,domain)
#        name_comb_fixed = name_comb.rstrip(' and ')
        print('[ INFO  ] : {} have an overlap of: {}'.format(name_comb,overlap_count))

def main():
    parsed_directory = parse_args()
    #print('[ INFO  ] : Using [{}] as parsed_directory'.format(parsed_directory))
    cwd = check_directory(parsed_directory)
    
    # Returns a list of unique domains per onion list
    domain_list = create_domain_list(parsed_directory)

    # Groups files for same onion lists together
    grouped_domain_list = group_domains(domain_list,parsed_directory)

    # Generates unique lists for each domain
    unique_lists,lengths = generate_unique_sets(grouped_domain_list,parsed_directory)

    display_lengths(domain_list,lengths)

    # Map all combinations for lists
    combinations = map_combinations(unique_lists)

    # Measure overlap
    measure_overlap(combinations,unique_lists,domain_list)

if __name__ == "__main__":
    main()
