#!/usr/bin/env python3

import re
import os 
import argparse
import requests
import urllib.request
from bs4 import BeautifulSoup 

#1
#URLS=[
#    'http://torlinkbgs6aabns.onion/',
#    'http://jh32yv5zgayyyts3.onion/',
#    'https://onions.danwin1210.me/',
#    'http://onionlstmjc7qkmj.onion/',
#    'http://torlinkbgs6aabns.onion/',
#    'http://xmh57jrzrnw6insl.onion/',
#    'http://5plvrsgydwy2sgce.onion/',
#    'http://uj3wazyk5u4hnvtk.onion/',
#    'http://haystakvxad7wbk5.onion/',
#    'http://qhhunyjzmdyx4i4d.onion/',
#    ]

def parse_args():
    parser = argparse.ArgumentParser(description='Script that measures page sizes of pages accessible through tor.')
    parser.add_argument('--sample-list','-s', required=True, default='./samples.lst', type=str, help='Relative path to file with a list of samples [s1,s2,s3]')
    args = parser.parse_args()
    f = args.sample_list
    if not os.path.exists(f):
        print('[ ERROR ] : File does not exist.')
        sys.exit(1)
    return args.sample_list

def read_list(sample_list):
    ret_data = []
    with open(sample_list, 'r') as f_read:
        data = f_read.readlines()
        for line in data:
            line_no_new = line.replace('\n','')
            if not line_no_new.startswith('http://'):
                pref = 'http://'+line_no_new
                ret_data.append(pref)
            else:
                ret_data.append(line_no_new)
    return ret_data

def check_online(URLS):
    up = []
    for url in URLS:
        domain_name = url.split('/')[2]

        print('[ INFO  ] : Checking whether [{}] responds'.format(url))
        #with open('{}_file.tmp'.format(domain_name),'w') as f_write:
        try:
            code = urllib.request.urlopen(url).getcode()
            if code == 200:
                print('[ INFO  ] : >> RESPONSE HTTP:200 for [{}]'.format(url))
                up.append(url)
            else:

                continue
        except:
            print('[ WARN  ] : !! Host [{}] not online. Discarding measurement'.format(url))
            pass
    return up

def save_content(URLS):
    """
    Saves tor links for size measurement
    """
    results = {}
    
    for url in URLS:    
        if not url.endswith('/'):
            url += '/'
        print('[ INFO  ] : Measuring size of [{}]'.format(url))
        try:
            r = requests.get(url)
            enc = r.encoding
            soup = BeautifulSoup(r.content,"lxml")
            sub_tot = 0
                
            links = soup.find_all('link')
            for link in links:
                content = link['href']
                #print(link['rel'])
                if not link['rel'] == ['alternate']: 
                    if not content == url:
                        if content.startswith('http'):
                            try:
                                print('[ INFO  ] : Measuring size of [{}]'.format(content))
                                page = urllib.request.urlopen(content)
                                data = page.read()
                                #print(len(data))
                                sub_tot += len(data)
                            except:
                                pass
                        elif content.startswith('/'):
                            try:
                                content_no_slash = content[1:]
                                content_comb = url+content_no_slash
                                print('[ INFO  ] : Measuring size of [{}]'.format(content_comb))
                                page = urllib.request.urlopen(content_comb)
                                data = page.read()
                                #print(len(data))
                                sub_tot += len(data)
                            except:
                                pass
                        elif not content.startswith('/'):
                            try:
                                content_comb = url+content
                                print('[ INFO  ] : Measuring size of [{}]'.format(content_comb))
                                page = urllib.request.urlopen(content_comb)
                                data = page.read()
                                #print(len(data))
                                sub_tot += len(data)
                            except:
                                pass
    
            imgs = soup.find_all('img')
            for img in imgs:
                #print(img)
                content = img['src']
                if content.startswith('http'):
                    try:
                        print('[ INFO  ] : Measuring size of [{}]'.format(content))
                        page = urllib.request.urlopen(content)
                        data = page.read()
                        #print(len(data))
                        sub_tot += len(data)
                    except:
                        pass
                elif content.startswith('/'):
                    try:
                        content_no_slash = content[1:]
                        content_comb = url+content_no_slash
                        print('[ INFO  ] : Measuring size of [{}]'.format(content_comb))
                        page = urllib.request.urlopen(content_comb)
                        data = page.read()
                        #print(len(data))
                        sub_tot += len(data)
                    except:
                        pass
                elif not content.startswith('/'):
                    try:
                        content_comb = url+content
                        print('[ INFO  ] : Measuring size of [{}]'.format(content_comb))
                        page = urllib.request.urlopen(content_comb)
                        data = page.read()
                        #print(len(data))
                        sub_tot += len(data)
                    except:
                        pass
    
            scripts = soup.find_all('script')
            entries = []
            for script in scripts:
                entries.append(str(script))
            for content_url in entries:
                if 'src' in content_url:
                   content = content_url.split('"')[1]
                   if content.startswith('http'):
                       try:
                           print('[ INFO  ] : Measuring size of [{}]'.format(content))
                           page = urllib.request.urlopen(content)
                           data = page.read()
                           #print(len(data))
                           sub_tot += len(data)
                       except:
                           pass
                   elif content.startswith('/'):
                       try:
                           content_no_slash = content[1:]
                           content_comb = url+content_no_slash
                           print('[ INFO  ] : Measuring size of [{}]'.format(content_comb))
                           page = urllib.request.urlopen(content_comb)
                           data = page.read()
                           #print(len(data))
                           sub_tot += len(data)
                       except:
                           pass
                   elif not content.startswith('/'):
                       try:
                           content_comb = url+content
                           print('[ INFO  ] : Measuring size of [{}]'.format(content_comb))
                           page = urllib.request.urlopen(content_comb)
                           data = page.read()
                           #print(len(data))
                           sub_tot += len(data)
                       except:
                           pass
    
            frames = soup.find_all('iframe')
            for frame in frames:
                #print(frame['src'])
                content = frame['src']
                if content.startswith('http'):
                    try:
                        print('[ INFO  ] : Measuring size of [{}]'.format(content))
                        page = urllib.request.urlopen(content)
                        data = page.read()
                        #print(len(data))
                        sub_tot += len(data)
                    except:
                        pass
                elif content.startswith('/'):
                    try:
                        content_no_slash = content[1:]
                        content_comb = url+content_no_slash
                        print('[ INFO  ] : Measuring size of [{}]'.format(content_comb))
                        page = urllib.request.urlopen(content_comb)
                        data = page.read()
                        #print(len(data))
                        sub_tot += len(data)
                    except:
                        pass
                elif not content.startswith('/'):
                    try:
                        content_comb = url+content
                        print('[ INFO  ] : Measuring size of [{}]'.format(content_comb))
                        page = urllib.request.urlopen(content_comb)
                        data = page.read()
                        #print(len(data))
                        sub_tot += len(data)
                    except:
                        pass

            page = urllib.request.urlopen(url)
            data = page.read()
            length = len(data)
            total = sub_tot + length
        except:
            print('[ ERROR ] : Not succeeded to measure [{}]'.format(url))
            pass
        results[url]=total
    return results

def main():
    sample_list = parse_args()
    URLS = read_list(sample_list)
    online_list = check_online(URLS)
    results = save_content(online_list)
    
    for key,val in results.items():
        print('[ INFO  ] : Domain [{k}] has size {v}'.format(k=key,v=val))

if __name__ == '__main__':
    main()
