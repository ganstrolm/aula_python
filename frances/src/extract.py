"""Extract lesson bodies from downloaded Tex pages into lessons.json (images inlined)."""
import re, json, os, sys, base64, subprocess, html as H
SP = sys.argv[1]
PAGES, IMGD = f"{SP}/pages", f"{SP}/imgs"
os.makedirs(IMGD, exist_ok=True)
idx = json.load(open(sys.argv[2]))
codes = {p["code"] for s in idx["sections"] for p in s["pages"]}
BASE = "https://www.laits.utexas.edu/tex/gr/"

def img_uri(src):
    url = requests_join(src)
    fn = f"{IMGD}/" + re.sub(r"[^\w.]", "_", url.split("/tex/")[-1])
    if not os.path.exists(fn):
        subprocess.run(["curl", "-sS", "--retry", "3", "-f", "-o", fn, url], check=False)
    if not os.path.exists(fn): return None
    ext = fn.rsplit(".", 1)[-1].lower().replace("jpg", "jpeg")
    return f"data:image/{ext};base64," + base64.b64encode(open(fn, "rb").read()).decode()

def requests_join(src):
    if src.startswith("http"): return src
    from urllib.parse import urljoin
    return urljoin(BASE, src)

def clean(c, code):
    c = re.sub(r"<!--.*?-->", "", c, flags=re.S)
    # audio links -> play buttons; clips live in ./audio/<id>.mp3 beside the page
    c = re.sub(r"<a href=\"javascript:;\"[^>]*open_aud\('[^']*','([^']+)'[^>]*>.*?</a>",
               r'<button class="aud" data-aud="\1" aria-label="Ouvir">▶</button>', c, flags=re.S | re.I)
    c = re.sub(r'<a href="javascript:;"[^>]*>(.*?)</a>', r"\1", c, flags=re.S | re.I)
    c = re.sub(r'<img[^>]*(transdot|sound\.gif)[^>]*>', "", c, flags=re.I)
    # links to pdf/zip/flash: unwrap
    c = re.sub(r'<a [^>]*href="[^"]*(\.pdf|\.zip|adobe\.com|/fi/)[^"]*"[^>]*>(.*?)</a>', r"\2", c, flags=re.S | re.I)
    def link(m):
        href = m.group(1)
        mm = re.match(r"(?:\.\./gr/)?([\w\-]+)\.html(#.*)?$", href)
        if mm and mm.group(1) in codes:
            return f'<a href="#{mm.group(1)}" data-anchor="{(mm.group(2) or "")[1:]}">'
        if href.startswith("#"):
            return f'<a href="#{code}" data-anchor="{href[1:]}">'
        return f'<a href="{requests_join(href)}" target="_blank" rel="noopener">'
    c = re.sub(r'<a href="([^"]+)"[^>]*>', link, c, flags=re.I)
    c = re.sub(r'<a name="([^"]+)"[^>]*>', lambda m: f'<a id="a-{H.escape(m.group(1))}">', c, flags=re.I)
    def img(m):
        s = re.search(r'src="([^"]+)"', m.group(0), re.I)
        alt = re.search(r'alt="([^"]*)"', m.group(0), re.I)
        u = s and img_uri(s.group(1))
        return f'<img src="{u}" alt="{alt.group(1) if alt else ""}" loading="lazy">' if u else ""
    c = re.sub(r"<img[^>]*>", img, c, flags=re.I)
    # strip presentational attributes
    c = re.sub(r'\s(width|height|align|valign|border|cellpadding|cellspacing|bgcolor|vspace|hspace|nowrap)=("[^"]*"|\S+?)(?=[\s>])', "", c, flags=re.I)
    c = re.sub(r"</?(center|font)[^>]*>", "", c, flags=re.I)
    c = re.sub(r"(<br\s*/?>\s*){3,}", "<br><br>", c, flags=re.I)
    c = c.replace("<td>&nbsp;</td>", "")
    return c.strip()

out = {}
for code in sorted(codes):
    f = f"{PAGES}/{code.replace('/', '_')}.html"
    h = open(f, encoding="latin-1").read()
    m = re.search(r"<!-- content -->(.*?)<!-- END content -->", h, re.S)
    if not m:
        print("skip (no content block):", code); continue
    out[code] = clean(m.group(1), code)
json.dump(out, open(f"{SP}/build/lessons.json", "w"), ensure_ascii=False)
print(len(out), "lessons", os.path.getsize(f"{SP}/build/lessons.json") // 1024, "KB")
