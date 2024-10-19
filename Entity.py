import os
import re
from google.cloud import language
from nltk import sent_tokenize
import nltk

nltk.download('punkt')

def getEntities(text):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"robust-cooler-420213-a095d7853caa.json"
    client = language.LanguageServiceClient()
    document = language.Document(content=text.title(), type_=language.Document.Type.PLAIN_TEXT)
    response = client.analyze_entities(document=document)
    return response.entities

def getWikipediaLinks(entities):
    wiki = {}
    for entity in entities:
        wiki_url = entity.metadata.get("wikipedia_url", "")
        if wiki_url:
            wiki[str(entity.name)] = str(wiki_url)
    return wiki

def addHTMLWikipediaLinks(wiki_links, text):
    return_text = text
    for link in wiki_links:
        pattern = re.compile(r'\b{}\b'.format(re.escape(link)), re.IGNORECASE)
        return_text = pattern.sub(f"<a href=\"{wiki_links[link]}\">{link}</a>", return_text)
    return return_text

def entityToHTMLLinks(text):
    entities = getEntities(text)
    wikilinks = getWikipediaLinks(entities)
    html = addHTMLWikipediaLinks(wikilinks, text)
    return html

def getFlashcards(summary):
    summary_processed = re.sub(r'[^\w\s.,]', '', summary)
    
    flashcards = []
    summary_sentences = sent_tokenize(summary_processed)
    
    for sent in summary_sentences:
        entities = getEntities(sent)
        if len(entities) != 0:
            for entity in entities:
                wiki_url = entity.metadata.get("wikipedia_url", "")
                if wiki_url:
                    flashcards.append([sent.replace(str(entity.name).lower(), "_____"), entity.name])
    
    return flashcards

if __name__ == "__main__":
    text = "YOUR QUESTION"
    print(getFlashcards(text))
