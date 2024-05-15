import os
from PyPDF2 import PdfReader
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict

class VirtualLibrarian:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.documents = defaultdict(set)
        self.stop_words = set(stopwords.words('english'))

    def index_documents(self):
        for file_name in os.listdir(self.folder_path):
            if file_name.endswith('.pdf'):
                file_path = os.path.join(self.folder_path, file_name)
                with open(file_path, 'rb') as pdf_file:
                    pdf_reader = PdfReader(pdf_file)
                    for page_num in range(len(pdf_reader.pages)):
                        page = pdf_reader.pages[page_num]
                        text = page.extract_text()
                        tokens = word_tokenize(text)
                        keywords = [word.lower() for word in tokens if word.lower() not in self.stop_words]
                        self.documents[file_name].update(set(keywords))

    def search(self, keyword):
        keyword_words = set(keyword.lower().split())
        matches = []
        for file_name, keywords in self.documents.items():
            if keyword_words.issubset(keywords):
                matches.append(file_name)
        return matches

if __name__ == '__main__':
    folder_path = input("Enter the path to search: ")
    librarian = VirtualLibrarian(folder_path)
    librarian.index_documents()
    while True:
        keyword = input('Enter a Keyword: ')
        if keyword == 'exit':
            break
        matches = librarian.search(keyword)
        if len(matches) == 0:
            print('No matches found.')
        else:
            for match in matches:
                print(match)
