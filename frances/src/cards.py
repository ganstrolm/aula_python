"""Derive study data (example pairs, key terms) from lessons.json."""
import json, re, sys, collections
from bs4 import BeautifulSoup
L = json.load(open(sys.argv[1]))
cards, terms = [], collections.defaultdict(lambda: collections.Counter())

def txt(el): return re.sub(r"\s+", " ", el.get_text(" ")).strip()

for code, html in L.items():
    soup = BeautifulSoup(html, "lxml")
    for span in soup.select("span.tb_blue, span.tt_blue"):
        t = txt(span).strip(" .,;:!?'\"()").lower()
        if 1 < len(t) <= 40: terms[t][code] += 1
    for tr in soup.find_all("tr"):
        if tr.find("table"): continue
        tds = [td for td in tr.find_all("td", recursive=False) if txt(td) and not td.find("button")]
        if len(tds) != 2: continue
        fr, en = tds
        # vocab grids: each cell is "<blue>fr</blue>, english" -> one card per cell
        if en.select("span.tb_blue"):
            for td in tds:
                sp = td.select_one("span.tb_blue")
                rest = txt(td)[len(txt(sp)):].lstrip(" ,:") if sp and txt(td).startswith(txt(sp)) else ""
                if sp and rest:
                    cards.append({"id": f"{code}:{len(cards)}", "l": code, "fr": str(sp), "en": rest, "a": None, "cz": []})
            continue
        if not fr.select("span.tb_blue") and not en.find("b"): continue
        ft, et = txt(fr), txt(en)
        if len(ft) < 3 or len(et) < 3 or ft == et or len(ft) > 220: continue
        # audio button: same row, else nearest enclosing table's first button
        b = tr.find("button") or next((x for t in tr.find_parents("table") if (x := t.find("button"))), None)
        cloze = [txt(s) for s in fr.select("span.tb_blue") if 0 < len(txt(s)) <= 30]
        cards.append({"id": f"{code}:{len(cards)}", "l": code,
                      "fr": fr.decode_contents().strip(), "en": en.decode_contents().strip(),
                      "a": b["data-aud"] if b else None, "cz": cloze})
# terms that appear in 2+ lessons or 3+ times are worth an index entry
idx = {t: dict(c) for t, c in terms.items() if len(c) >= 2 or sum(c.values()) >= 3}
json.dump({"cards": cards, "terms": idx}, open(sys.argv[2], "w"), ensure_ascii=False)
print(len(cards), "cards;", sum(1 for c in cards if c["cz"]), "with cloze;", sum(1 for c in cards if c["a"]), "with audio;", len(idx), "terms")
