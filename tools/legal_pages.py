# -*- coding: utf-8 -*-
"""
Builds the legal pages Stripe asks for: support, privacy, terms, refund-policy.
UK English, UK GDPR. Real data only: QUILLSTONE DIGITAL LLC (Wyoming),
1057 NW 136th Ave, Miami, FL 33182; brand Physics Study Lab; payments by Stripe
through the checkout at physics-study-lab.impultienda.ar; Meta Pixel on the site;
hosting on Vercel.

  python tools/legal_pages.py
"""
import io
import os
import json

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EMAIL = "info@physicsstudylab.com"
UPDATED = "17 September 2026"
CO = "QUILLSTONE DIGITAL LLC"
ADDR = "1057 NW 136th Ave, Miami, FL 33182, United States"
DESCRIPTOR = "PHYSICSSTUDYLAB"

CSS = """
:root{--primary:#2645a0;--primary-dark:#1c3479;--light:#f4f7fd;--text:#101828;--muted:#475467;--border:#e4e7ec}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;color:var(--text);background:var(--light);line-height:1.7;-webkit-font-smoothing:antialiased}
header{background:#fff;border-bottom:1px solid var(--border);padding:18px 20px;position:sticky;top:0}
.hc{max-width:800px;margin:0 auto;display:flex;justify-content:space-between;align-items:center;gap:12px}
.logo{font-weight:800;font-size:1.15rem;color:var(--primary);text-decoration:none}
.back{font-size:.9rem;font-weight:600;color:var(--primary);text-decoration:none}
main{max-width:800px;margin:32px auto;padding:0 16px}
.card{background:#fff;border:1px solid var(--border);border-radius:16px;padding:40px 36px}
h1{font-size:2rem;line-height:1.2;color:var(--primary-dark);margin-bottom:8px}
.upd{display:block;font-size:.85rem;color:var(--muted);border-bottom:1px solid var(--border);padding-bottom:16px;margin-bottom:24px}
h2{font-size:1.2rem;color:var(--primary-dark);margin:28px 0 10px}
p,ul,ol{margin-bottom:14px;color:#344054}
ul,ol{padding-left:22px}
li{margin-bottom:6px}
a{color:var(--primary)}
.box{background:var(--light);border-radius:12px;padding:22px;text-align:center;margin:24px 0}
.box a{font-weight:700;font-size:1.1rem;word-break:break-all}
footer{text-align:center;padding:28px 16px;color:var(--muted);font-size:.85rem}
footer a{color:inherit}
@media(max-width:600px){.card{padding:26px 20px}h1{font-size:1.6rem}}
"""

NAV = ('<a href="/">Home</a> · <a href="/support">Support</a> · <a href="/refund-policy">Refund Policy</a> · '
       '<a href="/privacy">Privacy</a> · <a href="/terms">Terms</a>')

PAGES = {
    "support": ("Customer Support", f"""
<p>Questions about an order, didn't get your download email, or want a refund? Email us and we'll reply within <strong>1–2 business days</strong>.</p>
<div class="box"><p style="margin-bottom:8px">Email us, with the address you used to buy and your order number if you have it:</p><a href="mailto:{EMAIL}">{EMAIL}</a></div>
<h2>Common questions</h2>
<p><strong>I didn't receive my download email.</strong><br>Check your spam or promotions folder. If it isn't there, email us from the address you used to buy and we'll resend it.</p>
<p><strong>I don't recognise a charge on my statement.</strong><br>Purchases on this site appear as <strong>{DESCRIPTOR}</strong>. If you don't recognise a charge, please contact us before your bank and we'll look into it straight away.</p>
<p><strong>I want a refund.</strong><br>You have 30 days from purchase. See our <a href="/refund-policy">Refund Policy</a> or just email us.</p>
<p><strong>Can I download the files more than once?</strong><br>Yes. The PDFs are yours to download, print and read on any device for personal use.</p>
<h2>Who we are</h2>
<p>Physics Study Lab is a brand of <strong>{CO}</strong>, {ADDR}.</p>
"""),
    "refund-policy": ("Refund Policy", f"""
<p>We want you to try Physics Study Lab with no risk.</p>
<h2>1. Digital products</h2>
<p>All our products are digital files (illustrated PDF guides and bonus materials) delivered by email right after payment.</p>
<h2>2. 30-day money-back guarantee</h2>
<p>If the material isn't what you expected or doesn't help you, you can ask for a <strong>full refund within 30 days</strong> of purchase, for any reason. You don't need to return anything.</p>
<h2>3. How to ask for a refund</h2>
<ol><li>Email <a href="mailto:{EMAIL}">{EMAIL}</a> with the subject "Refund request".</li><li>Include the email address you used to buy and your order number.</li></ol>
<p>We process refund requests within <strong>1–2 business days</strong>.</p>
<h2>4. When you'll see the money</h2>
<p>The refund goes back to the same card or payment method you used. It usually shows on your statement within <strong>5–10 business days</strong>, depending on your bank.</p>
<h2>5. Your statutory rights</h2>
<p>This guarantee is in addition to, and does not limit, your rights under the Consumer Rights Act 2015 and other applicable consumer law.</p>
"""),
    "privacy": ("Privacy Policy", f"""
<p>This policy explains what personal data we collect when you visit <strong>physicsstudylab.com</strong> or buy our digital products, why we use it and what rights you have, including under the UK GDPR and the Data Protection Act 2018.</p>
<h2>1. Who we are</h2>
<p><strong>{CO}</strong> (trading as Physics Study Lab), {ADDR}, is the controller of your personal data. Contact: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>2. Data we collect</h2>
<ul><li><strong>Order data:</strong> name, email address, country and purchase details.</li>
<li><strong>Payment data:</strong> handled directly by Stripe. We never see or store your full card number.</li>
<li><strong>Browsing data:</strong> pages visited, device, approximate location from your IP address and how you interact with the site, collected with cookies and similar technologies.</li>
<li><strong>Messages:</strong> anything you send us by email.</li></ul>
<h2>3. How we use it and our legal basis</h2>
<ul><li>To deliver your purchase and provide support (performance of a contract).</li>
<li>To process payments and refunds and prevent fraud (contract and legitimate interests).</li>
<li>To meet tax and accounting obligations (legal obligation).</li>
<li>To measure and improve our website and advertising (consent, where required).</li>
<li>To send you emails about our products, which you can unsubscribe from at any time (legitimate interests or consent).</li></ul>
<h2>4. Who we share it with</h2>
<p>We don't sell your data. We only share it with service providers that help us run the business:</p>
<ul><li><strong>Stripe</strong> — payment processing.</li>
<li><strong>Our checkout provider</strong> — order processing and delivery.</li>
<li><strong>Meta (Facebook/Instagram)</strong> — measuring our advertising through the Meta Pixel.</li>
<li><strong>Vercel</strong> — website hosting.</li></ul>
<p>Some of these providers are in the United States. Transfers are covered by appropriate safeguards such as the UK International Data Transfer Addendum, Standard Contractual Clauses or the UK Extension to the EU-US Data Privacy Framework.</p>
<h2>5. How long we keep it</h2>
<p>Order data is kept for as long as tax and accounting rules require. Browsing and marketing data is kept only as long as needed for those purposes or until you withdraw consent.</p>
<h2>6. Security</h2>
<p>The site uses encrypted connections (HTTPS). Payments are handled by Stripe, which is PCI DSS certified. Access to personal data is limited to the people and providers who need it to provide the service.</p>
<h2>7. Your rights</h2>
<p>You can ask to access, correct, delete or port your data, object to processing, or withdraw consent at any time by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>. You also have the right to complain to the Information Commissioner's Office (ICO) at ico.org.uk.</p>
<h2>8. Children</h2>
<p>If you are under 18, please buy with the involvement of a parent or guardian. We don't knowingly collect data from children without that involvement.</p>
<h2>9. Changes</h2>
<p>We may update this policy. The date at the top shows the latest version.</p>
"""),
    "terms": ("Terms of Service", f"""
<p>These terms apply to your use of <strong>physicsstudylab.com</strong> and your purchase of Physics Study Lab digital products, sold by <strong>{CO}</strong>, {ADDR} ("we", "us"). By buying, you agree to these terms.</p>
<h2>1. Products</h2>
<p>We sell illustrated digital study guides (PDF) for physics students. What each product includes is described on its offer page.</p>
<h2>2. Prices and payment</h2>
<p>Prices are shown on the offer page and at checkout. Payment is one-off, with no subscription or recurring charges, and is processed securely by Stripe. The charge appears on your statement as <strong>{DESCRIPTOR}</strong>.</p>
<h2>3. Delivery</h2>
<p>Products are delivered by email to the address you give at checkout, normally within a few minutes. By buying, you ask us to deliver the digital content immediately.</p>
<h2>4. Refunds</h2>
<p>We offer a <strong>30-day money-back guarantee</strong>, as described in our <a href="/refund-policy">Refund Policy</a>. This does not affect your statutory rights.</p>
<h2>5. Licence</h2>
<p>Your purchase gives you a <strong>personal, non-transferable licence</strong> to download, print and use the materials for your own study. You may not copy, share, resell, upload or use them commercially. All text and illustrations are protected by copyright.</p>
<h2>6. Educational use</h2>
<p>Our materials are study aids. They don't replace your school's or exam board's official materials, and results depend on each student.</p>
<h2>7. Liability</h2>
<p>We take care over our content but can't guarantee it is free of errors. To the extent permitted by law, we are not liable for losses arising from its use. Nothing in these terms limits rights you have as a consumer that cannot be excluded.</p>
<h2>8. Contact</h2>
<p>Questions? Email <a href="mailto:{EMAIL}">{EMAIL}</a> or visit our <a href="/support">Support</a> page.</p>
"""),
}


def page(slug, title, body):
    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — Physics Study Lab</title>
  <meta name="description" content="{title} for Physics Study Lab.">
  <link rel="canonical" href="https://www.physicsstudylab.com/{slug}">
  <meta name="robots" content="index, follow">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
  <style>{CSS}</style>
</head>
<body>
  <header><div class="hc"><a href="/" class="logo">Physics Study Lab</a><a href="/" class="back">← Back to Home</a></div></header>
  <main><div class="card">
    <h1>{title}</h1>
    <span class="upd">Last updated: {UPDATED}</span>
{body}
  </div></main>
  <footer><p>© 2026 Physics Study Lab · {NAV}</p><p style="margin-top:8px;font-size:.75rem;opacity:.7">{CO} · {ADDR}</p></footer>
</body>
</html>
"""


def main():
    for slug, (title, body) in PAGES.items():
        io.open(os.path.join(SITE, f"{slug}.html"), "w", encoding="utf-8", newline="\n").write(page(slug, title, body))
        print(slug)
    idx = os.path.join(SITE, "index.html")
    t = io.open(idx, encoding="utf-8").read()
    s = ' style="color: rgba(255,255,255,0.7); text-decoration: underline; margin-left: 8px;"'
    old = f'<a href="#"{s}>Refund Policy</a>'
    if old in t:
        t = t.replace(old, f'<a href="/refund-policy"{s}>Refund Policy</a><a href="/privacy"{s}>Privacy</a>'
                           f'<a href="/terms"{s}>Terms</a><a href="/support"{s}>Support</a>')
    ph = "[Add your contact details / business registration / address here if required in your jurisdiction.]"
    if ph in t:
        t = t.replace(ph, f"Sold by {CO}, {ADDR}. Support: <a href=\"mailto:{EMAIL}\" style=\"color:inherit\">{EMAIL}</a>")
    io.open(idx, "w", encoding="utf-8", newline="\n").write(t)
    vj = os.path.join(SITE, "vercel.json")
    if not os.path.exists(vj):
        io.open(vj, "w", encoding="utf-8", newline="\n").write(json.dumps({"cleanUrls": True}, indent=2) + "\n")


if __name__ == "__main__":
    main()
