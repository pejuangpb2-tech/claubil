"""Bahan bersama untuk membina semula Peta Misi Angkasa (6 hentian) daripada gambar asal."""
import os
import cv2
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "design", "peta")
SRC_PLAIN = cv2.imread(os.path.join(D, "asal", "4.png"))   # 3 label, tiada watak bersorak
SRC_FULL = cv2.imread(os.path.join(D, "asal", "6.png"))    # 5 label + watak bersorak

# Kotak elemen dalam gambar asal (x0, y0, x1, y1) dan titik pusatnya
BOX = {
    "ilmu":   ((15, 470, 352, 745), (210, 606)),
    "stesen": ((400, 375, 792, 745), (597, 555)),
    "zon":    ((792, 392, 1202, 742), (990, 565)),
    "maklum": ((1208, 432, 1528, 742), (1368, 585)),
    "semakan": ((1208, 432, 1528, 742), (1368, 585)),
    "misi":   ((1520, 288, 1912, 778), (1734, 630)),
}


def hsv(img):
    h = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    return h[..., 0].astype(int), h[..., 1].astype(int), h[..., 2].astype(int)


def make_plate(img):
    """Latar tanpa elemen dan label di jalur tengah (inpaint), ditabur bintang berbenih."""
    _, _, v = hsv(img)
    m = np.zeros(v.shape, np.uint8)
    band = np.zeros_like(m)
    band[372:912, :] = 1
    band[780:, :70] = 0
    band[800:, 1850:] = 0
    band[286:372, 1500:1915] = 1
    m[(v > 30) & (band > 0)] = 255
    m = cv2.dilate(m, np.ones((31, 31), np.uint8))
    m[band == 0] = 0
    small = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    ms = cv2.resize(m, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_NEAREST)
    pl = cv2.inpaint(small, ms, 12, cv2.INPAINT_TELEA)
    pl = cv2.resize(pl, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_CUBIC)
    pl = cv2.GaussianBlur(pl, (0, 0), 6)
    a = cv2.GaussianBlur((m > 0).astype(np.float32), (0, 0), 8)[..., None]
    out = (img * (1 - a) + pl * a).astype(np.float32)
    # bijian halus + bintang berbenih supaya kawasan yang ditampal tidak nampak licin
    rng = np.random.default_rng(2026)
    noise = rng.normal(0, 2.2, out.shape[:2]).astype(np.float32)
    out += (noise[..., None] * a)
    stars = np.zeros(out.shape[:2], np.float32)
    for _ in range(95):
        x, y = rng.integers(0, 1920), rng.integers(372, 912)
        if m[y, x] == 0:
            continue
        r = rng.choice([0.6, 0.8, 1.0, 1.4], p=[.45, .3, .17, .08])
        b = rng.uniform(90, 230)
        cv2.circle(stars, (int(x), int(y)), 3, float(b), -1)
    stars = cv2.GaussianBlur(stars, (0, 0), 0.9)
    out += stars[..., None] * np.array([1.0, 0.95, 0.9], np.float32) * 0.6
    return np.clip(out, 0, 255).astype(np.uint8)


def element_alpha(img, plate, box):
    x0, y0, x1, y1 = box
    d = np.abs(img[y0:y1, x0:x1].astype(int) - plate[y0:y1, x0:x1].astype(int)).max(2)
    a = np.clip((d - 10) / 45.0, 0, 1).astype(np.float32)
    a = cv2.GaussianBlur(a, (0, 0), 1.0)
    # lembutkan tepi kotak supaya tiada garis segi empat
    hh, ww = a.shape
    t = 18
    ry = np.clip(np.minimum(np.arange(hh), np.arange(hh)[::-1]) / t, 0, 1)
    rx = np.clip(np.minimum(np.arange(ww), np.arange(ww)[::-1]) / t, 0, 1)
    return a * ry[:, None] * rx[None, :]


def path_mask(img):
    """Laluan neon: halo ungu-magenta + teras putih kemerahan."""
    h, s, v = hsv(img)
    b, g, r = img[..., 0].astype(int), img[..., 1].astype(int), img[..., 2].astype(int)
    halo = (h >= 122) & (h <= 168) & (v > 110) & (s > 45)
    core = (v > 200) & (s < 90) & (r > g + 6) & (b > g)
    return halo | core
