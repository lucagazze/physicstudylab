# -*- coding: utf-8 -*-
"""
Physics Solved -- illustrated cover, built to the family template.

Measured off img/beyondsyllabus/cover-beyondsyllabus.png: cream page inside a
navy frame, PHYSICS STUDY LAB pill at the top, a gold ribbon badge, a two-line
title in navy and gold, the mascot centred on a soft colour blob with icons on
a dashed ring around it, topic chips along the bottom, and a white brand pill.
"""
import pathlib, subprocess
ROOT = pathlib.Path(__file__).resolve().parent
IMG = ROOT.parent.parent / "img"
CH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

NAVY, GOLD, CREAM = "#17244A", "#C9A24B", "#FAF5E4"

def icon(d, extra=""):
    return (f'<svg viewBox="0 0 48 48" fill="none" stroke="{NAVY}" stroke-width="2.4" '
            f'stroke-linecap="round" stroke-linejoin="round">{d}{extra}</svg>')

ICONS = [
    # a question mark on a sheet -- the problem page
    icon('<rect x="11" y="7" width="26" height="34" rx="3"/>'
         '<path d="M19 20c0-3 2-5 5-5s5 2 5 4.5-2 3-3.5 4.3S24 26 24 28"/><circle cx="24" cy="33" r="1.5" fill="'+NAVY+'"/>'),
    # numbered steps -- the solution
    icon('<circle cx="13" cy="14" r="3.2"/><line x1="21" y1="14" x2="38" y2="14"/>'
         '<circle cx="13" cy="24" r="3.2"/><line x1="21" y1="24" x2="38" y2="24"/>'
         '<circle cx="13" cy="34" r="3.2"/><line x1="21" y1="34" x2="38" y2="34"/>'),
    # the trap
    icon('<path d="M24 9 42 38H6Z"/><line x1="24" y1="20" x2="24" y2="28"/>'
         '<circle cx="24" cy="33" r="1.4" fill="'+NAVY+'"/>'),
    # a boxed answer
    icon('<rect x="7" y="14" width="34" height="20" rx="3"/><path d="M16 24.5 21.5 30 33 18.5"/>'),
    # five minutes before you turn the page
    icon('<circle cx="24" cy="24" r="16"/><path d="M24 14v10l7 4"/>'),
    # the maths behind it
    icon('<rect x="9" y="7" width="30" height="34" rx="3"/><line x1="15" y1="16" x2="33" y2="16"/>'
         '<line x1="16" y1="25" x2="22" y2="25"/><line x1="19" y1="22" x2="19" y2="28"/>'
         '<line x1="27" y1="25" x2="33" y2="25"/><line x1="16" y1="33" x2="22" y2="33"/>'
         '<line x1="27" y1="31" x2="33" y2="31"/><line x1="27" y1="35" x2="33" y2="35"/>'),
]
# positions on the ring, as percentages of the stage
POS = [(9, 12), (74, 6), (1, 44), (82, 40), (13, 74), (72, 72)]

bubbles = "".join(
    f'<div class="cv-bub" style="left:{x}%;top:{y}%">{ic}</div>' for ic, (x, y) in zip(ICONS, POS))

CHIPS = [("GCSE", "#17244A", "#fff"), ("A-LEVEL", "#9FC0E8", "#17244A"),
         ("50 PROBLEMS", "#C9A24B", "#2B2206"), ("STEP BY STEP", "#17244A", "#fff")]
chips = "".join(f'<span style="background:{b};color:{c}">{t}</span>' for t, b, c in CHIPS)

COVER_CSS = f"""
@page{{ size:210mm 297mm; margin:0 }}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:"Avenir Next","Avenir",sans-serif}}
.cv-page{{width:210mm;height:297mm;background:{NAVY};padding:5.5mm;position:relative}}
.cv-inner{{width:100%;height:100%;background:{CREAM};border-radius:4mm;position:relative;
  padding:11mm 10mm 9mm;display:flex;flex-direction:column;align-items:center;overflow:hidden}}
.cv-brand{{background:{NAVY};color:#fff;font-size:13pt;font-weight:800;letter-spacing:.22em;
  padding:2.6mm 9mm;border-radius:2.4mm}}
.cv-ribbon{{margin-top:5mm;background:{GOLD};color:#2B2206;font-size:11.5pt;font-weight:800;
  letter-spacing:.16em;padding:2mm 8mm;position:relative}}
.cv-ribbon::before,.cv-ribbon::after{{content:"";position:absolute;top:0;bottom:0;width:4mm;background:{GOLD}}}
.cv-ribbon::before{{left:-4mm;clip-path:polygon(0 0,100% 0,100% 100%,0 100%,38% 50%)}}
.cv-ribbon::after{{right:-4mm;clip-path:polygon(0 0,100% 0,62% 50%,100% 100%,0 100%)}}
.cv-page h1{{margin-top:6mm;font-size:62pt;font-weight:800;line-height:.96;color:{NAVY};
  letter-spacing:-.015em;text-align:center}}
.cv-page h1 em{{display:block;color:{GOLD};font-style:normal}}
.cv-sub{{margin-top:5mm;font-size:17pt;font-weight:600;color:#36405E;text-align:center}}
.cv-stage{{flex:1;width:100%;position:relative;margin-top:3mm}}
.cv-ring{{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);
  width:150mm;height:118mm;border:.7mm dashed rgba(23,36,74,.33);border-radius:50%}}
.cv-blob{{position:absolute;left:50%;top:52%;transform:translate(-50%,-50%);width:92mm;height:92mm;
  border-radius:50%;background:radial-gradient(circle at 38% 34%,rgba(159,192,232,.55),
  rgba(201,162,75,.34) 62%,rgba(250,245,228,0) 76%)}}
.cv-mascot{{position:absolute;left:50%;bottom:2%;transform:translateX(-50%);height:80%;}}
.cv-bub{{position:absolute;width:26mm;height:26mm;border-radius:50%;background:#fff;
  border:.6mm solid rgba(23,36,74,.18);box-shadow:0 2mm 5mm rgba(23,36,74,.14);
  display:flex;align-items:center;justify-content:center}}
.cv-bub svg{{width:14mm;height:14mm}}
.cv-chips{{display:flex;gap:2.4mm;justify-content:center;flex-wrap:wrap;margin-top:4mm;position:relative;z-index:2}}
.cv-chips span{{font-size:10.5pt;font-weight:800;letter-spacing:.06em;padding:2.4mm 5mm;border-radius:99mm}}
.cv-base{{margin-top:5mm;background:#fff;color:{NAVY};font-size:13pt;font-weight:700;
  padding:2.6mm 11mm;border-radius:99mm;box-shadow:0 1mm 3mm rgba(23,36,74,.12)}}
"""

COVER_BODY = f"""<div class="cv-page"><div class="cv-inner">
  <div class="cv-brand">PHYSICS STUDY LAB</div>
  <div class="cv-ribbon">PRACTICE</div>
  <h1>Physics<em>Solved</em></h1>
  <div class="cv-sub">50 exam problems, worked step by step</div>
  <div class="cv-stage">
    <div class="cv-ring"></div><div class="cv-blob"></div>
    <img class="cv-mascot" src="{(IMG/'physicssolved'/'mascot.png').as_uri()}" alt="">
    {bubbles}
  </div>
  <div class="cv-chips">{chips}</div>
  <div class="cv-base">Physics Study Lab</div>
</div></div>"""

if __name__ == "__main__":
    f = ROOT / "cover.html"
    f.write_text('<meta charset="utf-8"><style>' + COVER_CSS + "</style>" + COVER_BODY)
    subprocess.run([CH, "--headless", "--disable-gpu", "--force-device-scale-factor=2",
                    "--screenshot=" + str(ROOT / "cover-raw.png"),
                    "--window-size=794,1123", "--hide-scrollbars", f.as_uri()],
                   check=True, capture_output=True)
    from PIL import Image
    im = Image.open(ROOT / "cover-raw.png").convert("RGB")
    im.save(IMG / "physicssolved" / "cover.jpg", "JPEG", quality=92, optimize=True)
    print(f"{im.size[0]}x{im.size[1]} -> img/physicssolved/cover.jpg")
