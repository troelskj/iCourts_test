# -*- coding: utf-8 -*-

# this script will handle tasks 1, 2 and 3
# Use the command "python troels.py path/to/csv_file folder/for/txt_files 
# Developed and tested with python 2.7.6 and linux 3.13.0-55. Python packages was upgraded using PIP 1.5.4


import sqlite3
import glob
import sys
import os
#from PyPDF2 import PdfFileReader
#from openpyxl import load_workbook
import re
#import nltk, pprint
import subprocess
import codecs


cases = []
votes = []

def create_db(tableOfTuples):
	
	db = sqlite3.connect('metadata.db')
	d = db.cursor()
	db.text_factory = str

	d.execute('CREATE TABLE documents (date, case_name, case_number, file_number, parties, ruling)')
	d.executemany('INSERT INTO documents VALUES (?,?,?,?,?,?)', tableOfTuples)

	db.commit()

	
	for line in d.execute("SELECT * FROM documents ORDER BY date"):
		print line
		



def organizer(csvfile):

	sheet = open(csvfile, 'r')

	y = 1

	date = ""
	case_name = ""
	case_number = ""
	parties = ""
	ruling = ""
	
	for line in sheet:
		row = line.split("\t")
		
		case_desc = ""
		
		if len(row) == 3:

			
			
			if y == 1: 
				y += 1
				pass # to get rid of title line
				
			else:
				x = 0
				
				for cell in row:
					x += 1			
					
					if x == 1: pass						
					elif x == 2:
						
						filename = str(cell)

						case_number = int(filename.split("/")[-2])
						
						file_number = filename.split("/")[-1].split(".")[0]
						
					elif x == 3:
					   
						case = str(cell).split(" - ")
						
						case_desc = case[2]
						
						date = case[0][1:]
						ruling = case[1].split()[0]

						
						# finding parties by searching for parenthises
						# perhaps expand with named entity detection from nltk				

						parts = re.findall(".+\((.+)\)",case[2])
						
						if len(parts) == 0:  
							parties = "Unknown parties"
						else: 
							parties = str(parts[0])
						case_name = case[2].split(" (")[0]
						
						#print id,date,ruling,parties[0],case_name
						
						case_details = date, case_name, case_number, file_number, parties, ruling
						cases.append(case_details)


def pdfConverter(folder):
	
	subprocess.call(["mkdir","convertedDocs"])

	commands=[]

	files = glob.glob(folder + "*.pdf")
	
	for document in files:
		
		#allowing multiple processes to be spawned if supported by CPU. can potentially speed up this part. 
		subprocess.call(["pdftotext", document, "-enc", "UTF-8", "convertedDocs/" + document[(document.rfind("/")+1):-3] + "txt"])
		

def texthandler(textfolder="convertedDocs/",database="metadata.db"):
		
		for doc in glob.glob(textfolder + "*.txt"):		
			document = codecs.open(doc, 'r',encoding="utf-8")
			
			namedEntities = []
			
			text = ""
			
			docname = doc.split("/")[1][:doc.split("/")[1].find(".")]
			
			# converts text file to one single string for better nltk handling
			for w in document:
				w = w.split()
				for u in w:
					
					if u == "\r\n": 
						pass
					else:
						text = text + " " + u
			
			if len(text)>0: # in case some document was unreadable

				in_favour = re.findall(" favour : (.+?)against",text, flags=re.IGNORECASE)
				against = re.findall("against : (.+?)\; +\(",text, flags=re.IGNORECASE)

				for votation in in_favour:
				
					for people in votation.split(";"):
					
						names = people.split()
					
						if len(names)>0:
					
							if names[0].lower() == "president" or names[0].lower() == "vice-president":

								vote =  docname, votenumber, "IN FAVOUR", names[1], names[0]
	#							print vote
								votes.append(vote)
							elif names[0].lower() == "judge" or names[0].lower() == "judges" and names[1].lower() == "ad" and names[2].lower() == "hoc":
								for u in names[3:]:
									vote =  docname, votenumber, "IN FAVOUR", u, "Judge ad hoc"
	#								print vote
									votes.append(vote)
							elif names[0].lower() == "judge" or names[0].lower() == "judges" and names[1].lower() != "ad":
								for u in names[2:]:
									vote =  docname, votenumber, "IN FAVOUR", u, "Judge" 
	#								print vote
									votes.append(vote)

					votenumber += 1
				
				votenumber = 1
				 
				for votation in against:

				
					for people in votation.split(";"):
					
						names = people.split()
					
						if len(names)>0:
					
							if names[0].lower() == "president" or names[0].lower() == "vice-president":

								vote =  docname, votenumber, "AGAINST", names[1], names[0]
	#							print vote
								votes.append(vote)
							elif names[0].lower() == "judge" or names[0].lower() == "judges" and names[1].lower() == "ad" and names[2].lower() == "hoc":
								for u in names[3:]:
									vote =  docname, votenumber, "AGAINST", u, "Judge ad hoc"
	#								print vote
									votes.append(vote)
							elif names[0].lower() == "judge" or names[0].lower() == "judges" and names[1].lower() != "ad":
								for u in names[2:]:
									vote =  docname, votenumber, "AGAINST", u, "Judge" 
	#								print vote
									votes.append(vote)

					votenumber += 1
				
				
				
def create_db_votes(tableOfTuples,database="metadata.db"):

# Creates a database with details about votations. Input comes from list of tuples generated by function texthandler
	
	db = sqlite3.connect(database)
	d = db.cursor()
	db.text_factory = str

	d.execute('CREATE TABLE votation (file_number, votation_number, vote, name, title)')
	
	d.executemany('INSERT INTO votation VALUES (?,?,?,?,?)', tableOfTuples)

	db.commit()
	
	for line in d.execute("SELECT * FROM votation ORDER BY name"):
		print line	
			
		  

organizer(sys.argv[1])  # = task 1, specify csv file
create_db(cases) # = task 2

##pdfConverter(folder)   

# task 3
texthandler(sys.argv[2])  #specify folder for txt files
create_db_votes(votes)

