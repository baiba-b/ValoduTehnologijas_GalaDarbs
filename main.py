import requests
from bs4 import BeautifulSoup
import html
import re
import HTML_ieguve_no_url
import HTMLapstrade

url1 = input("Pirmais URL: ")
url2 = input("Otrais URL: ")

teksts1 = HTML_ieguve_no_url.get_body_html(url1)
teksts2 = HTML_ieguve_no_url.get_body_html(url2)


teksts1= HTMLapstrade.html_to_txt(teksts1)
teksts2 = HTMLapstrade.html_to_txt(teksts2)


print("\n=== Pirmais raksts ===")
print(teksts1)

# print("\n=== Otrais raksts ===")
# print(teksts2)