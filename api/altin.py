from http.server import BaseHTTPRequestHandler
import requests
from bs4 import BeautifulSoup
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = "https://www.altinkaynak.com/canli-kurlar/altin"
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        try:
            res = requests.get(url, headers=headers)
            soup = BeautifulSoup(res.text, 'html.parser')
            
            fiyatlar = []
            # Sitedeki her bir satırı (tr) buluyoruz
            rows = soup.find_all('tr')
            
            for row in rows:
                cols = row.find_all('td')
                if len(cols) > 0:
                    fiyatlar.append({
                        "tur": cols[0].text.strip(),
                        "alis": cols[1].text.strip(),
                        "satis": cols[2].text.strip(),
                        "degisim": cols[3].text.strip()
                    })

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*') # Flutter erişimi için kritik
            self.end_headers()
            
            self.wfile.write(json.dumps(fiyatlar).encode())
            
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())