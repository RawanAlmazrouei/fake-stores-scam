import re, io, csv
from urllib.parse import urlparse
from datetime import datetime
import streamlit as st

st.set_page_config(page_title="FAKESTORE | Trust Intelligence", page_icon="🛍️", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');
:root{--ink:#17233b;--muted:#68758d;--line:#e4e9f2;--paper:#f5f7fb;--teal:#087f78;--orange:#f29b38}
.stApp{background:radial-gradient(ellipse at 4% 0%,#d4f4ed 0,transparent 27%),radial-gradient(ellipse at 96% 10%,#dce8ff 0,transparent 26%),linear-gradient(135deg,#f8faff,#edf2f8 58%,#f4f8fb);color:var(--ink);font-family:'DM Sans',sans-serif}
.block-container{max-width:1240px;padding-top:1.5rem}
h1,h2,h3{font-family:'Space Grotesk',sans-serif;letter-spacing:-.03em}
.hero{background:linear-gradient(115deg,#101d38 0%,#173e56 52%,#087f78 100%);border:1px solid #3b7580;border-radius:28px;padding:34px 38px;color:white;position:relative;overflow:hidden;box-shadow:0 24px 65px #18354a35,inset 0 1px 0 #ffffff25}
.hero:after{content:"";position:absolute;width:280px;height:280px;border:1px solid #ffffff30;border-radius:50%;right:6%;top:-145px;box-shadow:0 0 0 30px #ffffff0d,0 0 0 65px #ffffff09}
.eyebrow{font-size:11px;letter-spacing:.18em;font-weight:800;color:#9ce9d9}
.hero h1{font-size:38px;margin:8px 0 4px;color:#fff}
.hero p{color:#d9f0ed;max-width:680px;margin:0}
.pill{display:inline-block;border:1px solid #ffffff4a;border-radius:30px;padding:6px 11px;margin:15px 7px 0 0;font-size:10px;font-weight:800;letter-spacing:.08em;color:#e5fffa}
.panel{background:linear-gradient(145deg,#ffffff,#f8fbff);border:1px solid #dce5f0;border-radius:21px;padding:22px;box-shadow:0 13px 35px #19365312,inset 0 1px 0 #fff}
.metric{background:linear-gradient(145deg,#fff,#eef8f7);border:1px solid #d7e7e8;border-radius:19px;padding:19px;box-shadow:0 10px 25px #1936530c}
.metric .num{font-family:'Space Grotesk';font-size:27px;font-weight:700;color:#123e4c}
.metric .cap{font-size:11px;color:var(--muted);font-weight:700;text-transform:uppercase;letter-spacing:.08em}
.smallmuted{font-size:12px;color:var(--muted)}
.sectiontag{font-size:11px;font-weight:800;color:#087f78;letter-spacing:.13em;text-transform:uppercase}
.stButton>button{border-radius:13px;border:0;background:linear-gradient(100deg,#087f78,#22a99a);color:white;font-weight:800;min-height:48px;box-shadow:0 8px 18px #087f7825}
.stButton>button:hover{background:linear-gradient(100deg,#066b66,#15998d);color:white}
div[data-baseweb="input"]>div,div[data-baseweb="textarea"]>div,div[data-baseweb="select"]>div{border-radius:11px}
div[data-testid="stMetric"]{background:#f7fafc;border:1px solid var(--line);padding:13px;border-radius:14px}
hr{border-color:var(--line)}
footer{visibility:hidden}
</style>
""", unsafe_allow_html=True)

if "history" not in st.session_state: st.session_state.history=[]
if "page" not in st.session_state: st.session_state.page="Store audit"

with st.sidebar:
    st.markdown("## 🛍️ **FAKESTORE**")
    st.caption("STORE TRUST LAB  /  COMPETITION MVP")
    st.markdown("---")
    page=st.radio("WORKSPACE",["Overview","Store audit","Store checklist","Compare stores","Scam patterns"],index=["Overview","Store audit","Store checklist","Compare stores","Scam patterns"].index(st.session_state.page))
    st.session_state.page=page
    st.markdown("---")
    st.markdown("**LIVE WORKSPACE**")
    st.success("Analysis engine ready")
    st.caption(f"Audits this session: {len(st.session_state.history)}")
    st.caption("No website is opened automatically.")
    st.markdown("---")
    st.caption("FAKESTORE DETECTOR • Prototype")

st.markdown("""
<div class="hero">
 <div class="eyebrow">DIGITAL COMMERCE • TRUST & SAFETY</div>
 <h1>Fake Store Detector</h1>
 <p>Spot warning signs before you shop. Review a store’s web address, policies, contact details and payment signals in one clear trust audit.</p>
 <span class="pill">URL SIGNALS</span><span class="pill">POLICY CHECK</span><span class="pill">PAYMENT SAFETY</span><span class="pill">BILINGUAL GUIDANCE</span>
</div>
""",unsafe_allow_html=True)
st.markdown('<div style="display:flex;gap:8px;flex-wrap:wrap;margin:0 0 14px"><span style="background:#e2f7f1;color:#087f78;padding:6px 11px;border-radius:30px;font-size:10px;font-weight:800">● PROTOTYPE ENGINE READY</span><span style="background:#e9efff;color:#405eaa;padding:6px 11px;border-radius:30px;font-size:10px;font-weight:800">8-POINT STORE REVIEW</span><span style="background:#fff2df;color:#9a6217;padding:6px 11px;border-radius:30px;font-size:10px;font-weight:800">SHOPPER-FIRST DESIGN</span></div>',unsafe_allow_html=True)
st.write("")

def url_signals(url):
    findings=[]
    raw=url.strip()
    if not raw.startswith(("http://","https://")): raw="https://"+raw
    try:
        p=urlparse(raw); host=p.netloc.lower().split(':')[0]; path=p.path
    except: return raw,[], "Invalid"
    if p.scheme!="https": findings.append(("High","Website does not use HTTPS","The connection may not be encrypted."))
    else: findings.append(("Good","HTTPS is present","This is a positive signal, but HTTPS does not prove a store is legitimate."))
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$",host): findings.append(("High","URL uses an IP address","Retail stores normally use a recognizable domain."))
    if len(host)>32: findings.append(("Medium","Unusually long domain name","Long domains can make brand impersonation harder to notice."))
    if host.count('-')>=3: findings.append(("Medium","Several hyphens in the domain","Check the spelling carefully for imitation names."))
    if any(x in host for x in ["secure-","verify-","account-","official-"]): findings.append(("Medium","Trust-related words in domain","These words can be used to make an unfamiliar domain look official."))
    if len(host.split('.'))>=4: findings.append(("Medium","Many domain levels","Extra subdomains can make a URL harder to read."))
    if any(x in raw.lower() for x in ["login","verify","wallet","gift","claim","promo","discount"]): findings.append(("Medium","Sensitive or promotional URL wording","Check whether the link is expected and belongs to the real store."))
    if not findings: findings.append(("Good","No obvious URL pattern warning","A clean-looking URL is not proof of safety."))
    return raw,findings,host

def evaluate(data):
    findings=[]
    url,uf,host=url_signals(data["url"])
    findings.extend(uf)
    checks=[
      ("Store has a clear physical/business address",data["address"],"Missing or unclear business address"),
      ("Working customer support details are shown",data["contact"],"No clear customer support details"),
      ("Returns/refunds policy is available",data["returns"],"Returns or refund policy is missing"),
      ("Privacy and terms pages are available",data["legal"],"Legal or privacy information is missing"),
      ("Payment methods look familiar and protected",data["payment"],"Payment options may be risky or unclear"),
      ("Prices look realistic compared with known retailers",data["prices"],"Prices seem unusually low or unrealistic"),
      ("Independent reviews can be found",data["reviews"],"No independent reviews were found"),
      ("Store identity and spelling are consistent",data["identity"],"Store identity or branding seems inconsistent"),
    ]
    for label,ok,bad in checks:
        findings.append(("Good" if ok else "Medium",label if ok else bad,"User-reported checklist signal. Not independently verified."))
    high=sum(1 for a,_,_ in findings if a=="High")
    med=sum(1 for a,_,_ in findings if a=="Medium")
    score=min(100,high*24+med*9)
    level="Higher concern" if score>=55 else "Review carefully" if score>=25 else "Fewer warning signs"
    return url,host,findings,score,level

def show_result(result,store):
    url,host,findings,score,level=result
    st.markdown("### Trust audit result")
    c1,c2,c3=st.columns(3)
    c1.metric("Warning indicator score",f"{score}/100")
    c2.metric("Assessment",level)
    c3.metric("Signals reviewed",len(findings))
    st.progress(score/100)
    if score>=55: st.error("Several warning signs were selected or detected. Avoid entering payment details until you verify the store independently.")
    elif score>=25: st.warning("Some details need checking. Do not rely on this result alone.")
    else: st.success("Fewer warning signs were found in this prototype check. This does not mean the store is verified or guaranteed safe.")
    st.markdown("#### What we noticed")
    for severity,title,desc in findings:
        icon="🔴" if severity=="High" else "🟠" if severity=="Medium" else "🟢"
        st.markdown(f"{icon} **{title}**  \n<small style='color:#68758d'>{desc}</small>",unsafe_allow_html=True)
    report=[f"FAKESTORE DETECTOR — STORE AUDIT",f"Store: {store or 'Not provided'}",f"URL: {url}",f"Domain: {host}",f"Indicator score: {score}/100",f"Assessment: {level}",f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", "", "Findings:"]+[f"- [{s}] {t}: {d}" for s,t,d in findings]+["","Prototype only: signals are heuristic and user-reported. No live domain, company, payment or review verification was performed."]
    st.download_button("⬇ Download audit report (.txt)","\n".join(report),file_name="fakestore_audit_report.txt",mime="text/plain")
    st.caption("The score is a warning indicator, not a probability of fraud and not a certification.")

if page=="Overview":
    st.markdown('<div class="sectiontag">COMMAND CENTER</div>',unsafe_allow_html=True)
    st.title("Store safety overview")
    st.markdown("""
    <div style="background:linear-gradient(105deg,#ffffff,#eef8f8);border:1px solid #d9e8ed;border-radius:18px;padding:17px 21px;margin:12px 0 20px;display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap">
      <div><div style="font-size:10px;letter-spacing:2px;color:#087f78;font-weight:800">TRUST INTELLIGENCE WORKSPACE</div>
      <div style="font-size:21px;font-weight:800;color:#17233b;margin-top:5px">A smarter way to shop online.</div>
      <div style="font-size:12px;color:#68758d;margin-top:3px">Inspect • Compare • Learn • Make informed decisions</div></div>
      <div style="align-self:center;font-size:42px">🛍️　🔐　✨</div>
    </div>
    """,unsafe_allow_html=True)
    a,b,c,d=st.columns(4)
    for col,num,cap in [(a,"01","URL review"),(b,"08","Store checks"),(c,"05","Workspace tools"),(d,str(len(st.session_state.history)),"Session audits")]:
        with col: st.markdown(f'<div class="metric"><div class="num">{num}</div><div class="cap">{cap}</div></div>',unsafe_allow_html=True)
    st.write("")
    st.markdown("#### ✦ Explore the trust toolkit")
    features = st.columns(4)
    feature_data = [("🔎","Deep store audit","URL + 8 shopper checks"),("📋","Smart checklist","Track what you verified"),("⚖️","Store comparison","Review two domains"),("🧠","Scam pattern library","Learn common tricks")]
    for col,(ic,title,desc) in zip(features,feature_data):
        with col:
            st.markdown(f'<div class="metric" style="min-height:118px"><div style="font-size:25px">{ic}</div><div style="font-weight:800;margin-top:8px">{title}</div><div class="smallmuted">{desc}</div></div>',unsafe_allow_html=True)
    st.write("")
    left,right=st.columns([1.2,1])
    with left:
        st.markdown('<div class="panel"><div class="sectiontag">HOW IT WORKS</div><h3>One audit, multiple signals</h3><p class="smallmuted">Review the URL structure, then answer a practical checklist about the store’s policies, contact information and checkout experience.</p><b>01 — Inspect the address</b><br><span class="smallmuted">Look for misspellings, unusual domain structures and connection signals.</span><br><br><b>02 — Review store details</b><br><span class="smallmuted">Check policies, contact information, payment options and independent reputation.</span><br><br><b>03 — Export your findings</b><br><span class="smallmuted">Create a simple report to support a safer decision.</span></div>',unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel"><div class="sectiontag">SAFETY FIRST</div><h3>Before you pay</h3><ul><li>Search the store name with words like “scam” or “reviews”.</li><li>Compare the domain with the brand’s official website.</li><li>Avoid bank transfers to unknown sellers.</li><li>Never share OTPs or full card details.</li><li>Remember: HTTPS alone does not mean a store is genuine.</li></ul></div>',unsafe_allow_html=True)
    st.info("This is a competition prototype. It does not connect to live WHOIS, company registries, payment processors or review platforms.")
elif page=="Store audit":
    st.markdown('<div class="sectiontag">01 / STORE AUDIT</div>',unsafe_allow_html=True)
    st.title("Inspect an online store")
    st.write("Enter the store address and answer what you can observe. You do not need to visit a suspicious link to use this form.")
    with st.form("audit"):
        url=st.text_input("Store website URL *",placeholder="https://shop-example.com")
        name=st.text_input("Store name (optional)",placeholder="Example Fashion")
        st.markdown("#### Store information checklist")
        st.caption("Tick only what you have personally confirmed on the store’s website or through trusted sources.")
        c1,c2=st.columns(2)
        with c1:
            address=st.checkbox("Clear business address is shown")
            returns=st.checkbox("Returns and refund policy is available")
            payment=st.checkbox("Familiar, protected payment methods are offered")
            reviews=st.checkbox("Independent reviews can be found")
        with c2:
            contact=st.checkbox("Working customer support details are shown")
            legal=st.checkbox("Privacy policy and terms are available")
            prices=st.checkbox("Prices look realistic")
            identity=st.checkbox("Brand name, domain and identity are consistent")
        submitted=st.form_submit_button("Run store trust audit →",use_container_width=True)
    if submitted:
        if not url.strip(): st.error("Please enter a store URL.")
        else:
            data=dict(url=url,address=address,returns=returns,payment=payment,reviews=reviews,contact=contact,legal=legal,prices=prices,identity=identity)
            result=evaluate(data)
            st.session_state.last=(result,name)
            st.session_state.history.append({"store":name or url,"score":result[3],"assessment":result[4]})
    if "last" in st.session_state:
        st.divider()
        show_result(st.session_state.last[0],st.session_state.last[1])
elif page=="Store checklist":
    st.markdown('<div class="sectiontag">02 / SHOPPER TOOLKIT</div>',unsafe_allow_html=True)
    st.title("Store verification checklist")
    st.write("Use this before ordering from an unfamiliar online store.")
    items=["I checked the exact spelling of the website domain.","I found the store through an independent search, not only an ad or message.","I found a real business address and working contact details.","I read the delivery, return and refund policy.","I checked independent customer reviews outside the store website.","The price is plausible compared with other retailers.","The checkout uses a payment method with buyer protection.","The store does not ask for an OTP, password or unnecessary personal information."]
    done=0
    for item in items:
        if st.checkbox(item,key="ck_"+str(items.index(item))): done+=1
    st.progress(done/len(items))
    st.metric("Checklist completed",f"{done} / {len(items)}")
    if done==len(items): st.success("Great — you completed the checklist. Still verify the seller independently.")
    else: st.info("Unanswered items are reminders to investigate, not proof that a store is fraudulent.")
elif page=="Compare stores":
    st.markdown('<div class="sectiontag">03 / SIDE-BY-SIDE</div>',unsafe_allow_html=True)
    st.title("Compare store warning signals")
    st.write("Enter two URLs and compare basic URL patterns. This quick comparison does not verify either business.")
    x,y=st.columns(2)
    with x: u1=st.text_input("Store A URL",placeholder="https://store-a.example")
    with y: u2=st.text_input("Store B URL",placeholder="https://store-b.example")
    if st.button("Compare URL signals",use_container_width=True):
        if not u1 or not u2: st.error("Enter both URLs to compare.")
        else:
            for label,u in [("Store A",u1),("Store B",u2)]:
                norm,finds,host=url_signals(u)
                st.markdown(f"### {label} · `{host}`")
                for sev,title,desc in finds:
                    st.write(("🟢" if sev=="Good" else "🟠" if sev=="Medium" else "🔴")+" "+title)
            st.caption("Compare findings as prompts for further research, not as a winner/loser safety verdict.")
elif page=="Scam patterns":
    st.markdown('<div class="sectiontag">04 / LEARN & RECOGNIZE</div>',unsafe_allow_html=True)
    st.title("Common fake-store patterns")
    patterns=[
      ("🏷️ Unrealistic discounts","A high-value product is offered at a price far below reputable retailers. Compare prices and check whether the promotion is genuine."),
      ("🧾 Missing business details","No usable address, phone number, company identity or clear support channel. Look for independently verifiable information."),
      ("💳 Risky payment requests","The seller insists on bank transfer, cryptocurrency, gift cards or payment outside a protected checkout."),
      ("🔤 Lookalike domains","The web address imitates a known brand using extra words, misspellings, hyphens or unusual domain endings."),
      ("📦 Unclear returns and delivery","Policies are missing, copied, contradictory or do not explain how to contact the seller."),
      ("⭐ Only perfect on-site reviews","All reviews appear generic or overly positive. Search for independent reviews from multiple sources.")
    ]
    cols=st.columns(2)
    for i,(title,desc) in enumerate(patterns):
        with cols[i%2]:
            st.markdown(f'<div class="panel" style="margin-bottom:14px;min-height:150px"><h3>{title}</h3><p class="smallmuted">{desc}</p></div>',unsafe_allow_html=True)
    st.warning("A single signal does not prove fraud. Combine independent checks and use trusted consumer-protection sources.")
