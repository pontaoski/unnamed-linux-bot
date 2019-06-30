#!/usr/bin/env python

def get_content(string, trim_words=2):
    array = string.split()
    return " ".join(array[trim_words:])