#!/bin/sh
# Build the macOS disk image for the Ngao Exploration Console — on Linux.
#
# Produces dist/NgaoExplorationConsole.dmg: an ISO9660 / HFS+ hybrid image
# with an Apple Partition Map, which macOS mounts like any disk image. It
# contains a double-clickable .app whose launcher opens the self-contained
# console in the default browser, plus the demo video and a README.
#
# Requires: xorriso, python3 + Pillow (for the icon).
set -eu
HERE="$(cd "$(dirname "$0")/.." && pwd)"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
APP="$WORK/root/Ngao Exploration Console.app"
mkdir -p "$APP/Contents/MacOS" "$APP/Contents/Resources"

# ── icon ──────────────────────────────────────────────────────
python3 - "$APP/Contents/Resources/ngao.icns" <<'PY'
from PIL import Image, ImageDraw
import struct, io, sys
def make(size):
    S=1024
    im=Image.new('RGBA',(S,S),(0,0,0,0)); d=ImageDraw.Draw(im); m=100
    d.rounded_rectangle((m,m,S-m,S-m),radius=185,fill=(19,17,16,255))
    d.rounded_rectangle((m,m,S-m,S-m),radius=185,outline=(51,44,36,255),width=6)
    g=Image.new('RGBA',(S,S),(0,0,0,0)); gd=ImageDraw.Draw(g)
    cx,cy,half=512,470,205
    for i in range(half,0,-2):
        t=i/half
        col=(int(246-106*t*0.9),int(208-100*t*0.9),int(107-73*t*0.9),255)
        gd.rounded_rectangle((cx-i,cy-i,cx+i,cy+i),radius=int(38*i/half)+8,fill=col)
    for k in range(-1400,1400,60):
        gd.line([(cx-half+k,cy+half+60),(cx-half+k+520,cy-half-60)],fill=(19,17,16,255),width=11)
    mask=Image.new('L',(S,S),0)
    ImageDraw.Draw(mask).rounded_rectangle((cx-half,cy-half,cx+half,cy+half),radius=46,fill=255)
    im.paste(g,(0,0),mask)
    ImageDraw.Draw(im).rounded_rectangle((cx-half,cy-half,cx+half,cy+half),radius=46,outline=(224,178,63,255),width=8)
    ramp=[(26,14,58),(124,28,106),(222,88,56),(252,231,168)]
    bx0,bx1,by=322,702,772; seg=(bx1-bx0)//len(ramp)
    for i,c in enumerate(ramp):
        ImageDraw.Draw(im).rounded_rectangle((bx0+i*seg,by,bx0+(i+1)*seg-8,by+34),radius=8,fill=c+(255,))
    return im if size==S else im.resize((size,size),Image.LANCZOS)
chunks=b''
for tag,sz in [('icp4',16),('icp5',32),('ic07',128),('ic08',256),('ic09',512),('ic10',1024)]:
    b=io.BytesIO(); make(sz).save(b,'PNG'); p=b.getvalue()
    chunks+=tag.encode()+struct.pack('>I',len(p)+8)+p
open(sys.argv[1],'wb').write(b'icns'+struct.pack('>I',len(chunks)+8)+chunks)
PY

# ── bundle ────────────────────────────────────────────────────
cp "$HERE/index.html" "$APP/Contents/Resources/index.html"
printf 'APPL????' > "$APP/Contents/PkgInfo"
cat > "$APP/Contents/Info.plist" <<'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>CFBundleInfoDictionaryVersion</key><string>6.0</string>
	<key>CFBundlePackageType</key><string>APPL</string>
	<key>CFBundleName</key><string>Ngao Exploration Console</string>
	<key>CFBundleDisplayName</key><string>Ngao Exploration Console</string>
	<key>CFBundleIdentifier</key><string>com.deeptechengineering.ngao</string>
	<key>CFBundleVersion</key><string>1.0.0</string>
	<key>CFBundleShortVersionString</key><string>1.0.0</string>
	<key>CFBundleExecutable</key><string>ngao</string>
	<key>CFBundleIconFile</key><string>ngao</string>
	<key>LSMinimumSystemVersion</key><string>10.13</string>
	<key>LSUIElement</key><true/>
	<key>NSHighResolutionCapable</key><true/>
	<key>CFBundleDevelopmentRegion</key><string>en</string>
</dict>
</plist>
PLIST
cat > "$APP/Contents/MacOS/ngao" <<'SH'
#!/bin/sh
# Ngao Exploration Console — opens the console in the default browser.
DIR="$(cd "$(dirname "$0")" && pwd)"
exec /usr/bin/open "$DIR/../Resources/index.html"
SH
chmod 755 "$APP/Contents/MacOS/ngao"

# ── companions ────────────────────────────────────────────────
cp "$HERE/demo/ngao-console-demo-deeptech.mp4" "$WORK/root/Demo (1 minute).mp4"
cp "$HERE/tools/dmg-readme.txt" "$WORK/root/README.txt"

# ── image ─────────────────────────────────────────────────────
mkdir -p "$HERE/dist"
xorriso -as mkisofs \
  -V "Ngao Exploration Console" \
  -r -J -joliet-long \
  -hfsplus -hfsplus-serial-no 4E47414F44454550 \
  -o "$HERE/dist/NgaoExplorationConsole.dmg" \
  "$WORK/root/"
ls -la "$HERE/dist/NgaoExplorationConsole.dmg"
