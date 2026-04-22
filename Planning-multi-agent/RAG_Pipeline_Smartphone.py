import json
import re
import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urlparse
from duckduckgo_search import DDGS
from deep_translator import GoogleTranslator

class RetrieverAgent:
      def __init__(self):
                self.headers = {
                              "User-Agent": "Mozilla/5.0",
                              "Accept": "text/html",
                              "Referer": "https://www.yahoo.com/"
                }

      def _expand_keywords(self, root_keyword: str) -> list:
                return [
                              f"{root_keyword} specifications features",
                              f"{root_keyword} camera battery display details",
                              f"{root_keyword} market share sales volume shipment price trend"
                ]

      def _scrape_google(self, query: str) -> list:
                results = []
                try:
                              with DDGS() as ddgs:
                                                ddg_results = list(ddgs.text(query, max_results=3))
                                                if ddg_results:
                                                                      ai_block = ddg_results[0]
                                                                      results.append({
                                                                          "url": ai_block.get('href', 'https://google.com'),
                                                                          "text": f"[Google AI] {ai_block.get('body', '')}"
                                                                      })
                                                                      for r in ddg_results[1:]:
                                                                                                results.append({
                                                                                                                              "url": r.get('href', ''),
                                                                                                                              "text": f"Title: {r.get('title', '')} | Content: {r.get('body', '')}"
                                                                                                  })
                except Exception as e:
                              print(f"Error: {e}")
                          return results

    def _scrape_yahoo(self, query: str) -> list:
              results = []
              try:
                            url = f"https://search.yahoo.com/search?p={query.replace(' ', '+')}"
                            response = requests.get(url, headers=self.headers, timeout=10)
                            if response.status_code == 200:
                                              soup = BeautifulSoup(response.text, "html.parser")
                                              items = soup.find_all('div', class_='algo-sr')
                                              if not items:
                                                                    items = soup.find_all(['h3', 'h2'])
                                                                for item in items[:4]:
                                                                                      title_tag = item.find(['h3', 'h2', 'a'])
                                                                                      snippet_tag = item.find(['p', 'span'], class_='compText') or item.find_next('p')
                                                                                      link_tag = item.find('a')
                                                                                      href = link_tag.get('href', '#') if link_tag else '#'
                                                                                      if title_tag:
                                                                                                                title = title_tag.get_text().strip()
                                                                                                                snippet = snippet_tag.get_text().strip() if snippet_tag else "No description available."
                                                                                                                if len(title) > 2:
                                                                                                                                              results.append({
                                                                                                                                                                                "url": href,
                                                                                                                                                                                "text": f"{title}: {snippet}"
                                                                                                                                                })
                                                                                        except Exception as e:
                                                                                                      print(f"Yahoo Search Error: {e}")
                                                                                                  return results

    def _scrape_social(self, query: str) -> list:
              results = []
        try:
                      with DDGS() as ddgs:
                                        sources = "site:reddit.com OR site:macrumors.com OR site:sammobile.com OR site:xda-developers.com OR site:androidcentral.com OR site:theverge.com"
                social_query = f"{query} ({sources}) review opinion"
                ddg_results = list(ddgs.text(social_query, max_results=15))
                for r in ddg_results:
                                      results.append({
                                                                "url": r.get('href', ''),
                                                                "text": f"[Social] Title: {r.get('title', '')} | Content: {r.get('body', '')}"
                                      })
except Exception as e:
            print(f"Social Search Error: {e}")
        return results

    def run(self, keyword: str) -> list:
              queries = self._expand_keywords(keyword)
        raw_db = []
        for i, q in enumerate(queries):
                      raw_db.extend(self._scrape_yahoo(q))
            if i == 0:
                              raw_db.extend(self._scrape_google(q))
                raw_db.extend(self._scrape_social(q))
elif i == 2:
                raw_db.extend(self._scrape_google(q))
            time.sleep(1)
        return raw_db

class SynthesizerAgent:
      def run(self, raw_data: list) -> list:
                seen = set()
        clean = []
        for d in raw_data:
                      if d["text"] not in seen and len(d["text"]) > 20:
                                        seen.add(d["text"])
                clean.append(d)
        return clean

class AnalystAgent:
      def __init__(self):
                self.categories = {
                              "AP": r"AP|Chip|Processor|Snapdragon|Apple A\d+|Exynos|Dimensity|NPU|M\d+|CPU|GPU|Bionic",
                              "Display": r"Display|OLED|LTPO|Screen|Inch|Resolution|Hz|Brightness|Nits|PPI|Dynamic Island",
                              "Camera": r"Camera|Rear|Front|Selfie|Main|Ultra|Wide|Telephoto|MP|Optical|Sensor|Flash|Lidar",
                              "Power": r"Power|Charging|Fast charge|Adapter|W|Magsafe|USB-C|Wireless",
                              "Battery": r"Battery|mAh|Wh|Battery life|Endurance|Usage time",
                              "Sensor": r"Sens
                              "Sensor": r"Sensor|Gyro|Fingerprint|Accelerometer|Proximity|Ambient|Compass|Lidar|Barometer",
            "Capacity": r"Capacity|Storage|RAM|GB|TB|Internal|Memory|NVMe",
            "Face ID": r"Face ID|Face Unlock|Biometric|Secure Enclave|Touch ID",
                              "Cellular": r"Cellular|Wireless|5G|LTE|Wi-Fi|Bluetooth|NFC|UWB|Esim|Satellite",
                              "Social": r"\[Social\]|Reddit|Twitter|X\.com|Thread|Facebook|Blog|Review|Opinion",
                              "Market": r"Market|Sales|Volume|Shipment|Share|Rank|Best selling|Demand|Price"
                }
        self.translator = GoogleTranslator(source='auto', target='ko')

    def _safe_translate(self, text: str) -> str:
              try:
                            if not text or len(text.strip()) < 3:
                                              return text
                                          return self.translator.translate(text)
                        except:
            return text

                              def _get_domain(self, url: str, text: str = "") -> str:
                                        if "[Google AI]" in text:
                                                      return "Google SGE (AI Overview)"
                                                  try:
                                                                domain = urlparse(url).netloc.replace("www.", "")
                                                                return domain if domain else "Source"
                                                            except:
            return "Source"

    def _generate_category_insight(self, category: str, points: list) -> str:
              if not points:
                            return "No info found."
        ai_points = [p['text'] for p in points if "[Google AI]" in p['text']]
        if ai_points:
                      ai_text = ai_points[0].replace("[Google AI]", "").strip()
                      if len(ai_text) > 20:
                                        return f"[AI] {ai_text.split('.')[0]}."
                                return f"{category} analysis done."

    def _categorize_data(self, documents: list) -> dict:
              structured_data = {cat: [] for cat in self.categories.keys()}
        for doc in documents:
                      text = doc["text"]
            for category, pattern in self.categories.items():
                              if re.search(pattern, text, re.IGNORECASE):
                                                    structured_data[category].append(doc)
                                        return structured_data

    def _generate_report(self, structured_data: dict, format: str, raw_data: list = None) -> str:
              if format == 'html':
                            sections = ""
            for cat, docs in structured_data.items():
                              sections += f"<div><h3>{cat}</h3><ul>"
                for d in docs[:3]:
                                      sections += f"<li>{d['text'][:100]}...</li>"
                                  sections += "</ul></div>"
            return f"<html><body>{sections}</body></html>"
        return "Report"

    def run(self, data: list, output_format: str = 'markdown') -> str:
              structured = self._categorize_data(data)
        return self._generate_report(structured, output_format, raw_data=data)

def execute_rag_pipeline(target_device: str, output_format: str = 'markdown') -> str:
      retriever = RetrieverAgent()
    raw_data = retriever.run(target_device)
    if not raw_data:
              return "No results."
    synthesizer = SynthesizerAgent()
    clean_data = synthesizer.run(raw_data)
    analyst = AnalystAgent()
    report = analyst.run(clean_data, output_format=output_format)
    return report

if __name__ == "__main__":
      print(execute_rag_pipeline("iPhone 16 Pro", output_format='markdown'))
