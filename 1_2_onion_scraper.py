#!/usr/bin/env python3

import os
import re
import sys
import time
import datetime
import urllib.request
import argparse

def parse_args():
    """
    Parses the arguments from the command line.
    Defaults to './url-seed-file.lst'
    """
    parser = argparse.ArgumentParser(description='Script that scrapes the onion addresses from websites on the onion seed list.')
    parser.add_argument('--raw-outdir','-r', required=True, type=str, help='Relative path to output directory of raw files')
    parser.add_argument('--parsed-outdir','-p', required=True, type=str, help='Relative path to output directory if parsed files')
    parser.add_argument('--url-seed-file','-u', default='./seed_lists/onion-seeds.lst', type=str, help='Relative path to file with urls to crawl and parse')
    parser.add_argument('--backoff','-b', default=0, type=str, help='Amount of files to parse before backing off')
    args = parser.parse_args()
    raw_outdir = args.raw_outdir
    if not raw_outdir.startswith('./'):
        raw_outdir = './' + raw_outdir
    if not raw_outdir.endswith('/'):
        raw_outdir += '/'
    parsed_outdir = args.parsed_outdir
    if not parsed_outdir.startswith('./'):
        parsed_outdir = './' + parsed_outdir
    if not parsed_outdir.endswith('/'):
        parsed_outdir += '/'
    if not os.path.exists(args.url_seed_file):
        print('Seed file not found. Get a copy here:\nhttps://gist.githubusercontent.com/Coen-Schuijt/15a73917ea884f21ae3482345ae48349/raw/onion-seeds.lst') 
        sys.exit(1)
    return args.url_seed_file,args.backoff,raw_outdir,parsed_outdir

def get_date():
    """
    Returns today's date
    """
    today = datetime.datetime.today().strftime('%m-%d-%Y')
    return today

def get_urls(url_file):
    """
    Returns a list with urls parsed from the seed file
    """
    url_list = []
    with open('{}'.format(url_file), 'r') as f_read:
        data = f_read.readlines()
        for line in data:
            line = line.strip('\n')
            if not line.startswith('#'):
                url_list.append(line)
    return url_list

def check_directories(raw_outdir,parsed_outdir):
    """
    Checks if directorys are existent.
    If not, creates them.
    """
    print('[ INFO  ] : Checking existence of [{r}] and [{p}]'.format(r=raw_outdir,p=parsed_outdir))
    if not os.path.exists(raw_outdir):
        print('[ INFO  ] : Creating [{r}] directory'.format(r=raw_outdir))
        os.makedirs(raw_outdir)
    else:
        print('[ INFO  ] : Directory [{r}] exists'.format(r=raw_outdir))
    if not os.path.exists(parsed_outdir):
        print('[ INFO  ] : Creating [{p}] directory'.format(p=parsed_outdir))
        os.makedirs(parsed_outdir)
    else:
        print('[ INFO  ] : Directory [{p}] exists'.format(p=parsed_outdir))
    return 

def save_pages(raw_outdir,parsed_outdir,backoff,date,url_list):
    """
    Saves full html copies of the urls in the url_list
    Defaults to './raw' directory
    """
    for url in url_list:
        domain_name = url.split('/')[2]
        if domain_name == 'github.com':
            domain_name = domain_name + '_' + url.split('/')[3]
        if not os.path.isfile('{r}{date}_{dom}_addresses_raw'.format(r=raw_outdir,date=date,dom=domain_name)):
            counter = 1 
            try:
                print('[ INFO  ] : Saving web page [{}]'.format(domain_name))
                urllib.request.urlretrieve('{site}'.format(site=url), '{r}{date}_{dom}_addresses_raw'.format(r=raw_outdir,date=date,dom=domain_name))
            except KeyboardInterrupt as e:
                print('\n[ INFO  ] : Quit by user')
                sys.exit(1)
            except (urllib.error.HTTPError,urllib.error.URLError) as e:
                print('[ ERROR ] : Not succeeded to save [{dom}]\n[ ERROR ] : {error}'.format(dom=domain_name,error=e))
                try:
                    print('[ INFO  ] : Trying once more. Saving web page [{}]'.format(domain_name))
                    urllib.request.urlretrieve('{site}'.format(site=url), '{r}{date}_{dom}_addresses_raw'.format(r=raw_outdir,date=date,dom=domain_name))
                except (urllib.error.HTTPError,urllib.error.URLError) as e:
                    print('[ ERROR ] : Not succeeded to save [{dom}]\n[ ERROR ] : {error}'.format(dom=domain_name,error=e))
                    pass
        elif os.path.isfile('{r}{date}_{dom}_addresses_raw'.format(r=raw_outdir,date=date,dom=domain_name)):
            try:
                counter += 1
            # If the script is run after an error, with './raw/' directory containing old data, raise an error.
            # Script will remove the old file and run the script again.
            except UnboundLocalError as e:
                print('[ ERROR ] : Old data in [{r}] directory'.format(r=raw_directory))
                print('[ INFO  ] : Removing old data')
                os.remove('{r}{date}_{dom}_addresses_raw'.format(r=raw_dir,date=date,dom=domain_name))
                print('[ INFO  ] : Running script again')
                os.system('./onion_scraper.py')
                sys.exit(1)
            
            # Backoff for 10 seconds after downloading 20 pages
            if int(backoff) > 0:
                if counter % backoff == 0:
                    print('[ INFO  ] : Backoff factor, sleeping for 5 seconds')
                time.sleep(5)
            
            # Try to save the page
            try:
                print('[ INFO  ] : Saving web page ({cntr}) as part of [{dom}]'.format(cntr=counter,dom=domain_name))
                urllib.request.urlretrieve('{site}'.format(site=url), '{r}date}_{dom}_addresses_raw_tmp'.format(r=raw_outdir,date=date,dom=domain_name))
            except (urllib.error.HTTPError,urllib.error.URLError) as e:
                print('[ ERROR ] : Not succeeded to save [{dom}]\n[ ERROR ] : {error}'.format(dom=domain_name,error=e))
                try:
                    print('[ INFO  ] : Trying once more. Saving web page [{}]'.format(domain_name))
                    urllib.request.urlretrieve('{site}'.format(site=url), '{r}{date}_{dom}_addresses_raw_tmp'.format(r=raw_outdir,date=date,dom=domain_name))
                except (urllib.error.HTTPError,urllib.error.URLError) as e:
                    print('[ ERROR ] : Not succeeded to save [{dom}]\n[ ERROR ] : {error}'.format(dom=domain_name,error=e))
                    pass
            except KeyboardInterrupt as e:
                print('\n[ INFO  ] : Quit by user')
                sys.exit(1)
            except:
#                print('[ ERROR ] : Disconnected. Backing off')
#                time.sleep(10)
                print('[ INFO  ] : Trying again')
                try:
                    print('[ INFO  ] : Saving web page ({cntr}) as part of [{dom}]'.format(cntr=counter,dom=domain_name))
                    urllib.request.urlretrieve('{site}'.format(site=url), '{r}{date}_{dom}_addresses_raw_tmp'.format(r=raw_outdir,date=date,dom=domain_name))
                except:
                    pass
            
            # Open raw file and attempt to append the partial data
            with open('{r}{date}_{dom}_addresses_raw'.format(r=raw_outdir,date=date,dom=domain_name),'a') as f_append:
                try:
                    with open('{r}{date}_{dom}_addresses_raw_tmp'.format(r=raw_outdir,date=date,dom=domain_name),'r') as f_read:
                        data = f_read.readlines()
                        for line in data:
                            clean_line = line.rstrip('\n')
                            f_append.writelines(clean_line)
                    os.remove('{r}{date}_{dom}_addresses_raw_tmp'.format(r=raw_outdir,date=date,dom=domain_name))
                except UnicodeDecodeError as e:
                    if 'utf-8' in str(e):
                        with open('{r}{date}_{dom}_addresses_raw_tmp'.format(r=raw_outdir,date=date,dom=domain_name),'r',encoding='utf-8',errors='replace') as f_read:
                            data = f_read.readlines()
                            for line in data:
                                clean_line = line.rstrip('\n')
                                f_append.writelines(clean_line)
                        os.remove('{r}{date}_{dom}_addresses_raw_tmp'.format(r=raw_outdir,date=date,dom=domain_name))
                    else:
                        print('[ ERROR ] : An error occured when parsing the page: {}'.format(e))
                        os.remove('{r}{date}_{dom}_addresses_raw_tmp'.format(r=raw_outdir,date=date,dom=domain_name))
                        pass

def parse_addresses(raw_outdir,parsed_outdir,date,url_list):
    """
    Parses the .onion links from all plain html files
    """
    for raw_file in os.listdir(raw_outdir):
        if raw_file.endswith('_addresses_raw'):
            no_suffix_filename = raw_file.rstrip('_raw')
            parsed_filename = no_suffix_filename + '_parsed'
            if not os.path.isfile(parsed_outdir+parsed_filename):
                print('[ INFO  ] : Parsing contents of [{}]'.format(row_outdir+raw_file))
                print('[ INFO  ] : Writing contents to [{}]'.format(parsed_outdir+parsed_filename))
                lines_parsed = set()
                with open(raw_outdir+raw_file, 'r',errors='replace') as f_read:
                    data = f_read.readlines()
                    with open(parsed_outdir+parsed_filename, 'w') as f_write:
                        for line in data:
                            for m in re.finditer(r'[a-zA-Z0-7]+\.onion\b', line, re.M | re.IGNORECASE):
                                if len(m.group(0)) < 16:
                                    pass
                                elif m.group(0) not in lines_parsed:
                                    f_write.writelines(m.group(0)+'\n')
                                    lines_parsed.add(m.group(0))
            if os.path.isfile(parsed_outdir+parsed_filename):
                time.sleep(10)
                lines_parsed = set()
                with open(parsed_outdir+parsed_filename, 'r') as f_read:
                    data = f_read.readlines()
                    for line in data:
                        line_clean = line.rstrip('\n')
                        lines_parsed.add(line_clean)
                    with open(parsed_outdir+parsed_filename, 'a') as f_append:
                        for line in data:
                            for m in re.finditer(r'[a-zA-Z0-7]+\.onion\b', line, re.M | re.IGNORECASE):
                                if len(m.group(0)) < 16:
                                    pass
                                elif m.group(0) not in lines_parsed:
                                    f_append.writelines(m.group(0)+'\n')
                                    lines_parsed.add(m.group(0))


def main():
    url_seed_file,backoff,raw_outdir,parsed_outdir = parse_args()
    print('[ INFO  ] : Using [{}] as seed file'.format(url_seed_file))
    date = get_date()
    url_list = get_urls(url_seed_file)
    cwd = check_directories(raw_outdir,parsed_outdir)
    save_pages(raw_outdir,parsed_outdir,backoff,date,url_list)
    parse_addresses(raw_outdir,parsed_outdir,date,url_list)

if __name__ == "__main__":
    main()
