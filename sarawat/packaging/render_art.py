#!/usr/bin/env python3
"""Render the app icon and the disk-image background, and pack the .icns.

The art templates carry @@TOKEN@@ placeholders for webfonts. Substitution is a
single regex pass over the template: a naive str.replace() chain corrupts the
output, because base64 font payloads contain the later tokens as substrings.
"""
import base64, io, os, re, struct, subprocess, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
# where `npm i playwright` put its modules; override with PLAYWRIGHT_NODE_PATH
NODE_MODULES = "%s/node_modules" % os.environ.get("PLAYWRIGHT_HOME", HERE)
GF = ("https://fonts.googleapis.com/css2"
      "?family=Montserrat:wght@800&family=IBM+Plex+Mono:wght@500&display=swap")
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"

def google_fonts():
    """Return {(family, weight): data-uri} for the latin subsets only."""
    css = urllib.request.urlopen(
        urllib.request.Request(GF, headers={"User-Agent": UA}), timeout=60).read().decode()
    out = {}
    for name, body in zip(*[iter(re.split(r"/\*\s*([a-z\-]+)\s*\*/", css)[1:])] * 2):
        if name != "latin":
            continue
        fam = re.search(r"font-family: '([^']+)'", body)
        wgt = re.search(r"font-weight: (\d+)", body)
        url = re.search(r"url\((https://[^)]+)\)", body)
        if not (fam and wgt and url):
            continue
        blob = urllib.request.urlopen(url.group(1), timeout=60).read()
        out[(fam.group(1), wgt.group(1))] = \
            "data:font/woff2;base64," + base64.b64encode(blob).decode()
    return out

def render(template, out_png, selector, width, height, tokens, transparent=False):
    src = open(os.path.join(HERE, template), encoding="utf-8").read()
    if tokens:
        missing = set(re.findall(r"@@([A-Z0-9_]+)@@", src)) - set(tokens)
        if missing:
            raise SystemExit("no font for token(s): %s" % ", ".join(sorted(missing)))
        # one pass, so a substituted payload can never be rescanned
        src = re.sub(r"@@([A-Z0-9_]+)@@", lambda m: tokens[m.group(1)], src)
    tmp = os.path.join(HERE, "._render.html")
    open(tmp, "w", encoding="utf-8").write(src)
    js = """
const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch({executablePath:process.argv[2],args:['--no-sandbox']});
const p=await b.newPage({viewport:{width:+process.argv[5],height:+process.argv[6]},deviceScaleFactor:1});
await p.goto('file://'+process.argv[3]); await p.waitForTimeout(900);
await p.locator(process.argv[7]).screenshot({path:process.argv[4],omitBackground:process.argv[8]==='1'});
await b.close();})();"""
    jsf = os.path.join(HERE, "._render.js")
    open(jsf, "w").write(js)
    env = dict(os.environ, NODE_PATH=os.environ.get("PLAYWRIGHT_NODE_PATH", NODE_MODULES))
    subprocess.run(["node", jsf, CHROME, tmp, os.path.join(HERE, out_png),
                    str(width), str(height), selector, "1" if transparent else "0"],
                   check=True, env=env)
    os.remove(tmp); os.remove(jsf)
    print("rendered %s" % out_png)

def pack_icns(png, out):
    from PIL import Image
    src = Image.open(os.path.join(HERE, png)).convert("RGBA")
    types = [(b"icp4", 16), (b"icp5", 32), (b"icp6", 64), (b"ic07", 128), (b"ic08", 256),
             (b"ic09", 512), (b"ic10", 1024), (b"ic11", 32), (b"ic12", 64),
             (b"ic13", 256), (b"ic14", 512)]
    chunks = b""
    for t, sz in types:
        buf = io.BytesIO()
        src.resize((sz, sz), Image.LANCZOS).save(buf, "PNG", optimize=True)
        d = buf.getvalue()
        chunks += t + struct.pack(">I", len(d) + 8) + d
    open(os.path.join(HERE, out), "wb").write(b"icns" + struct.pack(">I", len(chunks) + 8) + chunks)
    print("packed %s (%d reps)" % (out, len(types)))

if __name__ == "__main__":
    fonts = google_fonts()
    print("fonts: %s" % ", ".join("%s %s" % k for k in sorted(fonts)))
    tokens = {"MONTSERRAT_800": fonts[("Montserrat", "800")],
              "PLEXMONO_500":   fonts[("IBM Plex Mono", "500")]}
    render("icon.html", "icon1024.png", ".i", 1024, 1024, {}, transparent=True)
    render("bg.html",   "background.png", ".b", 640, 460, tokens)
    pack_icns("icon1024.png", "Sarawat.icns")
