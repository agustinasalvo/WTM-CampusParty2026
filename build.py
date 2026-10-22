#!/usr/bin/env python3
"""Builds the single-file app: wtm-campus-party-share-card.html

Embeds the official logos so the page works standalone (and the PNG export is never
"tainted" by cross-origin images).

  assets/wtm-logo-white.svg        -> official WTM white logo   (required)
  assets/campus-party-logo.(png|svg|webp|jpg) -> official Campus Party logo (optional;
                                      without it the card shows a clearly labelled placeholder)
"""
import base64, glob, mimetypes, os, sys

here = os.path.dirname(os.path.abspath(__file__))

def data_uri(path):
    mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
    if path.endswith(".svg"):
        mime = "image/svg+xml"
    with open(path, "rb") as f:
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode()

wtm = os.path.join(here, "assets", "wtm-logo-white.svg")
if not os.path.exists(wtm):
    sys.exit("Missing assets/wtm-logo-white.svg")

cp_files = sorted(glob.glob(os.path.join(here, "assets", "campus-party-logo.*")))
cp = data_uri(cp_files[0]) if cp_files else ""

with open(os.path.join(here, "template.html"), encoding="utf-8") as f:
    html = f.read()

html = html.replace("__OUTFIT400__", data_uri(os.path.join(here,"assets","outfit-400.woff2"))).replace("__OUTFIT600__", data_uri(os.path.join(here,"assets","outfit-600.woff2"))).replace("__WTM_LOGO__", data_uri(wtm)).replace("__CP_LOGO__", cp)

out = os.path.join(here, "wtm-campus-party-share-card.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(html)

print("Built", out)
print("Campus Party logo:", cp_files[0] if cp_files else "NOT FOUND -> placeholder shown on the card")
