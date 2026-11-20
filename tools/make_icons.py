"""Generates PNG icons (dark bg + mint progress ring) with no dependencies."""
import math, os, struct, zlib

def png(size, path):
    bg, acc, dim = (0, 0, 0), (255, 255, 255), (42, 42, 42)
    cx = cy = size / 2
    r, w = size * 0.30, size * 0.075
    ss = 3  # supersampling
    rows = []
    for y in range(size):
        row = bytearray([0])
        for x in range(size):
            tot = [0, 0, 0]
            for sy in range(ss):
                for sx in range(ss):
                    px, py = x + (sx + .5) / ss, y + (sy + .5) / ss
                    d = math.hypot(px - cx, py - cy)
                    c = bg
                    if abs(d - r) <= w / 2:
                        ang = (math.degrees(math.atan2(py - cy, px - cx)) + 90) % 360
                        c = acc if ang <= 270 else dim  # 75% filled
                    for i in range(3): tot[i] += c[i]
            row += bytes(v // (ss * ss) for v in tot)
        rows.append(bytes(row))
    raw = b''.join(rows)
    def chunk(t, d):
        c = struct.pack('>I', len(d)) + t + d
        return c + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
    data = b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', size, size, 8, 2, 0, 0, 0)) \
        + chunk(b'IDAT', zlib.compress(raw, 9)) + chunk(b'IEND', b'')
    open(path, 'wb').write(data)

out = os.path.join(os.path.dirname(__file__), '..', 'icons')
os.makedirs(out, exist_ok=True)
png(180, os.path.join(out, 'apple-touch-icon.png'))
png(192, os.path.join(out, 'icon-192.png'))
png(512, os.path.join(out, 'icon-512.png'))
print('ok')
