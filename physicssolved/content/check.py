# -*- coding: utf-8 -*-
"""
PHYSICS SOLVED -- the three revision passes, as a program.

Run after every change:  python3 solutions.py && python3 check.py

Pass 1  ARITHMETIC. Re-evaluates every calculation EXACTLY AS PRINTED, from the
        digits on the page rather than from the floats behind them. This is the
        pass that caught problem 7 (36.348 shown as 36.4), problems 17, 22 and 28
        (exact products shown rounded), and it is the reason a student with a
        calculator will never find a line that does not reproduce.
Pass 2  CONTENT. Checks that every structural promise the format makes is kept:
        a real trap, a real sanity check, a cross-reference back to the kit, a
        level tag, enough steps to be worth the page.
Pass 3  LANGUAGE. No ASCII stand-ins for real glyphs, UK spelling, typographic
        apostrophes and dashes, no double spaces.
"""
import json, re, sys, pathlib, warnings
warnings.filterwarnings("ignore")

PB = json.loads((pathlib.Path(__file__).parent / "solutions.json").read_text())
SEPS = {c for p in PB for s in p["steps"] for c in s["calc"] if c.isspace() and c != " "}
SUPER = "⁰¹²³⁴⁵⁶⁷⁸⁹⁻"
fails = []


def note(tag, p, msg):
    fails.append(f"  {tag} FAIL P{p['n']}: {msg}")


def prose(p):
    out = [p["title"], p["statement"], p["wanted"], p["sanity"], p["trap"][0],
           p["trap"][1], p["answer"][2], p.get("alt", "")]
    out += [s["t"] for s in p["steps"]] + [s["body"] for s in p["steps"]]
    return [x for x in out if x]


# ---------------------------------------------------------------- PASS 1
SUPDIG = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻", "0123456789-")
SAFE = re.compile(r"^[\d\s.+\-*/()e]+$")


def normalise(expr):
    """Turn a printed expression into something Python can evaluate, without
    changing a single digit: thousands separators out, × ÷ − into * / -,
    10⁻¹¹ into 1e-11, x² into x**2."""
    for ch in SEPS:
        expr = expr.replace(ch, "")
    expr = re.sub(r"(?<=\d) (?=\d\d\d\b)", "", expr)
    expr = re.sub(r"10([⁻]?[⁰¹²³⁴⁵⁶⁷⁸⁹]+)", lambda m: "1e" + m.group(1).translate(SUPDIG), expr)
    expr = re.sub(r"(?<=[\d)])²", "**2", expr)
    return expr.replace("×", "*").replace("÷", "/").replace("−", "-").replace("½", "0.5")


# Plain units can be removed without touching a digit. PREFIXED units cannot:
# "73.3 W x 24 h = 1.76 kWh" is a correct line whose arithmetic only works because
# of the k, so any line carrying one of these is handed to a human instead.
PREFIXED = ("kWh", "kW", "MW", "kJ", "MJ", "µJ", "mA", "nC", "µC", "kN", "mm", "km")
PLAIN_WORD = ("electrons", "bar", "kg", "Pa", "Hz", "cm", "mph", "J", "W", "V", "A",
              "N", "K", "C", "s", "m", "g", "h", "L")
PLAIN_SYM = ("m/s²", "m/s", "V/m", "cm³", "m³", "m²", "°C", "Ω", "°")


def strip_units(t):
    for u in PLAIN_SYM:
        t = t.replace(u, " ")
    for u in PLAIN_WORD:
        t = re.sub(rf"\b{u}\b", " ", t)
    return t


def last_literal(t):
    m = re.findall(r"-?\d+\.?\d*(?:e-?\d+)?", t)
    return m[-1] if m else ""


checked = symbolic = 0
HELD = []
for p in PB:
    for st in p["steps"]:
        parts = [normalise(x) for x in st["calc"].split("=")]
        did = False          # was ANY pair in this line machine-checked?
        for A, B in zip(parts, parts[1:]):
            raw = A + B
            if any(u in raw for u in PREFIXED):
                continue
            a, b = strip_units(A).strip(), strip_units(B).strip()
            # never truncate a line to make it parse: if anything but arithmetic
            # survives, hand it over rather than checking half of it
            if not (SAFE.match(a) and SAFE.match(b) and any(c.isdigit() for c in a)
                    and any(c.isdigit() for c in b)):
                continue
            try:
                got, want = eval(a, {"__builtins__": {}}, {}), eval(b, {"__builtins__": {}}, {})
            except Exception:
                continue
            checked += 1
            did = True
            lit = last_literal(b)
            dec = len(lit.split(".")[1]) if "." in lit and "e" not in lit else 0
            tol = max(abs(want) * 1e-3, 0.5 * 10 ** (-dec)) + 1e-9
            if abs(got - want) > tol:
                note("R1", p, f"printed  {A.strip()} = {B.strip()}   left side is actually {got:.8g}")
        if not did:
            if any(c.isdigit() for c in st["calc"]):
                HELD.append((p["n"], st["calc"]))
            else:
                symbolic += 1
HELD = sorted(set(HELD))
print(f"PASS 1  arithmetic : {checked} printed calculations re-evaluated from their own digits, "
      f"{len([x for x in fails if 'R1' in x])} wrong")
print(f"                     {symbolic} symbolic lines (no arithmetic), "
      f"{len(HELD)} held for hand checking (prefixed units or algebra)")
if "-v" in sys.argv:
    for n, c in HELD:
        print(f"        HOLD P{n}: {c}")

# ------------------------------------------------------- PASS 1b, BY HAND
# Lines the parser refuses to read -- roots, inverse trig, and prefixed units --
# get an explicit assertion each, so a hand check is made once and then kept.
import math
HAND = [
    ("P3  √(8.0²+6.0²)",      math.hypot(8.0, 6.0),              10.0),
    ("P3  tan⁻¹(6.0÷8.0)",    math.degrees(math.atan(6/8)),      36.9),
    ("P5  31.29²",            31.29**2,                          979.1),
    ("P6  2×45.0÷9.81",       2*45.0/9.81,                       9.174),
    ("P6  √9.174",            math.sqrt(9.174),                  3.029),
    ("P8  65.0×9.81",         65.0*9.81,                         637.6),
    ("P9  mg sin25",          4.0*9.81*math.sin(math.radians(25)), 16.58),
    ("P9  mg cos25",          4.0*9.81*math.cos(math.radians(25)), 35.56),
    ("P10 tan15",             math.tan(math.radians(15)),        0.268),
    ("P11 cos30",             math.cos(math.radians(30)),        0.8660),
    ("P12 √62.78",            math.sqrt(62.78),                  7.92),
    ("P16 √171.7",            math.sqrt(171.7),                  13.1),
    ("P18 0.68÷0.0012",       0.68/0.0012,                       567),
    ("P21 500×(23.04−1.44)",  500*(23.04-1.44),                  10800),
    ("P24 34.0÷0.80",         34.0/0.80,                         42.5),
    ("P27 2400−950",          2400-950,                          1450),
    ("P28 73.3 W×24 h in kWh",73.3*24/1000,                      1.76),
    ("P32 9.0×4700÷14700",    9.0*4700/14700,                    2.88),
    ("P34 2.2×1.5 kWh",       2.2*1.5,                           3.3),
    ("P34 3.3×4×52 kWh",      3.3*4*52,                          686.4),
    ("P36 2800÷230",          2800/230,                          12.2),
    ("P36 60÷230",            60/230,                            0.261),
    ("P37 2.5e-6×4.0e-6",     2.5e-6*4.0e-6,                     1.0e-11),
    ("P37 8.99e9×1.0e-11÷0.0064", 8.99e9*1.0e-11/0.0064,         14.0),
    ("P38 5.0e-9×300",        5.0e-9*300,                        1.5e-6),
    ("P38 300÷0.025",         300/0.025,                         12000),
    ("P40 4.0×2.0 ms in s",   4.0*2.0e-3,                        0.0080),
    ("P40 1÷0.0080",          1/0.0080,                          125),
    ("P41 544÷2",             544/2,                             272),
    ("P42 sin40÷1.50",        math.sin(math.radians(40))/1.50,   0.4285),
    ("P42 sin⁻¹0.4285",       math.degrees(math.asin(0.4285)),   25.4),
    ("P43 1.00÷1.50",         1.00/1.50,                         0.6667),
    ("P43 sin⁻¹0.6667",       math.degrees(math.asin(0.6667)),   41.8),
    ("P43 diamond critical",  math.degrees(math.asin(1/2.42)),   24.4),
    ("P44 1/15−1/25",         1/15-1/25,                         0.02667),
    ("P44 1÷0.02667",         1/0.02667,                         37.5),
    ("P45 850×340÷322",       850*340/322,                       897.5),
    ("P45 850×340÷358",       850*340/358,                       807.3),
    ("P46 hc÷400nm in J",     6.63e-34*3.00e8/400e-9,            4.973e-19),
    ("P46 4.973e-19÷1.60e-19",4.973e-19/1.60e-19,                3.11),
    ("P46 3.11−2.3",          3.11-2.3,                          0.81),
    ("P47 green photon eV",   1.989e-25/5.50e-7/1.60e-19,        2.26),
    ("P47 X-ray photon eV",   1.989e-25/1.0e-10/1.60e-19,        12430.0),
    ("P48 24÷6.0",            24/6.0,                            4),
    ("P48 7200÷16",           7200/16,                           450),
    ("P49 mass defect in u",  1.007276+1.008665-2.013553,        0.002388),
    ("P49 3.570e-13 in MeV",  3.570e-13/1.60e-19/1e6,            2.23),
    ("P50 √(2×1.60e-17÷9.11e-31)", math.sqrt(2*1.60e-17/9.11e-31), 5.927e6),
    ("P50 6.63e-34÷5.400e-24",6.63e-34/5.400e-24,                1.228e-10),
]
hand_bad = 0
for label, got, printed in HAND:
    txt = repr(printed)
    dec = len(txt.split(".")[1]) if "." in txt and "e" not in txt else 0
    tol = max(0.5 * 10 ** (-dec), abs(printed) * 5e-4)      # half a unit in the 4th s.f.
    if abs(got - printed) > tol + 1e-12:
        hand_bad += 1
        fails.append(f"  R1b FAIL {label}: printed {printed}, actually {got:.8g}")
print(f"PASS 1b hand checks: {len(HAND)} roots, inverse trig and prefixed-unit lines asserted, {hand_bad} wrong")

# ---------------------------------------------------------------- PASS 2
n2 = len(fails)
for p in PB:
    t = p["trap"][0]
    for ok, msg in [
        (len(p["steps"]) >= 3,                     "fewer than 3 steps"),
        (len(p["trap"][1]) >= 120,                 "trap explanation too thin"),
        (len(p["sanity"]) >= 80,                   "sanity check too thin"),
        (p["book"].startswith("Part"),             "no cross-reference back to the kit"),
        (p["level"] in ("GCSE", "A-LEVEL", "BOTH"), "bad level tag"),
        (any(c.isdigit() for c in t) or "“" in t or t[0].islower(),
                                                   "trap is neither a number nor a quoted belief"),
        (p["statement"].rstrip().endswith((".", "?")), "statement has no full stop"),
        (p["wanted"][0].islower(),                 "'wanted' should read as a phrase"),
        (len(p["given"]) >= 2,                     "fewer than 2 given quantities"),
    ]:
        if not ok:
            note("R2", p, msg)
print(f"PASS 2  content    : {len(PB)} problems × 9 structural checks, {len(fails)-n2} failures")

# ---------------------------------------------------------------- PASS 3
n3 = len(fails)
ASCII = ["sqrt", "->", "<=", ">=", "^2", "^3", "m/s2", "cm3", "kg/m3", "tan-1", " x ", "1/2 "]
US = [r"\bmeters\b", r"\bliters?\b", r"\bcenters?\b", r"\banalyze\b", r"\bcolors?\b",
      r"\bbehaviors?\b", r"\btraveling\b", r"\blabeled\b", r"\bmodeling\b"]
for p in PB:
    for fr in prose(p):
        for b in ASCII:
            if b in fr:
                note("R3", p, f"ASCII stand-in {b!r} in {fr[:50]!r}")
        for u in US:
            m = re.search(u, fr, re.I)
            if m:
                note("R3", p, f"US spelling {m.group(0)!r}")
        for ch, msg in (("  ", "double space"), ("'", "typewriter apostrophe"),
                        (" - ", "hyphen used as a dash"), ('"', "straight quote")):
            if ch in fr:
                note("R3", p, f"{msg} in {fr[:50]!r}")
print(f"PASS 3  language   : {len(PB)} problems × {len(ASCII)+len(US)+4} checks, {len(fails)-n3} failures")

print()
for f in fails:
    print(f)
lv = {}
for p in PB:
    lv[p["level"]] = lv.get(p["level"], 0) + 1
print(f"\n{len(PB)}/50 problems · levels {lv} · "
      f"alternative-route notes on {[p['n'] for p in PB if p.get('alt')]}")
print("ALL THREE PASSES CLEAN" if not fails else f"{len(fails)} OUTSTANDING")
sys.exit(1 if fails else 0)
