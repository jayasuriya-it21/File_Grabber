import tkinter as tk
import webbrowser
from PyPDF2 import PdfReader
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from PIL import ImageTk, Image


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

    def search(self, query):
        query_words = set(query.lower().split())
        matches = []
        for file_name, keywords in self.documents.items():
            if query_words.issubset(keywords):
                matches.append(file_name)
        return matches

class GUI:
    def __init__(self, window):
        self.window = window
        self.window.geometry("950x520")
        self.window.config(bg="#EFEFEF")
        
        
        self.folder_path_label = tk.Label(self.window, text="File Grabber ⏎", font=("Algerian", 29), bg="#ecf07d", fg="red")
        self.folder_path_label.grid(row=0, column=0, sticky="n")
        
        

        self.folder_path_label = tk.Label(self.window, text="Folder Path ⏎", font=("Arial", 14), bg="#ecf07d")
        self.folder_path_label.grid(row=5, column=0, padx=10, pady=5)

        self.folder_path_box = tk.Entry(self.window, font=("Arial", 14),width=70)
        self.folder_path_box.grid(row=6, column=0, padx=10, pady=5, sticky="nswe")

        self.select_folder_button = tk.Button(self.window, text="Select Folder", font=("Arial", 14), bg="#0070F7", fg="white", bd=0, command=self.handle_select_folder)
        self.select_folder_button.grid(row=6, column=1, padx=10, pady=5, sticky="nswe")

        self.search_label = tk.Label(self.window, text="Search ⏎", font=("Arial", 14), bg="#ecf07d")
        self.search_label.grid(row=8, column=0, padx=10, pady=5)

        self.search_box = tk.Entry(self.window, font=("Arial", 14),width=70)
        self.search_box.grid(row=9, column=0, padx=10, pady=5, sticky="nswe")

        self.search_button = tk.Button(self.window, text="Search", font=("Arial", 14), bg="#0070F7", fg="white", bd=0, command=self.handle_search)
        self.search_button.grid(row=9, column=1, padx=10, pady=5, sticky="nswe")

        self.result_listbox = tk.Listbox(self.window, font=("Arial", 14),width=70)
        self.result_listbox.grid(row=11, padx=10, pady=5, sticky="nswe")
        
        self.result_listbox.bind("<<ListboxSelect>>", self.handle_link_click)
        
        self.result_listbox.bind("<Enter>", self.handle_listbox_enter)
        self.result_listbox.bind("<Leave>", self.handle_listbox_leave)
        
        
        window.grid_columnconfigure(0, weight=1)
        window.grid_columnconfigure(1, weight=1)
        #window.columnconfigure(0, weight=1)
        #window.rowconfigure(0, weight=1)
        

        self.librarian = VirtualLibrarian('')

    def handle_listbox_enter(self, event):
        self.result_listbox.configure(cursor="hand2")

    def handle_listbox_leave(self, event):
        self.result_listbox.configure(cursor="")
    
    
    def handle_select_folder(self):
        folder_path = tk.filedialog.askdirectory()
        self.folder_path_box.delete(0, tk.END)
        self.folder_path_box.insert(0, folder_path)
        self.librarian.folder_path = folder_path
        self.librarian.index_documents()
        
        

    def handle_search(self):
        query = self.search_box.get()

        self.result_listbox.delete(0, tk.END)

        matches = self.librarian.search(query)

        if len(matches) == 0:
            self.result_listbox.insert(tk.END, 'No matches found.')
        else:
            for match in matches:
                file_path = os.path.join(self.librarian.folder_path, match)
                self.result_listbox.insert(tk.END, file_path)
    
    def handle_link_click(self, event):
        # Get the selected text from the list box
        index = self.result_listbox.curselection()[0]
        link = self.result_listbox.get(index)

        webbrowser.open(link)


if __name__ == '__main__':
    window = tk.Tk()
    window.config(bg="blue")

    gui = GUI(window)
    window.config(bg="#ecf07d")
    window.mainloop()
