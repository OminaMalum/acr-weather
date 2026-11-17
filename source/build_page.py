"""Builds ../index.html: the live ACR Contractor Forecast page for the store TVs (TPM Web layer).

The page itself pulls fresh National Weather Service data (api.weather.gov, public, no key) every 15 minutes
in the viewer's browser, so nothing here needs to run again unless the design changes.
  python3 build_page.py
URL options:  ?store=raleigh   (that store's own forecast on the left, its map chip highlighted)
              default           (all 8 stores)
"""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "index.html")
rings = json.load(open("/mnt/project-files/social/weekly-forecast/source/nc_outline.json"))

# Store points match social/weekly-forecast/source/fetch_nws.py; NWS grid cells from api.weather.gov/points.
STORES = [  # name, lat, lon, office, gridX, gridY, chip x, chip y (in the 1000x880 map box)
    ("Winston-Salem", 36.0999, -80.2442, "RAH", 15, 65, 130, 62),
    ("Greensboro", 36.0726, -79.7920, "RAH", 32, 66, 375, 62),
    ("Burlington", 36.0957, -79.4378, "RAH", 44, 68, 620, 62),
    ("Durham", 35.9940, -78.8986, "RAH", 64, 66, 865, 62),
    ("Carrboro", 35.9101, -79.0753, "RAH", 58, 61, 175, 480),
    ("Raleigh", 35.7796, -78.6382, "RAH", 75, 57, 450, 490),
    ("Greenville", 35.6127, -77.3664, "MHX", 30, 95, 860, 340),
    ("Wilmington", 34.2257, -77.9447, "ILM", 89, 75, 330, 700),
]
LON0, LON1, LAT1 = -81.25, -75.40, 36.70
K = math.cos(math.radians(35.2))
W, H, MAPW, OX, OY = 1000, 880, 900, 50, 200
sc = MAPW / ((LON1 - LON0) * K)
pr = lambda la, lo: (OX + (lo - LON0) * K * sc, OY + (LAT1 - la) * sc)
path = "".join('<path d="M' + " L".join(f"{pr(la, lo)[0]:.1f},{pr(la, lo)[1]:.1f}" for lo, la in r) + 'Z"/>' for r in rings)
CW, CH = 236, 120
chips = []
for n, la, lo, *_rest, lx, ly in STORES:
    px, py = pr(la, lo)
    key = n.lower().replace("-", "")
    chips.append(f'''<g class="s" id="s-{key}"><line x1="{px:.1f}" y1="{py:.1f}" x2="{lx}" y2="{ly}" stroke="#fff" stroke-width="3" opacity=".85"/>
<circle cx="{px:.1f}" cy="{py:.1f}" r="10" fill="#fff" stroke="#00467A" stroke-width="3"/>
<g transform="translate({lx - CW / 2},{ly - CH / 2})"><rect class="chipbg" width="{CW}" height="{CH}" rx="14"/>
<text x="{CW / 2}" y="38" text-anchor="middle" class="cn">{n}</text>
<text x="{CW / 2}" y="98" text-anchor="middle"><tspan class="ct" data-now="{key}">--</tspan><tspan class="cl" dx="10" data-low="{key}"></tspan></text></g></g>''')
svg = f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs><linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".14" stop-color="#fff"/></linearGradient>
<mask id="m"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask></defs>
<g mask="url(#m)" fill="rgba(255,255,255,.14)" stroke="rgba(255,255,255,.75)" stroke-width="3" stroke-linejoin="round">{path}</g>
{"".join(chips)}</svg>'''
stores_js = json.dumps([{"name": n, "key": n.lower().replace("-", ""), "office": o, "x": gx, "y": gy}
                        for n, la, lo, o, gx, gy, lx, ly in STORES])

html = open(os.path.join(HERE, "template.html")).read().replace("%%MAP%%", svg).replace("%%STORES%%", stores_js)
open(OUT, "w").write(html)
print("wrote", os.path.abspath(OUT), len(html), "bytes")
