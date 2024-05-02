import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import requests
from bs4 import BeautifulSoup
from textwrap import fill
from transformers import pipeline  # Requires installation of the transformers library

# Function to scrape news articles
def scrape_news():
    news = []
    url = 'https://example.com/news'  # Replace with the URL of the news website you want to scrape
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('article')
    for article in articles:
        title = article.find('h2').text.strip()
        link = article.find('a')['href']
        news.append({'title': title, 'link': link})
    return news

# Function to scrape social media posts
def scrape_social_media():
    social_media_posts = []
    url = 'https://example.com/social-media'  # Replace with the URL of the social media platform you want to scrape
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    posts = soup.find_all('div', class_='post')
    for post in posts:
        content = post.find('p').text.strip()
        social_media_posts.append(content)
    return social_media_posts

# Function to summarize text
def summarize_text(text):
    summarizer = pipeline("summarization")
    summarized_text = summarizer(text, max_length=150, min_length=50, do_sample=False)[0]['summary_text']
    return summarized_text

# Function to shorten URL
def shorten_url(url):
    # You can integrate with any URL shortening service API here
    shortened_url = "http://short.url"  # Placeholder shortened URL
    return shortened_url

# Function to handle the "Summarize" button click event
def summarize():
    text = text_area.get("1.0", tk.END)
    if text.strip() == "":
        messagebox.showinfo("Error", "Please enter some text to summarize.")
    else:
        summarized_text = summarize_text(text)
        text_area.delete("1.0", tk.END)
        text_area.insert(tk.END, summarized_text)

# Function to handle the "Shorten URL" button click event
def shorten():
    url = url_entry.get()
    if url.strip() == "":
        messagebox.showinfo("Error", "Please enter a URL to shorten.")
    else:
        shortened_url = shorten_url(url)
        url_entry.delete(0, tk.END)
        url_entry.insert(0, shortened_url)

# Function to fetch and display content
def fetch_content():
    # Scrape news articles
    news = scrape_news()
    news_text = "\n".join([f"{article['title']} - {article['link']}" for article in news])
    news_area.insert(tk.END, news_text)

    # Scrape social media posts
    social_media_posts = scrape_social_media()
    social_media_text = "\n".join(social_media_posts)
    social_media_area.insert(tk.END, social_media_text)

# Create the main application window
root = tk.Tk()
root.title("Content Aggregator")

# Create and configure the main frame
main_frame = tk.Frame(root)
main_frame.pack(padx=10, pady=10)

# Create and configure the news area
news_label = tk.Label(main_frame, text="News Articles")
news_label.grid(row=0, column=0, sticky="w")
news_area = ScrolledText(main_frame, width=50, height=10, wrap=tk.WORD)
news_area.grid(row=1, column=0, padx=5, pady=5, sticky="w")

# Create and configure the social media area
social_media_label = tk.Label(main_frame, text="Social Media Posts")
social_media_label.grid(row=0, column=1, sticky="w")
social_media_area = ScrolledText(main_frame, width=50, height=10, wrap=tk.WORD)
social_media_area.grid(row=1, column=1, padx=5, pady=5, sticky="w")

# Create and configure the text area for summarization
summarize_label = tk.Label(main_frame, text="Text to Summarize")
summarize_label.grid(row=2, column=0, columnspan=2, sticky="w")
text_area = ScrolledText(main_frame, width=100, height=5, wrap=tk.WORD)
text_area.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="w")

# Create and configure the Summarize button
summarize_button = tk.Button(main_frame, text="Summarize", command=summarize)
summarize_button.grid(row=4, column=0, sticky="w")

# Create and configure the entry for URL shortening
url_label = tk.Label(main_frame, text="URL to Shorten")
url_label.grid(row=5, column=0, sticky="w")
url_entry = tk.Entry(main_frame, width=50)
url_entry.grid(row=6, column=0, padx=5, pady=5, sticky="w")

# Create and configure the Shorten URL button
shorten_button = tk.Button(main_frame, text="Shorten URL", command=shorten)
shorten_button.grid(row=6, column=1, padx=5, pady=5, sticky="w")

# Create and configure the Fetch Content button
fetch_button = tk.Button(main_frame, text="Fetch Content", command=fetch_content)
fetch_button.grid(row=7, column=0, columnspan=2, pady=10)

# Start the Tkinter event loop
root.mainloop()
