# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 20:30:08 2020

@author: trhol
"""
import os
import requests
import time
import datetime
from bs4 import BeautifulSoup

#get_dir_page
# uses requests and BeautifulSoup to get parent page with links to lyrics
def get_dir_page(dir_url):
    # avoid getting 403'ed automatically:
    user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.37"
    
    num_pages = 10 # must check manually for length of infinite scroll
    
    # dir_url is the page with links to all lyric pdfs. we will fill directory_soup
    # with the page's contents
    print("Fetching... this process will take several minutes, to avoid spamming requests.")
    print("page 1 of {}...".format(num_pages))
    request_dir = requests.get(dir_url, headers={'User-Agent': user_agent})
    dir_content = request_dir.content
    time.sleep(30)
    
    #this is an infinite-scroll page, so we have to access each "page" of content:
    for i in range(num_pages - 1): 
        print("page {} of {}...".format((i+2),num_pages))
        scroll_url = dir_url + "page/" + str(i + 2) + "/"
        
        # use requests and beautifulsoup to get a section of the page's contents
        scroll_page = requests.get(scroll_url, headers={'User-Agent': user_agent})
        dir_content = dir_content + scroll_page.content
        time.sleep(30) # don't want site to get annoyed by scraping
    
    directory_soup = BeautifulSoup(dir_content, 'html.parser')
    print("Finished!")
    return directory_soup

# get_pdf_urls
# create a list of all urls of lyric pdf pages
def get_pdf_urls(directory_soup):
    #find containers for lyric links
    link_containers = directory_soup.find_all('div', attrs={'id' : 'posts-container'})
    
    # for each one, find all link boxes, then flatten that collection into a single list
    all_link_boxes = [container.find_all('div', attrs={'class': 'fusion-text'}) for container in link_containers]
    flat_link_boxes = [item for sublist in all_link_boxes for item in sublist]
    
    #for each of these link boxes:
    # - find the first link in it (sheet music links are always second)
    # - get the href of that link, and put it in a list
    all_urls = [box.find('a')['href'] for box in flat_link_boxes]
    
    print("urls obtained :)")
    return all_urls
    

# download_pdfs
# create a folder in "lyrics_pdf," labelled with the current date, and containing
# all lyric pdfs from lehrer's website as of that date
def download_pdfs(url_list):
    # make a new folder inside the pdf folder
    current_date = datetime.datetime.now().date()
    folder_name = current_date.isoformat()
    pdf_destination = '../lyrics-pdf/' + folder_name
    os.mkdir(pdf_destination)
    
    home_url = "https://tomlehrersongs.com/"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.37"
    
    print("Fetching... this process will take several minutes, to avoid spamming requests.")
    print("{",end="")
    for relative_url in url_list:
        print("|",end="")
        absolute_url = home_url + relative_url
        
        # request page from site
        r = requests.get(absolute_url, headers={'User-Agent': user_agent})
        pdf_name = absolute_url.split("/")[-1] # extract words after last / in url
        
        # download pdf to current folder
        download_pdf(r, pdf_name, pdf_destination + "/")
        
        time.sleep(10) # I'm impatient
    print("}")
    print("Finished!")
    
# download_pdf
def download_pdf(response, filename, path):
    file = open(path + filename, 'wb')
    file.write(response.content)
    file.close()