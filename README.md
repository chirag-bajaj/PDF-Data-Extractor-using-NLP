# Atlantis #

## Aim ##

### An application that extracts the title, authors and abstract from the pdf of a research paper. ###

## PDF to text conversion ##

The first step towards extraction of title, authors and abstract from a given pdf is conversion to of PDF file to text file.
Then the other step is splitting the Data into different parts for preprocessing.

## Title ##

Title of a research paper is usually given in beginning of the paper. But there are quite a number of papers which does not contain title. For these type of papers the **Title** will be generated.

## Authors ##

Authors of the research paper are listed in the beginning usually after the title. But they have weird indentation and also sometimes contains the name of the company/institute/school/laboratory. So if **Authors** are not available directly, they will be found using NLP.

## Abstract ##

An abstract may be a temporary outline of a research article, thesis, review, conference continuing, or any in-depth analysis of a selected subject and is commonly accustomed facilitate the reader quickly ascertain the paper's purpose. The abstract will either be the content already present under the heading **Abstract** or will be a summary made by ML(NLP).

## FRONTEND ##

The pdf file will be selected by the user and sent to local host. JSON format file will be returned with the prediction of the title, authors and abstract. It will be sent to the frontend and will be displayed content-wise.

## Conclusion ##

The user will get an intuition of what the research paper is saying and who are the authors and what are its references. This helps user to get an interest in the topic discussed in the  research paper.
