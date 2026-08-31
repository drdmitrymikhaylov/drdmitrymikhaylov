# Packaging

Builds `Sarawat-Terroir-Engine-<ver>.dmg` from Linux — no Mac required.

## How

`xorrisofs -hfsplus` writes a real HFS+ filesystem behind an Apple Partition
Map — the same thing `hdiutil create` produces — with an ISO 9660 + Rock Ridge
view alongside it. That is then wrapped in a UDIF/UDZO container. No HFS+
kernel module is needed, which matters because the build container has none.

    xorrisofs -hfsplus -D -l -V "<volume>" -no-pad -r -dir-mode 0755 -o out.iso dist/
    dmg out.iso out.dmg      # libdmg-hfsplus

The HFS+ catalog carries the executable bit on the launcher and writes
`/Applications` as a genuine HFS+ symlink (`slnk`/`rhap`), which is what makes
the drag-install work.

`build_dmg.py` also writes the `.DS_Store` that gives the mounted window its
background image, 640×400 size, 96 px icons and item positions — built with
`ds_store` and a hand-constructed `mac_alias` Alias record, since
`Alias.for_file()` only runs on macOS.

## Dependencies

    apt-get install xorriso cmake build-essential zlib1g-dev libbz2-dev libssl-dev
    pip install Pillow ds_store mac_alias
    git clone https://github.com/fanquake/libdmg-hfsplus && cd libdmg-hfsplus && cmake . && make

`icon.html` and `bg.html` are rendered to PNG with headless Chromium; the
Montserrat and IBM Plex Mono faces are injected as data URIs at build time.

## Verifying without a Mac

    python3 verify_dmg.py Sarawat-Terroir-Engine-4.2.dmg out.iso

Parses the koly trailer, decompresses every blkx chunk and checks the result is
byte-identical to the source filesystem. It also flags a `sectorCount` that
disagrees with the payload — libdmg-hfsplus leaves that field at zero, and
`build_dmg.py` patches in the real value.

## Gatekeeper

An unsigned app is quarantined on first launch. Because that cannot be fixed
from the build side, the image also ships `Open Sarawat directly.html` at the
top level: the same tool as a plain file, which Gatekeeper has no reason to
touch. The Read Me covers the Terminal `xattr` route and, for macOS 15
Sequoia, the System Settings "Open Anyway" button that replaced the old
right-click → Open shortcut.

## Not signed

The app contains no Mach-O binary — the launcher is a shell script — so it runs
on Apple Silicon without the ad-hoc signature an unsigned native binary would
need. It is still unsigned and un-notarised, so Gatekeeper quarantines it on
first launch: right-click → Open, once. Signing and notarising would require an
Apple Developer ID and a Mac to run `codesign`/`notarytool`.
