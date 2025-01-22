import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=)

sponsor_keywords = [
     'sponsor', 'spossored', 'partnership', 'partner', 'brought to you by',
     'thanks to', 'promotion', 'promotional', 'affiliate', 'discount code',
     'promo code', 'special offer', 'check out', 'sponsored by'
]

def extract_context(text: str, keyword: str, window_size: int = 100) -> str:
     '''
     Extract context around a keyword with specified window size berfore and after
     '''
     
     text = text.lower()
     keyword_pos = text.find(keyword.lower())
     
     if keyword_pos == -1:
          return ''
     
     start = max(0, keyword_pos - window_size)
     end = min(len(text), keyword_pos + len(keyword) + window_size)
     context = text[start:end].strip()
     
     return ''.join(context.split())


def find_sponsor(text: str, keywords: list[str]) -> list[tuple[str, str]]:
     ''' Find potential sponsor mentions in text using keyword matching .
     Returns list of tuples containing (context , keyword).
     '''
     if not text:
          return []
     
     found_contexts = []
     
     for keyword in keywords:
          text_lower = text.lower()
          start = 0
          while True:
               pos = text_lower.find(keyword, start)
               if pos == -1:
                    break
               
               context = extract_context(text[max(0, pos - 100): min(len(text), pos + 100 + len(keyword))], keyword)
               if context:
                    found_contexts.append((context, keyword))
                    
               start = pos + len(keyword)
               
     return found_contexts


def extract_sponsor_name(context: str) -> str:
     ''' 
     Use GPT to extract the sponsor name from the context.
     '''
     prompt = f''' Given this text, extract ONLY the company name that os sponsoring or advertising.
     If there ios no clear sponsor, respond with "None". If there is a sponsor but you can"t determine the exact name, respond with "Unknown".
     Respond with just the company name, no other text
     
     Text: {context} '''
     response = client.chat.completions