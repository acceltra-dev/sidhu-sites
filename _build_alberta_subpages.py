import os, re, glob, html, datetime

CITIES = {
 'alberta-calgary':      ('Calgary',       '(403) 200-3226', '+14032003226'),
 'alberta-edmonton':     ('Edmonton',      '(780) 886-8077', '+17808868077'),
 'alberta-lethbridge':   ('Lethbridge',    '(403) 888-4321', '+14038884321'),
 'alberta-red-deer':     ('Red Deer',      '(587) 777-6645', '+15877776645'),
 'alberta-sherwood-park':('Sherwood Park', '(587) 888-7654', '+15878887654'),
 'edmonton-deploy':      ('Edmonton',      '(780) 886-8077', '+17808868077'),
}

IMG = ["1449824913935-59a10b8d2000","1502744688674-c619d1586c9e","1568772585407-9361f9bf3a87" if False else "1517935706615-2717063c2225",
 "1508739773434-c26b3d09e071","1521791136064-7986c2920216","1573497491208-6b1acb260507",
 "1497366216548-37526070297c","1556761175-5973dc0f32e7","1559757175-5700dde675bc",
 "1576091160550-2173dba999ef","1581090122319-8fab9528eaaa","1581092160607-ee22621dd758",
 "1586387791290-429b5a2e8e47","1548164927-47eb3eef711c","1558618666-fcd25c85cd64",
 "1567613074247-5e2564e1b90a","1589391886645-d51941baf7fb","1611564494260-6f21b80af7ea",
 "1635713044350-af433eaba5dd","1642350371707-510555b9c478"]

# keyword in title -> (hero one-liner, 4 bullets)  [generic intro/closing built from phrase]
CAT = [
 ('Car Accident', 'car accident', "Hit on Alberta's roads? We deal with the insurer so you can focus on recovery.",
   ["Rear-end, intersection, and highway collision claims","Dealing with at-fault insurers and your own coverage","Compensation for vehicle damage, medical care, and lost wages","Serious and long-term injury claims"]),
 ('Truck', 'truck accident', "Commercial truck crashes are complex and high-stakes. We know how to handle them.",
   ["Claims against trucking companies and their insurers","Preserving black-box and logbook evidence fast","Catastrophic and multi-vehicle collisions","Federal and provincial trucking regulation issues"]),
 ('Motorcycle', 'motorcycle accident', "Riders get blamed unfairly. We fight to protect your side of the story.",
   ["Countering bias against motorcyclists","Severe road-rash, fracture, and head-injury claims","Helmet and right-of-way disputes","Maximizing recovery for long rehabilitation"]),
 ('Bicycle', 'bicycle accident', "Cyclists are vulnerable. We pursue full compensation when a driver is at fault.",
   ["Driver-at-fault and dooring collisions","Serious injury and concussion claims","Bike, gear, and medical cost recovery","Holding insurers accountable"]),
 ('Pedestrian', 'pedestrian accident', "Struck while walking? Pedestrian injuries are often severe, we can help.",
   ["Crosswalk and intersection collisions","Hit-and-run and uninsured driver claims","Serious and catastrophic injury cases","Coverage for long-term care needs"]),
 ('Boat', 'boating accident', "Watercraft and recreational boating injuries on Alberta lakes and rivers.",
   ["Operator negligence and impaired-operation claims","Passenger and water-sport injuries","Equipment failure and rental liability","Wrongful death on the water"]),
 ('Slip and Fall', 'slip and fall', "Property owners must keep premises safe. When they don't, we act.",
   ["Icy walkways, wet floors, and poor maintenance","Store, parking-lot, and stairwell falls","Proving owner negligence","Fractures, head, and back injuries"]),
 ('Recreational', 'recreational injury', "Injured during sport or recreation through someone else's negligence.",
   ["Facility and equipment-failure claims","Ski, gym, and organized-activity injuries","Waiver and liability disputes","Serious injury recovery"]),
 ('Brain', 'brain injury', "Traumatic brain injuries change lives. We pursue the full value of your claim.",
   ["Concussion and TBI claims","Cognitive, memory, and behavioural impacts","Lifetime care and lost-earning capacity","Expert medical and economic evidence"]),
 ('Spine', 'spinal injury', "Spinal and back injuries can mean lasting disability. We fight for what that costs.",
   ["Herniated disc, fracture, and paralysis claims","Chronic pain and mobility loss","Future care and home-modification costs","Long-term disability coordination"]),
 ('Catastrophic', 'catastrophic injury', "Life-altering injuries demand maximum compensation. That's our focus.",
   ["Amputation, paralysis, and severe burns","Lifetime care and rehabilitation costs","Lost future income and earning capacity","Structured settlements done right"]),
 ('Dog Bite', 'dog bite', "Dog owners are responsible for their animals. We recover for bites and scarring.",
   ["Owner-liability dog-attack claims","Scarring, infection, and nerve damage","Child-victim cases","Compensation for physical and emotional harm"]),
 ('Nursing Home', 'nursing home abuse', "When a senior is neglected or abused in care, we hold facilities accountable.",
   ["Neglect, bedsores, and malnutrition","Physical and financial abuse","Inadequate supervision and staffing","Protecting vulnerable family members"]),
 ('Personal Injury Claims', 'personal injury claim', "The full range of injury claims, handled start to finish.",
   ["Free claim assessment","Dealing with all insurers on your behalf","Medical, wage, and pain-and-suffering recovery","No fee unless we win"]),
 ('Insurance Claims', 'insurance claim', "Insurers protect their bottom line. We make sure you're treated fairly.",
   ["Denied and lowballed claim disputes","Bad-faith insurer conduct","First-party benefit claims","Negotiation and litigation"]),
 ('Tort', 'tort claim', "Tort claims pursue the at-fault party beyond standard benefits.",
   ["Establishing fault and liability","Recovering damages above no-fault benefits","Serious-injury thresholds","Court-ready case building"]),
 ('Special Damages', 'special damages', "Every out-of-pocket cost from your injury should be recovered.",
   ["Medical, prescription, and therapy receipts","Travel and home-care costs","Documenting and proving expenses","Maximizing your reimbursement"]),
 ('Contributory Negligence', 'contributory negligence', "Partly at fault? You may still be owed significant compensation.",
   ["Reducing unfair fault allegations","Apportionment and shared-liability claims","Protecting your percentage of recovery","Strong evidence and argument"]),
 ('DUI', 'impaired driving crash', "Hit by an impaired driver? We pursue every avenue of recovery.",
   ["Claims against impaired and criminal drivers","Uninsured and underinsured coverage","Coordinating with criminal proceedings","Serious and fatal collision claims"]),
 ('Wrongful Death', 'wrongful death', "Losing a loved one to negligence is devastating. We handle the claim with care.",
   ["Fatal-accident and dependency claims","Loss of income, care, and companionship","Funeral and estate-related costs","Compassionate, respectful representation"]),
]

def cat_for(title):
    t=html.unescape(title)
    for kw,*rest in CAT:
        if kw.lower() in t.lower():
            return rest  # (phrase, sub, bullets)
    # fallback
    return ('injury', "We help injured Albertans recover what they're owed.",
            ["Free case review","No fee unless we win","Medical and wage-loss recovery","Local Alberta representation"])

def img_for(idx): return IMG[idx % len(IMG)]

TPL = open('_alberta_subpage_template.html', encoding='utf-8').read()

def slugify(t):
    t=html.unescape(t).lower().replace('&',' ')
    return re.sub(r'[^a-z0-9]+','-',t).strip('-')

def slugs_from_backup(d):
    bak=sorted(glob.glob(f'{d}/index.html.bak_caseslink_*'))[-1]
    h=open(bak,encoding='utf-8').read()
    m=re.search(r'<div class="cases-grid">(.*?)</div>', h, re.S)
    pairs=[]
    for href,title in re.findall(r'<a href="([^"]*)">([^<]*)</a>', m.group(1)):
        slug = href.strip('/') if (href.startswith('/') and len(href)>2) else slugify(title)
        pairs.append((slug,title))
    return pairs

made=0
for d,(city,phone,tel) in CITIES.items():
    pairs=slugs_from_backup(d)
    # build sibling chip list (relative ../slug/)
    for i,(slug,title) in enumerate(pairs):
        phrase,sub,bullets=cat_for(title)
        others=''.join(f'<a href="../{o}/">{ot}</a>' for o,ot in pairs if o!=slug)
        intro=(f"If you or a loved one suffered a {phrase} in {city}, you may be owed compensation for medical costs, "
               f"lost income, and pain and suffering. Alberta Accident Law has recovered millions for injured Albertans, "
               f"and we work on contingency, so you pay nothing unless we win.")
        closing=(f"Every {phrase} claim is different. Get a free, confidential review of your case in {city}, "
                 f"no obligation and no upfront cost.")
        bl=''.join(f'<li>{b}</li>' for b in bullets)
        page=(TPL.replace('{{TITLE}}',title).replace('{{CITY}}',city).replace('{{PHONE}}',phone)
              .replace('{{TEL}}',tel).replace('{{IMAGE}}','https://images.unsplash.com/photo-'+img_for(i))
              .replace('{{SUB}}',sub).replace('{{H2}}',title).replace('{{INTRO}}',intro)
              .replace('{{BULLETS}}',bl).replace('{{CLOSING}}',closing).replace('{{OTHERS}}',others)
              .replace('{{META}}',f"{title} - free case review, no fee unless we win. Serving {city}, Alberta."))
        os.makedirs(f'{d}/{slug}', exist_ok=True)
        open(f'{d}/{slug}/index.html','w',encoding='utf-8').write(page)
        made+=1
    # relink main page cases-grid -> relative subpage paths
    p=f'{d}/index.html'; h=open(p,encoding='utf-8').read()
    newgrid='<div class="cases-grid">\n'+''.join(
        f'      <a href="{slug}/">{title}</a>\n' for slug,title in pairs)+'    </div>'
    h=re.sub(r'<div class="cases-grid">.*?</div>', newgrid, h, count=1, flags=re.S)
    open(p,'w',encoding='utf-8').write(h)
print(f"generated {made} subpages across {len(CITIES)} cities; main pages relinked")
