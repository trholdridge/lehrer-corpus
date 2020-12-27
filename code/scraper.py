# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 23:08:56 2020

@author: trhol
"""

from web_scraper_functions import *

print("Getting PDF links:")
directory = get_dir_page("https://tomlehrersongs.com/category/lyrics/")
urls = get_pdf_urls(directory)

print()
print("Downloading PDFs:")
download_pdfs(urls)
