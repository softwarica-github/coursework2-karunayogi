# The grand enhancement of our digital conduit
import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox, Toplevel
from PIL import Image, ImageTk
import tempfile
import os

# A function to cast our net into the digital sea and gather what we seek
def scrape_the_web(url, scrape_type):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        if scrape_type == 'Title':
            return soup.title.text if soup.title else "Title not found"
        elif scrape_type == 'Headlines':
            headlines = [h.get_text() for h in soup.find_all(['h1', 'h2', 'h3'])]
            return '\n'.join(headlines) if headlines else "No headlines found"
        elif scrape_type == 'Images':
            images = [img['src'] for img in soup.find_all('img') if img.get('src')]
            return '\n'.join(images) if images else "No images found"
        elif scrape_type == 'Links':
            links = [a['href'] for a in soup.find_all('a', href=True)]
            return '\n'.join(links) if links else "No links found"
        elif scrape_type == 'Full Text':
            paragraphs = [p.get_text() for p in soup.find_all('p')]
            return '\n'.join(paragraphs) if paragraphs else "Text not found"
    except Exception as e:
        return f"Failed to retrieve data: {e}"

# A function to download the first image from a URL
def download_first_image(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all('img')
        
        if not img_tags:
            return None
        
        img_url = img_tags[0]['src']
        if not img_url.startswith('http'):
            return None
        
        img_response = requests.get(img_url, stream=True)
        if img_response.status_code == 200:
            with tempfile.NamedTemporaryFile(delete=False) as f:
                for chunk in img_response.iter_content(1024):
                    f.write(chunk)
                return f.name
    except Exception as e:
        print(f"Failed to download image: {e}")
        return None

# The GUI, a conduit for our digital divinations
class CyberScrollApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Arcanum of the Web")
        self.geometry("800x500")  # A grander portal

        # URL input
        self.url_label = tk.Label(self, text="Enter the URL, seeker of truths:")
        self.url_label.pack()

        self.url_entry = tk.Entry(self, width=80)
        self.url_entry.pack()

        # Selection of the type of knowledge to seek
        self.scrape_type_label = tk.Label(self, text="Select the type of knowledge you seek:")
        self.scrape_type_label.pack()

        self.scrape_options = ttk.Combobox(self, values=['Title', 'Headlines', 'Images', 'Links', 'Full Text'])
        self.scrape_options.pack()
        self.scrape_options.current(0)  # Default to seeking 'Title'

        # Command button to initiate the search
        self.scrape_button = tk.Button(self, text="Unveil the digital secrets", command=self.uncover_secrets)
        self.scrape_button.pack()

        # A scrollable area to display the unearthed secrets
        self.result_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=100, height=20)
        self.result_area.pack()

        # Button to save the discovered secrets
        self.save_button = tk.Button(self, text="Save Secrets", command=self.save_secrets)
        self.save_button.pack()

        # Button to clear the search history
        self.clear_button = tk.Button(self, text="Clear History", command=self.clear_history)
        self.clear_button.pack()

    def uncover_secrets(self):
        # Gather the URL and the desired information type from the user
        url = self.url_entry.get()
        scrape_type = self.scrape_options.get()
        
        # Invoke our digital net to fetch the secrets
        result = scrape_the_web(url, scrape_type)
        
        # Display the found secrets in the scrollable area
        self.result_area.delete('1.0', tk.END)  # Clear previous findings
        self.result_area.insert(tk.INSERT, f"Discovered secrets: \n{result}")
        
        # If the user selects 'Images', download and display the first image
        if scrape_type == 'Images':
            img_path = download_first_image(url)
            if img_path:
                self.display_image(img_path)

    def save_secrets(self):
        # Save the contents of the result area to a file
        secrets = self.result_area.get('1.0', tk.END)
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, 'w') as file:
                file.write(secrets)
            messagebox.showinfo("Success", "The secrets have been safely stored in the scroll.")

    def clear_history(self):
        # Clear the URL entry and result area to start fresh
        self.url_entry.delete(0, tk.END)
        self.result_area.delete('1.0', tk.END)

    def display_image(self, path):
        if path is None:
            return
        
        # Display the downloaded image
        img_viewer = Toplevel(self)
        img_viewer.title("Image Viewer")
        img_viewer.geometry("400x400")
        
        img = Image.open(path)
        img = img.resize((380, 380), Image.ANTIALIAS)
        imgTk = ImageTk.PhotoImage(img)
        
        label = tk.Label(img_viewer, image=imgTk)
        label.image = imgTk
        label.pack()

# Summon the application to begin the quest for knowledge
if __name__ == "__main__":
    app = CyberScrollApp()
    app.mainloop()
