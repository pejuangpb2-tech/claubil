# Replace the burned-in caption "AWAK" with "AWOK" by swapping the 2nd A for the video's own O glyph.
import cv2, numpy as np, subprocess, sys, json
src, out, sheet_dir = sys.argv[1], sys.argv[2], sys.argv[3]
W, H, N = 720, 1280, None
def read_all(path):
    p = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", path, "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], capture_output=True, check=True)
    a = np.frombuffer(p.stdout, np.uint8); return a.reshape(-1, H, W, 3)
X0, Y0, X1, Y1 = 200, 930, 520, 1055
def stream(path):
    p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-i", path, "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE)
    n = W * H * 3
    while True:
        b = p.stdout.read(n)
        if len(b) < n: break
        yield np.frombuffer(b, np.uint8).reshape(H, W, 3)
C = np.stack([f[Y0:Y1, X0:X1].copy() for f in stream(src)]); N = len(C); print("frames", N)
G = C.astype(np.float32)
def find(ref_idx, thr=30):
    ref = cv2.cvtColor(C[ref_idx], cv2.COLOR_BGR2GRAY).astype(np.float32)
    fill = ref > 215
    near = cv2.dilate(fill.astype(np.uint8), np.ones((9, 9), np.uint8)) > 0
    mask = fill | ((ref < 45) & near)
    gray = G.mean(axis=3)
    d = np.abs(gray - ref)[:, mask].mean(axis=1)
    return np.nonzero(d < thr)[0]
awak = find(24); orang = find(31)
print("AWAK frames", len(awak), "ORANG frames", len(orang))
def ink(idx):
    s = G[idx]; std = s.std(axis=0).max(axis=2); med = np.median(s, axis=0)
    return std, med
std_a, med_a = ink(awak); std_o, med_o = ink(orang)
cols = lambda x0, x1: (slice(None), slice(x0 - X0, x1 - X0 + 1))
# 2nd A of AWAK: fill cols 371-418 -> ink region with stroke margin, bounded halfway to neighbours
a_ink = np.zeros(std_a.shape, bool); a_ink[cols(367, 423)] = (std_a < 10)[cols(367, 423)]
# O of ORANG: fill cols 232-277
o_ink = np.zeros(std_o.shape, bool); o_ink[cols(224, 282)] = (std_o < 10)[cols(224, 282)]
# keep the largest connected blob(s) touching the glyph only
def clean(m):
    n, lab, st, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), 8)
    keep = np.zeros_like(m)
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] > 200: keep |= lab == i
    return keep
def solid(m):
    m = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
    h, w = m.shape; ff = np.pad(m, 1).copy(); mk = np.zeros((h + 4, w + 4), np.uint8)
    cv2.floodFill(ff, mk, (0, 0), 2)
    return (ff[1:-1, 1:-1] != 2)
a_ink = solid(clean(a_ink)); o_ink = solid(clean(o_ink))
dx = round(((371 + 418) - (232 + 277)) / 2)
M = np.float32([[1, 0, dx], [0, 1, 0]])
o_ink_s = cv2.warpAffine(o_ink.astype(np.uint8), M, (X1 - X0, Y1 - Y0)) > 0
o_rgb_s = cv2.warpAffine(med_o, M, (X1 - X0, Y1 - Y0))
alpha = cv2.GaussianBlur(o_ink_s.astype(np.float32), (3, 3), 0.6)[..., None]
rm = cv2.dilate(a_ink.astype(np.uint8), np.ones((3, 3), np.uint8))
cv2.imwrite(f"{sheet_dir}/mask_a.png", a_ink.astype(np.uint8) * 255)
cv2.imwrite(f"{sheet_dir}/mask_o.png", o_ink_s.astype(np.uint8) * 255)
patched = {}
for i in awak:
    reg = C[i].copy()
    reg = cv2.inpaint(reg, rm, 5, cv2.INPAINT_TELEA).astype(np.float32)
    reg = reg * (1 - alpha) + o_rgb_s * alpha
    patched[int(i)] = np.clip(reg, 0, 255).astype(np.uint8)
json.dump([int(i) for i in awak], open(f"{sheet_dir}/awak_frames.json", "w"))
enc = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", "30",
    "-i", "-", "-i", src, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "slow", "-crf", "14", "-g", "30",
    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
for i, f in enumerate(stream(src)):
    if i in patched:
        f = f.copy(); f[Y0:Y1, X0:X1] = patched[i]
        if i in (24, 585, 750, 1248): cv2.imwrite(f"{sheet_dir}/after_{i}.png", f[Y0-60:Y1+20, 120:600]); cv2.imwrite(f"{sheet_dir}/before_{i}.png", C[i])
    enc.stdin.write(f.tobytes())
enc.stdin.close(); enc.wait(); print("written", out)
