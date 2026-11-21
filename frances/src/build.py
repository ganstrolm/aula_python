"""Monta frances/grammaire-tex.html a partir de app.html + dados. Uso: python3 frances/src/build.py"""
import json, os
B = os.path.dirname(os.path.abspath(__file__))
j = lambda f: open(os.path.join(B, f), encoding="utf-8").read().replace("</script", "<\\/script")
tr = j("tr_baked.json") if os.path.exists(os.path.join(B, "tr_baked.json")) else "{}"
html = (j("app.html").replace("<\\/script", "</script")  # app.html itself keeps its real script tags
        .replace("__INDEX__", json.dumps(json.load(open(os.path.join(B, "index.json"))), ensure_ascii=False))
        .replace("__LESSONS__", j("lessons.json")).replace("__STUDY__", j("study.json"))
        .replace("__TITLES__", j("titles_pt.json")).replace("__TR__", tr))
open(os.path.join(B, "..", "grammaire-tex.html"), "w", encoding="utf-8").write(html)
print("ok")
