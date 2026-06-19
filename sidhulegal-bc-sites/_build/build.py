#!/usr/bin/env python3
"""
Build Sidhu BC city sites from one Surrey-based template.
- make_template(): turns the live Surrey page into _build/template.html with {{TOKENS}}
- generate(slug): writes <dir>/index.html for a city from CITIES data
Layout always = Surrey's. Only city-specific fields change.
"""
import re, sys, os, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SURREY = os.path.join(ROOT, "sidhulegal-surrey", "index.html")
TPL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "template.html")

# master list (order = display order); name, slug, dir
CITIES_INDEX = [
    ("Surrey", "surrey", "sidhulegal-surrey"),
    ("Vancouver", "vancouver", "sidhulegal-vancouver"),
    ("Burnaby", "burnaby", "sidhulegal-burnaby"),
    ("Richmond", "richmond", "sidhulegal-richmond"),
    ("Coquitlam", "coquitlam", "sidhulegal-coquitlam"),
    ("Langley", "langley", "sidhulegal-langley"),
    ("Abbotsford", "abbotsford", "sidhulegal-abbotsford"),
    ("Delta", "delta", "sidhulegal-delta"),
    ("Maple Ridge", "maple-ridge", "sidhulegal-mapleridge"),
    ("New Westminster", "new-westminster", "sidhulegal-newwestminster"),
]

# per-city content. Fill local_* with REAL local facts. (Pilot: New West complete.)
CITIES = {
    "new-westminster": {
        "name": "New Westminster", "slug": "new-westminster", "dir": "sidhulegal-newwestminster",
        "meta_desc": "New Westminster's personal injury lawyers since 2013. Sidhu Legal fights ICBC and wins maximum compensation. Free consultation. No fee unless you win. Call (604) 907-3632.",
        "og_desc": "New Westminster's personal injury and ICBC lawyers since 2013. Free consultation, no fee unless you win.",
        "local_intro": "New Westminster is one of BC's oldest cities, a dense riverfront hub where the Pattullo and Queensborough bridges, Columbia Street, McBride Boulevard and the Highway 1 interchange funnel heavy traffic through tight corridors. If you have been hurt in or around New Westminster, here is the local context that shapes your claim.",
        "local_roads": "The Pattullo and Queensborough bridges, Columbia Street, McBride Boulevard, Stewardson Way, Brunette Avenue and the Highway 1 (Trans-Canada) interchange carry the city's heaviest traffic and are frequent collision points. Congestion through the Sapperton and Uptown corridors and wet conditions on the bridge approaches are common factors.",
        "local_hospital": "Serious injuries in New Westminster are treated at Royal Columbian Hospital, one of BC's busiest trauma centres. Keep every medical record and receipt, they are central to proving your claim.",
        "local_road_short": "the Pattullo Bridge", "local_area": "Sapperton",
    },
    "vancouver": {
        "name": "Vancouver", "slug": "vancouver", "dir": "sidhulegal-vancouver",
        "meta_desc": "Vancouver's personal injury lawyers since 2013. Sidhu Legal fights ICBC and wins maximum compensation. Free consultation. No fee unless you win. Call (604) 907-3632.",
        "og_desc": "Vancouver's personal injury and ICBC lawyers since 2013. Free consultation, no fee unless you win.",
        "local_intro": "Vancouver is BC's largest and most densely travelled city, where Knight Street, Oak Street, Granville Street, Kingsway and the Highway 1 corridor move enormous volumes of traffic every day. If you have been hurt in or around Vancouver, here is the local context that shapes your claim.",
        "local_roads": "Knight Street, Oak Street, Granville Street, Kingsway, Hastings Street and the Highway 1 corridor through East Vancouver carry the city's heaviest traffic and are frequent collision points. Dense downtown intersections, cyclists and heavy rain are common factors.",
        "local_hospital": "Serious injuries in Vancouver are treated at Vancouver General Hospital, one of Canada's busiest trauma centres. Keep every medical record and receipt, they are central to proving your claim.",
        "local_road_short": "Knight Street", "local_area": "Mount Pleasant",
    },
    "burnaby": {
        "name": "Burnaby", "slug": "burnaby", "dir": "sidhulegal-burnaby",
        "meta_desc": "Burnaby's personal injury lawyers since 2013. Sidhu Legal fights ICBC and wins maximum compensation. Free consultation. No fee unless you win. Call (604) 907-3632.",
        "og_desc": "Burnaby's personal injury and ICBC lawyers since 2013. Free consultation, no fee unless you win.",
        "local_intro": "Burnaby sits at the centre of Metro Vancouver, where Lougheed Highway, Kingsway, Canada Way, Willingdon Avenue and the Highway 1 corridor carry constant traffic between the region's busiest hubs. If you have been hurt in or around Burnaby, here is the local context that shapes your claim.",
        "local_roads": "Lougheed Highway, Kingsway, Canada Way, Willingdon Avenue and the Highway 1 (Trans-Canada) corridor carry the city's heaviest traffic and are frequent collision points. The Metrotown and Brentwood interchanges and wet conditions are common factors.",
        "local_hospital": "Serious injuries in Burnaby are treated at Burnaby Hospital and nearby Royal Columbian Hospital, among BC's busiest trauma centres. Keep every medical record and receipt, they are central to proving your claim.",
        "local_road_short": "Lougheed Highway", "local_area": "Metrotown",
    },
    "richmond": {
        "name": "Richmond", "slug": "richmond", "dir": "sidhulegal-richmond",
        "meta_desc": "Richmond's personal injury lawyers since 2013. Sidhu Legal fights ICBC and wins maximum compensation. Free consultation. No fee unless you win. Call (604) 907-3632.",
        "og_desc": "Richmond's personal injury and ICBC lawyers since 2013. Free consultation, no fee unless you win.",
        "local_intro": "Richmond is built on a network of flat, fast arterials and major crossings, where Highway 99, No. 3 Road, Steveston Highway, the Knight Street Bridge and the George Massey Tunnel funnel heavy traffic on and off Lulu Island. If you have been hurt in or around Richmond, here is the local context that shapes your claim.",
        "local_roads": "Highway 99, No. 3 Road, Steveston Highway, the Knight Street Bridge and the George Massey Tunnel carry the city's heaviest traffic and are frequent collision points. Airport traffic, fog off the Fraser and congested tunnel approaches are common factors.",
        "local_hospital": "Serious injuries in Richmond are treated at Richmond Hospital and regional trauma centres. Keep every medical record and receipt, they are central to proving your claim.",
        "local_road_short": "No. 3 Road", "local_area": "Steveston",
    },
    "coquitlam": {
        "name": "Coquitlam", "slug": "coquitlam", "dir": "sidhulegal-coquitlam",
        "meta_desc": "Coquitlam's personal injury lawyers since 2013. Sidhu Legal fights ICBC and wins maximum compensation. Free consultation. No fee unless you win. Call (604) 907-3632.",
        "og_desc": "Coquitlam's personal injury and ICBC lawyers since 2013. Free consultation, no fee unless you win.",
        "local_intro": "Coquitlam anchors the Tri-Cities, where the Lougheed Highway, Barnet Highway, Mary Hill Bypass and Highway 1 carry heavy commuter traffic through the northeast Lower Mainland. If you have been hurt in or around Coquitlam, here is the local context that shapes your claim.",
        "local_roads": "The Lougheed Highway, Barnet Highway, Mary Hill Bypass and the Highway 1 (Trans-Canada) corridor carry the city's heaviest traffic and are frequent collision points. Congestion around Coquitlam Centre and wet, hilly conditions are common factors.",
        "local_hospital": "Serious injuries in Coquitlam are treated at Eagle Ridge Hospital and nearby Royal Columbian Hospital. Keep every medical record and receipt, they are central to proving your claim.",
        "local_road_short": "the Lougheed Highway", "local_area": "Maillardville",
    },
    "langley": {
        "name": "Langley", "slug": "langley", "dir": "sidhulegal-langley",
        "meta_desc": "Langley's personal injury lawyers since 2013. Sidhu Legal fights ICBC and wins maximum compensation. Free consultation. No fee unless you win. Call (604) 907-3632.",
        "og_desc": "Langley's personal injury and ICBC lawyers since 2013. Free consultation, no fee unless you win.",
        "local_intro": "Langley spans fast-growing communities connected by the Highway 1 (Trans-Canada), Fraser Highway, 200th Street and Glover Road, which carry heavy traffic between Surrey, Abbotsford and the Fraser Valley. If you have been hurt in or around Langley, here is the local context that shapes your claim.",
        "local_roads": "The Highway 1 (Trans-Canada), Fraser Highway, 200th Street and Glover Road carry the city's heaviest traffic and are frequent collision points. Rapid growth in Willoughby and Walnut Grove and rural night driving are common factors.",
        "local_hospital": "Serious injuries in Langley are treated at Langley Memorial Hospital and regional trauma centres. Keep every medical record and receipt, they are central to proving your claim.",
        "local_road_short": "Fraser Highway", "local_area": "Willoughby",
    },
    "abbotsford": {
        "name": "Abbotsford", "slug": "abbotsford", "dir": "sidhulegal-abbotsford",
        "meta_desc": "Abbotsford's personal injury lawyers since 2013. Sidhu Legal fights ICBC and wins maximum compensation. Free consultation. No fee unless you win. Call (604) 907-3632.",
        "og_desc": "Abbotsford's personal injury and ICBC lawyers since 2013. Free consultation, no fee unless you win.",
        "local_intro": "Abbotsford is the largest city in the Fraser Valley, where the Highway 1 (Trans-Canada), Highway 11 (Sumas Way) and South Fraser Way carry heavy regional and cross-border traffic. If you have been hurt in or around Abbotsford, here is the local context that shapes your claim.",
        "local_roads": "The Highway 1 (Trans-Canada), Highway 11 (Sumas Way) and South Fraser Way carry the city's heaviest traffic and are frequent collision points. Cross-border traffic to the Sumas crossing, farm-vehicle routes and Valley fog are common factors.",
        "local_hospital": "Serious injuries in Abbotsford are treated at Abbotsford Regional Hospital, the Fraser Valley's main trauma centre. Keep every medical record and receipt, they are central to proving your claim.",
        "local_road_short": "Highway 11", "local_area": "Clearbrook",
    },
    "delta": {
        "name": "Delta", "slug": "delta", "dir": "sidhulegal-delta",
        "meta_desc": "Delta's personal injury lawyers since 2013. Sidhu Legal fights ICBC and wins maximum compensation. Free consultation. No fee unless you win. Call (604) 907-3632.",
        "og_desc": "Delta's personal injury and ICBC lawyers since 2013. Free consultation, no fee unless you win.",
        "local_intro": "Delta stretches from Ladner and Tsawwassen to North Delta, where Highway 91, Highway 99, the Alex Fraser Bridge and the George Massey Tunnel carry heavy traffic between the ferries, the border and the rest of Metro Vancouver. If you have been hurt in or around Delta, here is the local context that shapes your claim.",
        "local_roads": "Highway 91, Highway 99, the Alex Fraser Bridge, the George Massey Tunnel and Nordel Way carry the city's heaviest traffic and are frequent collision points. Ferry and border traffic and congested tunnel approaches are common factors.",
        "local_hospital": "Serious injuries in Delta are treated at Delta Hospital and regional trauma centres. Keep every medical record and receipt, they are central to proving your claim.",
        "local_road_short": "Highway 99", "local_area": "Ladner",
    },
    "maple-ridge": {
        "name": "Maple Ridge", "slug": "maple-ridge", "dir": "sidhulegal-mapleridge",
        "meta_desc": "Maple Ridge's personal injury lawyers since 2013. Sidhu Legal fights ICBC and wins maximum compensation. Free consultation. No fee unless you win. Call (604) 907-3632.",
        "og_desc": "Maple Ridge's personal injury and ICBC lawyers since 2013. Free consultation, no fee unless you win.",
        "local_intro": "Maple Ridge sits where the Lougheed Highway, Dewdney Trunk Road, the Haney Bypass and the Golden Ears Bridge carry traffic across the Fraser and through the northeast Fraser Valley. If you have been hurt in or around Maple Ridge, here is the local context that shapes your claim.",
        "local_roads": "The Lougheed Highway, Dewdney Trunk Road, the Haney Bypass and the Golden Ears Bridge carry the city's heaviest traffic and are frequent collision points. Bridge approaches, rural roads and wet-weather conditions are common factors.",
        "local_hospital": "Serious injuries in Maple Ridge are treated at Ridge Meadows Hospital. Keep every medical record and receipt, they are central to proving your claim.",
        "local_road_short": "the Lougheed Highway", "local_area": "Haney",
    },
}


def make_template():
    src = open(SURREY, encoding="utf-8").read()
    t = src

    # 1. master city variable
    t = t.replace('window._sidhuCity="Surrey"', 'window._sidhuCity="{{CITY}}"')

    # 2. meta description + og description
    t = re.sub(r'(<meta name="description" content=")(.*?)(">)', r'\1{{META_DESC}}\3', t, count=1)
    t = re.sub(r'(<meta property="og:description" content=")(.*?)(">)', r'\1{{OG_DESC}}\3', t, count=1)

    # 3. self-referential URL slug (canonical / og:url / schema url) -- Surrey isn't in its own link lists
    t = t.replace('surrey-personal-injury-lawyer', '{{SLUG}}-personal-injury-lawyer')

    # 4. local-knowledge section: swap city-specific inner content for tokens
    t = re.sub(r'(data-lx="lx_intro"[^>]*>)(.*?)(</p>)', r'\1{{LOCAL_INTRO}}\3', t, count=1, flags=re.S)
    t = re.sub(r'(data-lx="lx_pa"[^>]*>)(.*?)(</p>)',    r'\1{{LOCAL_ROADS}}\3', t, count=1, flags=re.S)
    t = re.sub(r'(data-lx="lx_pc"[^>]*>)(.*?)(</p>)',    r'\1{{LOCAL_HOSPITAL}}\3', t, count=1, flags=re.S)
    t = re.sub(r'(data-lx="lx_h2"[^>]*>)(.*?)(</h2>)',   r'\1Injury &amp; ICBC Claims in {{CITY}}: What to Know\3', t, count=1, flags=re.S)
    t = re.sub(r'(data-lx="lx_h3a"[^>]*>)(.*?)(</h3>)',  r'\1Where {{CITY}} crashes happen\3', t, count=1, flags=re.S)

    # 4b. local-fact values inside EVERY language's translation object -> city tokens (JS-string context)
    jsval = lambda key, tok: re.sub(key + r":'(?:\\.|[^'])*'", key + ":'" + tok + "'", t)
    t = jsval("lx_pa", "{{LOCAL_ROADS_JS}}")
    t = jsval("lx_pc", "{{LOCAL_HOSPITAL_JS}}")
    t = jsval("lx_intro", "{{LOCAL_INTRO_JS}}")
    t = jsval("lx_h2", "Injury & ICBC Claims in {{CITY}}: What to Know")
    t = jsval("lx_h3a", "Where {{CITY}} crashes happen")

    # 4d. hero subtitle + hero background image -> per-city tokens
    t = re.sub(r'(<p class="hero-sub">).*?(</p>)', r'\1{{HERO_SUB}}\2', t, count=1, flags=re.S)
    t = t.replace("https://images.unsplash.com/photo-1697755790236-2a455c4aa22c?auto=format&fit=crop&w=1920&q=80", "{{HERO_IMG}}")

    # 4e. testimonials grid -> per-city token (restore each city's own reviews)
    t = re.sub(r'(<div class="testi-grid">).*?(</div>\s*</div>\s*</section>)',
               r'\1\n{{TESTIMONIALS}}\n    \2', t, count=1, flags=re.S)

    # 4c. city landmarks hardcoded in testimonials -> tokens
    t = t.replace("After my accident on King George Blvd", "After my accident on {{LOCAL_ROAD_SHORT}}")
    t = t.replace("near Guildford", "near {{LOCAL_AREA}}")

    # 5. tokenize the few literal-"Surrey" values inside the _ST translation table -> {city} (runtime localizes)
    out = []
    for line in t.split("\n"):
        if "_ST[" in line and "Surrey" in line:
            line = line.replace("Surrey", "{city}")
        out.append(line)
    t = "\n".join(out)

    # 6b. blanket-replace the remaining city NAME -> {{CITY}}, protecting firm-HQ lines
    PROTECT = ("13737", "Suite 1104", "addressLocality", "V3V 0C6",
               "King George Blvd", "V3W 4Z9", "6832c",
               "output=embed", "maps/dir", "maps/search")
    HQ = ("based in Surrey", "based right here in Surrey", "right here in Surrey", "Based right here in Surrey")
    out2 = []
    for line in t.split("\n"):
        if any(p in line for p in PROTECT) or line.strip() == '"Surrey",':
            out2.append(line); continue
        # preserve HQ "based in Surrey" truth, tokenize the rest of the line
        holders = {}
        for i, h in enumerate(HQ):
            if h in line:
                key = f"\x00HQ{i}\x00"; line = line.replace(h, key); holders[key] = h
        line = line.replace("Serving Surrey", "Serving {{CITY}}")
        line = line.replace("Surrey", "{{CITY}}")
        for key, h in holders.items():
            line = line.replace(key, h)
        out2.append(line)
    t = "\n".join(out2)

    # 6. nearby-city link lists -> tokens (generated per city, excluding self)
    t = re.sub(r'(?:\s*<a href="https://sidhulegal\.com/[a-z-]+-personal-injury-lawyer/" class="serve-link">[^<]+</a>)+',
               '\n      {{SERVE_LINKS}}', t, count=1)
    t = re.sub(r'(?:\s*<a href="https://sidhulegal\.com/[a-z-]+-personal-injury-lawyer/"[^>]*>Personal Injury Lawyer [^<]+</a>)+',
               '\n        {{NETWORK_LINKS}}', t, count=1)

    open(TPL, "w", encoding="utf-8").write(t)
    leftover = t.count("Surrey")
    print(f"template.html written. tokens present:",
          all(tok in t for tok in ["{{CITY}}","{{SLUG}}","{{META_DESC}}","{{LOCAL_ROADS}}","{{SERVE_LINKS}}","{{NETWORK_LINKS}}"]))
    print(f"residual 'Surrey' occurrences in template (should be only firm address/HQ): {leftover}")
    for i,l in enumerate(t.split('\n'),1):
        if 'Surrey' in l:
            print(f"   L{i}: {l.strip()[:90]}")


def serve_links(slug):
    return "\n      ".join(
        f'<a href="https://sidhulegal.com/{s}-personal-injury-lawyer/" class="serve-link">{n}</a>'
        for n, s, _ in CITIES_INDEX if s != slug)

def network_links(slug):
    return "\n        ".join(
        f'<a href="https://sidhulegal.com/{s}-personal-injury-lawyer/" style="color:rgba(255,255,255,0.55);text-decoration:none;font-size:0.8rem">Personal Injury Lawyer {n}</a>'
        for n, s, _ in CITIES_INDEX if s != slug)


def generate(slug, dry=True):
    c = CITIES[slug]
    _bd = os.path.dirname(os.path.abspath(__file__))
    hero = json.load(open(os.path.join(_bd, "hero.json"), encoding="utf-8"))
    testi = json.load(open(os.path.join(_bd, "testimonials.json"), encoding="utf-8"))
    hkey = c["dir"].replace("sidhulegal-", "")  # json keyed by dir suffix (mapleridge, newwestminster)
    h = hero[hkey]
    t = open(TPL, encoding="utf-8").read()
    jsesc = lambda s: s.replace("\\", "\\\\").replace("'", "\\'")
    # JS-escaped variants first (their token names are supersets, so order matters)
    js_repl = {
        "{{LOCAL_INTRO_JS}}": jsesc(c["local_intro"]),
        "{{LOCAL_ROADS_JS}}": jsesc(c["local_roads"]),
        "{{LOCAL_HOSPITAL_JS}}": jsesc(c["local_hospital"]),
    }
    repl = {
        "{{CITY}}": c["name"], "{{SLUG}}": c["slug"],
        "{{META_DESC}}": c["meta_desc"], "{{OG_DESC}}": c["og_desc"],
        "{{LOCAL_INTRO}}": c["local_intro"], "{{LOCAL_ROADS}}": c["local_roads"],
        "{{LOCAL_HOSPITAL}}": c["local_hospital"],
        "{{LOCAL_ROAD_SHORT}}": c["local_road_short"], "{{LOCAL_AREA}}": c["local_area"],
        "{{HERO_SUB}}": h["hero_sub"], "{{HERO_IMG}}": h["hero_img"],
        "{{TESTIMONIALS}}": testi[hkey],
        "{{SERVE_LINKS}}": serve_links(slug), "{{NETWORK_LINKS}}": network_links(slug),
    }
    for k, v in {**js_repl, **repl}.items():
        t = t.replace(k, v)
    assert "{{" not in t, "unfilled token remains: " + t[t.find("{{"):t.find("{{")+40]
    dest = os.path.join(ROOT, c["dir"], "index.new.html" if dry else "index.html")
    open(dest, "w", encoding="utf-8").write(t)
    print(f"generated -> {dest}")
    return dest


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "template"
    if cmd == "template":
        make_template()
    elif cmd == "gen":
        generate(sys.argv[2], dry=(len(sys.argv) < 4 or sys.argv[3] != "live"))
