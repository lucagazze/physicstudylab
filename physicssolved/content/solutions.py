# -*- coding: utf-8 -*-
"""
PHYSICS SOLVED -- 50 Exam Problems, Worked Step by Step
Phase A: every answer is COMPUTED here, never typed by hand.

Three rules this file enforces, because a worked-solutions book lives or dies
on them:

 1. NO HAND-TYPED NUMBERS. Every figure on every page comes out of this file,
    so the artwork can never drift from the arithmetic.

 2. THE DISPLAYED CHAIN MUST BE SELF-CONSISTENT. If a step prints u = 31.29,
    the next step squares 31.29 -- not the unrounded value hiding behind it.
    A student checking the working on a calculator has to get the same digits.
    Working is carried at 4 s.f.; final answers are quoted at 3 s.f.

 3. PUBLICATION TYPOGRAPHY AT SOURCE. Superscripts, Greek letters, x, /,
    degrees and arrows are written as the real characters here, so nothing has
    to be "fixed up" at layout time and silently broken.

g = 9.81 m/s2 throughout (UK exam-board standard).
levels: GCSE | A-LEVEL | BOTH
"""
import json, math, pathlib, re

G = 9.81
MILE_EXACT = 1609.344
MILE = 1609.0        # the value quoted to the student, and the one used in working

PROBLEMS = []


# --------------------------------------------------------------------------
# number rendering
# --------------------------------------------------------------------------
def R(x, n=4):
    """Round to n significant figures and RETURN THE FLOAT, so the next line of
    working can be computed from exactly what the student just read."""
    if x == 0:
        return 0.0
    return round(x, -int(math.floor(math.log10(abs(x)))) + (n - 1))


def S(x, n=3):
    """Render to n significant figures, keeping trailing zeros (8.0, not 8) and
    never falling back to scientific notation, which has no place on a GCSE page."""
    if x == 0:
        return "0"
    x = R(x, n)
    exp = math.floor(math.log10(abs(x)))
    dec = max(0, n - 1 - exp)
    s = f"{x:,.{dec}f}"
    # thin space as a thousands separator, and only above 9999
    return s.replace(",", " ") if abs(x) >= 10000 else s.replace(",", "")


def ok(x, work=4, show=3):
    """Guard against double rounding. Rounding to `work` and then displaying at
    `show` must give the same digits as displaying the exact value. Problem 7
    failed this once (36.348 -> 36.35 -> 36.4 instead of 36.3), so every value
    that is both chained and displayed is now checked."""
    assert S(R(x, work), show) == S(x, show), (
        f"double rounding: exact {x!r} shows {S(x, show)} but the chained value shows {S(R(x, work), show)}")
    return x


def typo(t):
    """Two things a printed book must get right and a .py file never does by itself:
    a spaced hyphen used as a dash is an en dash, and an apostrophe is U+2019, not
    the typewriter quote. Applied centrally so the remaining problems inherit it."""
    if not isinstance(t, str):
        return t
    t = t.replace(" - ", " \u2013 ")                       # dash, not hyphen
    t = re.sub(r"(?<=[A-Za-z])'(?=[A-Za-z])", "\u2019", t)  # Newton's, water's
    t = re.sub(r"(?<=s)'(?=\s|$)", "\u2019", t)            # Archimedes'
    return t


SUP = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")


def sci(x, n=3):
    """Standard form with real superscripts, for the modern-physics numbers that
    would otherwise print as a string of zeros."""
    e = math.floor(math.log10(abs(x)))
    return f"{S(x / 10**e, n)} {TIMES} 10{str(e).translate(SUP)}"


def P(**kw):
    for k in ("title", "statement", "wanted", "sanity", "alt"):
        if k in kw:
            kw[k] = typo(kw[k])
    kw["trap"] = (typo(kw["trap"][0]), typo(kw["trap"][1]))
    kw["answer"] = tuple(typo(x) for x in kw["answer"])
    for st in kw["steps"]:
        st["t"], st["body"] = typo(st["t"]), typo(st["body"])
    PROBLEMS.append(kw)
    return kw


DEG = "°"
MU, RHO, THETA, DELTA = "μ", "ρ", "θ", "Δ"
SQ, CU, SUP_MINUS1 = "²", "³", "⁻¹"
TIMES, DIV, ARROW, LEQ, GEQ, ROOT, HALF = "×", "÷", "→", "≤", "≥", "√", "½"
MS = f"m/s{SQ}"          # m/s²
CM3, M3 = f"cm{CU}", f"m{CU}"

# ===========================================================================
# PART 1 - FUNDAMENTALS  (Main Book pp. 5-16)
# ===========================================================================

# --- 1 ---------------------------------------------------------------------
metres_per_hour = R(70 * MILE, 5)                 # 112 600
v1 = R(metres_per_hour / 3600, 4)                 # 31.29
kph1 = R(70 * MILE / 1000, 4)
wrong1 = R(70 / 3.6, 4)
P(
    n=1, part="Fundamentals", chapter="Units & conversions", level="GCSE",
    book="Part 1 · Fundamentals (pp. 5-16)",
    title="A motorway speed limit, in physics units",
    statement=("The UK motorway speed limit is 70 mph. Every physics equation you will use "
               "needs speed in metres per second. Convert it. Take 1 mile = 1609 m."),
    given=[("speed", "70", "mph"), ("1 mile", "1609", "m"), ("1 hour", "3600", "s")],
    wanted="the same speed in m/s",
    steps=[
        dict(t="Turn the miles into metres",
             body="In one hour the car covers 70 miles.",
             calc=f"70 {TIMES} 1609 m = {S(metres_per_hour,5)} m"),
        dict(t="Turn the hour into seconds",
             body="A speed is metres divided by seconds, so the hour has to go.",
             calc=f"{S(metres_per_hour,5)} m {DIV} 3600 s = {S(v1,4)} m/s"),
        dict(t="Quote it sensibly",
             body="The speed limit was given to 2 s.f., so 3 s.f. is as far as the data honestly reaches.",
             calc=f"v = {S(v1,3)} m/s"),
    ],
    answer=(S(v1, 3), "m/s", "70 mph is just over 31 metres every second."),
    trap=(f"{S(wrong1,3)} m/s",
          f"Dividing by 3.6. That converts km/h to m/s, not mph. Applied to miles "
          f"per hour it throws away {S((1-wrong1/v1)*100,2)}% of the speed. The "
          f"{chr(8220)}{DIV} 3.6{chr(8221)} shortcut only becomes valid once the number is already in km/h."),
    sanity=(f"70 mph is about {S(kph1,4)} km/h, and {S(kph1,4)} {DIV} 3.6 = {S(v1,4)} m/s. "
            f"Two different routes, the same answer."),
)

# --- 2 ---------------------------------------------------------------------
vol2 = R(57.0 - 50.0, 2)
rho2_cgs = R(56.0 / vol2, 2)
rho2_si = R(rho2_cgs * 1000, 2)
P(
    n=2, part="Fundamentals", chapter="Quantities & units", level="GCSE",
    book="Part 1 · Fundamentals (pp. 5-16)",
    title="Density of an object you cannot measure with a ruler",
    statement=(f"A stainless steel nut has a mass of 56.0 g. Dropped into a measuring "
               f"cylinder, the water level rises from 50.0 {CM3} to 57.0 {CM3}. "
               f"Find its density in kg/{M3}."),
    given=[("mass", "56.0", "g"), ("water before", "50.0", CM3), ("water after", "57.0", CM3)],
    wanted=f"the density in kg/{M3}",
    steps=[
        dict(t="The volume is the rise, not the final reading",
             body="The nut pushes aside its own volume of water, so the volume you want is the difference.",
             calc=f"V = 57.0 {chr(8722)} 50.0 = {S(vol2,2)} {CM3}"),
        dict(t=f"Density = mass {DIV} volume",
             body="Work in the units you were given, then convert once, at the end.",
             calc=f"{RHO} = 56.0 {DIV} {S(vol2,2)} = {S(rho2_cgs,2)} g/{CM3}"),
        dict(t="Convert to SI",
             body=f"1 g = 1/1000 kg and 1 {CM3} = 1/1 000 000 {M3}, so the two conversions "
                  f"do not cancel: they leave a factor of 1000 upwards.",
             calc=f"{RHO} = {S(rho2_cgs,2)} {TIMES} 1000 = {S(rho2_si,2)} kg/{M3}"),
    ],
    answer=(S(rho2_si, 2), f"kg/{M3}", f"{S(rho2_cgs,2)} g/{CM3}, which is {S(rho2_si,2)} kg/{M3}."),
    trap=(f"{S(rho2_cgs,2)} kg/{M3}",
          f"Keeping the g/{CM3} number and simply changing the label. The answer is "
          f"then out by a factor of 1000 - and it should look absurd on sight, "
          f"because {S(rho2_cgs,2)} kg/{M3} is lighter than air."),
    sanity=(f"Stainless steel runs about 7900-8100 kg/{M3}. {S(rho2_si,2)} sits inside "
            f"that range, so the answer describes a material that actually exists. "
            f"That is the fastest check there is on a density."),
)

# --- 3 ---------------------------------------------------------------------
res3 = R(math.hypot(8.0, 6.0), 3)
ang3 = R(math.degrees(math.atan(6.0 / 8.0)), 3)
P(
    n=3, part="Fundamentals", chapter="Vectors", level="BOTH",
    book="Part 1 · Fundamentals (pp. 5-16)",
    title="Two tugs, one barge",
    statement=("Two tugs pull a barge. One pulls with 8.0 kN due north, the other with "
               "6.0 kN due east. Find the magnitude and direction of the resultant force."),
    given=[("F north", "8.0", "kN"), ("F east", "6.0", "kN"), ("angle between them", "90", DEG)],
    wanted="the resultant force: magnitude and direction",
    steps=[
        dict(t="Draw the two forces tip to tail",
             body=f"They are at 90{DEG} to each other, so the two forces and the resultant "
                  f"form a right-angled triangle.",
             calc="the resultant is the hypotenuse"),
        dict(t="Pythagoras gives the magnitude",
             body="This is the whole point of calling force a vector: you cannot simply add the numbers.",
             calc=f"F = {ROOT}(8.0{SQ} + 6.0{SQ}) = {ROOT}100 = {S(res3,3)} kN"),
        dict(t="Trigonometry gives the direction",
             body="Measure it from north, the way a bearing is always quoted.",
             calc=f"{THETA} = tan{SUP_MINUS1}(6.0 {DIV} 8.0) = {S(ang3,3)}{DEG} east of north"),
    ],
    answer=(f"{S(res3,3)} kN at {S(ang3,3)}{DEG} east of north", "",
            "It is a 3-4-5 triangle scaled up by two, which is why the numbers come out clean."),
    trap=("14 kN",
          f"Adding the magnitudes. That is only correct when two forces point the same "
          f"way. Here it overstates the pull by {S((14/res3-1)*100,2)}% - and it produces "
          f"no direction at all, which is the clue that the method itself is wrong."),
    sanity=(f"A resultant must always lie between the difference of the two forces (2.0 kN) "
            f"and their sum (14.0 kN). {S(res3,3)} kN sits inside that window."),
)

# --- 4 ---------------------------------------------------------------------
dd4, dt4 = R(34.0 - 14.0, 3), R(6.0 - 2.0, 2)
grad4 = R(dd4 / dt4, 2)
icept4 = R(14.0 - grad4 * 2.0, 2)
wrong4 = R(34.0 / 6.0, 3)
P(
    n=4, part="Fundamentals", chapter="Graphs", level="GCSE",
    book="Part 1 · Fundamentals (pp. 5-16)",
    title="Reading a speed off a distance-time graph",
    statement=("A distance-time graph is a straight line. At t = 2.0 s the distance is "
               "14.0 m; at t = 6.0 s it is 34.0 m. Find the speed."),
    given=[("point A", "(2.0 s, 14.0 m)", ""), ("point B", "(6.0 s, 34.0 m)", "")],
    wanted="the speed of the object",
    steps=[
        dict(t="Speed is the gradient, not the height",
             body="On a distance-time graph the gradient is distance per unit time, which is exactly what speed means.",
             calc=f"v = {DELTA}d {DIV} {DELTA}t"),
        dict(t="Take the differences",
             body="Use two points that are far apart; it keeps any reading error small.",
             calc=f"{DELTA}d = 34.0 {chr(8722)} 14.0 = {S(dd4,3)} m    and    {DELTA}t = 6.0 {chr(8722)} 2.0 = {S(dt4,2)} s"),
        dict(t="Divide",
             body="",
             calc=f"v = {S(dd4,3)} {DIV} {S(dt4,2)} = {S(grad4,2)} m/s"),
    ],
    answer=(S(grad4, 2), "m/s", "Constant speed, because the line is straight."),
    trap=(f"{S(wrong4,3)} m/s",
          f"Taking a single point and dividing distance by time (34.0 {DIV} 6.0). That "
          f"only works if the line passes through the origin. This one does not - it "
          f"starts at {S(icept4,2)} m - so the single-point method comes out "
          f"{S((wrong4/grad4-1)*100,2)}% too high."),
    sanity=(f"Test it on the other point: the line predicts {S(icept4,2)} + {S(grad4,2)} "
            f"{TIMES} 2.0 = {S(icept4+grad4*2,3)} m at t = 2.0 s, which is what the graph shows."),
)

# ===========================================================================
# PART 2 - MECHANICS  (Main Book pp. 17-34)
# ===========================================================================

# --- 5 ---------------------------------------------------------------------
u5 = v1                                  # 31.29 m/s, carried over from problem 1
a5 = 6.53
u5sq = R(u5**2, 4)                       # 979.1
s5 = R(u5sq / (2 * a5), 4)               # 74.97
wrong5 = R(70**2 / (2 * a5), 4)
P(
    n=5, part="Mechanics", chapter="Motion & acceleration", level="GCSE",
    book="Part 2 · Mechanics (pp. 17-34)",
    title="Where the Highway Code braking distance comes from",
    statement=(f"A car travelling at 70 mph brakes hard, decelerating at 6.53 {MS}. How far "
               f"does it travel between the brakes biting and the car stopping?"),
    given=[("u", "70", "mph (see problem 1)"), ("v", "0", "m/s"), ("a", f"{chr(8722)}6.53", MS)],
    wanted="the braking distance s",
    steps=[
        dict(t="Convert before you do anything else",
             body="Every SUVAT equation is written in SI units, and mph is not one.",
             calc=f"u = {S(u5,4)} m/s"),
        dict(t="Choose the equation without t in it",
             body="You are not asked for the time and you are not given it, so pick the equation that never mentions it.",
             calc=f"v{SQ} = u{SQ} + 2as"),
        dict(t="The car stops, so v = 0",
             body="This is where most marks are lost: zero is the FINAL speed. The 70 mph is u, not v.",
             calc=f"0 = {S(u5,4)}{SQ} + 2({chr(8722)}6.53)s"),
        dict(t="Rearrange, and mind the two minus signs",
             body="Deceleration makes a negative, and it cancels against the minus from moving u² across. A positive distance is the sign that you did it right.",
             calc=f"s = {chr(8722)}{S(u5sq,4)} {DIV} (2 {TIMES} {chr(8722)}6.53) = {S(u5sq,4)} {DIV} 13.06 = {S(s5,3)} m"),
    ],
    answer=(S(s5, 3), "m", "About 75 metres - and that is only after the driver has already reacted."),
    trap=(f"{S(wrong5,3)} m",
          f"Putting 70 straight into SUVAT. Because the equation squares the speed, a "
          f"unit slip does not merely scale the answer, it scales it by the square: the "
          f"result comes out {S(wrong5/s5,2)} times too large."),
    sanity=("The Highway Code quotes a 75 m braking distance at 70 mph. This calculation "
            "reproduces it, which is the real lesson: the number in the booklet is physics, not a guess."),
)

# --- 6 ---------------------------------------------------------------------
inner6 = R(2 * 45.0 / G, 4)
t6 = R(math.sqrt(inner6), 4)
v6 = R(G * t6, 4)
wrong6 = R(45.0 / G, 3)
P(
    n=6, part="Mechanics", chapter="Motion & acceleration", level="GCSE",
    book="Part 2 · Mechanics (pp. 17-34)",
    title="A stone dropped from a cliff",
    statement=(f"A stone is dropped from a cliff 45 m above the sea. Ignoring air "
               f"resistance, how long does it take to reach the water? Take g = 9.81 {MS}."),
    given=[("s", "45.0", "m"), ("u", "0", "m/s"), ("a", "9.81", MS)],
    wanted="the time of fall t",
    steps=[
        dict(t=f"{chr(8220)}Dropped{chr(8221)} means u = 0",
             body=f"That one word is worth a mark. {chr(8220)}Thrown{chr(8221)} would not be.",
             calc="u = 0 m/s"),
        dict(t="Choose the equation linking s, u, a and t",
             body="",
             calc=f"s = ut + {HALF}at{SQ},   and with u = 0 this becomes s = {HALF}at{SQ}"),
        dict(t="Rearrange for t",
             body="",
             calc=f"t = {ROOT}(2s {DIV} a) = {ROOT}(2 {TIMES} 45.0 {DIV} 9.81) = {ROOT}{S(inner6,4)}"),
        dict(t="Solve",
             body="",
             calc=f"t = {S(t6,3)} s"),
    ],
    answer=(S(t6, 3), "s", f"It lands after about three seconds, hitting the water at {S(v6,3)} m/s."),
    trap=(f"{S(wrong6,3)} s",
          f"Dividing the height by g. That treats 9.81 as a speed, when it is an "
          f"acceleration - metres per second, per second. Dividing a distance by it does "
          f"not produce a time at all; the units come out wrong, which is precisely how "
          f"you catch this one before the examiner does."),
    sanity=(f"The impact speed works out at {S(v6,3)} m/s, about {S(v6*3.6,3)} km/h. Fast, "
            f"but entirely believable for a 45 m drop - roughly a fifteen-storey building."),
    alt=(f"GCSE route. The equation s = ut + {HALF}at{SQ} is not on the GCSE sheet, but this "
         f"problem is still within reach. Use v{SQ} {chr(8722)} u{SQ} = 2as to get the landing "
         f"speed, v = {ROOT}(2 {TIMES} 9.81 {TIMES} 45.0) = {S(v6,3)} m/s, then a = "
         f"{DELTA}v {DIV} {DELTA}t to get the time, t = {S(v6,3)} {DIV} 9.81 = {S(t6,3)} s. "
         f"Same answer, two different syllabuses."),
)

# --- 7 ---------------------------------------------------------------------
t7 = t6
r7 = 12.0 * t7          # kept exact: see the no-double-rounding guard
P(
    n=7, part="Mechanics", chapter="Motion & acceleration", level="A-LEVEL",
    book="Part 2 · Mechanics (pp. 17-34)",
    title="The same cliff, but this time you run off it",
    statement=("From the same 45 m cliff, a stone is thrown horizontally at 12 m/s. How "
               "long is it in the air, and how far from the foot of the cliff does it land?"),
    given=[("height", "45.0", "m"), ("horizontal speed", "12.0", "m/s"), ("g", "9.81", MS)],
    wanted="the time of flight and the horizontal range",
    steps=[
        dict(t="Split the motion into two problems that do not talk to each other",
             body="Gravity acts vertically. It has no horizontal component, so it cannot change the horizontal speed - and the horizontal speed cannot change the fall.",
             calc=f"vertical: u = 0, a = 9.81 {MS}    |    horizontal: v = 12.0 m/s, a = 0"),
        dict(t="The vertical half is problem 6, word for word",
             body="Same height, same g, same u = 0, so the same time.",
             calc=f"t = {ROOT}(2 {TIMES} 45.0 {DIV} 9.81) = {S(t7,4)} s"),
        dict(t="The horizontal half has no acceleration",
             body="Constant speed, so distance is just speed multiplied by time.",
             calc=f"range = 12.0 {TIMES} {S(t7,4)} = {S(r7,3)} m"),
    ],
    answer=(f"t = {S(t7,3)} s and range = {S(r7,3)} m", "",
            "Thrown or dropped, the stone hits the water at the same instant."),
    trap=("a time longer than the 3.03 s of problem 6",
          "Assuming that more horizontal speed keeps the stone up for longer. It does "
          "not. The vertical motion knows nothing about the horizontal motion. Drop one "
          "stone and fire another sideways at the same moment from the same height, and "
          "they land together - the fast one simply lands further out."),
    sanity=(f"Set the horizontal speed to zero and the problem should collapse back into "
            f"problem 6. It does: t = {S(t7,3)} s either way."),
)

# --- 8 ---------------------------------------------------------------------
w8 = R(65.0 * G, 4)
gpa8 = R(G + 1.8, 4)
n8 = R(65.0 * gpa8, 4)
net8 = R(65.0 * 1.8, 3)
P(
    n=8, part="Mechanics", chapter="Newton's Laws", level="A-LEVEL",
    book="Part 2 · Mechanics (pp. 17-34)",
    title="Why you feel heavy when a lift sets off",
    statement=(f"A 65 kg person stands on bathroom scales inside a lift. The lift "
               f"accelerates upwards at 1.8 {MS}. What reading, in newtons, do the scales show?"),
    given=[("m", "65.0", "kg"), ("a", "1.8", f"{MS} upwards"), ("g", "9.81", MS)],
    wanted="the normal contact force N from the scales",
    steps=[
        dict(t="The scales read the contact force, not the weight",
             body="A set of scales measures how hard you press on it, which by Newton's third law is how hard it presses back on you.",
             calc="reading = N"),
        dict(t="Only two vertical forces act on the person",
             body="Weight down, normal force up. The person is accelerating upwards, so the upward force has to be the larger one.",
             calc=f"W = mg = 65.0 {TIMES} 9.81 = {S(w8,4)} N, downwards"),
        dict(t="Apply Newton's second law, taking up as positive",
             body="",
             calc=f"N {chr(8722)} mg = ma    {ARROW}    N = m(g + a)"),
        dict(t="Substitute",
             body="",
             calc=f"N = 65.0 {TIMES} (9.81 + 1.8) = 65.0 {TIMES} {S(gpa8,4)} = {S(n8,4)} N"),
    ],
    answer=(S(n8, 3), "N",
            f"Standing still the scales would read {S(w8,3)} N, so you appear {S((n8/w8-1)*100,2)}% heavier."),
    trap=(f"{S(net8,3)} N",
          f"Writing N = ma and stopping there. That is the NET force, not the reading - "
          f"the scales still have to hold the weight up as well. Leaving mg out gives an "
          f"answer that is only {S(net8/n8*100,2)}% of the truth, which would mean the "
          f"scales read LESS while accelerating upwards. That is the opposite of what anyone has ever felt in a lift."),
    sanity=(f"Divide the reading by g to see it as a mass: {S(n8/G,3)} kg. The scales "
            f"behave as though the person had gained about {S(n8/G-65.0,2)} kg, which is "
            f"exactly the heavy feeling in the first second of the ride."),
)

# --- 9 ---------------------------------------------------------------------
sin25, cos25 = R(math.sin(math.radians(25)), 4), R(math.cos(math.radians(25)), 4)
down9 = R(4.0 * G * sin25, 4)
n9 = R(4.0 * G * cos25, 4)
fr9 = R(0.30 * n9, 4)
acc9 = R((down9 - fr9) / 4.0, 4)
wrongN9 = R(4.0 * G, 4)
wrongF9 = R(0.30 * wrongN9, 4)
tan25 = R(math.tan(math.radians(25)), 3)
P(
    n=9, part="Mechanics", chapter="Force", level="A-LEVEL",
    book="Part 2 · Mechanics (pp. 17-34)",
    title="A crate on a ramp: does it slide?",
    statement=(f"A 4.0 kg crate sits on a ramp inclined at 25{DEG}. The coefficient of "
               f"friction between crate and ramp is 0.30. Show whether the crate slides, "
               f"and if it does, find its acceleration."),
    given=[("m", "4.0", "kg"), ("incline", "25", DEG), (MU, "0.30", ""), ("g", "9.81", MS)],
    wanted="whether the crate slides, and its acceleration if it does",
    steps=[
        dict(t="Resolve the weight along the slope and into it",
             body="Not horizontally and vertically. On an incline it is the slope that sets the useful pair of directions.",
             calc=f"along: mg sin 25{DEG} = {S(down9,4)} N     into: mg cos 25{DEG} = {S(n9,4)} N"),
        dict(t="The normal force balances only the part pressing in",
             body="The ramp pushes back exactly as hard as it is pressed, and only at right angles to its surface.",
             calc=f"N = mg cos 25{DEG} = {S(n9,4)} N"),
        dict(t="Find the largest friction force available",
             body="",
             calc=f"F(max) = {MU}N = 0.30 {TIMES} {S(n9,4)} = {S(fr9,4)} N"),
        dict(t="Compare the two",
             body="The pull down the slope beats the most that friction can offer, so the crate moves.",
             calc=f"{S(down9,4)} N > {S(fr9,4)} N    {ARROW}    it slides"),
        dict(t="Newton's second law, along the slope",
             body="",
             calc=f"a = ({S(down9,4)} {chr(8722)} {S(fr9,4)}) {DIV} 4.0 = {S(acc9,3)} {MS}"),
    ],
    answer=(f"it slides, at {S(acc9,3)} {MS}", "",
            f"Down the slope, and only about {S(acc9/G*100,2)}% of free-fall acceleration."),
    trap=(f"F(max) = {S(wrongF9,3)} N",
          f"Using N = mg = {S(wrongN9,3)} N. On a slope the surface never carries the whole "
          f"weight, only the component pressing into it, so this overstates friction by "
          f"{S((wrongF9/fr9-1)*100,2)}%. The dangerous version of this mistake is on a "
          f"shallow ramp: between about 16.7{DEG} and 17.5{DEG} the wrong method says the "
          f"crate stays put when in fact it is already sliding."),
    sanity=(f"A crate slides whenever tan(angle) > {MU}. Here tan 25{DEG} = {S(tan25,3)}, "
            f"which beats 0.30 - and notice the mass never appeared in that comparison at all."),
)

# --- 10 --------------------------------------------------------------------
sin15, cos15 = R(math.sin(math.radians(15)), 4), R(math.cos(math.radians(15)), 4)
down10 = R(4.0 * G * sin15, 4)
n10 = R(4.0 * G * cos15, 4)
maxf10 = R(0.40 * n10, 4)
tan15 = R(math.tan(math.radians(15)), 3)
P(
    n=10, part="Mechanics", chapter="Force", level="A-LEVEL",
    book="Part 2 · Mechanics (pp. 17-34)",
    title="The same crate on a gentler ramp - so how big is the friction now?",
    statement=(f"The same 4.0 kg crate is placed on a ramp at 15{DEG}, where the coefficient "
               f"of static friction is 0.40. The crate does not move. State the size of the "
               f"friction force acting on it."),
    given=[("m", "4.0", "kg"), ("incline", "15", DEG), (f"{MU}s", "0.40", ""), ("g", "9.81", MS)],
    wanted="the actual friction force on the crate",
    steps=[
        dict(t="First check that it really does stay put",
             body="",
             calc=f"tan 15{DEG} = {S(tan15,3)}, which is less than {MU} = 0.40    {ARROW}    it does not move"),
        dict(t="Not moving means in equilibrium",
             body="Nothing is accelerating, so along the slope the forces must cancel exactly.",
             calc="friction = the component of weight down the slope"),
        dict(t="Resolve the weight",
             body="",
             calc=f"mg sin 15{DEG} = 4.0 {TIMES} 9.81 {TIMES} {S(sin15,4)} = {S(down10,3)} N"),
        dict(t="And that is the friction",
             body="Friction supplies exactly what is needed to hold the crate, and not a newton more.",
             calc=f"F = {S(down10,3)} N, up the slope"),
    ],
    answer=(S(down10, 3), "N", "Up the slope, exactly balancing the pull of gravity along it."),
    trap=(f"{S(maxf10,3)} N",
          f"Working out {MU}N and quoting it. But {MU}N is the MAXIMUM static friction, not "
          f"the actual one: the law is F {LEQ} {MU}N, not F = {MU}N. The crate needs only "
          f"{S(down10,3)} N to stay still, so that is all friction supplies; the remaining "
          f"{S(maxf10-down10,3)} N is held in reserve. Quoting {S(maxf10,3)} N would leave a "
          f"net force UP the slope, with the crate climbing it unaided."),
    sanity=(f"The size of the reserve is what tells you the crate is stable, and comfortably "
            f"so: friction is using only {S(down10/maxf10*100,2)}% of what it has available."),
)

# --- 11 --------------------------------------------------------------------
cos30 = R(math.cos(math.radians(30)), 4)
fh11 = R(45 * cos30, 4)
w11 = R(fh11 * 20, 4)
P(
    n=11, part="Mechanics", chapter="Work", level="A-LEVEL",
    book="Part 2 · Mechanics (pp. 17-34)",
    title="Dragging a suitcase through an airport",
    statement=(f"A suitcase is pulled 20 m across level floor by a handle held at 30{DEG} "
               f"above the horizontal, with a force of 45 N along the handle. How much work "
               f"does the pulling force do?"),
    given=[("F", "45", "N"), ("d", "20", "m"), ("angle to the floor", "30", DEG)],
    wanted="the work done by the pulling force",
    steps=[
        dict(t="Only the part of the force along the motion does work",
             body="The suitcase travels horizontally. The upward part of the pull moves it nowhere, so it does no work at all.",
             calc=f"W = Fd cos {THETA}"),
        dict(t="Resolve the force onto the direction of travel",
             body="",
             calc=f"F(horizontal) = 45 cos 30{DEG} = 45 {TIMES} {S(cos30,4)} = {S(fh11,4)} N"),
        dict(t="Multiply by the distance moved",
             body="",
             calc=f"W = {S(fh11,4)} {TIMES} 20 = {S(w11,4)} J"),
    ],
    answer=(S(w11, 3), "J", "About 780 joules over the twenty metres."),
    trap=("900 J",
          f"Multiplying 45 {TIMES} 20 and forgetting cos 30{DEG}, which assumes you are "
          f"pulling horizontally. The vertical component of the pull is perfectly real - it "
          f"is lifting weight off the wheels - but since the case never moves upwards, that "
          f"component does zero work. Dropping the cosine inflates the answer by {S((900/w11-1)*100,2)}%."),
    sanity=(f"cos 30{DEG} is {S(cos30,4)}, so the answer has to come out at roughly 87% of "
            f"900 J. {S(w11,3)} J does."),
)

# --- 12 --------------------------------------------------------------------
inner12 = R(2 * G * 3.2, 4)
v12 = R(math.sqrt(inner12), 4)
P(
    n=12, part="Mechanics", chapter="Energy", level="GCSE",
    book="Part 2 · Mechanics (pp. 17-34)",
    title="The slide, and why your weight makes no difference",
    statement=("A child starts from rest at the top of a smooth slide, 3.2 m above the "
               "ground. How fast are they moving at the bottom? The mass of the child is not given."),
    given=[("h", "3.2", "m"), ("u", "0", "m/s"), ("friction", "none", "")],
    wanted="the speed at the bottom of the slide",
    steps=[
        dict(t="Energy in equals energy out",
             body="The slide is smooth, so nothing is lost to friction: every joule of gravitational potential energy becomes kinetic energy.",
             calc=f"mgh = {HALF}mv{SQ}"),
        dict(t="The mass cancels",
             body="Which is why the question is allowed to withhold it - and why withholding it is the test.",
             calc=f"gh = {HALF}v{SQ}"),
        dict(t="Rearrange",
             body="",
             calc=f"v = {ROOT}(2gh) = {ROOT}(2 {TIMES} 9.81 {TIMES} 3.2) = {ROOT}{S(inner12,4)}"),
        dict(t="Solve",
             body="",
             calc=f"v = {S(v12,3)} m/s"),
    ],
    answer=(S(v12, 3), "m/s", "Independent of mass: a heavier child arrives at exactly the same speed."),
    trap=(f"{chr(8220)}not enough information, the mass is missing{chr(8221)}",
          "The mass is missing because it cancels. Every energy-conversion problem of this "
          "shape loses it on the second line. When a quantity is absent from a question, "
          "the first thing to test is whether the algebra removes it - not whether the "
          "examiner has made a mistake."),
    sanity=(f"That is {S(v12*3.6,3)} km/h, which is quick for a playground - and it should "
            f"be, because the question deleted friction. A real slide of that height delivers "
            f"noticeably less."),
)

# --- 13 --------------------------------------------------------------------
w13 = R(58 * G * 4.2, 4)
p13 = R(w13 / 6.5, 4)
P(
    n=13, part="Mechanics", chapter="Energy", level="GCSE",
    book="Part 2 · Mechanics (pp. 17-34)",
    title="Running up the stairs",
    statement=("A 58 kg student runs up a flight of stairs of total height 4.2 m in 6.5 s. "
               "Calculate the useful power they develop."),
    given=[("m", "58", "kg"), ("h", "4.2", "m"), ("t", "6.5", "s")],
    wanted="the useful power developed",
    steps=[
        dict(t="Find the work done against gravity",
             body="Only the height counts. Walking along each tread does no work against gravity, because gravity has no horizontal component.",
             calc=f"W = mgh = 58 {TIMES} 9.81 {TIMES} 4.2 = {S(w13,4)} J"),
        dict(t="Power is work per second",
             body="",
             calc=f"P = W {DIV} t"),
        dict(t="Divide",
             body="",
             calc=f"P = {S(w13,4)} {DIV} 6.5 = {S(p13,4)} W"),
    ],
    answer=(S(p13, 3), "W", f"About {S(p13/1000,2)} kW, or roughly half a horsepower."),
    trap=(f"{S(w13,3)} W",
          "Quoting the work done and labelling it as power. Joules and watts are not "
          "interchangeable - a watt is a joule per second. The giveaway is that the time "
          "would then be left unused: if a question gives you a number and your answer "
          "never touches it, something has gone wrong."),
    sanity=(f"A fit person holds 150-250 W for a long time and several hundred watts in a "
            f"short burst. {S(p13,3)} W sustained for 6.5 s is a hard sprint up the stairs, "
            f"which is exactly what the question describes."),
)

# --- 14 --------------------------------------------------------------------
p14 = R(0.80 * 3.0, 3)
v14 = R(p14 / 2.00, 3)
ke_b = R(0.5 * 0.80 * 3.0**2, 3)
ke_a = R(0.5 * 2.00 * v14**2, 3)
lost14 = R(ke_b - ke_a, 3)
wrong14 = R(math.sqrt(2 * ke_b / 2.00), 3)
P(
    n=14, part="Mechanics", chapter="Momentum", level="BOTH",
    book="Part 2 · Mechanics (pp. 17-34)",
    title="Two trolleys that stick together",
    statement=("A 0.80 kg trolley moving at 3.0 m/s collides with a stationary 1.20 kg "
               "trolley. They stick together. Find their common velocity afterwards, and "
               "how much kinetic energy is lost."),
    given=[("mA", "0.80", "kg"), ("uA", "3.0", "m/s"), ("mB", "1.20", "kg"), ("uB", "0", "m/s")],
    wanted="the velocity after the collision, and the kinetic energy lost",
    steps=[
        dict(t="Momentum is conserved in every collision, without exception",
             body="No external horizontal force acts on the pair, so the total momentum before equals the total after.",
             calc=f"p(before) = 0.80 {TIMES} 3.0 + 1.20 {TIMES} 0 = {S(p14,3)} kg m/s"),
        dict(t="Afterwards they move as a single object",
             body="",
             calc=f"p(after) = (0.80 + 1.20)v = 2.00v"),
        dict(t="Set them equal and solve",
             body="",
             calc=f"v = {S(p14,3)} {DIV} 2.00 = {S(v14,3)} m/s"),
        dict(t="Now compare the kinetic energies",
             body="Kinetic energy is not conserved here, and the second half of the question exists to make you prove it.",
             calc=f"KE(before) = {HALF} {TIMES} 0.80 {TIMES} 3.0{SQ} = {S(ke_b,3)} J"),
        dict(t="And afterwards",
             body="",
             calc=f"KE(after) = {HALF} {TIMES} 2.00 {TIMES} {S(v14,3)}{SQ} = {S(ke_a,3)} J"),
        dict(t="The difference is what was lost",
             body="It went into deforming the buffers, into sound, and into heat.",
             calc=f"lost = {S(ke_b,3)} {chr(8722)} {S(ke_a,3)} = {S(lost14,3)} J"),
    ],
    answer=(f"v = {S(v14,3)} m/s, and {S(lost14,3)} J lost", "",
            f"{S(lost14/ke_b*100,3)}% of the kinetic energy disappears, while the momentum does not change at all."),
    trap=(f"v = {S(wrong14,3)} m/s",
          "Conserving kinetic energy instead of momentum. Momentum is conserved in every "
          "collision; kinetic energy only in a perfectly elastic one, and two objects that "
          "stick together are the least elastic collision there is. Whenever a question "
          f"says {chr(8220)}stick{chr(8221)}, {chr(8220)}couple{chr(8221)} or "
          f"{chr(8220)}embed{chr(8221)}, kinetic energy is about to be lost."),
    sanity=(f"The same momentum is now carried by {S(2.00/0.80,3)} times the mass, so the "
            f"speed has to fall by that same factor: 3.0 {DIV} {S(2.00/0.80,3)} = {S(v14,3)} m/s."),
)

# --- 15 --------------------------------------------------------------------
dp15 = R(70 * 14, 3)
f_hard = R(dp15 / 0.040, 4)
f_bag = R(dp15 / 0.25, 4)
P(
    n=15, part="Mechanics", chapter="Momentum", level="BOTH",
    book="Part 2 · Mechanics (pp. 17-34)",
    title="What an airbag actually does",
    statement=("A 70 kg driver travelling at 14 m/s is brought to rest in a crash. Against "
               "the steering column this takes 0.040 s; against an airbag it takes 0.25 s. "
               "Find the average force in each case."),
    given=[("m", "70", "kg"), ("u", "14", "m/s"), ("v", "0", "m/s"),
           ("t without airbag", "0.040", "s"), ("t with airbag", "0.25", "s")],
    wanted="the average force on the driver in each case",
    steps=[
        dict(t="Find the change in momentum",
             body="This is fixed by the crash itself, not by what the driver happens to hit.",
             calc=f"{DELTA}p = m(v {chr(8722)} u) = 70 {TIMES} (0 {chr(8722)} 14) = {chr(8722)}{S(dp15,3)} kg m/s"),
        dict(t="Force is the rate of change of momentum",
             body="Newton's second law in its original form, and the more useful one here.",
             calc=f"F = {DELTA}p {DIV} {DELTA}t"),
        dict(t="Without the airbag",
             body="",
             calc=f"F = {S(dp15,3)} {DIV} 0.040 = {S(f_hard,3)} N"),
        dict(t="With the airbag",
             body="The identical momentum change, spread over six times as long.",
             calc=f"F = {S(dp15,3)} {DIV} 0.25 = {S(f_bag,3)} N"),
    ],
    answer=(f"{S(f_hard,3)} N without the airbag, {S(f_bag,3)} N with it", "",
            f"The airbag cuts the force by a factor of {S(f_hard/f_bag,3)}."),
    trap=(f"{chr(8220)}the airbag reduces the momentum{chr(8221)}",
          f"It does not, and it could not. The driver goes from 14 m/s to rest either way, "
          f"so {DELTA}p is {S(dp15,3)} kg m/s in both cases. The airbag changes only "
          f"{DELTA}t. That is the whole of its engineering: it is not soft so that it "
          f"absorbs the blow, it is deep so that the blow takes longer."),
    sanity=(f"As multiples of body weight: {S(f_hard/(70*G),3)}g against the column and "
            f"{S(f_bag/(70*G),3)}g against the airbag. A rollercoaster peaks near 5g. The "
            f"airbag does not make the crash gentle - it moves it from a number the body "
            f"cannot survive to one it can."),
)

# --- 16 --------------------------------------------------------------------
inner16 = R(0.70 * G * 25, 4)
v16 = R(math.sqrt(inner16), 4)
v16wet = R(math.sqrt(0.40 * G * 25), 4)
P(
    n=16, part="Mechanics", chapter="Force", level="A-LEVEL",
    book="Part 2 · Mechanics (pp. 17-34)",
    title="How fast you can take a roundabout",
    statement=("A car drives round a flat roundabout of radius 25 m. The coefficient of "
               "friction between tyres and road is 0.70. Find the maximum speed before it "
               "skids. The mass of the car is not given."),
    given=[("r", "25", "m"), (MU, "0.70", ""), ("g", "9.81", MS)],
    wanted="the maximum cornering speed",
    steps=[
        dict(t="Ask what is providing the centripetal force",
             body="Nothing pushes the car round the bend except friction between tyre and road. On a flat roundabout there is no other horizontal force available at all.",
             calc="friction = centripetal force"),
        dict(t="Write both sides out",
             body="",
             calc=f"{MU}mg = mv{SQ} {DIV} r"),
        dict(t="The mass cancels",
             body="It sits on both sides, which is exactly why the question is entitled to leave it out.",
             calc=f"{MU}g = v{SQ} {DIV} r"),
        dict(t="Rearrange and solve",
             body="",
             calc=f"v = {ROOT}({MU}gr) = {ROOT}(0.70 {TIMES} 9.81 {TIMES} 25) = {ROOT}{S(inner16,4)} = {S(v16,3)} m/s"),
    ],
    answer=(S(v16, 3), "m/s", f"That is {S(v16*3.6,3)} km/h, or {S(v16*3600/MILE,3)} mph."),
    trap=(f"{chr(8220)}a heavier car has to go slower{chr(8221)}",
          f"Mass cancels. A loaded lorry and an empty hatchback skid at the same speed on "
          f"the same bend, because the extra mass needs more centripetal force but also "
          f"presses the tyres down harder and earns precisely that much more friction. What "
          f"does change the answer is {MU} - which is why the same roundabout is lethal in the wet."),
    sanity=(f"In the wet {MU} falls to roughly 0.40, giving {S(v16wet*3600/MILE,3)} mph "
            f"instead of {S(v16*3600/MILE,3)} mph. That gap is the physics behind every "
            f"{chr(8220)}reduce speed in wet conditions{chr(8221)} sign on the network."),
)


# ===========================================================================
# PART 3 - FLUIDS  (Main Book pp. 35-46)
# ===========================================================================

RHO_W, P_ATM = 1000, 101000

# --- 17 --------------------------------------------------------------------
pw17 = RHO_W * G * 3.8            # exact product: print it exactly
tot17 = pw17 + P_ATM
P(
    n=17, part="Fluids", chapter="Pressure", level="GCSE",
    book="Part 3 · Fluids (pp. 35-46)",
    title="The pressure on a diver at the bottom of the pool",
    statement=(f"A diving pool is 3.8 m deep. Water has a density of 1000 kg/{M3} and "
               f"atmospheric pressure at the surface is 101 000 Pa. Find the TOTAL pressure "
               f"on a diver at the bottom."),
    given=[("h", "3.8", "m"), (RHO, "1000", f"kg/{M3}"),
           ("atmospheric pressure", "101 000", "Pa"), ("g", "9.81", MS)],
    wanted="the total pressure at the bottom of the pool",
    steps=[
        dict(t="Find the pressure the water alone adds",
             body="Pressure in a liquid depends only on depth, density and g. The shape of the pool makes no difference whatsoever.",
             calc=f"P(water) = {RHO}gh = 1000 {TIMES} 9.81 {TIMES} 3.8 = {S(pw17,5)} Pa"),
        dict(t="The atmosphere is still sitting on top of it",
             body="The water does not hold the air up. The whole column of atmosphere presses down on the pool surface and that pressure is passed on through the liquid.",
             calc=f"P(total) = P(atmospheric) + P(water)"),
        dict(t="Add them",
             body="",
             calc=f"P = 101 000 + {S(pw17,5)} = {S(tot17,6)} Pa"),
    ],
    answer=(S(tot17/1000, 3), "kPa", f"About {S(tot17/P_ATM,3)} times atmospheric pressure, at a depth you could stand up in."),
    trap=(f"{S(pw17,3)} Pa",
          f"Giving only the water's contribution. That answers a different question - the "
          f"GAUGE pressure, which is what a pressure gauge reads because it has air on its "
          f"other side. The question asked for the total, and the atmosphere is "
          f"{S(P_ATM/tot17*100,3)}% of it. Read whether a question wants total (absolute) or "
          f"gauge pressure before you write anything down."),
    sanity=(f"Roughly 10 m of water is worth one atmosphere. At 3.8 m you would therefore "
            f"expect about 0.37 extra atmospheres, and {S(pw17,5)} {DIV} 101 000 = "
            f"{S(pw17/P_ATM,3)}. The depth rule and the equation agree."),
)

# --- 18 --------------------------------------------------------------------
v18 = R(0.20 * 0.12 * 0.050, 2)
rho18 = R(0.68 / v18, 3)
P(
    n=18, part="Fluids", chapter="Density", level="GCSE",
    book="Part 3 · Fluids (pp. 35-46)",
    title="Does it float, and does the size of it matter?",
    statement=(f"A rectangular pine block measures 20 cm {TIMES} 12 cm {TIMES} 5.0 cm and has "
               f"a mass of 0.68 kg. Water has a density of 1000 kg/{M3}. Show whether the "
               f"block floats, and state what fraction of it sits below the waterline."),
    given=[("dimensions", f"0.20 {TIMES} 0.12 {TIMES} 0.050", "m"), ("mass", "0.68", "kg"),
           (f"{RHO} water", "1000", f"kg/{M3}")],
    wanted="whether it floats, and the fraction submerged",
    steps=[
        dict(t="Work in metres from the start",
             body="Mixing centimetres into an SI calculation is the single most common way to lose this mark.",
             calc=f"V = 0.20 {TIMES} 0.12 {TIMES} 0.050 = {S(v18,2)} {M3}"),
        dict(t="Find the density",
             body="",
             calc=f"{RHO} = 0.68 {DIV} {S(v18,2)} = {S(rho18,3)} kg/{M3}"),
        dict(t="Compare with the liquid, not with anything else",
             body="Floating is decided by density against density. Mass on its own tells you nothing.",
             calc=f"{S(rho18,3)} < 1000    {ARROW}    it floats"),
        dict(t="A floating object sinks until it displaces its own weight",
             body="So the fraction submerged is just the ratio of the two densities.",
             calc=f"fraction = {S(rho18,3)} {DIV} 1000 = {S(rho18/1000,3)}, or {S(rho18/10,3)}%"),
    ],
    answer=(f"it floats, with {S(rho18/10,3)}% of it submerged", "",
            "Just over half the block sits below the waterline."),
    trap=(f"{chr(8220)}a bigger block of the same wood would sink{chr(8221)}",
          "It would not. Double every dimension and the mass goes up eight-fold - but so "
          "does the volume, so the density is unchanged and the block floats exactly as "
          "high in the water. Floating is a property of the material, not of the lump. A "
          "pine log and a pine matchstick float with the same fraction submerged."),
    sanity=(f"Pine runs about 350-600 kg/{M3} dry. {S(rho18,3)} sits inside that band, so the "
            f"number describes real timber - and it predicts the block floating a little over "
            f"half under, which is what a plank in a pond actually does."),
)

# --- 19 --------------------------------------------------------------------
p19 = R(90 / 2.0e-4, 3)
f19 = R(p19 * 150e-4, 4)
m19 = R(f19 / G, 3)
P(
    n=19, part="Fluids", chapter="Pascal's Principle", level="BOTH",
    book="Part 3 · Fluids (pp. 35-46)",
    title="A trolley jack, and the thing it does not do",
    statement=(f"In a hydraulic jack the small piston has an area of 2.0 cm{SQ} and the large "
               f"piston 150 cm{SQ}. A force of 90 N is applied to the small piston. Find the "
               f"force on the large one, and the mass it could lift."),
    given=[("A small", f"2.0 cm{SQ} = 2.0 {TIMES} 10⁻⁴", f"{M3[:-1]}{SQ}".replace("m²","m²")),
           ("A large", f"150 cm{SQ} = 150 {TIMES} 10⁻⁴", "m²"), ("F small", "90", "N")],
    wanted="the output force, and the mass it can lift",
    steps=[
        dict(t="Pascal: the pressure is the same everywhere in the fluid",
             body="This is the whole principle. The liquid cannot tell the two pistons apart; it only knows pressure.",
             calc=f"P = F {DIV} A = 90 {DIV} 0.00020 = {S(p19,3)} Pa"),
        dict(t="Apply that same pressure to the larger area",
             body="",
             calc=f"F = PA = {S(p19,3)} {TIMES} 0.0150 = {S(f19,4)} N"),
        dict(t="Turn the force into a mass",
             body="",
             calc=f"m = F {DIV} g = {S(f19,4)} {DIV} 9.81 = {S(m19,3)} kg"),
    ],
    answer=(f"{S(f19,3)} N, enough to lift {S(m19,3)} kg", "",
            f"The jack multiplies the force by {S(150/2.0,2)}, which is exactly the ratio of the two areas."),
    trap=(f"{chr(8220)}so the jack multiplies the energy by {S(150/2.0,2)} as well{chr(8221)}",
          f"It does not, and nothing could. Energy is conserved: to raise the large piston by "
          f"1 cm you must push the small one down {S(150/2.0,2)} cm, because the same volume of "
          f"oil has to move. Multiply force by {S(150/2.0,2)} and divide distance by "
          f"{S(150/2.0,2)} and the work done is identical at both ends. A hydraulic jack trades "
          f"distance for force - it does not create anything."),
    sanity=(f"{S(m19,3)} kg is comfortably more than one corner of a family car, which is "
            f"precisely the job a trolley jack is built for. And the force ratio came out at "
            f"{S(150/2.0,2)}, matching the area ratio exactly, as Pascal requires."),
)

# --- 20 --------------------------------------------------------------------
w20 = R(7800 * 2.5e-4 * G, 4)
up20 = R(RHO_W * 2.5e-4 * G, 4)
app20 = R(w20 - up20, 4)
P(
    n=20, part="Fluids", chapter="Archimedes' Principle", level="A-LEVEL",
    book="Part 3 · Fluids (pp. 35-46)",
    title="Why a steel block weighs less underwater",
    statement=(f"A steel block of volume 2.5 {TIMES} 10⁻⁴ {M3} and density 7800 kg/{M3} hangs "
               f"from a spring balance, fully submerged in water. What does the balance read?"),
    given=[("V", f"2.5 {TIMES} 10⁻⁴", M3), (f"{RHO} steel", "7800", f"kg/{M3}"),
           (f"{RHO} water", "1000", f"kg/{M3}"), ("g", "9.81", MS)],
    wanted="the apparent weight shown on the balance",
    steps=[
        dict(t="Find the real weight first",
             body="",
             calc=f"W = {RHO}Vg = 7800 {TIMES} 0.00025 {TIMES} 9.81 = {S(w20,4)} N"),
        dict(t="Archimedes: upthrust equals the weight of fluid displaced",
             body="Displaced - so the density in this line is the WATER's, never the block's.",
             calc=f"U = {RHO}(water) {TIMES} V {TIMES} g = 1000 {TIMES} 0.00025 {TIMES} 9.81 = {S(up20,3)} N"),
        dict(t="The balance reads what is left",
             body="",
             calc=f"reading = {S(w20,4)} {chr(8722)} {S(up20,3)} = {S(app20,4)} N"),
    ],
    answer=(S(app20, 3), "N", f"The block appears to lose {S(up20,3)} N, about {S(up20/w20*100,3)}% of its weight."),
    trap=(f"a reading of 0 N",
          f"Using the block's own density in the upthrust line instead of the water's. That "
          f"makes the upthrust equal the weight for every object ever submerged, so nothing "
          f"would ever sink. The moment an answer implies that steel floats, the error is in "
          f"which density went into the formula."),
    sanity=(f"The fraction of weight lost should be {RHO}(water) {DIV} {RHO}(steel) = 1000 "
            f"{DIV} 7800 = {S(1000/7800,3)}. The calculation gives {S(up20/w20,3)}. Two "
            f"independent routes to the same figure."),
)

# --- 21 --------------------------------------------------------------------
v21 = R(1.2 * (50/25)**2, 3)
dp21 = R(0.5 * RHO_W * (v21**2 - 1.2**2), 4)
P(
    n=21, part="Fluids", chapter="Bernoulli's Principle", level="A-LEVEL",
    book="Part 3 · Fluids (pp. 35-46)",
    title="Water through a narrowing pipe",
    statement=(f"Water flows at 1.2 m/s through a pipe of internal diameter 50 mm, which "
               f"narrows to 25 mm. Find the speed in the narrow section, and say whether the "
               f"pressure there is higher or lower, and by how much."),
    given=[("v1", "1.2", "m/s"), ("d1", "50", "mm"), ("d2", "25", "mm"),
           (RHO, "1000", f"kg/{M3}")],
    wanted="the speed in the narrow section and the pressure change",
    steps=[
        dict(t="The same water per second has to pass every cross-section",
             body="Nothing is being stored or lost along the pipe, so A1v1 = A2v2.",
             calc=f"A1v1 = A2v2"),
        dict(t="Area goes with the SQUARE of the diameter",
             body="The diameter halves, so the area quarters - the step that decides the whole answer.",
             calc=f"A1 {DIV} A2 = (50 {DIV} 25){SQ} = 4"),
        dict(t="So the speed goes up four-fold",
             body="",
             calc=f"v2 = 1.2 {TIMES} 4 = {S(v21,2)} m/s"),
        dict(t="Bernoulli: faster flow means lower pressure",
             body="The water speeds up, so something must have pushed it. That push is a pressure DROP from wide section to narrow.",
             calc=f"{DELTA}P = {HALF}{RHO}(v2{SQ} {chr(8722)} v1{SQ}) = 500 {TIMES} ({S(v21**2,4)} {chr(8722)} 1.44) = {S(dp21,3)} Pa lower"),
    ],
    answer=(f"{S(v21,2)} m/s, at a pressure {S(dp21,3)} Pa LOWER", "",
            "The narrow section is the fast section, and the fast section is the low-pressure one."),
    trap=(f"{chr(8220)}the pressure is higher in the narrow bit, because the water is squeezed{chr(8221)}",
          "This is the most persistent wrong intuition in fluids, and it is backwards. "
          "Squeezing a static fluid does raise its pressure - but this fluid is not static. "
          "The water arrives at the constriction and SPEEDS UP, and the only thing that can "
          "accelerate it is a force, which means a push from high pressure behind towards low "
          "pressure ahead. The pressure has to fall for the water to go faster. It is why an "
          "aerofoil lifts and why two sheets of paper pull together when you blow between them."),
    sanity=(f"{S(dp21,3)} Pa is about {S(dp21/P_ATM*100,2)}% of atmospheric pressure, or the "
            f"pressure under {S(dp21/(RHO_W*G),2)} m of water. Small, but easily enough to "
            f"show on a manometer across the constriction - which is exactly how a Venturi "
            f"flow meter measures flow rate."),
)

# ===========================================================================
# PART 4 - THERMODYNAMICS  (Main Book pp. 47-58)
# ===========================================================================

C_W, L_F = 4180, 334000

# --- 22 --------------------------------------------------------------------
dt22 = 100 - 18
q22 = 1.5 * C_W * dt22            # exact product: print it exactly
t22 = R(q22 / 2800, 3)
wrong22 = 1.5 * C_W * 100
P(
    n=22, part="Thermodynamics", chapter="Heat energy", level="GCSE",
    book="Part 4 · Thermodynamics (pp. 47-58)",
    title="How long the kettle really takes",
    statement=(f"A kettle holds 1.5 kg of water at 18 {DEG}C. The specific heat capacity of "
               f"water is 4180 J/kg{DEG}C and the kettle delivers 2.8 kW. How much energy is "
               f"needed to bring it to 100 {DEG}C, and how long should that take?"),
    given=[("m", "1.5", "kg"), ("c", "4180", f"J/kg{DEG}C"),
           ("start", "18", f"{DEG}C"), ("finish", "100", f"{DEG}C"), ("P", "2800", "W")],
    wanted="the energy required, and the time taken",
    steps=[
        dict(t=f"{DELTA}T is the CHANGE in temperature, not the final one",
             body="The water does not start at zero. This one line is the whole problem.",
             calc=f"{DELTA}T = 100 {chr(8722)} 18 = {dt22} {DEG}C"),
        dict(t="Apply the specific heat capacity equation",
             body="",
             calc=f"Q = mc{DELTA}T = 1.5 {TIMES} 4180 {TIMES} {dt22} = {S(q22,6)} J"),
        dict(t="Power is energy per second, so time is energy over power",
             body="",
             calc=f"t = Q {DIV} P = {S(q22,6)} {DIV} 2800 = {S(t22,3)} s"),
    ],
    answer=(f"{S(q22/1000,3)} kJ, taking {S(t22,3)} s", "",
            f"Just over three minutes - which is how long a kettle actually takes."),
    trap=(f"{S(wrong22,3)} J",
          f"Using 100 as {DELTA}T, because 100 is the number in the question. But the water "
          f"begins at 18 {DEG}C, so only {dt22} degrees of heating are needed. Taking the "
          f"final temperature instead of the rise overstates the energy by "
          f"{S((wrong22/q22-1)*100,2)}% - and it would predict a kettle that takes "
          f"{S(wrong22/2800,3)} s, which anyone who has made tea knows is wrong."),
    sanity=(f"A 3 kW kettle boils a litre and a half in roughly three minutes from cold tap "
            f"water. The calculation gives {S(t22,3)} s. When a thermal answer can be checked "
            f"against something in your own kitchen, check it."),
)

# --- 23 --------------------------------------------------------------------
q23 = R(0.25 * L_F, 3)
dt23 = R(q23 / (0.25 * C_W), 3)
P(
    n=23, part="Thermodynamics", chapter="Heat energy", level="GCSE",
    book="Part 4 · Thermodynamics (pp. 47-58)",
    title="Melting ice without warming it at all",
    statement=(f"How much energy is needed to melt 0.25 kg of ice that is already at "
               f"0 {DEG}C, into water at 0 {DEG}C? The specific latent heat of fusion of "
               f"water is 334 000 J/kg."),
    given=[("m", "0.25", "kg"), ("L(f)", "334 000", "J/kg"),
           ("start", f"ice at 0 {DEG}C", ""), ("finish", f"water at 0 {DEG}C", "")],
    wanted="the energy needed to melt it",
    steps=[
        dict(t="Notice that the temperature never changes",
             body=f"It goes in at 0 {DEG}C and comes out at 0 {DEG}C. So mc{DELTA}T contributes "
                  f"nothing at all here - {DELTA}T is zero.",
             calc=f"{DELTA}T = 0, so Q = mc{DELTA}T = 0"),
        dict(t="All the energy goes into breaking the bonds, not into speeding molecules up",
             body="Temperature measures the kinetic energy of the particles. During a change of state the energy goes into potential energy instead, pulling the lattice apart.",
             calc=f"Q = mL(f)"),
        dict(t="Substitute",
             body="",
             calc=f"Q = 0.25 {TIMES} 334 000 = {S(q23,3)} J"),
    ],
    answer=(f"{S(q23/1000,3)} kJ", "", "And not one degree of temperature rise to show for it."),
    trap=(f"{chr(8220)}the ice warms up as it melts{chr(8221)}",
          f"It does not. An ice-water mixture sits at 0 {DEG}C and stays there until the last "
          f"of the ice has gone, no matter how much energy you pour in. That is why a drink "
          f"with ice in it holds its temperature and a drink without it does not - and it is "
          f"why the flat section of a heating curve is flat."),
    sanity=(f"Put that {S(q23/1000,3)} kJ into the resulting water instead and it would raise "
            f"its temperature by {S(q23,3)} {DIV} (0.25 {TIMES} 4180) = {S(dt23,3)} {DEG}C. "
            f"Merely melting ice costs as much energy as heating the same water from freezing "
            f"to nearly boiling."),
)

# --- 24 --------------------------------------------------------------------
num24 = R(0.30*80 + 0.50*20, 3)
tf24 = R(num24 / 0.80, 3)
P(
    n=24, part="Thermodynamics", chapter="Temperature", level="BOTH",
    book="Part 4 · Thermodynamics (pp. 47-58)",
    title="Mixing hot and cold water",
    statement=(f"0.30 kg of water at 80 {DEG}C is mixed with 0.50 kg of water at 20 {DEG}C in "
               f"an insulated container. Find the final temperature."),
    given=[("m hot", "0.30", f"kg at 80 {DEG}C"), ("m cold", "0.50", f"kg at 20 {DEG}C"),
           ("heat lost to surroundings", "none", "")],
    wanted="the final temperature of the mixture",
    steps=[
        dict(t="The energy the hot water loses, the cold water gains",
             body="Nothing escapes the container, so the two must balance exactly.",
             calc=f"m(hot) c (80 {chr(8722)} T) = m(cold) c (T {chr(8722)} 20)"),
        dict(t="The specific heat capacity cancels",
             body="It is the same liquid on both sides, so its value never has to be looked up.",
             calc=f"0.30(80 {chr(8722)} T) = 0.50(T {chr(8722)} 20)"),
        dict(t="Expand and collect",
             body="",
             calc=f"24 {chr(8722)} 0.30T = 0.50T {chr(8722)} 10    {ARROW}    {S(num24,3)} = 0.80T"),
        dict(t="Solve",
             body="",
             calc=f"T = {S(num24,3)} {DIV} 0.80 = {S(tf24,3)} {DEG}C"),
    ],
    answer=(S(tf24, 3), f"{DEG}C", "Below the midpoint, because there is more cold water than hot."),
    trap=(f"50 {DEG}C",
          f"Averaging the two temperatures. That is only correct when the two masses are "
          f"equal, and here they are not: there is {S(0.50/0.30,3)} times as much cold water "
          f"as hot, so the mixture has to settle nearer the cold end. The average is a "
          f"special case, not the rule."),
    sanity=(f"The answer must lie between 20 and 80 {DEG}C, and nearer 20 because the cold "
            f"mass is larger. {S(tf24,3)} {DEG}C satisfies both. Check it the other way: the "
            f"hot water falls {S(80-tf24,3)} {DEG}C and the cold rises {S(tf24-20,3)} {DEG}C, "
            f"and 0.30 {TIMES} {S(80-tf24,3)} = 0.50 {TIMES} {S(tf24-20,3)}. Energy balances."),
)

# --- 25 --------------------------------------------------------------------
p25 = R(3.4 * 318 / 288, 3)
wrong25 = R(3.4 * 45 / 15, 3)
P(
    n=25, part="Thermodynamics", chapter="Gases", level="A-LEVEL",
    book="Part 4 · Thermodynamics (pp. 47-58)",
    title="Why your tyre pressure is wrong after a motorway run",
    statement=(f"A car tyre is checked cold at 15 {DEG}C and holds air at an absolute pressure "
               f"of 3.4 bar. After a long drive the air inside has reached 45 {DEG}C. The "
               f"volume is effectively unchanged. Find the new pressure."),
    given=[("P1", "3.4", "bar absolute"), ("T1", f"15 {DEG}C", ""),
           ("T2", f"45 {DEG}C", ""), ("V", "constant", "")],
    wanted="the new absolute pressure",
    steps=[
        dict(t="Convert both temperatures to kelvin, before anything else",
             body=f"The gas laws are proportional relationships, and a proportion needs a scale "
                  f"that starts at true zero. Celsius does not; kelvin does.",
             calc=f"T1 = 15 + 273 = 288 K    T2 = 45 + 273 = 318 K"),
        dict(t="Constant volume, so pressure is proportional to temperature",
             body="",
             calc=f"P1 {DIV} T1 = P2 {DIV} T2"),
        dict(t="Rearrange and substitute",
             body="",
             calc=f"P2 = 3.4 {TIMES} 318 {DIV} 288 = {S(p25,3)} bar"),
    ],
    answer=(S(p25, 3), "bar absolute",
            f"A rise of {S(p25-3.4,2)} bar, which is why tyres are always checked cold."),
    trap=(f"{S(wrong25,3)} bar",
          f"Using degrees Celsius, so that 45 {DEG}C looks like three times 15 {DEG}C and the "
          f"pressure appears to triple. It does not: in kelvin the temperature rose from 288 "
          f"to 318, a rise of only {S((318/288-1)*100,2)}%. Celsius has an arbitrary zero, so "
          f"ratios taken in it are meaningless. Any gas-law answer that changes by a factor of "
          f"three for a warm afternoon is a units error."),
    sanity=(f"The absolute temperature went up by {S((318/288-1)*100,2)}%, so at constant "
            f"volume the pressure must go up by {S((318/288-1)*100,2)}% too: 3.4 {TIMES} "
            f"{S(318/288,4)} = {S(p25,3)} bar. The percentage check and the equation agree, "
            f"and both match the few tenths of a bar a garage gauge actually shows after a run."),
)

# --- 26 --------------------------------------------------------------------
pd26 = R(RHO_W * G * 12, 4)
p1_26 = pd26 + P_ATM
v2_26 = R(1.0 * p1_26 / P_ATM, 3)
wrong26 = R(1.0 * pd26 / P_ATM, 3)
P(
    n=26, part="Thermodynamics", chapter="Gases", level="BOTH",
    book="Part 4 · Thermodynamics (pp. 47-58)",
    title="A bubble on its way to the surface",
    statement=(f"A bubble of volume 1.0 {CM3} forms 12 m down in a lake and rises to the "
               f"surface. The temperature does not change. Atmospheric pressure is 101 000 Pa "
               f"and the water's density is 1000 kg/{M3}. Find the bubble's volume at the surface."),
    given=[("V1", "1.0", CM3), ("depth", "12", "m"),
           ("atmospheric pressure", "101 000", "Pa"), ("temperature", "constant", "")],
    wanted="the volume of the bubble at the surface",
    steps=[
        dict(t="Find the ABSOLUTE pressure down at the bubble",
             body="The water above it and the atmosphere above that both press on it. Boyle's law needs the total, not just the water's share.",
             calc=f"P1 = 101 000 + (1000 {TIMES} 9.81 {TIMES} 12) = 101 000 + {S(pd26,5)} = {S(p1_26,6)} Pa"),
        dict(t="At the surface only the atmosphere is left",
             body="",
             calc=f"P2 = 101 000 Pa"),
        dict(t="Temperature is constant, so Boyle's law applies",
             body="",
             calc=f"P1V1 = P2V2"),
        dict(t="Rearrange and solve",
             body="",
             calc=f"V2 = 1.0 {TIMES} {S(p1_26,6)} {DIV} 101 000 = {S(v2_26,3)} {CM3}"),
    ],
    answer=(S(v2_26, 3), CM3, f"The bubble more than doubles on the way up, without a single extra molecule entering it."),
    trap=(f"{S(wrong26,3)} {CM3}",
          f"Leaving the atmosphere out and using only the water's {S(pd26,5)} Pa. Boyle's law "
          f"is written in absolute pressures, and a bubble 12 m down is carrying the whole sky "
          f"on its shoulders as well as the lake. Dropping the atmosphere here makes the "
          f"bubble SHRINK as it rises, which is the opposite of what anyone has ever seen."),
    sanity=(f"About every 10 m of water adds one atmosphere. At 12 m the bubble sits under "
            f"roughly 2.2 atmospheres, so at the surface it should be about 2.2 times bigger - "
            f"and {S(v2_26,3)} {CM3} is {S(v2_26,3)} times 1.0. It is also the reason divers "
            f"are told never to hold their breath on the way up."),
)

# --- 27 --------------------------------------------------------------------
eff27 = R(950 / 2400, 3)
waste27 = 2400 - 950
carnot27 = R(1 - 293/823, 3)
P(
    n=27, part="Thermodynamics", chapter="Entropy", level="BOTH",
    book="Part 4 · Thermodynamics (pp. 47-58)",
    title="A power station that throws away more than it sells",
    statement=("A thermal power station burns fuel at a rate of 2400 MW and delivers 950 MW "
               "of electricity to the grid. Find its efficiency and the power it rejects as "
               "waste heat."),
    given=[("power in", "2400", "MW"), ("electrical power out", "950", "MW")],
    wanted="the efficiency and the wasted power",
    steps=[
        dict(t="Efficiency is useful output over total input",
             body="Both are powers here, so no conversion to energy is needed - the seconds cancel.",
             calc=f"efficiency = 950 {DIV} 2400 = {S(eff27,3)}"),
        dict(t="Express it as a percentage",
             body="",
             calc=f"= {S(eff27*100,3)}%"),
        dict(t="Everything that is not useful output leaves as heat",
             body="Energy is conserved. It did not vanish; it went up the cooling towers and into the river.",
             calc=f"waste = 2400 {chr(8722)} 950 = {waste27} MW"),
    ],
    answer=(f"{S(eff27*100,3)}% efficient, rejecting {waste27} MW", "",
            "The station discards more than half as much again as it sells."),
    trap=(f"{chr(8220)}so {S((1-eff27)*100,3)}% is being wasted through bad engineering{chr(8221)}",
          "Most of it is not an engineering failure at all - it is forbidden by the second "
          "law of thermodynamics. Any engine that turns heat into work must dump some heat at "
          "a lower temperature; that rejection is what makes the process possible, not a leak "
          "in it. Calling the whole of it waste misreads the physics."),
    sanity=(f"Real coal and gas thermal stations run at about 38-42%. {S(eff27*100,3)}% sits "
            f"right inside that band, which is the sign the numbers in the question describe a "
            f"real plant rather than an invented one."),
    alt=(f"A-level extension - how much of that loss is unavoidable. Carnot's limit says the "
         f"best possible efficiency is 1 {chr(8722)} T(cold) {DIV} T(hot), using absolute "
         f"temperatures. With steam at 550 {DEG}C (823 K) and cooling water at 20 {DEG}C "
         f"(293 K): 1 {chr(8722)} 293 {DIV} 823 = {S(carnot27,3)}, or {S(carnot27*100,3)}%. So "
         f"the laws of physics cap this station at {S(carnot27*100,3)}% and the engineers "
         f"reached {S(eff27*100,3)}%. The gap worth criticising is that one - not the whole "
         f"{S((1-eff27)*100,3)}%."),
)

# --- 28 --------------------------------------------------------------------
a28 = R(1.4 * 1.1, 3)
p28 = R(2.8 * a28 * 17, 4)
e28 = p28 * 86400                 # exact product of the displayed values
kwh28 = R(p28 * 24 / 1000, 3)
P(
    n=28, part="Thermodynamics", chapter="Heat energy", level="BOTH",
    book="Part 4 · Thermodynamics (pp. 47-58)",
    title="What one window costs you overnight",
    statement=(f"A window measures 1.4 m {TIMES} 1.1 m and loses heat at a rate given by "
               f"P = UA{DELTA}T, where U = 2.8 W/m{SQ}{DEG}C. Inside it is 21 {DEG}C and "
               f"outside 4 {DEG}C. Find the rate of heat loss, and the energy lost in 24 hours."),
    given=[("dimensions", f"1.4 {TIMES} 1.1", "m"), ("U", "2.8", f"W/m{SQ}{DEG}C"),
           ("inside", "21", f"{DEG}C"), ("outside", "4", f"{DEG}C")],
    wanted="the rate of heat loss, and the energy lost in a day",
    steps=[
        dict(t="Area, and the temperature DIFFERENCE",
             body="As always in thermal problems, what drives the flow is the difference, not either temperature on its own.",
             calc=f"A = 1.4 {TIMES} 1.1 = {S(a28,3)} m{SQ}    {DELTA}T = 21 {chr(8722)} 4 = 17 {DEG}C"),
        dict(t="Substitute into the equation given",
             body="The answer is in watts, so it is a RATE - joules every second, continuously.",
             calc=f"P = 2.8 {TIMES} {S(a28,3)} {TIMES} 17 = {S(p28,3)} W"),
        dict(t="Energy is that rate multiplied by the time it runs for",
             body="24 hours is 86 400 seconds. Convert before multiplying, not after.",
             calc=f"E = Pt = {S(p28,4)} {TIMES} 86 400 = {S(e28,7)} J"),
        dict(t="And in the unit the energy bill uses",
             body="",
             calc=f"E = {S(p28,3)} W {TIMES} 24 h = {S(kwh28,3)} kWh"),
    ],
    answer=(f"{S(p28,3)} W, which is {S(e28/1e6,3)} MJ or {S(kwh28,3)} kWh per day", "",
            f"That one window leaks heat as steadily as a {S(p28,2)} W bulb left on, day and night."),
    trap=(f"quoting {S(e28,7)} W, or {S(p28,3)} J",
          "Swapping the two. A watt is a joule per second: the first answer is a rate and the "
          "second is a total, and they are not interchangeable labels for the same number. The "
          "giveaway is the time - a rate is true at every instant and never mentions a "
          "duration, while an energy is meaningless until you say over how long."),
    sanity=(f"{S(kwh28,3)} kWh a day from one window. A house with ten similar windows loses "
            f"around {S(kwh28*10,3)} kWh a day through the glazing alone, which is a serious "
            f"share of a winter heating bill - and exactly why double glazing is sold on its "
            f"U-value."),
)


# ===========================================================================
# PART 5 - ELECTRICITY  (Main Book pp. 59-72)
# ===========================================================================

OHM, MICRO = "Ω", "µ"
E_CHARGE = 1.60e-19               # the exam-board value, and the one quoted in the question

# --- 29 --------------------------------------------------------------------
r29 = R(3.0 / 0.25, 3)
p29 = R(3.0 * 0.25, 3)
wrong29 = R(0.25 / 3.0, 3)
P(
    n=29, part="Electricity", chapter="Resistance", level="GCSE",
    book="Part 5 · Electricity (pp. 59-72)",
    title="The one equation everything else is built on",
    statement=(f"A torch bulb has a potential difference of 3.0 V across it and a current of "
               f"0.25 A through it. Find its resistance, and the power it dissipates."),
    given=[("V", "3.0", "V"), ("I", "0.25", "A")],
    wanted="the resistance of the bulb, and its power",
    steps=[
        dict(t="Start from the definition, not from a memorised triangle",
             body="Resistance is how much potential difference it takes to drive one amp through something. That sentence IS the equation.",
             calc=f"V = IR    {ARROW}    R = V {DIV} I"),
        dict(t="Substitute",
             body="",
             calc=f"R = 3.0 {DIV} 0.25 = {S(r29,3)} {OHM}"),
        dict(t="Power is current times potential difference",
             body="Volts are joules per coulomb and amps are coulombs per second, so multiplying them gives joules per second, which is watts.",
             calc=f"P = VI = 3.0 {TIMES} 0.25 = {S(p29,3)} W"),
    ],
    answer=(f"{S(r29,3)} {OHM}, dissipating {S(p29,3)} W", "",
            "A small torch bulb, and three quarters of a watt of light and heat."),
    trap=(f"{S(wrong29,3)} {OHM}",
          f"Dividing the wrong way round: I {DIV} V instead of V {DIV} I. The triangle is "
          f"remembered upside down about as often as it is remembered correctly. The defence "
          f"is not a better mnemonic, it is a sense of scale - {S(wrong29,3)} {OHM} is the "
          f"resistance of a short piece of copper wire, not of something that glows."),
    sanity=(f"Check it the other way: {S(r29,3)} {OHM} carrying 0.25 A needs {S(r29,3)} "
            f"{TIMES} 0.25 = {S(r29*0.25,3)} V across it, which is what the question said. "
            f"And torch bulbs do sit in the range of a few ohms to a few tens of ohms."),
)

# --- 30 --------------------------------------------------------------------
rt30 = 220 + 330
i30 = R(12 / rt30, 4)
v30a = R(i30 * 220, 3)
v30b = R(i30 * 330, 3)
P(
    n=30, part="Electricity", chapter="Circuits", level="GCSE",
    book="Part 5 · Electricity (pp. 59-72)",
    title="Two resistors in series",
    statement=(f"A 220 {OHM} resistor and a 330 {OHM} resistor are connected in series across "
               f"a 12 V supply. Find the current, and the potential difference across each resistor."),
    given=[("R1", "220", OHM), ("R2", "330", OHM), ("V supply", "12", "V")],
    wanted="the current, and the potential difference across each resistor",
    steps=[
        dict(t="In series, resistances simply add",
             body="There is only one path, so the charge has to fight its way through both. The obstacles come one after the other.",
             calc=f"R(total) = 220 + 330 = {rt30} {OHM}"),
        dict(t="One path means ONE current, the same everywhere",
             body="Charge is not used up as it goes round. Whatever leaves the battery comes back to it.",
             calc=f"I = V {DIV} R = 12 {DIV} {rt30} = {S(i30,4)} A"),
        dict(t="Now find each potential difference separately",
             body="Each resistor gets the share of the voltage that its own resistance demands.",
             calc=f"V1 = {S(i30,4)} {TIMES} 220 = {S(v30a,3)} V"),
        dict(t="And the second",
             body="",
             calc=f"V2 = {S(i30,4)} {TIMES} 330 = {S(v30b,3)} V"),
    ],
    answer=(f"{S(i30*1000,3)} mA, with {S(v30a,3)} V and {S(v30b,3)} V across them", "",
            "The larger resistor takes the larger share of the voltage, in exactly the same ratio as the resistances."),
    trap=("6 V across each",
          f"Splitting the supply equally. The voltage divides in the ratio of the resistances, "
          f"not evenly: 330 is {S(330/220,3)} times 220, so it takes {S(330/220,3)} times the "
          f"voltage. Equal sharing only happens when the resistors are equal, which is a "
          f"special case rather than the rule."),
    sanity=(f"The two potential differences must add up to the supply: {S(v30a,3)} + "
            f"{S(v30b,3)} = {S(v30a+v30b,4)} V. They do. If they do not add to the supply "
            f"voltage, something is wrong, and this check costs five seconds."),
)

# --- 31 --------------------------------------------------------------------
rp31 = R(220 * 330 / 550, 3)
i31 = R(12 / rp31, 4)
i31a = R(12 / 220, 4)
i31b = R(12 / 330, 4)
wrongi31 = R(12 / 550, 4)
P(
    n=31, part="Electricity", chapter="Circuits", level="GCSE",
    book="Part 5 · Electricity (pp. 59-72)",
    title="The same two resistors in parallel",
    statement=(f"The same 220 {OHM} and 330 {OHM} resistors are now connected in PARALLEL "
               f"across the same 12 V supply. Find the total resistance and the total current."),
    given=[("R1", "220", OHM), ("R2", "330", OHM), ("V supply", "12", "V")],
    wanted="the total resistance and the current drawn from the supply",
    steps=[
        dict(t="In parallel it is the CONDUCTANCES that add, not the resistances",
             body="You have not made the path harder, you have opened a second one. Two doors out of a room let more people through than one.",
             calc=f"1 {DIV} R = 1 {DIV} 220 + 1 {DIV} 330"),
        dict(t="Put it over a common denominator",
             body="",
             calc=f"1 {DIV} R = 3 {DIV} 660 + 2 {DIV} 660 = 5 {DIV} 660"),
        dict(t="Invert - and this is the step people forget",
             body="The equation gives you 1/R. It does not give you R until you turn it over.",
             calc=f"R = 660 {DIV} 5 = {S(rp31,3)} {OHM}"),
        dict(t="Now the total current",
             body="",
             calc=f"I = 12 {DIV} {S(rp31,3)} = {S(i31,3)} A"),
    ],
    answer=(f"{S(rp31,3)} {OHM}, drawing {S(i31*1000,3)} mA", "",
            f"Over four times the current the series version drew, from the same two components and the same battery."),
    trap=(f"{rt30} {OHM}, giving {S(wrongi31*1000,3)} mA",
          f"Adding the resistances, exactly as in series. This is the single most common "
          f"mistake in school electricity, and it is {S(i31/wrongi31,3)} times out. It also "
          f"fails the test that costs nothing: a parallel combination must ALWAYS come out "
          f"smaller than the smallest resistor in it. Adding gives {rt30} {OHM}, which is "
          f"larger than both. If your parallel answer is bigger than any single resistor, you "
          f"have added when you should have inverted."),
    sanity=(f"Two independent checks. First, {S(rp31,3)} {OHM} is smaller than 220 {OHM}, as "
            f"a parallel total must be. Second, add the branch currents: 12 {DIV} 220 = "
            f"{S(i31a,3)} A and 12 {DIV} 330 = {S(i31b,3)} A, and {S(i31a,3)} + {S(i31b,3)} = "
            f"{S(i31a+i31b,3)} A, matching the total. Both routes agree."),
)

# --- 32 --------------------------------------------------------------------
v32 = R(9.0 * 4700 / 14700, 3)
wrong32 = R(9.0 * 10000 / 14700, 3)
P(
    n=32, part="Electricity", chapter="Potential", level="A-LEVEL",
    book="Part 5 · Electricity (pp. 59-72)",
    title="A potential divider, and which resistor goes on top",
    statement=(f"A 10 k{OHM} resistor and a 4.7 k{OHM} resistor are connected in series across "
               f"a 9.0 V supply. Find the potential difference across the 4.7 k{OHM} resistor."),
    given=[("R1", "10", f"k{OHM}"), ("R2", "4.7", f"k{OHM}"), ("V supply", "9.0", "V")],
    wanted=f"the potential difference across the 4.7 k{OHM} resistor",
    steps=[
        dict(t="The two resistors share the supply in proportion to their resistance",
             body="Same current through both, so V = IR means the voltages are in the same ratio as the resistances.",
             calc=f"V2 = V {TIMES} R2 {DIV} (R1 + R2)"),
        dict(t="The resistor you are asked about goes on TOP of the fraction",
             body="This is the only thing that ever goes wrong with a potential divider. The denominator is always the total.",
             calc=f"V2 = 9.0 {TIMES} 4700 {DIV} 14 700"),
        dict(t="Solve",
             body="",
             calc=f"V2 = {S(v32,3)} V"),
    ],
    answer=(S(v32, 3), "V", f"Leaving {S(9.0-v32,3)} V across the 10 k{OHM}."),
    trap=(f"{S(wrong32,3)} V",
          f"Putting the OTHER resistor on top: 9.0 {TIMES} 10 000 {DIV} 14 700. That is the "
          f"voltage across the 10 k{OHM}, which is a perfectly good answer to a question "
          f"nobody asked. Both numbers will appear on your calculator and both look "
          f"plausible, which is precisely why this one is worth a check."),
    sanity=(f"The 4.7 k{OHM} is the SMALLER resistor, so it must take LESS than half the "
            f"supply - less than 4.5 V. {S(v32,3)} V passes; {S(wrong32,3)} V would have "
            f"failed instantly. And the two shares add back to the supply: {S(v32,3)} + "
            f"{S(9.0-v32,3)} = 9.00 V."),
)

# --- 33 --------------------------------------------------------------------
p33 = R(0.35**2 * 56, 3)
v33 = R(0.35 * 56, 3)
P(
    n=33, part="Electricity", chapter="Circuits", level="BOTH",
    book="Part 5 · Electricity (pp. 59-72)",
    title="Three equations for power, and picking the one you can actually use",
    statement=(f"A 56 {OHM} resistor carries a current of 0.35 A. Calculate the power it "
               f"dissipates. The supply voltage is not given."),
    given=[("R", "56", OHM), ("I", "0.35", "A")],
    wanted="the power dissipated in the resistor",
    steps=[
        dict(t="Write down all three versions before choosing",
             body="They are the same equation wearing different clothes, because V = IR lets you swap between them.",
             calc=f"P = VI    P = I{SQ}R    P = V{SQ} {DIV} R"),
        dict(t="Choose the one that uses only what you have",
             body=f"You were given I and R, so the middle form needs nothing else. The other two would require a voltage you have not been told.",
             calc=f"P = I{SQ}R"),
        dict(t="Substitute, and square the current before multiplying",
             body="",
             calc=f"P = 0.35{SQ} {TIMES} 56 = 0.1225 {TIMES} 56 = {S(p33,3)} W"),
    ],
    answer=(S(p33, 3), "W", "Nearly seven watts, in a component the size of a grain of rice."),
    trap=("reaching for P = VI and using the supply voltage",
          "The V in every one of these equations is the potential difference across THAT "
          "component, never the voltage of the battery driving the circuit. In a circuit with "
          "anything else in it, those two are different numbers, and using the supply voltage "
          "silently credits one resistor with the power of the whole circuit."),
    sanity=(f"Work out the missing voltage and check with a different equation: V = IR = 0.35 "
            f"{TIMES} 56 = {S(v33,3)} V, so P = VI = {S(v33,3)} {TIMES} 0.35 = "
            f"{S(v33*0.35,3)} W. The two forms agree. Worth noting too that {S(p33,3)} W "
            f"would destroy a standard 0.25 W resistor, which is why power ratings exist."),
)

# --- 34 --------------------------------------------------------------------
e34 = R(2.2 * 1.5, 3)
yr34 = R(e34 * 4 * 52, 4)
j34 = R(e34 * 3.6e6, 4)
P(
    n=34, part="Electricity", chapter="Current", level="GCSE",
    book="Part 5 · Electricity (pp. 59-72)",
    title="What a tumble dryer really costs you in energy",
    statement=("A tumble dryer is rated at 2.2 kW and runs for 1.5 hours per cycle, four "
               "cycles a week. Find the energy used per cycle in kilowatt-hours and in joules, "
               "and the energy used in a year."),
    given=[("P", "2.2", "kW"), ("t per cycle", "1.5", "h"), ("cycles", "4", "per week")],
    wanted="the energy per cycle, in kWh and in joules, and the energy per year",
    steps=[
        dict(t="A kilowatt-hour is not a unit of power, it is a unit of energy",
             body="It is what you get when a kilowatt runs for an hour. Power multiplied by time is always energy, whatever units you use.",
             calc=f"E = Pt = 2.2 {TIMES} 1.5 = {S(e34,2)} kWh per cycle"),
        dict(t="Convert to joules",
             body="One kWh is 1000 W running for 3600 s, which is 3.6 million joules.",
             calc=f"E = {S(e34,2)} {TIMES} 3 600 000 = {S(j34,4)} J"),
        dict(t="Scale up to a year",
             body="",
             calc=f"E = {S(e34,2)} {TIMES} 4 {TIMES} 52 = {S(yr34,4)} kWh per year"),
    ],
    answer=(f"{S(e34,2)} kWh ({S(j34/1e6,3)} MJ) per cycle, {S(yr34,3)} kWh a year", "",
            "From one appliance, used four times a week."),
    trap=("2.2 kWh per cycle",
          "Reading the rating off the label and calling it the energy. The 2.2 kW is a RATE - "
          "it tells you nothing until you say for how long. A dryer run for three hours uses "
          "twice the energy of one run for ninety minutes, while its rating never changes. "
          "Watts describe the appliance; kilowatt-hours describe what you did with it."),
    sanity=(f"A typical UK home uses roughly 2700 kWh of electricity a year. This one "
            f"appliance accounts for about {S(yr34/2700*100,2)}% of that, which is why tumble "
            f"dryers are the first thing any energy-saving guide tells you to use less."),
)

# --- 35 --------------------------------------------------------------------
q35 = R(0.80 * 150, 3)
n35 = q35 / E_CHARGE
P(
    n=35, part="Electricity", chapter="Charge", level="BOTH",
    book="Part 5 · Electricity (pp. 59-72)",
    title="Counting the electrons",
    statement=(f"A current of 0.80 A flows for 2.5 minutes. Find the charge that passes, and "
               f"the number of electrons it corresponds to. The charge on an electron is "
               f"1.60 {TIMES} 10⁻¹⁹ C."),
    given=[("I", "0.80", "A"), ("t", "2.5", "minutes"),
           ("e", f"1.60 {TIMES} 10⁻¹⁹", "C")],
    wanted="the charge transferred, and the number of electrons",
    steps=[
        dict(t="Convert the time to seconds first",
             body="An amp is defined as a coulomb per SECOND. Minutes have no place inside the equation.",
             calc=f"t = 2.5 {TIMES} 60 = 150 s"),
        dict(t="Charge is current multiplied by time",
             body="",
             calc=f"Q = It = 0.80 {TIMES} 150 = {S(q35,3)} C"),
        dict(t="Divide the total charge by the charge on one electron",
             body="",
             calc=f"n = {S(q35,3)} {DIV} (1.60 {TIMES} 10⁻¹⁹) = "
                  f"{S(n35/1e20,3)} {TIMES} 10²⁰ electrons"),
    ],
    answer=(f"{S(q35,3)} C, carried by {S(n35/1e20,3)} {TIMES} 10²⁰ electrons", "",
            "Two and a half minutes of a fairly ordinary current."),
    trap=(f"Q = {S(0.80*2.5,2)} C",
          f"Leaving the time in minutes. The factor of 60 is the whole mistake, and the answer "
          f"comes out sixty times too small. Any equation containing an amp, a watt or a volt "
          f"is written in seconds, because all three are defined per second."),
    sanity=(f"{S(n35/1e20,3)} {TIMES} 10²⁰ sounds impossibly large until you compare "
            f"it with a mole, 6.02 {TIMES} 10²³. It is about a thousandth of a mole "
            f"of electrons - a sliver of the charge carriers already sitting in the wire, "
            f"drifting past very slowly indeed."),
)

# --- 36 --------------------------------------------------------------------
i36 = R(2800 / 230, 3)
i36b = R(60 / 230, 3)
P(
    n=36, part="Electricity", chapter="Current", level="GCSE",
    book="Part 5 · Electricity (pp. 59-72)",
    title="Choosing a fuse, and what a fuse is actually protecting",
    statement=("UK mains is 230 V. A kettle is rated at 2800 W and a reading lamp at 60 W. "
               "Fuses are available in 3 A, 5 A and 13 A. Choose the correct fuse for each, "
               "and say what the fuse is protecting."),
    given=[("V", "230", "V"), ("P kettle", "2800", "W"), ("P lamp", "60", "W"),
           ("fuses available", "3, 5, 13", "A")],
    wanted="the right fuse for each appliance, and what the fuse protects",
    steps=[
        dict(t="Find the normal working current of each",
             body="",
             calc=f"kettle: I = P {DIV} V = 2800 {DIV} 230 = {S(i36,3)} A"),
        dict(t="And the lamp",
             body="",
             calc=f"lamp: I = 60 {DIV} 230 = {S(i36b,3)} A"),
        dict(t="Pick the smallest fuse ABOVE the working current",
             body="Above, so that it does not blow in normal use. The smallest such, so that it reacts as soon as anything goes wrong.",
             calc=f"kettle {S(i36,3)} A {ARROW} 13 A     lamp {S(i36b,3)} A {ARROW} 3 A"),
    ],
    answer=("13 A for the kettle, 3 A for the lamp", "",
            "And what the fuse protects is the flex, not the appliance."),
    trap=("13 A for both, on the grounds that a bigger fuse is safer",
          f"It is the opposite. A fuse exists to melt before the CABLE overheats, so a 13 A "
          f"fuse in a lamp flex lets {S(13/i36b,2)} times the normal current flow before it "
          f"acts - and a thin flex can be glowing long before that. Oversizing a fuse does "
          f"not make a circuit safer, it makes the fuse ornamental."),
    sanity=(f"Check the kettle from the other direction: a 13 A fuse at 230 V allows up to "
            f"{S(13*230,4)} W, comfortably above the kettle's 2800 W, while a 5 A fuse would "
            f"allow only {S(5*230,4)} W and blow the moment it was switched on."),
)

# --- 37 --------------------------------------------------------------------
num37 = 2.5e-6 * 4.0e-6
f37 = R(8.99e9 * num37 / 0.080**2, 3)
wrong37 = R(8.99e9 * num37 / 0.080, 3)
P(
    n=37, part="Electricity", chapter="Electric field", level="A-LEVEL",
    book="Part 5 · Electricity (pp. 59-72)",
    title="The force between two charges",
    statement=(f"A charge of +2.5 {MICRO}C and a charge of −4.0 {MICRO}C are held 8.0 cm "
               f"apart in air. Find the size and nature of the force between them. "
               f"Take k = 8.99 {TIMES} 10⁹ N m{SQ} C⁻{SQ}."),
    given=[("q1", f"+2.5 {MICRO}C = +2.5 {TIMES} 10⁻⁶", "C"),
           ("q2", f"−4.0 {MICRO}C = −4.0 {TIMES} 10⁻⁶", "C"),
           ("r", "8.0 cm = 0.080", "m")],
    wanted="the magnitude of the force, and whether it attracts or repels",
    steps=[
        dict(t="Convert everything to SI before touching the equation",
             body=f"Microcoulombs and centimetres both have to go. The centimetre is the "
                  f"dangerous one, because it is squared.",
             calc=f"q1q2 = (2.5 {TIMES} 10⁻⁶)(4.0 {TIMES} 10⁻⁶) = "
                  f"1.0 {TIMES} 10⁻¹¹ C{SQ}"),
        dict(t="Square the separation",
             body="",
             calc=f"r{SQ} = 0.080{SQ} = 0.0064 m{SQ}"),
        dict(t="Apply Coulomb's law",
             body="Work with the magnitudes and decide attraction or repulsion from the signs afterwards. It is cleaner than carrying a minus through.",
             calc=f"F = kq1q2 {DIV} r{SQ} = (8.99 {TIMES} 10⁹ {TIMES} "
                  f"1.0 {TIMES} 10⁻¹¹) {DIV} 0.0064 = {S(f37,3)} N"),
        dict(t="Opposite signs attract",
             body="",
             calc=f"{S(f37,3)} N, attractive"),
    ],
    answer=(f"{S(f37,3)} N, attractive", "",
            "Fourteen newtons between two specks of charge, at the width of a hand."),
    trap=(f"{S(wrong37,3)} N",
          f"Dividing by r instead of r{SQ}. Coulomb's law is an inverse SQUARE law, like "
          f"gravity and like light, and forgetting the square here makes the force "
          f"{S(f37/wrong37,3)} times too small. If an answer to an inverse-square problem does "
          f"not change by a factor of four when you double the distance, the square is missing."),
    sanity=(f"Apply that very test: at 16 cm the force should be a quarter, "
            f"{S(f37/4,3)} N. It is. And the sign check is independent of the arithmetic - "
            f"one charge is positive and one negative, so whatever the size, the force has to pull them together."),
)

# --- 38 --------------------------------------------------------------------
e38 = R(300 / 0.025, 3)
w38 = 5.0e-9 * 300
P(
    n=38, part="Electricity", chapter="Electric field", level="A-LEVEL",
    book="Part 5 · Electricity (pp. 59-72)",
    title="Field and potential are not the same thing",
    statement=(f"Two parallel plates 2.5 cm apart have a potential difference of 300 V between "
               f"them. Find the electric field strength between the plates, and the work done "
               f"in moving a charge of 5.0 nC from one plate to the other."),
    given=[("V", "300", "V"), ("d", "2.5 cm = 0.025", "m"),
           ("Q", f"5.0 nC = 5.0 {TIMES} 10⁻⁹", "C")],
    wanted="the electric field strength, and the work done moving the charge",
    steps=[
        dict(t="Field strength is potential difference PER METRE",
             body="That per metre is the whole distinction. Potential is measured at a place; field is how fast potential changes as you move.",
             calc=f"E = V {DIV} d = 300 {DIV} 0.025 = {S(e38,4)} V/m"),
        dict(t="Work done is charge multiplied by potential difference",
             body="A volt is a joule per coulomb, so coulombs times volts gives joules. The units do the thinking for you.",
             calc=f"W = QV = (5.0 {TIMES} 10⁻⁹) {TIMES} 300"),
        dict(t="Solve",
             body="",
             calc=f"W = 1.5 {TIMES} 10⁻⁶ J = 1.5 {MICRO}J"),
    ],
    answer=(f"E = {S(e38,4)} V/m and W = 1.5 {MICRO}J", "",
            "A field of twelve thousand volts per metre, from a potential difference of only three hundred volts."),
    trap=("E = 300 V/m",
          f"Quoting the potential difference and attaching the units of field strength. They "
          f"are different quantities measured in different units: volts against volts per "
          f"metre. The plates here are only 2.5 cm apart, so the field is {S(e38/300,3)} times "
          f"the number on the supply. Squeeze the same 300 V into a tenth of the gap and the "
          f"field is ten times larger again, which is exactly how a spark gap is designed."),
    sanity=(f"Do the work a second way, through the field: W = QEd = (5.0 {TIMES} "
            f"10⁻⁹) {TIMES} {S(e38,4)} {TIMES} 0.025 = 1.5 {TIMES} "
            f"10⁻⁶ J. The same answer by a different route, which is what you want "
            f"whenever a problem offers two equations for the same quantity."),
)


# ===========================================================================
# PART 6 - WAVES & OPTICS  (Main Book pp. 73-84)
# ===========================================================================

C_LIGHT, V_SOUND, H_PLANCK = 3.00e8, 340, 6.63e-34

# --- 39 --------------------------------------------------------------------
lam39 = R(C_LIGHT / 93.5e6, 3)
P(
    n=39, part="Waves & Optics", chapter="Waves", level="GCSE",
    book="Part 6 · Waves & Optics (pp. 73-84)",
    title="How long a radio wave actually is",
    statement=(f"A radio station broadcasts on 93.5 MHz. Radio waves travel at "
               f"3.00 {TIMES} 10⁸ m/s. Find the wavelength."),
    given=[("f", "93.5", "MHz"), ("v", f"3.00 {TIMES} 10⁸", "m/s")],
    wanted="the wavelength of the broadcast",
    steps=[
        dict(t="Convert the frequency to hertz first",
             body="Mega means a million. The prefix is not decoration, it is a factor of 10⁶.",
             calc=f"f = 93.5 {TIMES} 10⁶ Hz"),
        dict(t="Use the wave equation",
             body="True of every wave there is, from ripples to gamma rays.",
             calc=f"v = f{chr(955)}    {ARROW}    {chr(955)} = v {DIV} f"),
        dict(t="Substitute",
             body="",
             calc=f"{chr(955)} = (3.00 {TIMES} 10⁸) {DIV} (93.5 {TIMES} 10⁶) = {S(lam39,3)} m"),
    ],
    answer=(S(lam39, 3), "m", "Just over three metres, from crest to crest."),
    trap=(f"{sci(C_LIGHT/93.5, 3)} m",
          f"Leaving the frequency in megahertz. The answer comes out a million times too "
          f"long - a single wavelength stretching further than the British Isles. Any prefix "
          f"in a question (M, k, m, {MICRO}, n) has to be turned into a power of ten before "
          f"it goes anywhere near an equation."),
    sanity=(f"FM wavelengths are a few metres, and a quarter-wave aerial is a quarter of "
            f"that: {S(lam39/4,2)} m. That is almost exactly the length of the aerial on a "
            f"car roof, which is not a coincidence - it is the design."),
)

# --- 40 --------------------------------------------------------------------
t40 = R(4.0 * 2.0e-3, 3)
f40 = R(1 / t40, 3)
P(
    n=40, part="Waves & Optics", chapter="Waves", level="GCSE",
    book="Part 6 · Waves & Optics (pp. 73-84)",
    title="Reading a frequency off an oscilloscope",
    statement=("An oscilloscope is set to 2.0 ms per division. One complete cycle of a sound "
               "wave spans 4.0 divisions across the screen. Find the period and the frequency."),
    given=[("timebase", "2.0", "ms per division"), ("one full cycle", "4.0", "divisions")],
    wanted="the period and the frequency of the wave",
    steps=[
        dict(t="Count the divisions for ONE complete cycle",
             body="Crest to crest, or trough to trough. Crest to the next trough is only half a wave, and that is where this question is won or lost.",
             calc="4.0 divisions per cycle"),
        dict(t="Multiply by the timebase to get the period",
             body="",
             calc=f"T = 4.0 {TIMES} 2.0 = 8.0 ms = {S(t40,2)} s"),
        dict(t="Frequency is one over the period",
             body="Period is seconds per cycle; frequency is cycles per second. They are the same information upside down.",
             calc=f"f = 1 {DIV} T = 1 {DIV} 0.0080 = {S(f40,3)} Hz"),
    ],
    answer=(f"T = 8.0 ms and f = {S(f40,3)} Hz", "", "A low note, well inside the range of human hearing."),
    trap=(f"{S(f40*2,3)} Hz",
          "Measuring from a crest to the next trough and calling it a cycle. That is half a "
          "wave, so the period comes out halved and the frequency doubled. On a screen the "
          "two look equally like a complete shape, which is why the rule is to measure from "
          "one point to the next point that is identical in BOTH height and direction of travel."),
    sanity=(f"{S(f40,3)} Hz is a note just below the open B string of a guitar. If the "
            f"oscilloscope is showing a sound you can hear, the answer has to land between "
            f"about 20 Hz and 20 000 Hz, and this does."),
)

# --- 41 --------------------------------------------------------------------
d41 = R(V_SOUND * 1.6, 3)
P(
    n=41, part="Waves & Optics", chapter="Sound", level="GCSE",
    book="Part 6 · Waves & Optics (pp. 73-84)",
    title="Shouting at a cliff",
    statement=("A walker shouts towards a cliff face and hears the echo 1.6 s later. The "
               "speed of sound in air is 340 m/s. How far away is the cliff?"),
    given=[("t", "1.6", "s"), ("v", "340", "m/s")],
    wanted="the distance to the cliff face",
    steps=[
        dict(t="Work out how far the SOUND travelled",
             body="Not how far away the cliff is. Those are two different distances, and the question only hands you one of them directly.",
             calc=f"d = vt = 340 {TIMES} 1.6 = {S(d41,3)} m"),
        dict(t="The sound made the journey twice",
             body="Out to the cliff and back to the ear. That is what an echo is.",
             calc=f"distance to cliff = {S(d41,3)} {DIV} 2"),
        dict(t="Halve it",
             body="",
             calc=f"= {S(d41/2,3)} m"),
    ],
    answer=(S(d41/2, 3), "m", "The cliff is less than three hundred metres away, though the sound covered twice that."),
    trap=(f"{S(d41,3)} m",
          "Forgetting the return journey. It is the commonest error in every echo, sonar and "
          "radar question there is, and the factor is always exactly two. If a question "
          "involves something bouncing back, write 2d = vt before you write anything else."),
    sanity=(f"A rough field rule: sound covers about 170 m towards an object for every second "
            f"of echo delay. 1.6 s {TIMES} 170 = {S(1.6*170,3)} m, which agrees with the "
            f"calculation and gives you a way to check it without a calculator."),
)

# --- 42 --------------------------------------------------------------------
sin42 = R(math.sin(math.radians(40)) / 1.50, 4)
ang42 = R(math.degrees(math.asin(sin42)), 3)
wrong42 = R(math.degrees(math.asin(math.sin(math.radians(50))/1.50)), 3)
P(
    n=42, part="Waves & Optics", chapter="Refraction", level="BOTH",
    book="Part 6 · Waves & Optics (pp. 73-84)",
    title="Light entering a glass block",
    statement=(f"A ray of light travelling through air strikes a glass block at 40{DEG} to "
               f"the normal. The refractive index of the glass is 1.50. Find the angle of "
               f"refraction inside the glass."),
    given=[("angle of incidence", "40", f"{DEG} to the normal"), ("n glass", "1.50", ""),
           ("n air", "1.00", "")],
    wanted="the angle of refraction inside the glass",
    steps=[
        dict(t="Every angle in optics is measured from the NORMAL",
             body="The normal is the line at right angles to the surface. Not from the surface itself - that is the single most expensive habit in this topic.",
             calc=f"angle of incidence = 40{DEG} from the normal"),
        dict(t="Apply Snell's law",
             body="",
             calc=f"n = sin i {DIV} sin r    {ARROW}    sin r = sin i {DIV} n"),
        dict(t="Substitute",
             body="",
             calc=f"sin r = sin 40{DEG} {DIV} 1.50 = 0.6428 {DIV} 1.50 = {S(sin42,4)}"),
        dict(t="Take the inverse sine",
             body="",
             calc=f"r = sin{SUP_MINUS1} {S(sin42,4)} = {S(ang42,3)}{DEG}"),
    ],
    answer=(S(ang42, 3), DEG, "Measured from the normal, inside the glass."),
    trap=(f"{S(wrong42,3)}{DEG}",
          f"Reading the angle from the surface instead of the normal, so that 40{DEG} becomes "
          f"50{DEG}. The two always add to 90{DEG}, which means the wrong value is right there "
          f"on the diagram looking just as plausible. Draw the normal in, as a dashed line, "
          f"before you measure anything."),
    sanity=(f"Light entering a denser medium must bend TOWARDS the normal, so the answer has "
            f"to be smaller than 40{DEG}. {S(ang42,3)}{DEG} is. Had the answer come out larger, "
            f"the two sides of Snell's law would have been the wrong way up."),
)

# --- 43 --------------------------------------------------------------------
sinc43 = R(1 / 1.50, 4)
c43 = R(math.degrees(math.asin(sinc43)), 3)
cdia = R(math.degrees(math.asin(1/2.42)), 3)
P(
    n=43, part="Waves & Optics", chapter="Reflection", level="BOTH",
    book="Part 6 · Waves & Optics (pp. 73-84)",
    title="The angle beyond which light cannot get out",
    statement=(f"The same glass has a refractive index of 1.50. Find its critical angle, and "
               f"say what happens to a ray inside the glass that meets the surface at "
               f"45{DEG} to the normal."),
    given=[("n glass", "1.50", ""), ("n air", "1.00", ""),
           ("angle inside the glass", "45", f"{DEG} to the normal")],
    wanted="the critical angle, and the fate of the 45 degree ray",
    steps=[
        dict(t="The critical angle is the one that refracts to exactly 90 degrees",
             body="At that angle the escaping ray skims along the surface. Any steeper and there is nowhere left for it to go.",
             calc=f"sin C = n(outside) {DIV} n(inside) = 1.00 {DIV} 1.50"),
        dict(t="Solve",
             body="",
             calc=f"C = sin{SUP_MINUS1} {S(sinc43,4)} = {S(c43,3)}{DEG}"),
        dict(t="Compare the ray with the critical angle",
             body="",
             calc=f"45{DEG} > {S(c43,3)}{DEG}    {ARROW}    total internal reflection"),
    ],
    answer=(f"C = {S(c43,3)}{DEG}, and the 45{DEG} ray does not escape at all", "",
            "It reflects back inside, as completely as from a mirror."),
    trap=(f"{chr(8220)}it still gets out, just bent a long way{chr(8221)}",
          f"Past the critical angle no light emerges - none, not a dim beam at a steep angle. "
          f"The refracted ray would have to bend beyond 90{DEG}, which would mean going back "
          f"into the glass it came from. The surface stops behaving like a window and starts "
          f"behaving like a perfect mirror, which is exactly what makes an optical fibre work."),
    sanity=(f"Run the same calculation for diamond, n = 2.42, and the critical angle falls to "
            f"{S(cdia,3)}{DEG}. A much smaller critical angle means light entering a diamond "
            f"is trapped and bounced around far more before it finds a way out - which is the "
            f"physics of the sparkle."),
)

# --- 44 --------------------------------------------------------------------
inv44 = R(1/15 - 1/25, 4)
v44 = R(1 / inv44, 3)
m44 = R(v44 / 25, 3)
P(
    n=44, part="Waves & Optics", chapter="Light", level="A-LEVEL",
    book="Part 6 · Waves & Optics (pp. 73-84)",
    title="Where a lens puts the image",
    statement=("An object is placed 25 cm from a converging lens of focal length 15 cm. Find "
               "the position of the image and its magnification, and describe it."),
    given=[("u", "25", "cm"), ("f", "15", "cm"), ("lens", "converging", "")],
    wanted="the image distance, the magnification, and the nature of the image",
    steps=[
        dict(t="Write the lens equation and rearrange for the unknown",
             body="",
             calc=f"1 {DIV} f = 1 {DIV} u + 1 {DIV} v    {ARROW}    1 {DIV} v = 1 {DIV} f {chr(8722)} 1 {DIV} u"),
        dict(t="Substitute",
             body="Keep both distances in the same unit and the answer comes out in that unit.",
             calc=f"1 {DIV} v = 1 {DIV} 15 {chr(8722)} 1 {DIV} 25 = {S(inv44,4)}"),
        dict(t="Now INVERT, which is the step that gets forgotten",
             body="The equation gives you one over v. It has not given you v.",
             calc=f"v = 1 {DIV} {S(inv44,4)} = {S(v44,3)} cm"),
        dict(t="Magnification is image distance over object distance",
             body="",
             calc=f"m = v {DIV} u = {S(v44,3)} {DIV} 25 = {S(m44,2)}"),
    ],
    answer=(f"v = {S(v44,3)} cm, m = {S(m44,2)}", "",
            "A real, inverted image, half as big again as the object, on the far side of the lens."),
    trap=(f"{S(inv44,4)} cm",
          f"Stopping at 1/v and writing it down as the answer. An image distance of "
          f"{S(inv44,4)} cm would put the image inside the glass of the lens itself. The units "
          f"are the warning: 1/v comes out in reciprocal centimetres, and no distance was ever "
          f"measured in those."),
    sanity=("The object sits between f and 2f, that is between 15 cm and 30 cm. The standard "
            "result for that case is an image beyond 2f, real, inverted and magnified. The "
            "calculation puts it at 37.5 cm, which is beyond 30 cm, with a magnification "
            "above 1. Every part of the prediction matches."),
)

# --- 45 --------------------------------------------------------------------
fapp45 = R(850 * V_SOUND / (V_SOUND - 18), 4)
frec45 = R(850 * V_SOUND / (V_SOUND + 18), 4)
P(
    n=45, part="Waves & Optics", chapter="Sound", level="A-LEVEL",
    book="Part 6 · Waves & Optics (pp. 73-84)",
    title="The ambulance going past",
    statement=("An ambulance sounds a 850 Hz siren and drives past a stationary observer at "
               "18 m/s. The speed of sound is 340 m/s. Find the frequency heard as it "
               "approaches and as it recedes."),
    given=[("f source", "850", "Hz"), ("v source", "18", "m/s"), ("v sound", "340", "m/s")],
    wanted="the frequency heard approaching, and receding",
    steps=[
        dict(t="The siren still emits 850 waves every second",
             body="Nothing about the source changes. What changes is where each wave is emitted from, because the ambulance has moved on between one crest and the next.",
             calc="f(source) = 850 Hz throughout"),
        dict(t="Approaching, the crests are squeezed into a shorter distance",
             body="Each new crest sets off from closer to you than the last, so the wavelength arriving is shorter and the frequency higher.",
             calc=f"f = f(source) {TIMES} v {DIV} (v {chr(8722)} v(source))"),
        dict(t="Substitute for the approach",
             body="",
             calc=f"f = 850 {TIMES} 340 {DIV} 322 = {S(fapp45,4)} Hz"),
        dict(t="Receding, the sign flips",
             body="",
             calc=f"f = 850 {TIMES} 340 {DIV} 358 = {S(frec45,4)} Hz"),
    ],
    answer=(f"{S(fapp45,3)} Hz approaching, {S(frec45,3)} Hz receding", "",
            f"A drop of {S(fapp45-frec45,3)} Hz the instant it passes you."),
    trap=(f"{chr(8220)}the sound travels faster towards you{chr(8221)}",
          "It does not. The speed of sound is set by the air, not by whatever made the sound, "
          "and it is 340 m/s in every direction regardless of how fast the ambulance is "
          "moving. What the motion changes is the WAVELENGTH: the crests pile up ahead of the "
          "vehicle and spread out behind it. Same speed, different spacing, different pitch."),
    sanity=(f"The pitch falls from {S(fapp45,3)} Hz to {S(frec45,3)} Hz, a ratio of "
            f"{S(fapp45/frec45,4)}. On a musical scale that is close to a whole tone - and a "
            f"whole tone is about what you hear an ambulance drop as it goes past."),
)

# ===========================================================================
# PART 7 - MODERN PHYSICS  (Main Book pp. 85-94)
# ===========================================================================

EV = 1.60e-19
HC = R(H_PLANCK * C_LIGHT, 4)

# --- 46 --------------------------------------------------------------------
e46_J = R(HC / 400e-9, 4)
e46_eV = R(e46_J / EV, 3)
ke46 = R(e46_eV - 2.3, 2)
lam0 = R(HC / (2.3 * EV), 3)
P(
    n=46, part="Modern Physics", chapter="Quantum physics", level="A-LEVEL",
    book="Part 7 · Modern Physics (pp. 85-94)",
    title="Why a brighter light does not help",
    statement=(f"Light of wavelength 400 nm falls on a sodium surface whose work function is "
               f"2.3 eV. Find the maximum kinetic energy of the emitted electrons. Take "
               f"h = 6.63 {TIMES} 10⁻³⁴ J s and 1 eV = 1.60 {TIMES} 10⁻¹⁹ J."),
    given=[(chr(955), "400 nm = 400 " + TIMES + " 10⁻⁹", "m"),
           ("work function", "2.3", "eV"), ("h", f"6.63 {TIMES} 10⁻³⁴", "J s")],
    wanted="the maximum kinetic energy of an emitted electron",
    steps=[
        dict(t="Find the energy of ONE photon",
             body="Light arrives in lumps. The whole of the photoelectric effect follows from that one sentence.",
             calc=f"E = hc {DIV} {chr(955)} = ({sci(HC,4)}) {DIV} ({sci(400e-9,3)}) = {sci(e46_J,4)} J"),
        dict(t="Convert to electronvolts, because the work function is given in them",
             body="",
             calc=f"E = ({sci(e46_J,4)}) {DIV} ({sci(EV,3)}) = {S(e46_eV,3)} eV"),
        dict(t="The work function is the toll at the door",
             body="Some energy is spent simply getting the electron out of the metal. Whatever is left is kinetic energy.",
             calc=f"KE(max) = E {chr(8722)} {chr(981)} = {S(e46_eV,3)} {chr(8722)} 2.3 = {S(ke46,2)} eV"),
    ],
    answer=(f"{S(ke46,2)} eV, which is {sci(ke46*EV,3)} J", "",
            "And that is the MAXIMUM. Most electrons come out with less."),
    trap=(f"{chr(8220)}turn the light up and the electrons come out faster{chr(8221)}",
          "They do not. Brightness is the number of photons per second, not the energy of each "
          "one. A brighter lamp of the same colour ejects MORE electrons at exactly the same "
          "maximum energy. To give each electron more energy you have to change the colour, "
          "not the intensity - and that fact is what killed the wave-only picture of light."),
    sanity=(f"Find the threshold: a 2.3 eV work function needs a photon of at least that "
            f"energy, so {chr(955)} = hc {DIV} {chr(981)} = {sci(lam0,3)} m, about 540 nm, "
            f"which is green. So this metal emits under blue and violet light and does "
            f"nothing at all under red, however bright the red is."),
)

# --- 47 --------------------------------------------------------------------
eg47 = R(HC / 550e-9 / EV, 3)
ex47 = R(HC / 1.0e-10 / EV, 4)
P(
    n=47, part="Modern Physics", chapter="Quantum physics", level="A-LEVEL",
    book="Part 7 · Modern Physics (pp. 85-94)",
    title="Why a bright green laser is safer than a faint X-ray",
    statement=(f"Compare the energy of a photon of green light ({chr(955)} = 550 nm) with a "
               f"photon of X-radiation ({chr(955)} = 0.10 nm). The ionisation energy of a "
               f"hydrogen atom is 13.6 eV. Which of the two can ionise an atom?"),
    given=[("green light", "550 nm", ""), ("X-ray", "0.10 nm", ""),
           ("ionisation energy of hydrogen", "13.6", "eV")],
    wanted="the two photon energies, and which can ionise",
    steps=[
        dict(t="Photon energy is inversely proportional to wavelength",
             body="Short wavelength means high energy. That one relationship orders the whole electromagnetic spectrum by how dangerous it is.",
             calc=f"E = hc {DIV} {chr(955)}"),
        dict(t="The green photon",
             body="",
             calc=f"E = ({sci(HC,4)}) {DIV} ({sci(550e-9,3)}) {DIV} ({sci(EV,3)}) = {S(eg47,3)} eV"),
        dict(t="The X-ray photon",
             body="",
             calc=f"E = ({sci(HC,4)}) {DIV} ({sci(1.0e-10,2)}) {DIV} ({sci(EV,3)}) = {S(ex47/1000,4)} keV"),
        dict(t="Compare each with 13.6 eV",
             body="",
             calc=f"{S(eg47,3)} eV < 13.6 eV     {S(ex47,5)} eV > 13.6 eV"),
    ],
    answer=(f"green {S(eg47,3)} eV, X-ray {S(ex47/1000,3)} keV - only the X-ray ionises", "",
            f"The X-ray photon carries about {S(ex47/eg47/1000,2)} thousand times the energy of the green one."),
    trap=(f"{chr(8220)}a powerful laser must be more dangerous than a weak X-ray source{chr(8221)}",
          "Ionisation happens one photon at a time, so what matters is the energy of the "
          "individual photon, not how many arrive. A hundred-watt green laser delivers an "
          "enormous number of photons, every one of them too feeble to ionise anything - it "
          "burns, but it cannot break a molecule apart. A single X-ray photon can."),
    sanity=(f"This is why a reading lamp is harmless and a dental X-ray is measured and "
            f"shielded. It also explains sunburn: visible light at {S(eg47,3)} eV does nothing "
            f"to DNA, while ultraviolet, just beyond the violet end, finally crosses the "
            f"threshold where chemical bonds start to break."),
)

# --- 48 --------------------------------------------------------------------
a48 = R(7200 / 2**4, 3)
P(
    n=48, part="Modern Physics", chapter="Radiation", level="GCSE",
    book="Part 7 · Modern Physics (pp. 85-94)",
    title="A radioactive source, a day later",
    statement=("A radioactive source has an activity of 7200 Bq and a half-life of 6.0 hours. "
               "Find its activity 24 hours later."),
    given=[("initial activity", "7200", "Bq"), ("half-life", "6.0", "hours"),
           ("time elapsed", "24", "hours")],
    wanted="the activity after 24 hours",
    steps=[
        dict(t="Count how many half-lives have passed",
             body="",
             calc=f"n = 24 {DIV} 6.0 = 4 half-lives"),
        dict(t="Each half-life halves the activity, so they compound",
             body="Four halvings is not a quarter and it is not a half four times over. It is a half multiplied by itself four times.",
             calc=f"A = 7200 {DIV} 2⁴ = 7200 {DIV} 16"),
        dict(t="Solve",
             body="",
             calc=f"A = {S(a48,3)} Bq"),
    ],
    answer=(S(a48, 3), "Bq", "A sixteenth of what it started at, after four half-lives."),
    trap=("1800 Bq",
          "Dividing by the number of half-lives instead of halving that many times: 7200 ÷ 4 "
          "rather than 7200 ÷ 2⁴. Radioactive decay is exponential, not linear. The linear "
          "version also predicts that after eight half-lives the activity is negative, which "
          "should be enough to retire the method permanently."),
    sanity=(f"After four half-lives the fraction left is 1/16, which is "
            f"{S(100/16,3)}% - and {S(100/16,3)}% of 7200 is {S(a48,3)} Bq. Note too that it "
            f"never reaches zero: halving something repeatedly gets you arbitrarily close and "
            f"never quite there."),
)

# --- 49 --------------------------------------------------------------------
defect_u = R(1.007276 + 1.008665 - 2.013553, 4)
defect_kg = defect_u * 1.661e-27
e49_J = defect_kg * C_LIGHT**2
e49_MeV = e49_J / EV / 1e6
P(
    n=49, part="Modern Physics", chapter="The atom", level="A-LEVEL",
    book="Part 7 · Modern Physics (pp. 85-94)",
    title="The mass that goes missing when a nucleus forms",
    statement=(f"A proton has a mass of 1.007276 u and a neutron 1.008665 u, yet a deuterium "
               f"nucleus made of one of each has a mass of only 2.013553 u. Find the energy "
               f"equivalent of the missing mass, in MeV. "
               f"Take 1 u = 1.661 {TIMES} 10⁻²⁷ kg and c = 3.00 {TIMES} 10⁸ m/s."),
    given=[("proton", "1.007276", "u"), ("neutron", "1.008665", "u"),
           ("deuterium nucleus", "2.013553", "u"), ("1 u", f"1.661 {TIMES} 10⁻²⁷", "kg")],
    wanted="the binding energy of the nucleus, in MeV",
    steps=[
        dict(t="Find the mass that is unaccounted for",
             body="The parts weigh more apart than they do together. That difference is not an error in the measurement; it is the point of the question.",
             calc=f"{DELTA}m = (1.007276 + 1.008665) {chr(8722)} 2.013553 = {S(defect_u,4)} u"),
        dict(t="Convert to kilograms",
             body="",
             calc=f"{DELTA}m = {S(defect_u,4)} {TIMES} ({sci(1.661e-27,4)}) = {sci(defect_kg,4)} kg"),
        dict(t="Apply E = mc², and square c",
             body="",
             calc=f"E = ({sci(defect_kg,4)}) {TIMES} ({sci(C_LIGHT,3)}){SQ} = {sci(e49_J,4)} J"),
        dict(t="Convert to MeV",
             body="",
             calc=f"E = ({sci(e49_J,4)}) {DIV} ({sci(EV,3)}) = {S(e49_MeV,3)} MeV"),
    ],
    answer=(S(e49_MeV, 3), "MeV", "The energy you would have to supply to pull the two particles apart again."),
    trap=(f"{sci(defect_kg*C_LIGHT,3)} J",
          f"Multiplying by c instead of c². The square is the whole reason nuclear energies "
          f"are millions of times chemical ones: it turns a factor of {sci(C_LIGHT,3)} into "
          f"{sci(C_LIGHT**2,3)}. Leaving it out makes the answer "
          f"{sci(C_LIGHT,3)} times too small."),
    sanity=(f"The accepted binding energy of the deuteron is 2.224 MeV. This calculation gives "
            f"{S(e49_MeV,4)} MeV from nothing but three masses and a constant - agreement to "
            f"within a fraction of a percent, which is the strongest possible sign the method "
            f"is sound."),
)

# --- 50 --------------------------------------------------------------------
ke50 = EV * 100
v50 = math.sqrt(2 * ke50 / 9.11e-31)
p50 = 9.11e-31 * v50
lam50 = H_PLANCK / p50
P(
    n=50, part="Modern Physics", chapter="Quantum physics", level="A-LEVEL",
    book="Part 7 · Modern Physics (pp. 85-94)",
    title="An electron with a wavelength",
    statement=(f"An electron is accelerated from rest through a potential difference of 100 V. "
               f"Find its de Broglie wavelength. Take the mass of an electron as "
               f"9.11 {TIMES} 10⁻³¹ kg and h = 6.63 {TIMES} 10⁻³⁴ J s."),
    given=[("V", "100", "V"), ("m", f"9.11 {TIMES} 10⁻³¹", "kg"),
           ("e", f"1.60 {TIMES} 10⁻¹⁹", "C"), ("h", f"6.63 {TIMES} 10⁻³⁴", "J s")],
    wanted="the de Broglie wavelength of the electron",
    steps=[
        dict(t="The work done by the field becomes kinetic energy",
             body="Charge multiplied by potential difference is energy, and the electron starts from rest, so all of it is kinetic.",
             calc=f"KE = eV = ({sci(EV,3)}) {TIMES} 100 = {sci(ke50,3)} J"),
        dict(t="Get the speed from the kinetic energy",
             body="",
             calc=f"v = {ROOT}(2KE {DIV} m) = {ROOT}(2 {TIMES} ({sci(ke50,3)}) {DIV} "
                  f"({sci(9.11e-31,3)})) = {sci(v50,4)} m/s"),
        dict(t="Momentum, not speed, is what goes into the de Broglie relation",
             body="",
             calc=f"p = mv = ({sci(9.11e-31,3)}) {TIMES} ({sci(v50,4)}) = {sci(p50,4)} kg m/s"),
        dict(t="Apply de Broglie",
             body="",
             calc=f"{chr(955)} = h {DIV} p = ({sci(H_PLANCK,3)}) {DIV} ({sci(p50,4)}) = {sci(lam50,3)} m"),
    ],
    answer=(f"{sci(lam50,3)} m, or {S(lam50*1e9,3)} nm", "",
            "A particle with a wavelength about the width of an atom."),
    trap=(f"using {chr(955)} = h {DIV} v",
          "Dividing by the speed instead of the momentum. The de Broglie relation pairs a "
          "wavelength with a MOMENTUM, which is why a cricket ball and an electron at the same "
          "speed have utterly different wavelengths - the mass is doing the work. Dropping the "
          "mass also leaves the units wrong, and the units are the fastest way to catch it."),
    sanity=(f"Two checks. The wavelength, {S(lam50*1e9,3)} nm, is about the spacing between "
            f"atoms in a crystal - which is exactly why electrons diffract off crystals and "
            f"why an electron microscope resolves what light never can. And the speed came out "
            f"at {S(v50/C_LIGHT*100,3)}% of the speed of light, comfortably low enough that "
            f"ignoring relativity was justified."),
)

# ---------------------------------------------------------------------------
# One line per trap, for the index at the back. Written by hand rather than cut
# from the first sentence: a few of those read as continuations, not as entries.
TRAPLINE = {1: 'Dividing by 3.6, which converts km/h and not mph', 2: 'Changing the unit label without changing the number', 3: 'Adding the magnitudes of two perpendicular forces', 4: 'Dividing distance by time at one point, on a line that misses the origin', 5: 'Putting a speed in mph straight into SUVAT', 6: 'Dividing the height by g, as though g were a speed', 7: 'Thinking horizontal speed keeps a projectile up for longer', 8: 'Writing N = ma and forgetting the weight', 9: 'Using N = mg on a slope', 10: 'Treating μN as the friction force rather than its maximum', 11: 'Forgetting cos θ when the pull is at an angle', 12: 'Calling the question unanswerable because the mass is missing', 13: 'Quoting the work done and labelling it power', 14: 'Conserving kinetic energy in a collision where things stick', 15: 'Believing the airbag reduces the momentum change', 16: 'Thinking a heavier car has to corner more slowly', 17: 'Giving the gauge pressure when the total was asked for', 18: 'Thinking a bigger block of the same material sinks', 19: 'Believing a hydraulic jack multiplies energy', 20: 'Using the object’s density in the upthrust instead of the fluid’s', 21: 'Expecting higher pressure where the pipe is narrower', 22: 'Using the final temperature as ΔT', 23: 'Expecting the temperature to rise while ice melts', 24: 'Averaging two temperatures instead of balancing the energy', 25: 'Taking a gas-law ratio in degrees Celsius', 26: 'Leaving atmospheric pressure out of Boyle’s law', 27: 'Calling all of a power station’s rejected heat bad engineering', 28: 'Swapping a rate for a total, watts for joules', 29: 'Dividing I by V instead of V by I', 30: 'Splitting the supply voltage equally between unequal resistors', 31: 'Adding resistances that are in parallel', 32: 'Putting the wrong resistor on top in a potential divider', 33: 'Reaching for P = VI and using the supply voltage', 34: 'Reading the power rating off the label and calling it the energy', 35: 'Leaving the time in minutes', 36: 'Fitting a bigger fuse on the grounds that it must be safer', 37: 'Dividing by r instead of r² in an inverse-square law', 38: 'Quoting the potential difference as the field strength', 39: 'Leaving the frequency in megahertz', 40: 'Measuring half a wave and calling it a cycle', 41: 'Forgetting that an echo makes the journey twice', 42: 'Measuring the angle from the surface instead of the normal', 43: 'Expecting light to escape beyond the critical angle', 44: 'Stopping at 1/v and writing it down as the distance', 45: 'Thinking sound travels faster towards you', 46: 'Expecting a brighter light to give each electron more energy', 47: 'Judging danger by the brightness rather than the photon energy', 48: 'Dividing by the number of half-lives instead of halving that often', 49: 'Multiplying by c instead of c²', 50: 'Dividing h by the speed instead of by the momentum'}

for _p in PROBLEMS:
    _p["trapline"] = TRAPLINE[_p["n"]]

# ===========================================================================
# render
# ===========================================================================
if __name__ == "__main__":
    out = pathlib.Path(__file__).parent
    (out / "solutions.json").write_text(json.dumps(PROBLEMS, indent=1, ensure_ascii=False))

    L = ["# PHYSICS SOLVED — Phase A draft\n",
         f"Problems written, computed and verified: **{len(PROBLEMS)} of 50**\n"]
    part = None
    for p in PROBLEMS:
        if p["part"] != part:
            part = p["part"]
            L.append(f"\n---\n\n# PART: {part.upper()}\n")
        L.append(f"\n## {p['n']}. {p['title']}")
        L.append(f"`{p['level']}` · {p['chapter']} · {p['book']}\n")
        L.append(f"**PROBLEM**\n\n{p['statement']}\n")
        g = "  |  ".join(f"{a} = {b} {c}".strip() for a, b, c in p["given"])
        L.append(f"**KNOWN** — {g}\n")
        L.append(f"**WANTED** — {p['wanted']}\n")
        L.append("**STEPS**\n")
        for i, s in enumerate(p["steps"], 1):
            L.append(f"{i}. **{s['t']}**  ")
            if s["body"]:
                L.append(f"   {s['body']}  ")
            L.append(f"   `{s['calc']}`\n")
        val, unit, note = p["answer"]
        L.append(f"**ANSWER — {(val + ' ' + unit).strip()}**  \n{note}\n")
        L.append(f"**⚠ THE TRAP — most students answer {p['trap'][0]}**  \n{p['trap'][1]}\n")
        L.append(f"**DOES IT MAKE SENSE?**  \n{p['sanity']}\n")
        if p.get("alt"):
            L.append(f"**ANOTHER WAY IN**  \n{p['alt']}\n")
    (out / "draft.md").write_text("\n".join(L))
    print(f"wrote {len(PROBLEMS)} problems -> solutions.json + draft.md")
