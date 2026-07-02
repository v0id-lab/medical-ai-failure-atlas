#!/usr/bin/env python3
"""Verify pal2024medhelm and levkovich2024dosing references via arXiv API + PubMed."""
import urllib.request
import xml.etree.ElementTree as ET
import json

ns = {'a': 'http://www.w3.org/2005/Atom', 'arxiv': 'http://arxiv.org/schemas/atom'}
results = []

# 1) pal2024medhelm — search arXiv
url = "https://export.arxiv.org/api/query?search_query=au:Pal+AND+ti:MedHELM&max_results=5"
req = urllib.request.Request(url, headers={'User-Agent': 'C0R3/1.0'})
data = urllib.request.urlopen(req, timeout=30).read().decode()
root = ET.fromstring(data)
entries = root.findall('a:entry', ns)
if entries:
    for e in entries:
        t = e.find('a:title', ns)
        title = t.text.strip()[:120] if t is not None else 'N/A'
        ids = [l.attrib.get('href') for l in e.findall('a:link', ns) if l.attrib.get('title') == 'arXiv']
        eprint = ids[0] if ids else 'N/A'
        results.append(f"pal2024medhelm: Title='{title}' arXiv={eprint}")
else:
    results.append("pal2024medhelm: No arXiv results found — check PubMed/Direct")

# 2) levkovich2024dosing — search arXiv
url2 = "https://export.arxiv.org/api/query?search_query=au:Levkovich+AND+ti:dosing&max_results=5"
req2 = urllib.request.Request(url2, headers={'User-Agent': 'C0R3/1.0'})
data2 = urllib.request.urlopen(req2, timeout=30).read().decode()
root2 = ET.fromstring(data2)
entries2 = root2.findall('a:entry', ns)
if entries2:
    for e in entries2:
        t = e.find('a:title', ns)
        title = t.text.strip()[:120] if t is not None else 'N/A'
        ids = [l.attrib.get('href') for l in e.findall('a:link', ns) if l.attrib.get('title') == 'arXiv']
        eprint = ids[0] if ids else 'N/A'
        results.append(f"levkovich2024dosing: Title='{title}' arXiv={eprint}")
else:
    results.append("levkovich2024dosing: No arXiv results — check PubMed DOI")

for r in results:
    print(r)