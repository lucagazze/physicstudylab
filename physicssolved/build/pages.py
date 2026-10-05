# -*- coding: utf-8 -*-
"""
PHYSICS SOLVED -- page generator.

Reads content/solutions.json and writes one HTML file, which Chrome prints to a
real A4 PDF. Vector text, not pictures of text: the file stays small, the type
stays sharp at any zoom, and -- the reason it matters here -- every number comes
straight out of the engine and cannot be re-drawn wrong.

Palette and furniture are sampled from the approved page in the family,
img/thebiggerpicture/p1-4-worked.png, so this book sits beside the others.

  python3 pages.py            # all 50
  python3 pages.py 1 2 3 4    # just those problems
  python3 pages.py --watermark   # same diagonal mark as The Final Book
"""
import json, pathlib, subprocess, sys, html
from cover import COVER_CSS, COVER_BODY

ROOT = pathlib.Path(__file__).resolve().parent
PB = json.loads((ROOT.parent / "content" / "solutions.json").read_text())
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

CSS = """
:root{
  --cream:#F8F2DA; --card:#FBF8F0; --navy:#25314B; --navy2:#1F3155;
  --grey:#E7E6DC; --gold:#E5C386; --gold2:#C19A4E; --ink:#1B1B1B;
  --muted:#6E6A60; --rule:#D8D3BF;
}
@page{ size:A4; margin:0 }
*{ box-sizing:border-box; margin:0; padding:0 }
body{ font-family:"Avenir Next","Avenir",sans-serif; color:var(--ink); }
.page{
  width:210mm; min-height:297mm; background:var(--cream);
  padding:13mm 14mm 13mm; position:relative;
  page-break-after:always; display:flex; flex-direction:column;
}
.page:last-child{ page-break-after:auto }

/* ---- furniture ---- */
.top{ display:flex; justify-content:space-between; align-items:center; margin-bottom:7mm }
.pill{
  background:var(--navy); color:#fff; font-weight:700; font-size:9.5pt;
  letter-spacing:.09em; padding:2.1mm 5mm; border-radius:2.2mm; text-transform:uppercase;
}
.right{ display:flex; align-items:center; gap:3mm }
.lvl{
  font-size:8.2pt; font-weight:700; letter-spacing:.09em; text-transform:uppercase;
  color:var(--navy2); border:1.1pt solid var(--navy2); border-radius:2mm; padding:1.5mm 3.2mm;
}
.num{
  background:var(--navy); color:var(--gold); font-weight:800; font-size:11pt;
  width:10mm; height:10mm; border-radius:50%; display:flex;
  align-items:center; justify-content:center;
}
h1{
  font-size:27pt; font-weight:800; color:var(--navy); letter-spacing:.015em;
  text-align:center; margin-bottom:1.5mm;
}
h2.ttl{
  font-size:12.5pt; font-weight:600; color:var(--muted); text-align:center;
  margin-bottom:6mm; font-style:italic;
}

/* ---- blocks ---- */
.box{ border-radius:3mm; padding:5mm 6mm; box-shadow:0 1.1mm 2.4mm rgba(60,52,30,.13) }
.problem{ background:var(--grey); font-size:13pt; line-height:1.52 }
.known{ display:flex; gap:4mm; margin:5mm 0 }
.known > div{ background:var(--card); border-radius:2.5mm; padding:3.5mm 4.5mm; flex:1;
  box-shadow:0 .8mm 1.8mm rgba(60,52,30,.10) }
.known h3{ font-size:8.4pt; letter-spacing:.1em; color:var(--navy2); margin-bottom:2mm;
  text-transform:uppercase }
.known p{ font-size:10.4pt; line-height:1.55 }

.body{ flex:1; display:flex; flex-direction:column; justify-content:center }
.dense .body{ justify-content:flex-start }
.steps{ display:flex; flex-direction:column; gap:3.4mm; margin-top:1mm }
.step{ background:var(--card); border-radius:3mm; padding:3.8mm 5mm 4mm;
  display:flex; gap:4mm; box-shadow:0 1mm 2.1mm rgba(60,52,30,.12) }
.dot{ background:var(--navy); color:#fff; font-weight:800; font-size:10pt; flex:0 0 7mm;
  height:7mm; border-radius:50%; display:flex; align-items:center; justify-content:center;
  margin-top:.4mm }
.step h4{ font-size:11.6pt; font-weight:700; color:var(--navy); line-height:1.3 }
.step p{ font-size:10.2pt; line-height:1.5; color:#333; margin-top:1.2mm }
.calc{ font-size:11.4pt; font-weight:600; text-align:center; margin-top:2.4mm;
  color:var(--navy2); line-height:1.5 }

.answer{ background:var(--gold); border-radius:3mm; padding:4.5mm 6mm; margin-top:4mm;
  box-shadow:0 1.2mm 2.6mm rgba(90,70,20,.22) }
.answer .k{ font-size:9pt; font-weight:800; letter-spacing:.12em; color:#5B4412 }
.answer .v{ font-size:16pt; font-weight:800; margin:1mm 0 1.5mm }
.answer .n{ font-size:10.2pt; line-height:1.45 }

.trap{ background:#FBEDE6; border-left:1.6mm solid #C05A33; border-radius:2.5mm;
  padding:4mm 5mm; margin-top:3.5mm }
.trap .k{ font-size:9pt; font-weight:800; letter-spacing:.1em; color:#9A3D1C;
  font-variant-emoji:text;
  margin-bottom:1.5mm }
.trap p{ font-size:10pt; line-height:1.48 }
.sense{ background:var(--card); border-left:1.6mm solid var(--navy2); border-radius:2.5mm;
  padding:4mm 5mm; margin-top:3mm }
.sense .k{ font-size:9pt; font-weight:800; letter-spacing:.1em; color:var(--navy2);
  margin-bottom:1.5mm }
.sense p{ font-size:10pt; line-height:1.48 }
.alt{ background:#EEF1F7; border-left:1.6mm solid #6B82B5; border-radius:2.5mm;
  padding:4mm 5mm; margin-top:3mm }
.alt .k{ font-size:9pt; font-weight:800; letter-spacing:.1em; color:#3C5590; margin-bottom:1.5mm }
.alt p{ font-size:9.6pt; line-height:1.46 }

/* ---- the attempt space on a problem page ---- */
.work{ flex:1; min-height:70mm; margin-top:4mm; display:flex; flex-direction:column }
.work div{ flex:1; border-bottom:.28mm solid var(--rule) }
.work div:last-child{ border-bottom:none }
.worklab{ font-size:8.4pt; font-weight:700; letter-spacing:.1em; color:var(--muted);
  text-transform:uppercase; margin-top:5mm }
.prompt{ text-align:center; font-size:10.6pt; font-style:italic; color:var(--muted);
  margin-top:4mm }
.foot{ position:absolute; left:14mm; right:14mm; bottom:6mm; display:flex;
  justify-content:space-between; font-size:8.4pt; color:var(--muted); letter-spacing:.05em }
.tiny{ font-size:8.4pt; color:var(--muted) }
.fill{ flex:1 }

.wm{ position:absolute; top:50%; left:50%; z-index:9; pointer-events:none;
  transform:translate(-50%,-50%) rotate(-36deg); white-space:nowrap;
  font-family:"Times New Roman",Georgia,serif; font-size:40pt; letter-spacing:.02em;
  color:rgba(60,70,96,0.11); }

/* ---- cover and matter ---- */
.cover{ background:var(--navy); color:#fff; justify-content:center; align-items:center;
  text-align:center; padding:0 22mm 34mm }
.cover .rule{ width:34mm; height:1.4mm; background:var(--gold); border-radius:1mm; margin:0 auto }
.cover h1{ font-size:46pt; color:#fff; line-height:1.02; letter-spacing:.01em; margin:9mm 0 0 }
.cover h1 em{ color:var(--gold); font-style:normal; display:block }
.cover .sub{ font-size:14.5pt; color:#C9D2E4; margin:7mm 0 9mm; line-height:1.45 }
.cover .lvls{ display:flex; gap:4mm; justify-content:center; margin-bottom:11mm }
.cover .lvls span{ border:1.2pt solid var(--gold); color:var(--gold); border-radius:2mm;
  padding:1.8mm 5mm; font-size:10pt; font-weight:700; letter-spacing:.12em }
.cover .brand{ position:absolute; bottom:16mm; left:0; right:0; font-size:10pt;
  letter-spacing:.3em; color:#8FA0C0 }
.mat h1{ font-size:25pt; margin-bottom:2mm }
.mat .lead{ font-size:12.5pt; line-height:1.55; text-align:center; color:var(--muted);
  margin-bottom:7mm; font-style:italic }
.mat p{ font-size:11pt; line-height:1.6; margin-bottom:3.5mm }
.rows{ display:flex; flex-direction:column; gap:2.4mm }
.row{ background:var(--card); border-radius:2.5mm; padding:2.4mm 4mm; display:flex; gap:4mm;
  box-shadow:0 .7mm 1.6mm rgba(60,52,30,.10) }
.row b{ flex:0 0 31mm; color:var(--navy); font-size:10.2pt }
.row span{ font-size:9.3pt; line-height:1.42 }
.rows{ gap:1.8mm }
.cols{ display:flex; gap:7mm }
.cols > div{ flex:1 }
.kv{ display:flex; justify-content:space-between; gap:3mm; font-size:9.6pt;
  padding:1.5mm 0; border-bottom:.25mm solid var(--rule) }
.kv b{ color:var(--navy); flex:0 0 7mm }
.kv span{ text-align:right; font-weight:600; color:#2C2C2C }
.tl{ display:flex; gap:3.5mm; font-size:9.8pt; padding:2mm 0;
  border-bottom:.25mm solid var(--rule); line-height:1.4 }
.tl b{ color:var(--navy2); flex:0 0 8mm }
.part{ font-size:8.6pt; font-weight:800; letter-spacing:.12em; color:var(--gold2);
  text-transform:uppercase; margin:4mm 0 1mm }
.part:first-child{ margin-top:0 }
.toc{ display:flex; justify-content:space-between; font-size:11.5pt; padding:2.8mm 0;
  border-bottom:.3mm solid var(--rule) }
.toc b{ color:var(--navy) } .toc span{ color:var(--muted); font-size:10pt }
.nx{ background:var(--card); border-radius:3mm; padding:4.5mm 5.5mm; margin-bottom:3.2mm;
  box-shadow:0 .9mm 2mm rgba(60,52,30,.11); border-left:1.6mm solid var(--gold2) }
.nx b{ font-size:12pt; color:var(--navy) }
.nx p{ font-size:10.2pt; line-height:1.5; margin:1.5mm 0 0 }

/* long solutions tighten up rather than spill onto a third page */
.dense .step{ padding:2.6mm 4.5mm } .dense .step h4{ font-size:10.4pt }
.dense .step p{ font-size:9.2pt; margin-top:.8mm } .dense .calc{ font-size:10.2pt; margin-top:1.6mm }
.dense .trap p,.dense .sense p,.dense .alt p{ font-size:9pt; line-height:1.4 }
.dense .steps{ gap:2.2mm } .dense .answer{ padding:3.4mm 6mm; margin-top:3mm }
.dense .answer .v{ font-size:13.5pt } .dense .answer .n{ font-size:9.4pt }
.dense .trap,.dense .sense,.dense .alt{ padding:3mm 5mm; margin-top:2.4mm }
.dense h1{ font-size:24pt } .dense h2.ttl{ font-size:11.5pt; margin-bottom:4mm }
"""


WM = '<div class="wm">Physics Study Lab</div>'


def e(t):
    return html.escape(str(t), quote=False)


def page_problem(p, n):
    k = "  ·  ".join(f"{a} = {b} {c}".strip() for a, b, c in p["given"])
    return f"""
<div class="page">
  {WM}
  <div class="top">
    <div class="pill">{e(p['book'].split('(')[0].strip())}</div>
    <div class="right"><div class="lvl">{e(p['level'])}</div><div class="num">{p['n']}</div></div>
  </div>
  <h1>PROBLEM</h1>
  <h2 class="ttl">{e(p['title'])}</h2>
  <div class="box problem">{e(p['statement'])}</div>
  <div class="known">
    <div><h3>What you know</h3><p>{e(k)}</p></div>
    <div><h3>What you want</h3><p>{e(p['wanted'])}</p></div>
  </div>
  <div class="worklab">Your working</div>
  <div class="work"><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div></div>
  <div class="prompt">Give it five minutes before you turn the page.</div>
  <div class="foot"><span>PHYSICS SOLVED</span><span>{n}</span></div>
</div>"""


def page_solution(p, n):
    steps = "".join(f"""
    <div class="step"><div class="dot">{i}</div><div class="fill">
      <h4>{e(s['t'])}</h4>{f"<p>{e(s['body'])}</p>" if s['body'] else ""}
      <div class="calc">{e(s['calc'])}</div></div></div>"""
                    for i, s in enumerate(p["steps"], 1))
    val, unit, note = p["answer"]
    alt = (f"""<div class="alt"><div class="k">ANOTHER WAY IN</div><p>{e(p['alt'])}</p></div>"""
           if p.get("alt") else "")
    weight = (sum(len(s["t"]) + len(s["body"]) + len(s["calc"]) for s in p["steps"])
              + len(p["trap"][1]) + len(p["sanity"]) + len(p.get("alt", "")))
    dense = " dense" if (len(p["steps"]) >= 5 or weight > 1050 or p.get("alt")) else ""
    return f"""
<div class="page{dense}">
  {WM}
  <div class="top">
    <div class="pill">{e(p['book'].split('(')[0].strip())}</div>
    <div class="right"><div class="lvl">{e(p['level'])}</div><div class="num">{p['n']}</div></div>
  </div>
  <h1>SOLUTION</h1>
  <h2 class="ttl">{e(p['title'])}</h2>
  <div class="body">
  <div class="steps">{steps}</div>
  <div class="answer">
    <div class="k">ANSWER</div>
    <div class="v">{e((val + ' ' + unit).strip())}</div>
    <div class="n">{e(note)}</div>
  </div>
  <div class="trap"><div class="k">&#9888; THE TRAP &mdash; most students answer {e(p['trap'][0])}</div>
    <p>{e(p['trap'][1])}</p></div>
  <div class="sense"><div class="k">DOES IT MAKE SENSE?</div><p>{e(p['sanity'])}</p></div>
  {alt}
  </div>
  <div class="foot"><span>THEORY: {e(p['book'])}</span><span>{n}</span></div>
</div>"""




# ===========================================================================
# front and back matter
# ===========================================================================
PARTS = ["Fundamentals", "Mechanics", "Fluids", "Thermodynamics",
         "Electricity", "Waves & Optics", "Modern Physics"]

COMMAND_WORDS = [
    ("State, Give, Name", "Recall it. No working, no reason, no sentence. If you find yourself explaining, you are spending time you will not be paid for."),
    ("Define", "Give the precise meaning, usually in the form of a word equation or a sentence that would stand up in a glossary."),
    ("Describe", "Say WHAT happens. No reasons. A description that drifts into because has started answering a different question."),
    ("Explain", "Say WHY it happens. Your answer needs the word because, or a word doing the same job. Marks here are for the link, not the fact."),
    ("Calculate", "Produce a number. Show the equation, the substitution and the answer, with a unit. Working earns marks even when the final number is wrong."),
    ("Determine", "Also a number, but you must first get the data yourself, from a graph, a table or a diagram. The hunt for the data is part of the question."),
    ("Show that", "The answer is already printed in the question. Work to one more significant figure than the one quoted, then write a line stating that it agrees."),
    ("Estimate", "Calculate from assumptions you state. The right order of magnitude scores. State every assumption you make, because they are marked too."),
    ("Suggest", "Apply physics to a situation you have never seen. There is rarely one correct answer, and the examiner is looking for sound reasoning."),
    ("Compare", "Both things, in every sentence. Use whereas and while. Two separate paragraphs describing one thing each is not a comparison."),
    ("Sketch", "The shape of a graph, with the key values and intercepts labelled. Graph paper is not needed and accuracy of plotting is not marked."),
    ("Justify, Evaluate", "State a conclusion and the evidence for it. Evaluate also expects the weaknesses, not only the case in favour."),
]

SEVEN = [
    ("Read it twice", "The second time with a pencil, underlining every number and every command word. Most lost marks are lost here, before any physics happens."),
    ("Write down what you know", "With units, in a column. The act of listing them is what reveals which equation is available to you."),
    ("Write down what you want", "One line. If you cannot state what you are looking for, no equation will help you find it."),
    ("Draw it", "A diagram, however rough, with the forces, rays or circuit on it. Problems 9, 10 and 42 in this book are all won or lost on the drawing."),
    ("Choose the equation that fits what you have", "Not the one you remember best. The right equation contains what you were given and what you want, and nothing else."),
    ("Convert to SI before you substitute", "Centimetres, minutes, megahertz and microcoulombs have ended more questions than any piece of physics. Convert first, every time."),
    ("Check three things", "The unit, the size, and whether you answered the question that was asked. Half the traps in this book are caught by the second one alone."),
]


def page_cover():
    return COVER_BODY


def page_contents(n):
    rows = ""
    first = 6
    for part in PARTS:
        ps = [p for p in PB if p["part"] == part]
        lo, hi = ps[0]["n"], ps[-1]["n"]
        rows += (f'<div class="toc"><b>{e(part)}</b>'
                 f'<span>problems {lo}&ndash;{hi} &nbsp;&middot;&nbsp; page {first}</span></div>')
        first += 2 * len(ps)
    return f"""
<div class="page mat">
  {WM}
  <div class="top"><div class="pill">Contents</div><div class="right"><div class="lvl">50 problems</div></div></div>
  <h1>CONTENTS</h1>
  <div class="lead">Every problem is anchored to a chapter of the Physics Study Lab kit,
  and every solution tells you which page of it the theory lives on.</div>
  {rows}
  <div style="margin-top:9mm">
    <div class="toc"><b>Answer key</b><span>page {2*len(PB)+6}</span></div>
    <div class="toc"><b>The fifty traps, in one place</b><span>page {2*len(PB)+8}</span></div>
    <div class="toc"><b>Where to go next</b><span>page {2*len(PB)+11}</span></div>
  </div>
  <div class="foot"><span>PHYSICS SOLVED</span><span>{n}</span></div>
</div>"""


def page_howto(n):
    return f"""
<div class="page mat">
  {WM}
  <div class="top"><div class="pill">How to use this book</div><div class="right"><div class="lvl">read this first</div></div></div>
  <h1>HOW TO USE THIS BOOK</h1>
  <div class="lead">There is a right way and a wrong way, and the difference is about five minutes.</div>
  <p><b>Every problem gets two pages.</b> The question is on the left, on its own, with space to
  work. The full solution is on the right, where you cannot see it until you turn over.</p>
  <p><b>That is deliberate.</b> Reading a worked solution feels like learning and mostly is not.
  You follow each line, every line makes sense, and nothing sticks, because recognising a step
  someone else has taken is a far easier task than choosing it yourself. The learning happens in
  the five minutes before you turn the page &mdash; including, and especially, the minutes where
  you are stuck.</p>
  <p><b>So: five minutes, pencil down, before you look.</b> Get something on the page even if it
  is wrong. A wrong attempt you then correct is worth more than a right answer you only watched.</p>
  <p><b>When you do turn over, read the trap first.</b> Every solution carries a block marked
  THE TRAP: the specific wrong answer most students give, and the reason the brain produces it.
  If that was your answer, you have just learned more from this page than from getting it right.</p>
  <p><b>Then check it makes sense.</b> The last block of every solution tests the answer against
  something you already know &mdash; a number from the Highway Code, the time a kettle takes, the
  density of steel. That habit catches more errors in a real exam than any amount of re-reading.</p>
  <p><b>If a step does not click</b>, the footer of every solution tells you where the theory
  lives in the Physics Study Lab kit. This book does not explain physics. It shows you what to do
  with it.</p>
  <p><b>About the level tags.</b> Each problem is marked GCSE, A&#8209;LEVEL or BOTH. Boards differ
  slightly, so treat the tag as a guide rather than a ruling; where two syllabuses take different
  routes to the same answer, the solution shows both.</p>
  <div class="foot"><span>PHYSICS SOLVED</span><span>{n}</span></div>
</div>"""


def page_command(n):
    rows = "".join(f'<div class="row"><b>{e(a)}</b><span>{e(b)}</span></div>' for a, b in COMMAND_WORDS)
    return f"""
<div class="page mat">
  {WM}
  <div class="top"><div class="pill">Before the physics</div><div class="right"><div class="lvl">worth marks on its own</div></div></div>
  <h1 style="font-size:22pt">HOW TO READ A PHYSICS QUESTION</h1>
  <div class="lead" style="margin-bottom:5mm">More marks are lost to the command word than to the maths.</div>
  <div class="rows">{rows}</div>
  <div class="foot"><span>PHYSICS SOLVED</span><span>{n}</span></div>
</div>"""


def page_seven(n):
    rows = "".join(f'<div class="step"><div class="dot">{i}</div><div class="fill">'
                   f'<h4>{e(a)}</h4><p>{e(b)}</p></div></div>'
                   for i, (a, b) in enumerate(SEVEN, 1))
    return f"""
<div class="page mat">
  {WM}
  <div class="top"><div class="pill">The method</div><div class="right"><div class="lvl">all 50 problems</div></div></div>
  <h1>SEVEN STEPS THAT SOLVE ANYTHING</h1>
  <div class="lead">Every solution in this book follows the same seven moves, in the same order.</div>
  <div class="steps">{rows}</div>
  <div class="foot"><span>PHYSICS SOLVED</span><span>{n}</span></div>
</div>"""


def pages_answers(n):
    half = (len(PB) + 1) // 2
    def col(items):
        return "".join(f'<div class="kv"><b>{p["n"]}</b>'
                       f'<span>{e((p["answer"][0] + " " + p["answer"][1]).strip())}</span></div>'
                       for p in items)
    out = []
    for i, chunk in enumerate([PB[:half], PB[half:]]):
        mid = (len(chunk) + 1) // 2
        out.append(f"""
<div class="page mat">
  {WM}
  <div class="top"><div class="pill">Answer key</div><div class="right"><div class="lvl">{'1 of 2' if i==0 else '2 of 2'}</div></div></div>
  <h1>ANSWER KEY</h1>
  <div class="lead">Numbers only. If yours does not match, the method is on the solution page &mdash;
  and so is the reason you got the one you got.</div>
  <div class="cols"><div>{col(chunk[:mid])}</div><div>{col(chunk[mid:])}</div></div>
  <div class="foot"><span>PHYSICS SOLVED</span><span>{n+i}</span></div>
</div>""")
    return out


def pages_traps(n):
    # grouped by part rather than cut at a fixed count: this is the page people
    # photograph and send to each other, so it is allowed the room to breathe
    groups = [["Fundamentals", "Mechanics", "Fluids"],
              ["Thermodynamics", "Electricity"],
              ["Waves & Optics", "Modern Physics"]]
    out = []
    for i, names in enumerate(groups):
        chunk = [p for p in PB if p["part"] in names]
        body, part = "", None
        for p in chunk:
            if p["part"] != part:
                part = p["part"]
                body += f'<div class="part">{e(part)}</div>'
            body += f'<div class="tl"><b>{p["n"]}</b><span>{e(p["trapline"])}</span></div>'
        out.append(f"""
<div class="page mat">
  {WM}
  <div class="top"><div class="pill">The fifty traps</div><div class="right"><div class="lvl">{i+1} of 3</div></div></div>
  <h1>EVERY TRAP, IN ONE PLACE</h1>
  <div class="lead">Read this page the night before. It is the shortest revision in the book.</div>
  {body}
  <div class="foot"><span>PHYSICS SOLVED</span><span>{n+i}</span></div>
</div>""")
    return out


def page_next(n):
    return f"""
<div class="page mat">
  {WM}
  <div class="top"><div class="pill">Where to go next</div><div class="right"><div class="lvl">physics study lab</div></div></div>
  <h1>WHERE TO GO NEXT</h1>
  <div class="lead">This book was built to sit beside the others, not to replace them.</div>
  <div class="nx"><b>Physics Study Lab &mdash; the Kit</b>
    <p>Seven parts and thirty-eight illustrated chapters: the theory behind every problem in this
    book. The footer of each solution tells you the page. If a step did not click, start there.</p></div>
  <div class="nx"><b>The Words of Physics</b>
    <p>104 terms, each with its own drawing and its own why. Most of what looks like a physics
    problem is a vocabulary problem wearing a disguise &mdash; see the command words page.</p></div>
  <div class="nx"><b>Beyond the Syllabus</b>
    <p>Quantum physics, capacitance and RC circuits, gravitational fields, particle physics and
    cosmology, derived rather than merely defined. The next step up from the hardest problems here.</p></div>
  <div class="nx"><b>The Final Book of Physics</b>
    <p>127 pages, twelve parts, from Newton&#8217;s laws to dark energy, plus a master reference of
    every formula, constant, unit and symbol. The one to keep when the exams are over.</p></div>
  <p style="margin-top:7mm; text-align:center; font-size:11pt; color:var(--muted); font-style:italic">
  Understanding physics and being able to use it are two different skills.<br>
  You have now practised the second one fifty times.</p>
  <div class="foot"><span>PHYSICS SOLVED</span><span>{n}</span></div>
</div>"""


if __name__ == "__main__":
    mark = "--watermark" in sys.argv
    if not mark:
        globals()["WM"] = ""
    want = [int(a) for a in sys.argv[1:] if a.lstrip("-").isdigit()] or [p["n"] for p in PB]
    sel = [p for p in PB if p["n"] in want]
    whole = len(sel) == len(PB)
    pages, n = [], 1
    if whole:
        pages.append(page_cover())                       # the cover carries no number
        for fn in (page_contents, page_howto, page_command, page_seven):
            pages.append(fn(n + 1)); n += 1
        n += 1
    for p in sel:
        pages.append(page_problem(p, n)); n += 1
        pages.append(page_solution(p, n)); n += 1
    if whole:
        pages += pages_answers(n); n += 2
        pages += pages_traps(n); n += 3
        pages.append(page_next(n))
    out = ROOT / (("physics-solved-watermarked.html" if mark else "physics-solved.html") if whole else "preview.html")
    out.write_text(f"<meta charset='utf-8'><style>{CSS}{COVER_CSS}</style>" + "".join(pages))
    pdf = out.with_suffix(".pdf")
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf}", out.as_uri()],
                   check=True, capture_output=True)
    import re
    got = max(int(x) for x in re.findall(rb"/Count (\d+)", pdf.read_bytes()))
    ok = "no overflow" if got == len(pages) else f"*** {got-len(pages)} PAGES OF OVERFLOW ***"
    print(f"{len(sel)} problems -> {len(pages)} pages -> {pdf.name} "
          f"({pdf.stat().st_size/1024:.0f} KB) -- PDF has {got}, {ok}")
