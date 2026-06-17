import HTML_ieguve_no_url
import HTMLapstrade

url1 = input("Pirmais URL: ")
url2 = input("Otrais URL: ")

raksts1 = HTML_ieguve_no_url.get_body_html(url1)
raksts2 = HTML_ieguve_no_url.get_body_html(url2)

site1 = raksts1["site"]
site2 = raksts2["site"]

teksts1 = HTMLapstrade.html_to_txt(raksts1["html"])
teksts2 = HTMLapstrade.html_to_txt(raksts2["html"])

print("\n=== Pirmais raksts ===")
print("Vietne:", site1)
# print(raksts1)
# print(teksts1)