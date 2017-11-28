#!/bin/python

import re
import os
import sys
import uuid
import random
import requests
import genanki
import string

from nltk.tokenize import sent_tokenize
from bs4 import BeautifulSoup
from gtts import gTTS
from googletrans import Translator

reload(sys);
sys.setdefaultencoding("utf8")

_base91_extra_chars = "!#$%&()*+,-./:;<=>?@[]^_`{|}~"

def base62(num, extra=""):
    s = string; table = s.ascii_letters + s.digits + extra
    buf = ""
    while num:
        num, i = divmod(num, len(table))
        buf = table[i] + buf
    return buf

def base91(num):
    return base62(num, _base91_extra_chars)

def guid64():
    return base91(random.randint(0, 2**64-1))

def normalize(sent):
    return re.sub('(?<! )(?=[.,!?()])|(?<=[.,!?()])(?! )', r' ', remove_characters(sent))

def hash(sent):
    return hashlib.md5(sent)

def remove_characters(sent):
    return  re.sub('[\xe2]', '', sent)

def generate_recording(sent, fname):
    tts = gTTS(text=sent, lang='cs', slow=True)
    tts.save(fname)

def add_note_to_deck(czech_sent, eng_sent, soundfile ):
    my_model = genanki.Model( 1607392319, 'Simple Model',fields=[{'name': 'Sentence'},{'name': 'Answer'},],
       templates=[
         {
           'name': 'Card 1',
           'qfmt': '{{Sentence}}',
           'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
         },
       ])
    my_note = genanki.Note(model=my_model, fields=[czech_sent + "[sound:" + soundfile + "]", eng_sent], guid=guid64(), sort_field="question") 
    my_deck.add_note(my_note)

if __name__ == "__main__":

    MAX_SENTENCE_LENGTH=60

    my_deck = genanki.Deck(2059400110,'Czech Listening Exercises')
    media_files = []

    base = "https://www.project-syndicate.org/"
    r  = requests.get(base + "archive?language=czech")
    data = r.text
    soup = BeautifulSoup(data, "html.parser")

    for listing in soup.find_all('article', { "class" : "listing listing--default " }):

         article_text = ""
         path = listing.find('a')["href"] + "/czech"
         cr  = requests.get(base + path)
         cdata = cr.text
         soup = BeautifulSoup(cdata, "html.parser")

         for paragraph in soup.find_all('p', { "data-line-id" : True }):
             article_text +=  normalize(paragraph.text)

         for line in sent_tokenize(article_text, language='czech'):

             if len(line) < MAX_SENTENCE_LENGTH:
                 translator = Translator()
                 soundfile = uuid.uuid4().get_hex().upper()[0:6] + ".mp3"
                 generate_recording(line, soundfile)
                 media_files.append(soundfile)
                 translation = translator.translate(line.encode('utf-8').strip()).text
                 add_note_to_deck(line, translation, soundfile)
                 print('Czech: %20s | English: %20s | Audio: %10s' % (line, translation, soundfile))

    my_package = genanki.Package(my_deck)
    my_package.media_files = media_files
    my_package.write_to_file('czech-sentences.apkg')

