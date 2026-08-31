#!/usr/bin/env python3
"""Build a macOS .dmg for the Sarawat Terroir Engine from Linux.

ISO 9660 + Rock Ridge image wrapped in a UDIF/UDZO container by libdmg-hfsplus,
the same route Bitcoin Core uses for its Linux-built macOS disk images.
"""
import os, shutil, subprocess, datetime, plistlib, sys
from ds_store import DSStore
from mac_alias import Alias, VolumeInfo, TargetInfo
import mac_alias.alias as MA

SP   = os.path.dirname(os.path.abspath(__file__))
ROOT = "/home/user/drdmitrymikhaylov/sarawat"
VOL  = "Sarawat Terroir Engine"
APP  = "Sarawat Terroir Engine.app"
VER  = "4.2"
OUT  = os.path.join(ROOT, "Sarawat-Terroir-Engine-%s.dmg" % VER)
DIST = os.path.join(SP, "dist")
DMGTOOL = os.path.join(SP, "..", "libdmg", "dmg", "dmg")

# ---------------------------------------------------------------- app bundle
shutil.rmtree(DIST, ignore_errors=True)
appdir = os.path.join(DIST, APP)
for d in ("Contents/MacOS", "Contents/Resources/app"):
    os.makedirs(os.path.join(appdir, d))

info = {
    "CFBundleName": "Sarawat",
    "CFBundleDisplayName": "Sarawat Terroir Engine",
    "CFBundleIdentifier": "engineering.deeptech.sarawat",
    "CFBundleVersion": VER + ".0",
    "CFBundleShortVersionString": VER,
    "CFBundleExecutable": "Sarawat",
    "CFBundleIconFile": "Sarawat",
    "CFBundlePackageType": "APPL",
    "CFBundleSignature": "????",
    "CFBundleInfoDictionaryVersion": "6.0",
    "CFBundleDevelopmentRegion": "en",
    "LSMinimumSystemVersion": "10.13",
    "LSApplicationCategoryType": "public.app-category.productivity",
    "NSHighResolutionCapable": True,
    "NSSupportsAutomaticGraphicsSwitching": True,
    "NSHumanReadableCopyright": "DeepTech Engineering",
}
with open(os.path.join(appdir, "Contents/Info.plist"), "wb") as f:
    plistlib.dump(info, f)
open(os.path.join(appdir, "Contents/PkgInfo"), "w").write("APPL????")

launcher = r'''#!/bin/bash
# Sarawat Terroir Engine - opens the bundled tool in your default browser.
#
# Deliberately does not start a local web server: on a stock macOS the
# /usr/bin/python3 shim triggers the Xcode Command Line Tools installer just by
# being executed, which is a terrible first-run experience. Opening the file
# directly always works. See "Read Me.txt" for the local-server recipe if you
# need an http:// origin for a referrer-restricted Google Maps key.
RES="$(cd "$(dirname "$0")/../Resources" && pwd)"
PAGE="$RES/app/index.html"

if [ ! -f "$PAGE" ]; then
  osascript -e 'display alert "Sarawat Terroir Engine" message "The application files are missing. Reinstall from the disk image."' >/dev/null 2>&1
  exit 1
fi

open "$PAGE"
'''
lp = os.path.join(appdir, "Contents/MacOS/Sarawat")
open(lp, "w").write(launcher)
os.chmod(lp, 0o755)

shutil.copy(os.path.join(SP, "Sarawat.icns"), os.path.join(appdir, "Contents/Resources/Sarawat.icns"))
shutil.copy(os.path.join(ROOT, "index.html"),  os.path.join(appdir, "Contents/Resources/app/index.html"))

# ------------------------------------------------------------ window dressing
os.symlink("/Applications", os.path.join(DIST, "Applications"))
os.makedirs(os.path.join(DIST, ".background"))
shutil.copy(os.path.join(SP, "background.png"), os.path.join(DIST, ".background/background.png"))

readme = """SARAWAT TERROIR ENGINE %s
DeepTech Engineering

--------------------------------------------------------------------
IF MACOS REFUSES TO OPEN THE APP
--------------------------------------------------------------------
This is expected. The app is not signed with an Apple Developer ID, so
macOS quarantines it and reports that it is damaged, or that it cannot
be checked for malicious software. The app is fine; it simply has no
Apple signature, which costs a paid developer account to obtain.

Three ways round it, in order of reliability.

1. NO INSTALL AT ALL
   Double-click "Open Sarawat directly.html" in this window. Same tool,
   opens straight in your browser, nothing for Gatekeeper to block.
   If the app is giving you trouble, just use this.

2. TERMINAL - works on every macOS version
   Drag the app to Applications first, then run:

       xattr -dr com.apple.quarantine "/Applications/Sarawat Terroir Engine.app"

   Then open it normally. You only ever do this once.

3. SYSTEM SETTINGS
   Double-click the app and let it be blocked. Then open
   System Settings > Privacy & Security, scroll to Security, and press
   "Open Anyway" next to the message about Sarawat. Confirm with Touch ID
   or your password.

   On macOS 14 Sonoma and earlier you can instead right-click (or
   Control-click) the app and choose Open. Apple removed that shortcut in
   macOS 15 Sequoia, so on Sequoia use "Open Anyway" or the Terminal
   command above.

--------------------------------------------------------------------
INSTALL
--------------------------------------------------------------------
Drag "Sarawat Terroir Engine" onto the Applications folder in this
window. Launching it opens the tool in your default browser. Everything
runs locally; nothing is uploaded and no network is required.

--------------------------------------------------------------------
MAPS
--------------------------------------------------------------------
The relief map is drawn by the app itself and needs no network. To swap
in live Google imagery, press "Google map" on any map and paste a Maps
JavaScript API key.

A key restricted by HTTP referrer needs an http:// origin, which a file
opened directly cannot provide. If yours is restricted, serve the app
instead - in Terminal:

    cd "/Applications/Sarawat Terroir Engine.app/Contents/Resources/app"
    python3 -m http.server 8765 --bind 127.0.0.1

then open http://127.0.0.1:8765/index.html and authorise that origin for
the key. Press Control-C when you are finished.

--------------------------------------------------------------------
REQUIREMENTS
--------------------------------------------------------------------
macOS 10.13 or later, and any modern browser.
""" % VER
open(os.path.join(DIST, "Read Me.txt"), "w").write(readme)

# Gatekeeper quarantines any unsigned app. A plain .html file is not an
# executable, so it always opens - the same tool, nothing to install.
shutil.copy(os.path.join(ROOT, "index.html"),
            os.path.join(DIST, "Open Sarawat directly.html"))

# ------------------------------------------------------------------ .DS_Store
now = datetime.datetime(2026, 1, 1, tzinfo=datetime.timezone.utc)
def alias_for(rel, name, folder):
    vol = VolumeInfo(name=VOL, creation_date=now, fs_type=b"H+",
                     disk_type=MA.ALIAS_FIXED_DISK, attribute_flags=0, fs_id=b"\0\0",
                     posix_path="/Volumes/" + VOL)
    tgt = TargetInfo(kind=MA.ALIAS_KIND_FILE, filename=name, folder_cnid=0, cnid=0,
                     creation_date=now, creator_code=b"\0\0\0\0", type_code=b"\0\0\0\0",
                     levels_from=-1, levels_to=-1, folder_name=folder,
                     carbon_path="%s:%s:%s" % (VOL, folder, name),
                     posix_path="/Volumes/%s/%s" % (VOL, rel))
    return Alias(volume=vol, target=tgt).to_bytes()

icvp = {
    "viewOptionsVersion": 1, "backgroundType": 2,
    "backgroundColorRed": 1.0, "backgroundColorGreen": 1.0, "backgroundColorBlue": 1.0,
    "backgroundImageAlias": alias_for(".background/background.png", "background.png", ".background"),
    "gridOffsetX": 0.0, "gridOffsetY": 0.0, "gridSpacing": 100.0,
    "arrangeBy": "none", "showIconPreview": False, "showItemInfo": False,
    "labelOnBottom": True, "textSize": 12.0, "iconSize": 96.0,
    "scrollPositionX": 0.0, "scrollPositionY": 0.0,
}
bwsp = {
    "WindowBounds": "{{220, 150}, {640, 460}}",
    "ShowStatusBar": False, "ShowToolbar": False, "ShowTabView": False,
    "ShowPathbar": False, "ShowSidebar": False, "ContainerShowSidebar": False,
    "PreviewPaneVisibility": False, "SidebarWidth": 0,
}
ds = os.path.join(DIST, ".DS_Store")
with DSStore.open(ds, "w+") as d:
    d["."]["icvp"] = icvp
    d["."]["bwsp"] = bwsp
    d["."]["vSrn"] = ("long", 1)
    d["."]["ICVO"] = ("bool", True)
    d[APP]["Iloc"]                          = (170, 165)
    d["Applications"]["Iloc"]               = (470, 165)
    d["Open Sarawat directly.html"]["Iloc"] = (170, 335)
    d["Read Me.txt"]["Iloc"]                = (470, 335)
    d[".background"]["Iloc"]                = (900, 900)
print("built .DS_Store (%d bytes)" % os.path.getsize(ds))

# ------------------------------------------------------------------ image
iso = os.path.join(SP, "sarawat.iso")
# -hfsplus writes a real HFS+ filesystem alongside ISO 9660; macOS mounts the
# HFS+ view, which is what a hand-made .dmg normally contains.
subprocess.run(["xorrisofs", "-hfsplus", "-D", "-l", "-V", VOL, "-no-pad", "-r",
                "-dir-mode", "0755", "-o", iso, DIST], check=True,
               stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
print("iso %.2f MB" % (os.path.getsize(iso) / 1e6))
if os.path.exists(OUT):
    os.remove(OUT)
subprocess.run([DMGTOOL, iso, OUT], check=True, stdout=subprocess.DEVNULL)
print("dmg %.2f MB -> %s" % (os.path.getsize(OUT) / 1e6, OUT))

# ------------------------------------------------------- fix the koly trailer
# libdmg-hfsplus leaves SectorCount at 0; write the real value so the UDIF
# trailer describes the image it actually contains.
import struct
with open(OUT, "rb") as f:
    buf = bytearray(f.read())
sectors = os.path.getsize(iso) // 512
base = len(buf) - 512
buf[base + 0x1EC: base + 0x1F4] = struct.pack(">Q", sectors)
with open(OUT, "wb") as f:
    f.write(bytes(buf))
print("koly sectorCount -> %d" % sectors)
