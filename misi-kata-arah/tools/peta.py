#!/usr/bin/env python3
"""Bina semula Peta Misi Angkasa dengan 6 hentian (tambah Planet Semakan) daripada gambar asal.

Usage (dari misi-kata-arah/):  python3 tools/peta.py
Input:  design/peta/asal/4.png (3 label, tiada watak bersorak) dan 6.png (5 label + watak bersorak)
Output: design/peta/peta-1.png ... peta-6.png (1920x1080), label muncul ikut urutan hentian.

Elemen asal (planet, stesen, watak, label) dipotong daripada gambar asal, dikecilkan 0.8 dan
disusun semula. Planet Semakan dibina daripada tekstur planet asal (warna diubah ke merah jambu)
dengan ikon papan semak. Label PLANET SEMAKAN disusun daripada huruf label asal.
"""
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(__file__))
from peta_lib import BOX, D, SRC_FULL, SRC_PLAIN, element_alpha, make_plate, path_mask  # noqa: E402

K = 0.8                      # skala elemen
YC_SRC, YC_NEW = 600, 650    # paksi menegak: y_baru = YC_NEW + (y - YC_SRC) * K
PINK = (246, 140, 182)       # warna Planet Semakan (RGB), sepadan dengan "Ekspedisi Kata Arah"

SOLID = {"ilmu": (210, 606, 120), "zon": (982, 566, 118), "maklum": (1368, 585, 138), "semakan": (1368, 585, 138),
         "misi": (1734, 630, 110)}

plate = make_plate(SRC_PLAIN)
plate_full = make_plate(SRC_FULL)


def cut(name, src, pl):
    """Potong elemen + alfa, buang serpihan laluan neon lama dalam zon tertentu."""
    (x0, y0, x1, y1), (cx, cy) = BOX[name]
    a = element_alpha(src, pl, (x0, y0, x1, y1))
    pm = path_mask(src)[y0:y1, x0:x1]
    yy, xx = np.mgrid[y0:y1, x0:x1]
    if name == "ilmu":
        zone = xx > 303
        a[(xx > 290) & (yy < 590) & ((xx - cx) ** 2 + (yy - cy) ** 2 > 126 ** 2)] = 0
    elif name == "stesen":
        feet = (xx > 612) & (xx < 708) & (yy > 640) & (yy < 738)
        zone = ((xx < 472) & (yy > 492) & (yy < 562)) | ((yy > 680) & ~feet) | ((xx > 722) & (yy > 630))
    elif name == "zon":
        zone = yy > 652
    elif name in ("maklum", "semakan"):
        zone = (xx - cx) ** 2 + (yy - cy) ** 2 > 147 ** 2
    elif name == "misi":
        zone = (xx < 1600) & (yy > 640)
    kill = cv2.dilate((pm & zone).astype(np.uint8), np.ones((9, 9), np.uint8)) > 0
    a[kill & zone] = 0
    # teras planet pepejal supaya laluan di belakangnya tidak tembus
    if name in SOLID:
        sx, sy, sr = SOLID[name]
        disc = np.zeros(a.shape, np.float32)
        cv2.circle(disc, (sx - x0, sy - y0), sr, 1.0, -1, cv2.LINE_AA)
        a = np.maximum(a, cv2.GaussianBlur(disc, (0, 0), 2))
    return src[y0:y1, x0:x1].copy(), a, (x0, y0), (cx, cy)


def semakan():
    """Planet Semakan: tekstur planet Maklum Balas, ikon dibuang, warna ke merah jambu, ikon papan semak."""
    rgb, a, org, c = cut("semakan", SRC_PLAIN, plate)
    x0, y0 = org
    # buang ikon gelembung (kawasan mint terang) dengan inpaint
    sub = rgb.astype(int)
    b, g, r = sub[..., 0], sub[..., 1], sub[..., 2]
    yy, xx = np.mgrid[y0:y0 + rgb.shape[0], x0:x0 + rgb.shape[1]]
    icon = (xx > 1312) & (xx < 1430) & (yy > 535) & (yy < 650) & (g > 150)
    icon = cv2.dilate(icon.astype(np.uint8) * 255, np.ones((11, 11), np.uint8))
    rgb = cv2.inpaint(rgb, icon, 9, cv2.INPAINT_TELEA)
    # ubah rona: teal -> merah jambu (OpenCV hue 0-180), hanya pada planet dan cahayanya
    hsv = cv2.cvtColor(rgb, cv2.COLOR_BGR2HSV).astype(int)
    hsv[..., 0] = (hsv[..., 0] + 74) % 180
    hsv[..., 1] = np.clip(hsv[..., 1] * 1.05, 0, 255)
    hsv[..., 2] = np.clip(hsv[..., 2] * 1.12, 0, 255)
    shifted = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR).astype(np.float32)
    rr = np.sqrt((xx - c[0]) ** 2 + (yy - c[1]) ** 2)
    wgt = np.clip((178 - rr) / 22, 0, 1)[..., None]
    rgb = (shifted * wgt + rgb.astype(np.float32) * (1 - wgt)).astype(np.uint8)
    a = a * np.clip((192 - rr) / 22, 0, 1).astype(np.float32)
    # bulan kecil (tekstur planet Misi Berjaya, warna lilac) di kanan atas
    (mx0, my0, mx1, my1), (mcx, mcy) = BOX["misi"]
    R = 112
    disc = SRC_PLAIN[mcy - R:mcy + R, mcx - R:mcx + R].copy()
    dh = cv2.cvtColor(disc, cv2.COLOR_BGR2HSV).astype(int)
    dh[..., 0] = (dh[..., 0] + 112) % 180
    dh[..., 1] = np.clip(dh[..., 1] * 0.75, 0, 255)
    disc = cv2.cvtColor(dh.astype(np.uint8), cv2.COLOR_HSV2BGR)
    mr = 27
    disc = cv2.resize(disc, (2 * mr, 2 * mr), interpolation=cv2.INTER_AREA)
    dm = np.zeros((2 * mr, 2 * mr), np.float32)
    cv2.circle(dm, (mr, mr), mr - 2, 1.0, -1, cv2.LINE_AA)
    dm = cv2.GaussianBlur(dm, (0, 0), 0.8)
    px, py = c[0] + 112 - x0, c[1] - 116 - y0
    glow = np.zeros(a.shape, np.float32)
    cv2.circle(glow, (px, py), mr + 6, 1.0, -1)
    glow = cv2.GaussianBlur(glow, (0, 0), 6) * 0.45
    rgb = rgb.astype(np.float32)
    rgb = rgb * (1 - glow[..., None]) + np.array([255, 190, 215], np.float32) * glow[..., None]
    a = np.maximum(a, glow)
    reg = (slice(py - mr, py + mr), slice(px - mr, px + mr))
    rgb[reg] = rgb[reg] * (1 - dm[..., None]) + disc * dm[..., None]
    a[reg] = np.maximum(a[reg], dm)
    # ikon papan semak (dilukis 4x lalu dikecilkan)
    S = 4
    W, H = 104, 124
    im = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([6 * S, 12 * S, (W - 6) * S, (H - 4) * S], radius=16 * S, fill=(255, 214, 233, 255))
    d.rounded_rectangle([6 * S, 12 * S, (W - 6) * S, 40 * S], radius=16 * S, fill=(255, 232, 243, 255))
    d.rectangle([6 * S, 30 * S, (W - 6) * S, 40 * S], fill=(255, 214, 233, 255))
    d.rounded_rectangle([34 * S, 2 * S, (W - 34) * S, 24 * S], radius=8 * S, fill=(214, 76, 138, 255))
    d.ellipse([(W / 2 - 5) * S, 7 * S, (W / 2 + 5) * S, 17 * S], fill=(255, 214, 233, 255))
    for i, yv in enumerate((52, 76, 100)):
        d.line([(20 * S, yv * S), (27 * S, (yv + 7) * S), (40 * S, (yv - 7) * S)], fill=(214, 76, 138, 255), width=6 * S, joint="curve")
        d.rounded_rectangle([48 * S, (yv - 4) * S, (W - 18) * S, (yv + 4) * S], radius=4 * S, fill=(244, 160, 198, 255))
    im = im.resize((W, H), Image.LANCZOS)
    ic = np.asarray(im).astype(np.float32)
    ia = ic[..., 3] / 255.0 * 0.96
    icb = ic[..., [2, 1, 0]]
    ix, iy = c[0] - W // 2 - x0, c[1] - H // 2 + 6 - y0
    gl = cv2.GaussianBlur(ia, (0, 0), 7) * 0.55
    reg = (slice(iy, iy + H), slice(ix, ix + W))
    rgb[reg] = rgb[reg] * (1 - gl[..., None]) + np.array([235, 185, 255], np.float32) * gl[..., None]
    rgb[reg] = rgb[reg] * (1 - ia[..., None]) + icb * ia[..., None]
    return np.clip(rgb, 0, 255).astype(np.uint8), a, org, c


def paste(canvas, rgb, a, org, c, new_c):
    """Tampal elemen yang dikecilkan K dengan pusat c (asal) -> new_c (baru)."""
    h, w = a.shape
    nw, nh = int(round(w * K)), int(round(h * K))
    rs = cv2.resize(rgb, (nw, nh), interpolation=cv2.INTER_AREA).astype(np.float32)
    ra = cv2.resize(a, (nw, nh), interpolation=cv2.INTER_AREA)[..., None]
    nx = int(round(new_c[0] + (org[0] - c[0]) * K))
    ny = int(round(YC_NEW + (org[1] - YC_SRC) * K))
    x0, y0 = max(nx, 0), max(ny, 0)
    x1, y1 = min(nx + nw, canvas.shape[1]), min(ny + nh, canvas.shape[0])
    sx, sy = x0 - nx, y0 - ny
    reg = canvas[y0:y1, x0:x1]
    ra = ra[sy:sy + y1 - y0, sx:sx + x1 - x0]
    rs = rs[sy:sy + y1 - y0, sx:sx + x1 - x0]
    canvas[y0:y1, x0:x1] = reg * (1 - ra) + rs * ra


def catmull(pts, n=24):
    out = []
    P = [pts[0]] + pts + [pts[-1]]
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = map(np.array, P[i - 1:i + 3])
        for t in np.linspace(0, 1, n, endpoint=False):
            t2, t3 = t * t, t * t * t
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    out.append(np.array(pts[-1]))
    return np.array(out)


def neon(canvas, curves, arrows):
    """Laluan neon: halo magenta + teras putih-merah jambu (diukur daripada gambar asal), campuran 'screen'."""
    S = 2
    hh, ww = canvas.shape[0] * S, canvas.shape[1] * S
    layers = {k: np.zeros((hh, ww), np.float32) for k in ("glow", "mid", "core")}
    widths = {"glow": 16, "mid": 8, "core": 4}

    def stroke(poly):
        p = (np.array(poly) * S).astype(np.int32).reshape(-1, 1, 2)
        for k, wv in widths.items():
            cv2.polylines(layers[k], [p], False, 1.0, int(wv * S), cv2.LINE_AA)

    for c in curves:
        stroke(catmull(c))
    for (x, y, ang) in arrows:
        L, spread = 24, np.radians(36)
        th = np.radians(ang)
        for sgn in (-1, 1):
            stroke([(x - L * np.cos(th + sgn * spread), y - L * np.sin(th + sgn * spread)), (x, y)])
    blur = {"glow": 7, "mid": 1.6, "core": 0.6}
    cols = {"glow": (100, 30, 120), "mid": (150, 85, 175), "core": (242, 230, 255)}  # BGR
    img = canvas.astype(np.float32) / 255
    for k in ("glow", "mid", "core"):
        m = cv2.GaussianBlur(layers[k], (0, 0), blur[k] * S)
        m = cv2.resize(m, (canvas.shape[1], canvas.shape[0]), interpolation=cv2.INTER_AREA)
        col = np.array(cols[k], np.float32) / 255
        add = m[..., None] * col * (0.9 if k == "glow" else 1.0)
        img = 1 - (1 - img) * (1 - np.clip(add, 0, 1))
    canvas[...] = np.clip(img * 255, 0, 255)


# ---- label
LBOX = {"ilmu": (95, 768, 296, 878), "stesen": (425, 768, 760, 878), "zon": (875, 768, 1110, 878),
        "maklum": (1180, 768, 1560, 878), "misi": (1610, 762, 1850, 900)}


def label_from_src(name):
    x0, y0, x1, y1 = LBOX[name]
    crop = SRC_FULL[y0:y1, x0:x1]
    v = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)[..., 2].astype(np.float32)
    a = np.clip((v - 60) / 70, 0, 1)
    if name == "misi":  # buang serpihan orbit di atas tulisan
        a[:12] = 0
    return crop.copy(), a


def glyph(x0, x1, y0=770, y1=826):
    v = cv2.cvtColor(SRC_FULL[y0:y1, x0 - 2:x1 + 3], cv2.COLOR_BGR2HSV)[..., 2].astype(np.float32)
    return np.clip((v - 60) / 70, 0, 1)


def label_semakan():
    l1 = glyph(110, 292)                                   # PLANET
    g = [glyph(504, 527), glyph(564, 588), glyph(1192, 1225), glyph(1230, 1257),
         glyph(1263, 1284), glyph(1230, 1257), glyph(650, 678)]   # S E M A K A N
    gap = 1
    l2 = np.concatenate(sum([[x, np.zeros((x.shape[0], gap), np.float32)] for x in g], [])[:-1], 1)
    W = max(l1.shape[1], l2.shape[1])
    H = 53 + l2.shape[0]
    a = np.zeros((H, W), np.float32)
    a[0:l1.shape[0], (W - l1.shape[1]) // 2:(W - l1.shape[1]) // 2 + l1.shape[1]] = l1
    a[53:53 + l2.shape[0], (W - l2.shape[1]) // 2:(W - l2.shape[1]) // 2 + l2.shape[1]] = np.maximum(
        a[53:53 + l2.shape[0], (W - l2.shape[1]) // 2:(W - l2.shape[1]) // 2 + l2.shape[1]], l2)
    rgb = np.zeros((H, W, 3), np.uint8)
    rgb[...] = PINK[::-1]
    return rgb, a


def paste_label(canvas, rgb, a, cx, top):
    h, w = a.shape
    nw, nh = int(round(w * K)), int(round(h * K))
    rs = cv2.resize(rgb, (nw, nh), interpolation=cv2.INTER_AREA).astype(np.float32)
    ra = cv2.resize(a, (nw, nh), interpolation=cv2.INTER_AREA)
    ys, xs = np.where(ra > 0.3)
    x0 = int(round(cx - (xs.min() + xs.max()) / 2))
    y0 = int(round(top - ys.min()))
    reg = canvas[y0:y0 + nh, x0:x0 + nw]
    canvas[y0:y0 + nh, x0:x0 + nw] = reg * (1 - ra[..., None]) + rs * ra[..., None]


# ---- susun atur 6 hentian (pusat x baharu)
ORDER = ["ilmu", "stesen", "zon", "semakan", "maklum", "misi"]
NEWX = {"ilmu": 179, "stesen": 490, "zon": 853, "semakan": 1186, "maklum": 1480, "misi": 1769}
LTOP = {"ilmu": 790, "stesen": 790, "zon": 790, "semakan": 790, "maklum": 790, "misi": 806}

elems = {n: cut(n, SRC_PLAIN, plate) for n in ("ilmu", "stesen", "zon", "maklum", "misi")}
elems["semakan"] = semakan()
misi_party = cut("misi", SRC_FULL, plate_full)
labels = {n: label_from_src(n) for n in ("ilmu", "stesen", "zon", "maklum", "misi")}
labels["semakan"] = label_semakan()

curves = [[(253, 720), (300, 724), (362, 714)],
          [(470, 716), (600, 712), (728, 703)],
          [(735, 704), (853, 744), (990, 728), (1062, 713)],
          [(1150, 716), (1260, 718), (1356, 713)],
          [(1440, 716), (1560, 718), (1652, 705)],
          [(1652, 705), (1665, 703)]]
arrows = [(362, 714, -6), (728, 703, -4), (1062, 713, -12), (1356, 713, -3), (1652, 705, -8)]

DY = YC_NEW - 630
curves = [[(x, y + DY) for x, y in c] for c in curves]
arrows = [(x, y + DY, t) for x, y, t in arrows]
base = plate.astype(np.float32).copy()
neon(base, curves, arrows)
for n in ORDER:
    if n == "misi":
        continue
    rgb, a, org, c = elems[n]
    paste(base, rgb, a, org, c, (NEWX[n], 0))

for step in range(1, 7):
    img = base.copy()
    rgb, a, org, c = misi_party if step == 6 else elems["misi"]
    paste(img, rgb, a, org, c, (NEWX["misi"], 0))
    for n in ORDER[:step]:
        lr, la = labels[n]
        paste_label(img, lr, la, NEWX[n], LTOP[n])
    out = os.path.join(D, f"peta-{step}.png")
    cv2.imwrite(out, np.clip(img, 0, 255).astype(np.uint8))
print("peta-1.png ... peta-6.png ditulis dalam design/peta/")
