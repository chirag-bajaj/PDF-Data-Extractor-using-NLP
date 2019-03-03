from PyPDF2 import PdfFileReader
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import BytesIO as StringIO
import bs4 as bs
import urllib.request
import re
import heapq
# ---------------------------------------------------------------------------------------------------------------------------------------------------

import nltk

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

# ---------------------------------------------------------------------------------------------------------------------------------------------------------

def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

# ------------------------------------------------------------------------------------------------------------------------------------------------------

check = int(input("Enter\n1 for file with abstract\n2 for file without abstract: "))

path = u"/home/kandarp/1506.02640.pdf"
path = path.encode(encoding='UTF-8',errors='strict')

# ---------------------------------------------------------------------------------------------------------------------------------------------------------

if check == 1:
    with open("plain.txt", "wb") as f:
        f.write(convert_pdf_to_txt(path))

    before_abstract = str(convert_pdf_to_txt(path)).split('\\nAbstract')[0]
    title = str(before_abstract).split('\\n')[0]
    length_of_title = len(title)

# ---------------------------------------------------------------------------------------------------------------------------------------------------------

    sample = str.encode(before_abstract)
    sentences = nltk.sent_tokenize(sample.decode())
    tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
    tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
    chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=True)

    def extract_entity_names(t):
        entity_names = []

        if hasattr(t, 'label') and t.label:
            if t.label() == 'NE':
                entity_names.append(' '.join([child[0] for child in t]))
            else:
                for child in t:
                    entity_names.extend(extract_entity_names(child))

        return entity_names

    entity_names = []
    for tree in chunked_sentences:
        # Print results per sentence
        # print extract_entity_names(tree)

        entity_names.extend(extract_entity_names(tree))

    # Print all entity names
    #print entity_names

    # Print unique entity names
    author = set(entity_names)

# ---------------------------------------------------------------------------------------------------------------------------------------------------------

    if before_abstract.startswith(title):
       before_abstract = before_abstract[len(title):]

# ---------------------------------------------------------------------------------------------------------------------------------------------------------

    if str(before_abstract) == str(convert_pdf_to_txt(path)):
        fo = open('plain.txt', 'r')
        article_text = fo.read()

        article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
        # print(article_text)
        article_text = re.sub(r'\s+', ' ', article_text)
        # print(article_text)

        formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text)
        # print(formatted_article_text)
        formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
        # print(formatted_article_text)

        sentence_list = nltk.sent_tokenize(article_text)

        stopwords = nltk.corpus.stopwords.words('english')

        word_frequencies = {}
        for word in nltk.word_tokenize(formatted_article_text):
            if word not in stopwords:
                if word not in word_frequencies.keys():
                    word_frequencies[word] = 1
                else:
                    word_frequencies[word] += 1

        maximum_frequncy = max(word_frequencies.values())

        for word in word_frequencies.keys():
            word_frequencies[word] = (word_frequencies[word] / maximum_frequncy)

        sentence_scores = {}
        for sent in sentence_list:
            for word in nltk.word_tokenize(sent.lower()):
                if word in word_frequencies.keys():
                    if len(sent.split(' ')) < 30:
                        if sent not in sentence_scores.keys():
                            sentence_scores[sent] = word_frequencies[word]
                        else:
                            sentence_scores[sent] += word_frequencies[word]

        summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

        summary = ' '.join(summary_sentences)
        abstract=summary
        abstract = re.sub("[^a-zA-Z]", " ", abstract)
        with open('abstract.txt', 'w+') as f:
            f.write(abstract)

        f = open('abstract.txt', 'rb')
        abstract = f.read()


# ---------------------------------------------------------------------------------------------------------------------------------------------------------

        references = before_abstract.split('References')[1]
        with open('references.txt', 'w+') as f:
            f.write(references)

        f = open('references.txt', 'rb')
        references = f.read()

# ---------------------------------------------------------------------------------------------------------------------------------------------------------

    else:
        abstract = str(convert_pdf_to_txt(path)).split('Abstract')[1].split('Introduction')[0]
        abstract = re.sub("[^a-zA-Z]", " ",  abstract)
        with open('abstract.txt', 'w+') as f:
            f.write(abstract)

        f = open('abstract.txt', 'rb')
        abstract = f.read()

# ---------------------------------------------------------------------------------------------------------------------------------------------------------

        references = str(convert_pdf_to_txt(path)).split('Abstract')[1].split('Introduction')[1].split('References')[1]
        with open('references.txt', 'w+') as f:
            f.write(references)

        f = open('references.txt', 'rb')
        references = f.read()

# ---------------------------------------------------------------------------------------------------------------------------------------------------------

    title = title[2:]
    author = list(author)
    #print("Title: ", title)
    #print("\n\n\n\n")
    #print("Before Abstract: ", before_abstract)
    #print("\n\n\n\n")
    #print("Author:", author)
    #print("\n\n\n\n")
    #print("Abstract: ", abstract)

# ---------------------------------------------------------------------------------------------------------------------------------------------------------

    OUTPUT = {
        'Title': title,
        'Author': author,
        'Abstract': str(abstract),
        'References': str(references)
    }

    import json

    s = json.dumps(OUTPUT)
    with open('final_output.json', 'w') as f:
        f.write(s)

# ---------------------------------------------------------------------------------------------------------------------------------------------------------

else:
    text = convert_pdf_to_txt(path)

    with open('plain.txt', 'wb') as f:
        f.write(text)

# ---------------------------------------------------------------------------------------------------------------------------------------------------------

    fo = open('plain.txt', 'r')
    article_text = fo.read()

    article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
    # print(article_text)
    article_text = re.sub(r'\s+', ' ', article_text)
    # print(article_text)

    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text)
    # print(formatted_article_text)
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
    # print(formatted_article_text)

    sentence_list = nltk.sent_tokenize(article_text)

    stopwords = nltk.corpus.stopwords.words('english')

    word_frequencies = {}
    for word in nltk.word_tokenize(formatted_article_text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

    maximum_frequncy = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word] / maximum_frequncy)

    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]

    summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

    summary = ' '.join(summary_sentences)
    abstract = summary
    abstract = re.sub("[^a-zA-Z]", " ", abstract)

    with open('abstract.txt','w+') as f:
        f.write(abstract)

    f = open('abstract.txt', 'rb')
    abstract = f.read()

# ---------------------------------------------------------------------------------------------------------------------------------------------------------

    references = article_text.split('References')[1]
    with open('references.txt', 'w+') as f:
        f.write(references)

    f = open('references.txt', 'rb')
    references = f.read()

# ---------------------------------------------------------------------------------------------------------------------------------------------------------

    OUTPUT = {
        'Title': None,
        'Author': None,
        'Abstract': str(abstract),
        'References': None
    }

    # print(OUTPUT)

    import json

    s = json.dumps(OUTPUT)

    with open('final_output.json', 'w') as f:
        f.write(s)

# ---------------------------------------------------------------------------------------------------------------------------------------------------------
