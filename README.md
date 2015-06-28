<h1>Notes:</h1>


<h2>Task 1:</h2>


I took a shortcut and converted the xlsx file to a csv file. That made it much easier to work with the data, as I could focus on python's string methods and not struggle with a third party module for accessing the xslx.


<h2>Task 2:</h2>


I created an SQLite database called "metadata.db". SQLite was chosen for the easy integration with python 2.7

In the database are two tables: 

documents contain data from task one. The structure is:

id, date, case_name, case_number, file_number, parties, ruling


<h2>Task 3:</h2>


After struggling with pyPDF2 and PDFMiner for some time I decided to use pdftotext from xpdf to do the conversion from pdf to txt. 

The files were added to a folder called "convertedDocs/" and named after their original file with a change in the extension from ".pdf" to ".txt".

I created a new table in "metadata.db" for this task called votations.

My solutions seems to prefer IN FAVOUR from AGAINST. I think a more intelligent indication for when the name listings have stopped will help. 



<h2>Task 4:</h2>


Tables documents and votations are joined to one table using NATURAL JOIN as file_number is a column in both tables: 

<code>CREATE TABLE docsandvotes AS SELECT * FROM documents NATURAL JOIN votation;</code>

Using SELECT and WHERE methods I have created two CSV files to be used in the visualization:

<code>sqlite3 -header -csv metadata.db "SELECT * FROM docsandvotes WHERE ruling<>'Order' AND title='President';" > presidentsonly_advisoryandjudgments.csv</code>

<code>sqlite3 -header -csv metadata.db "SELECT * FROM docsandvotes WHERE ruling<>'Order' ;" > advisoryandjudgments.csv</code>

I have uploaded these CSV files to Google's Fusion API where I also made the visualizations.

Advisory and jugments chart can be seen here: 

<a href="https://www.google.com/fusiontables/DataSource?docid=1DQC5tKOzAcEt1_L1BUgUKfv6f9Fzo8zS6IUnAmMc" target=_blank>https://www.google.com/fusiontables/DataSource?docid=1DQC5tKOzAcEt1_L1BUgUKfv6f9Fzo8zS6IUnAmMc</a>

Presidents only can be seen here: 

<a href="https://www.google.com/fusiontables/DataSource?docid=1edRzB3aNvonn9gkf_dGp2hXTSJ7BsSHUdoJVXDo_" target=_blank>https://www.google.com/fusiontables/DataSource?docid=1edRzB3aNvonn9gkf_dGp2hXTSJ7BsSHUdoJVXDo_</a>

In both cases, the visualization is on the third tab. 

The presidents only visualization shows that some cases seems to have more than one president, e.g. case number 124 - which is also a larger case. My texthandler looks for only one president and vice-president. But these are per votation, and there may be several in a case. 




<h2>Task 5:</h2>

I have no functional solution for this task, as I did not have time to complete it. This is my plain text suggestion to what could be done:

Use the references to create wordnet-like structure. Given this info, and perhaps use keyword extraction on the label text and the quoted articles, could be lead to an understanding of what the cases are about. 

Since these texts are about citizenship in the European Union, a classifier could be trained on a corpus with such text. 



<h2>Suggested improvements:</h2>


Give pyPDF2 and PDFMiner another go and check if more texts will be readable (e.g. including spaces between words and removing spaces between letters). Furthermore introduce OCR software to make the last files readable for my script.

Switch to Python3 for better UTF-8 support - there really isn't any reason not to as no external modules except nltk are used. PDFMiner did not suport Python 3, hence the selected version. 

The function "texthandler" in troels.py could with some modifications work faster in a multi process environment by spawning new processes each time one ends (something like subprocess.call or subprocess.popen). The output is added to a database and is not needed for anything else. Total processing time on my machine (i5 650, about 5 years old) is about 15 minutes with the current version. 

I have manily worked in the English parts of the documents. A simple extension could be to check for French votes (Pour/Contre) when no English are found. 

Making a language classifier (English or French) could also help and speed up the name finding process.

NLTK did not produce a good output for me when I tried finding named entities. To improve this, a classifier could be trained on a database of judge names. 

It looks like these documentes are following some standards regarding their setup, similar to biblipographies (e.g. APA style). If this is true, a judge document classifier can be used to determine e.g. which regex statements to use.

I may be interesting to try other visualizations in order to see where people agree and disagree. 


