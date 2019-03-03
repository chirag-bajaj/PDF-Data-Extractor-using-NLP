import nltk

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

def auth(sample):
    sentences = nltk.sent_tokenize(sample)
    tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
    tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
    chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=True)
    entity(chunked_sentences)


def extract_entity_names(t):
    entity_names = []

    if hasattr(t, 'label') and t.label:
        if t.label() == 'NE':
            entity_names.append(' '.join([child[0] for child in t]))
        else:
            for child in t:
                entity_names.extend(extract_entity_names(child))
    #print(set(entity_names))
    return set(entity_names)

def entity(chunked_sentences):
    entity_names = []
    for tree in chunked_sentences:
        # Print results per sentence
        # print extract_entity_names(tree)

        entity_names.extend(extract_entity_names(tree))

# Print all entity names
#print entity_names

# Print unique entity names
#print(set(entity_names))

#sample = "\n\nTapabrata Chakraborti1,2, Brendan McCane1, Steven Mills1, and Umapada Pal2\n\n1Dept. of Computer Science, University of Otago, NZ\n\n2CVPR Unit, Indian Statistical Institute, India\n\nJanuary 29, 2019\n\n"

#auth(sample)