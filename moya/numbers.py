import csv
import random
import re

NUMBER_MATCHER = re.compile(r'^[0-9]{7,15}$')

def is_number(thing):
    return NUMBER_MATCHER.match(thing)

def file_reader(fh, batch_size=10000):
    """
    Read through a file with phone numbers on each line and return the valid looking ones in batches
    """
    buf = []
    for number in fh:
        number = number.strip()
        if not is_number(number):
            print(f"Line {number} doesn't look like a phone number - skipping")
            continue

        buf.append(number)
        if len(buf) >= batch_size:
            yield buf
            buf = []
    if buf:
        yield buf

def csv_reader(fh, batch_size=1000):
    """
    Read through a CSV with headers, it must contain at least a column called to which contains the numbers
    """
    buf = []
    for row in csv.DictReader(fh):
        number = row['to']
        if not is_number(number):
            raise Exception("Line {number} doesn't look like a phone number")
        buf.append((number, row))

        if len(buf) >= batch_size:
            yield buf
            buf = []
    if buf:
        yield buf

def random_numbers(count=50, batch_size=10000):
    """
    For internal testing purposes, generate a batch of random numbers. Do not use in production.
    """
    buf = []
    for n in range(1, count):
        buf.append("279%07d" % random.randrange(10000000))
        if len(buf) > batch_size:
            yield buf
            buf = []
    yield buf
