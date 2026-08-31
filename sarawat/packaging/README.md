# Packaging

Builds `Sarawat-Terroir-Engine-<ver>.dmg` from Linux — no Mac required.

## How

macOS mounts more than HFS+. The image here is ISO 9660 with Rock Ridge
extensions (which carry the POSIX permission bits and the `/Applications`
symlink a drag-install needs), wrapped in a UDIF/UDZO container. This is the
same route Bitcoin Core uses for its Linux-built macOS disk images, and it
avoids needing an HFS+ kernel module the container does not have.

    xorrisofs -D -l -V "<volume>" -no-pad -r -dir-mode 0755 -o out.iso dist/
    dmg out.iso out.dmg      # libdmg-hfsplus

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

## Not signed

The app contains no Mach-O binary — the launcher is a shell script — so it runs
on Apple Silicon without the ad-hoc signature an unsigned native binary would
need. It is still unsigned and un-notarised, so Gatekeeper quarantines it on
first launch: right-click → Open, once. Signing and notarising would require an
Apple Developer ID and a Mac to run `codesign`/`notarytool`.
