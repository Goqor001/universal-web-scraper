# Universal Web Scraper

A Python-based web scraping tool that extracts structured data from multi-page websites.

## Features

* Scrapes data from multiple pages (pagination support)
* Extracts structured data (text, authors, tags, links, etc.)
* Cleans and organizes data using pandas
* Exports results to CSV

## Technologies Used

* Python
* requests
* BeautifulSoup
* pandas

## How It Works

1. Sends HTTP requests to the target website
2. Parses HTML using BeautifulSoup
3. Extracts relevant data elements
4. Automatically follows pagination
5. Stores clean data into CSV

## Example Output

* CSV file with structured data (see `data/sample_output.csv`)

## How to Run

1. Install dependencies:

pip install -r requirements.txt

2. Run the script:

python universal_scraper.py

## Use Cases

* Data collection from websites
* Market research
* Content aggregation
* Lead generation (basic level)

## Notes

This scraper is designed for static websites (non-JavaScript heavy pages).
