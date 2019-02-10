# README.MD

This repository contains some scripts that were used for scraping a part of the dark web available through TOR.

## Prerequisites

1. Make sure to use a VPN and TOR gatway.
2. Clone this repository
3. Install pip3 and virtualenv
4. Install requirements
```bash
pip3 install -r requirements.txt
```
5. Creat a virtual environment:
```bash
virtualenv venv
source venv/bin/activate
```

Script usage below

### 1_1_surface_scraper.py
Script for scraping onion sites from seed lists found on the surface web:
```bash
usage: 1_1_surface_scraper.py [-h] --raw-outdir RAW_OUTDIR --parsed-outdir
                              PARSED_OUTDIR [--url-seed-file URL_SEED_FILE]
```

url seed file defaults to `./seed_lists/surface-seeds.lst`.

### 1_2_onion_scraper.py
Script for scraping onion sites from seed lists found on the dark web:
```bash
usage: 1_2_onion_scraper.py [-h] --raw-outdir RAW_OUTDIR --parsed-outdir
                            PARSED_OUTDIR [--url-seed-file URL_SEED_FILE]
                            [--backoff BACKOFF]
```

The --backoff can be used to pause for 5 seconds after BACKOFF scraped sites. Use this if you are getting Connection refused errors.
url seed file defaults to `./seed_lists/onion-seeds.lst`.

### 2_measure_growth.py
Measures the growth of onion lists over time and plots the results (requires matplotlib).
```bash
usage: 2_measure_growth.py [-h] --parsed-directory PARSED_DIRECTORY
```

### 3_measure_overlap.py
Script that measures the overlap of of several datasets as generated with 1_1 and 1_2:
```bash
usage: 3_measure_overlap.py [-h] --parsed-directory PARSED_DIRECTORY
```

### 4_create_sample.py
Creates a number of samles based on a file and writes to another file:
```bash
usage: 4_create_sample.py [-h] --in-file IN_FILE --out-file OUT_FILE --count
                          COUNT
```

Some sample lists are included in `./sample_lists`

### 5_1_measure_mean_size_synchronous.py
Script that measures the page sizes synchronously, based on a sample list:
```bash
usage: 5_1_measure_mean_size_synchronous.py [-h] --sample-list SAMPLE_LIST
```

Beware: this script is SLOW!

### 5_2_measure_mean_size_asynchronous.py
Script to measure page sizes asynchronously, based on a sample list:
```bash
usage: 5_2_measure_mean_size_asynchronous.py [-h] --sample-list SAMPLE_LIST
```
