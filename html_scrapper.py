from bs4 import BeautifulSoup
import requests

different_tables = {
    
}


url = "https://tradingeconomics.com/commodities"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9"
}

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, 'html.parser')

with open("commodities_rendered.html", "w", encoding="utf-8") as f:
    f.write(soup.prettify())

print("html file has been scrapped")

metal_search = soup.select("table.table-heatmap")

with open("scrapped_table.html", "w", encoding="utf-8") as f:
    print(metal_search, file=f)

rows_out = []

for table in metal_search:
    for row in table.select("tr"):
        cells = [c.get_text(strip=True) for c in row.select("th, td")]
        if cells:
            rows_out.append(cells)

with open("table_rows.txt", "w", encoding="utf-8") as f:
    print(rows_out, file=f)