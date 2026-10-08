from __future__ import annotations
import json,re
from abc import ABC,abstractmethod
import requests
from bs4 import BeautifulSoup
from ..models import ProductObservation,ProductStatus
USER_AGENT="pokemon-stock-tracker/1.0 (+personal availability checker; no automated purchase)"
class StoreBlocked(Exception): pass
class StoreAdapter(ABC):
    name:str
    def __init__(self,product_name,postal_code="",city=""): self.product_name,self.postal_code,self.city=product_name,postal_code,city
    def check(self,url):
        try:
            html,status=self._fetch(url); o=self.parse(html,url); o.http_status=status; return o
        except StoreBlocked as e:return ProductObservation(self.name,self.product_name,url,ProductStatus.BLOCKED,error=str(e))
        except requests.RequestException as e:return ProductObservation(self.name,self.product_name,url,ProductStatus.UNKNOWN,error=str(e))
        except Exception as e:return ProductObservation(self.name,self.product_name,url,ProductStatus.UNKNOWN,error=str(e))
    def _fetch(self,url):
        r=requests.get(url,headers={"User-Agent":USER_AGENT,"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language":"es-ES,es;q=0.9,en;q=0.5"},timeout=(5,15),allow_redirects=True)
        if r.status_code in {403,429,503}: raise StoreBlocked(f"HTTP {r.status_code}")
        r.raise_for_status()
        if any(x in r.text.casefold() for x in ("captcha","cf-chl-challenge","challenge-platform")): raise StoreBlocked("CAPTCHA/anti-bot challenge detected")
        return r.text,r.status_code
    @abstractmethod
    def parse(self,html,url): ...
def parse_generic_product_page(*,html,url,store,product_name,rules):
    soup=BeautifulSoup(html,"html.parser"); text=" ".join(soup.stripped_strings); low=text.casefold()
    schema=extract_schema_offers(soup); price=extract_price(soup)
    if price is None and schema.get("price"):
        try: price=float(schema["price"].replace(",",".")) 
        except ValueError: pass
    av=schema.get("availability","").casefold()
    out=[x for x in rules["out_of_stock"] if x.casefold() in low]; online=[x for x in rules["online"] if x.casefold() in low]
    pickup=[x for x in rules["pickup"] if x.casefold() in low]; pre=[x for x in rules["preorder"] if x.casefold() in low]; res=[x for x in rules["reservation"] if x.casefold() in low]
    sin=any(x in av for x in ("instock","limitedavailability","preorder")); sout=any(x in av for x in ("outofstock","soldout"))
    purchase=bool(online) or sin; pick=bool(pickup); reservation=bool(res or pre)
    if pick and not purchase: status=ProductStatus.PICKUP_AVAILABLE
    elif reservation and not purchase: status=ProductStatus.PREORDER
    elif purchase and not out and not sout: status=ProductStatus.IN_STOCK
    elif out or sout: status=ProductStatus.OUT_OF_STOCK; purchase=False
    else: status=ProductStatus.UNKNOWN
    evidence=[]
    for label,h in (("out-of-stock",out),("online",online),("pickup",pickup),("preorder",pre),("reservation",res)):
        if h:evidence.append(f"{label}: {', '.join(h[:3])}")
    if av:evidence.append(f"schema.org availability={av}")
    return ProductObservation(store,product_name,url,status,price=price,purchase_online=purchase,pickup=pick,reservation=reservation,evidence=evidence)
def extract_price(soup):
    for el in soup.select('meta[itemprop="price"],meta[property="product:price:amount"],[itemprop="price"],.price,[class*="price"]'):
        raw=el.get("content") or el.get_text(" ",strip=True); n=re.sub(r"[^0-9,.]","",raw)
        if "," in n and "." in n:n=n.replace(".","").replace(",",".")
        elif "," in n:n=n.replace(",",".")
        try:
            v=float(n)
            if 0<v<10000:return v
        except ValueError: pass
    return None
def extract_schema_offers(soup):
    out={}
    for s in soup.select('script[type="application/ld+json"]'):
        try:d=json.loads(s.string or s.get_text())
        except (TypeError,json.JSONDecodeError):continue
        for o in (d if isinstance(d,list) else [d]):
            if isinstance(o,dict) and isinstance(o.get("offers"),dict):
                if o["offers"].get("availability"):out["availability"]=str(o["offers"]["availability"])
                if o["offers"].get("price"):out["price"]=str(o["offers"]["price"])
    return out
