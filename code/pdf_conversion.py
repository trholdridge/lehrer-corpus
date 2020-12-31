# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 19:20:16 2020

@author: trhol
"""
import os
from PyPDF2 import PdfFileReader

# pdf_folder_to_text_files
# use path to folder of pdfs, get raw text of all and store in new text files in lyrics-text
def pdf_folder_to_text_files(path):
    new_folder = path.replace("lyrics-pdf", "lyrics-text")
    os.mkdir(new_folder)
    
    print("{",end="")
    # create a corresponding raw text file for each pdf
    for pdf_name in os.listdir(path):
        print("|",end="")
        txt_name = pdf_name.replace(".pdf",".txt")
        
        raw_text_file = open(new_folder + "/" + txt_name,"w")
        text = pdf_to_raw(path + "/" + pdf_name)
        raw_text_file.write(text)
        raw_text_file.close()
    print("}")
    
    print("Finished!")
        
    

# pdf_to_raw
# use path to pdf file, get raw text using PyPDF
def pdf_to_raw(path):
    pdf = PdfFileReader(path)
    full_text = "" #fill this with each page's content
    
    for i in range(pdf.getNumPages()):
        # include a space between one page's content and the next, if none already
        if len(full_text) > 0 and full_text[-1] != " ":
            full_text += " "
            
        temp_page = pdf.getPage(i)
        full_text += temp_page.extractText()
    
    return full_text