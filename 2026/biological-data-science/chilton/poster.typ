// Galaxy Workflow Foundry poster, CSHL Biological Data Science 2026: a four-column poster. Info boxes carry the story; receipts are figures. 44in x 44in.
// Receipts from receipts.json; the route diagram from route.json (both extracted from the Foundry run).
// Flags (sys.inputs): bleed=1 adds 0.125in bleed; count=1 hides word-count-exempt text;
// noguard=1 turns layout asserts into red on-page messages; debug=1 prints each column's slack.

#let d = json("receipts.json")
#let route = json("route.json")
#let q = json("assets/qr.json")
#let bleed = if sys.inputs.at("bleed", default: "0") == "1" { 0.125in } else { 0pt }
#let counting = sys.inputs.at("count", default: "0") == "1"
#let noguard = sys.inputs.at("noguard", default: "0") == "1"
#let debug = sys.inputs.at("debug", default: "0") == "1"
#let guard(cond, message: "") = if not noguard { assert(cond, message: message) } else if not cond {
  text(font: "IBM Plex Mono", size: 30pt, fill: red, weight: "bold", "GUARD: " + message) }
#let exempt(body) = if counting { hide(body) } else { body } // title, authors, refs, QR captions

// ---------- Galaxy+ tokens (opaque, except masthead stars and rings) ----------
#let paper = rgb("#edf4fa")
#let grid-minor = rgb("#daecf8")
#let grid-major = rgb("#aecce7")
#let slip = rgb("#ffffff")
#let tint = rgb("#f1f9fe")
#let ink = rgb("#2c3143")
#let ink-deep = rgb("#1a1f2e")
#let ink-soft = rgb("#58585a")
#let space = rgb("#121629")
#let pen = rgb("#25537b")
#let info = rgb("#197cd2")
#let glow = rgb("#3b6fd6")
#let gold = rgb("#ffd700")
#let gold-dark = rgb("#d19e00")
#let nova = rgb("#ff6a2b")
#let nova-dark = rgb("#c2410c")
#let hl-col = rgb("#fff489")
#let tape-col = rgb("#cde0f0")
#let orbit-col = rgb("#aecce7")
#let rule-col = rgb("#dee2e6")
#let shadow-col = rgb("#c9d6e3")
#let stamp-ink = rgb("#e31a1e")
#let stamp-ok = rgb("#006f50")
#let ochre = gold-dark
#let thermal = gradient.linear(gold, nova)
#let bar-grad = gradient.linear(gold, gold, nova)
#let feat-bar = gradient.linear(gold, nova, angle: 90deg)
#let mast-white = rgb(255, 255, 255, 38)

// IBM Plex last: glyph fallback only (→, №), which Atkinson lacks
#let sans = ("Atkinson Hyperlegible Next", "IBM Plex Sans")
#let display = sans
#let mono = ("Atkinson Hyperlegible Mono", "IBM Plex Mono")
#let hand = ("Kalam", "IBM Plex Sans")
#let r-card = 0.25in
#let r-small = 0.08in

// ---------- copy that changes most ----------
#let hero1 = [Build better skills. Build better workflows.]
#let hero2 = (lead: [Keep the ], mark: [receipts], tail: [.])
#let thesis = [A skill is compiled from notes people can read; a workflow is type-checked before any job runs; both print a receipt you can keep.]
#let authors = [John Chilton¹, Marius van den Beek¹, Dannon Baker², Danielle Callan³, Scott Cain¹, Anton Nekrutenko¹]
#let affils = [¹The Pennsylvania State University, University Park, PA, USA #h(0.6em) ²Johns Hopkins University, Baltimore, MD, USA #h(0.6em) ³Temple University, Philadelphia, PA, USA]

// ---------- geometry (inches from the trim) ----------
#let W = 44in
#let safe = 43in // content stays 1in inside the trim
#let cw = 9.9in // column width
#let cg = 0.8in // column gutter
#let colx = range(4).map(i => 1.0in + i * (cw + cg))
#let y0 = 9.15in // column tops
#let span-h = 9.95in // route card (columns 2-4)
#let y1 = y0 + span-h + 0.55in // columns 2-4 start under the route card
#let gapv = 0.45in // space between stacked items in a column
#let rpad = 0.5in // receipt side inset
#let qr-w = 4.4in

#guard(colx.last() + cw <= safe, message: "columns outside the 1in safe zone")

#set page(width: W + 2 * bleed, height: W + 2 * bleed, margin: 0pt, fill: paper,
  background: {
    for i in range(-1, 178) {
      let p = bleed + i * 0.25in
      let st = if calc.rem(i, 4) == 0 { 1.6pt + grid-major } else { 0.8pt + grid-minor }
      place(top + left, line(start: (p, 0pt), end: (p, W + 2 * bleed), stroke: st))
      place(top + left, line(start: (0pt, p), end: (W + 2 * bleed, p), stroke: st))
    }
  })
#set text(font: mono, size: 28pt, fill: ink, lang: "en")
#set par(leading: 0.42em, spacing: 0.5em)
#set smartquote(enabled: true)
#show raw: it => text(font: mono, size: 1.25em, it.text) // undo raw's 0.8em default

// ---------- helpers ----------
#let dots = box(width: 1fr, repeat(gap: 0.18em)[#text(fill: grid-major)[.]])
#let hl(body, top: "x-height") = highlight(fill: hl-col, extent: 3pt, top-edge: top, bottom-edge: "descender", body)
#let anchor(name) = [#metadata(name)#label(name)]
#let put(x, y, w, limit: safe, what: "block", body) = context {
  let h = measure(block(width: w, body)).height
  guard(y + h <= limit, message: what + " overflows by " + repr((y + h - limit).to-absolute()))
  place(top + left, dx: x + bleed, dy: y + bleed, block(width: w, body))
}
// a line that must not wrap: fails the build if its natural width exceeds the space it sits in
#let one-line(body, what: "line") = layout(sz => {
  let w = measure(body).width
  guard(w <= sz.width, message: what + " too wide by " + repr((w - sz.width).to-absolute()))
  body
})

// section badge: a filled disc, white numeral; hot = the one featured (nova) badge
#let badge(n, r: 0.46in, hot: false) = box(baseline: 18%, circle(radius: r, fill: if hot { nova } else { pen }, inset: 0pt,
  align(center + horizon, text(font: sans, weight: 800, size: 54pt, fill: slip, str(n)))))

#let arrow-st(th) = (paint: pen, thickness: th, cap: "round", join: "round")
// pen arrow in local coordinates (inside a box)
#let arrow(x0, y0, x1, y1, bend: 0.12, th: 5.5pt, head: 30) = {
  let (fx, fy, tx, ty) = (x0.pt(), y0.pt(), x1.pt(), y1.pt())
  let (mx, my) = (fx + (tx - fx) / 2 - (ty - fy) * bend, fy + (ty - fy) / 2 + (tx - fx) * bend)
  place(top + left, curve(stroke: arrow-st(th), curve.move((fx * 1pt, fy * 1pt)),
    curve.quad((mx * 1pt, my * 1pt), (tx * 1pt, ty * 1pt))))
  let a = calc.atan2(tx - mx, ty - my)
  for s in (150deg, -150deg) {
    let b = a + s
    place(top + left, curve(stroke: arrow-st(th), curve.move((tx * 1pt, ty * 1pt)),
      curve.line(((tx + head * calc.cos(b)) * 1pt, (ty + head * calc.sin(b)) * 1pt))))
  }
}

// double-bordered, rotated; gx-ok for PASS (never nova or gold)
#let stamp(angle: -8deg, size: 62pt, col: stamp-ok, body) = rotate(angle, reflow: false, box(
  inset: 0.07in, radius: 12pt, stroke: (paint: col, thickness: 6pt), box(
  inset: (x: 0.24in, y: 0.08in), radius: 6pt, stroke: (paint: col, thickness: 2.5pt),
  text(font: sans, weight: 800, size: size, fill: col, tracking: 0.06em, body))))


#let zig(w, fill, n: 28) = {
  let step = w / n
  let pts = ((0pt, 0pt),)
  for i in range(n) {
    pts.push(((i + 0.5) * step, 0.24in))
    pts.push(((i + 1) * step, 0pt))
  }
  polygon(fill: fill, stroke: none, ..pts)
}

#let code-of(name, w) = { let m = q.at(name).modules; w * m / (m + 2 * q.border) }
#let qr-tile(name, cap, w: qr-w) = block(width: w)[
  #guard(code-of(name, w) >= 2.5in, message: name + " code under 2.5in")
  #box(width: w, height: w, radius: r-card, clip: true, stroke: 2pt + rule-col, image("assets/" + name + ".svg", width: w))
  #v(-0.05em)
  #exempt(align(center, text(font: sans, size: 30pt, weight: "bold", fill: ink, cap)))
]
// white tile, the poster's only coloured ring
#let placeholder(w, h, body) = rect(width: w, height: h, radius: r-card, fill: slip, stroke: 3pt + nova,
  inset: 0.3in, align(center + horizon, text(weight: "bold", fill: ink, body)))

// ---------- text styles ----------
#let prose(body) = {
  set text(font: sans, size: 30pt, fill: ink)
  set par(leading: 0.34em, spacing: 0.62em, justify: false)
  body
}
#let lead(body) = block(below: 0.32in, {
  set text(font: sans, size: 38pt, weight: "semibold", fill: ink)
  set par(leading: 0.26em)
  body
})
#let penhead(body) = block(above: 0.3in, below: 0.16in,
  text(font: hand, weight: "bold", size: 54pt, fill: pen, body))
#let pen-text(size: 36pt, body) = {
  set text(font: hand, size: size, fill: pen)
  set par(leading: 0.24em, spacing: 0.4em)
  body
}
#let cmd(body) = one-line(what: "command", text(font: mono, size: 28pt, weight: "semibold", tracking: -0.012em, body))

// ---------- cards: white Galaxy cards; feat = gold-to-nova left bar and nova badge (one per poster) ----------
#let card(n, head, body, w: cw, inset: 0.5in, aside: none, aside-w: 20in, feat: false, head-in-body: false) = context {
  let hd = {
    set par(leading: 0.12em)
    if n != none [#badge(n, hot: feat)#h(0.3em)]
    text(font: display, weight: 700, size: 72pt, tracking: -0.02em, fill: ink, head)
  }
  let inner = block(width: w, inset: (x: inset, top: 0.45in, bottom: 0.42in), {
    if head-in-body { } else if aside == none { block(below: 0.26in, hd) } else {
      block(below: 0.3in, grid(columns: (1fr, aside-w), column-gutter: 0.6in, align: (left + top, left + top), hd, prose(aside)))
    }
    prose(body)
  })
  let h = measure(inner).height
  box(width: w, height: h, {
    place(top + left, dx: 0.08in, dy: 0.08in, rect(width: w, height: h, radius: r-card, fill: shadow-col))
    place(top + left, box(width: w, height: h, radius: r-card, clip: true, fill: slip,
      if feat { place(top + left, rect(width: 0.12in, height: h, fill: feat-bar)) }))
    place(top + left, inner)
  })
}

// ---------- receipts: thermal slips with a torn foot, in column flow ----------
#let part(body, top: 0.08in, bottom: 0.08in) = block(width: 100%, inset: (top: top, bottom: bottom), spacing: 0pt, body)
#let row(l, r, what: "receipt row") = part(layout(sz => {
  let (wl, wr) = (measure(l).width, measure(r).width)
  guard(wl + wr + 0.6in <= sz.width, message: what + " too wide (" + repr((wl + wr + 0.6in - sz.width).to-absolute()) + ")")
  [#l#h(0.3em)#dots#h(0.3em)#r]
}))
#let rule(top: 0.14in, bottom: 0.14in) = part(top: top, bottom: bottom,
  line(length: 100%, stroke: (paint: ink, thickness: 2.5pt, dash: "dashed")))
#let head(n, word, when, sub) = (
  part(top: 0pt, bottom: 0.04in, grid(columns: (1fr, auto), align: (left + bottom, right + bottom),
    text(weight: "bold", size: 60pt, tracking: 0.05em, word),
    text(size: 28pt)[#text(fill: ink-soft)[№#n#h(0.4em)]#when])),
  part(top: 0.06in, bottom: 0.02in, one-line(what: "receipt sub-head", text(size: 28pt, fill: ink-soft, sub))),
)
#let jobs(n, tail: none) = part(top: 0.12in, bottom: 0.06in, layout(sz => {
  let b = text(size: 38pt, weight: "bold")[JOBS RUN#h(0.3em)#dots#h(0.3em)#n#if tail != none [#text(size: 28pt, weight: "regular")[#h(0.3em)#tail]]]
  let natural = measure(text(size: 38pt, weight: "bold")[JOBS RUN #n#if tail != none [#text(size: 28pt)[ #tail]]]).width
  guard(natural + 0.6in <= sz.width, message: "JOBS RUN row too wide")
  box(width: 100%, b)
}))
#let signed(prog) = part(top: 0.12in, bottom: 0pt, grid(columns: (auto, 1fr), column-gutter: 0.35em, align: bottom,
  text(size: 28pt, fill: ink-soft)[SIGNED],
  block(width: 100%, stroke: (bottom: 2.5pt + ink), inset: (bottom: 0.08in), text(size: 36pt, weight: "bold", hl(prog)))))

// square white slip, gold-to-nova thermal strip on top, torn foot
#let receipt(parts, w: cw, stamp-over: none) = context {
  let inner = block(width: w, inset: (x: rpad, top: 0.44in, bottom: 0.36in), stack(spacing: 0pt, ..parts))
  let h = measure(inner).height
  box(width: w, height: h + 0.26in, {
    place(top + left, dx: 0.08in, dy: 0.08in, rect(width: w, height: h, fill: shadow-col))
    place(top + left, dx: 0.08in, dy: h + 0.08in - 1pt, zig(w, shadow-col))
    place(top + left, dy: h - 1pt, zig(w, slip))
    place(top + left, rect(width: w, height: h, fill: slip))
    place(top + left, rect(width: w, height: 0.08in, fill: thermal))
    place(top + left, inner)
    if stamp-over != none { place(top + left, dx: stamp-over.dx, dy: stamp-over.dy, stamp-over.body) }
  })
}
#let caption(n, title, body) = block(width: 100%, above: 0.22in, below: 0pt, inset: (left: 0.1in, right: 0.1in), {
  set text(font: sans, size: 28pt, fill: ink)
  set par(leading: 0.3em)
  [#text(weight: "bold")[Figure #n · #title.] #body]
})
#let figure-slip(n, title, cap, parts, stamp-over: none) = stack(spacing: 0pt,
  receipt(parts, stamp-over: stamp-over), caption(n, title, cap))

// ---------- header: nebula masthead, full bleed ----------
#let mast-h = 8.35in // band foot, from the trim
#let bar-h = 0.25in
#let stars = tiling(size: (0.5in, 0.5in))[
  #place(dx: 0.1in, dy: 0.12in, circle(radius: 1.2pt, fill: rgb(255, 255, 255, 30)))
  #place(dx: 0.36in, dy: 0.38in, circle(radius: 0.7pt, fill: rgb(255, 255, 255, 20)))
]
// points along a rotated ellipse, for rings and the one nova swoosh
#let orbit-pts(cx, cy, a, b, rot, t0, t1, n: 90) = range(n + 1).map(i => {
  let t = t0 + (t1 - t0) * i / n
  let (x, y) = (a * calc.cos(t), b * calc.sin(t))
  (cx + x * calc.cos(rot) - y * calc.sin(rot), cy + x * calc.sin(rot) + y * calc.cos(rot))
})
#let orbit-path(pts, st) = curve(stroke: st, curve.move(pts.at(0)), ..pts.slice(1).map(q => curve.line(q)))
#let MW = W + 2 * bleed
#let MH = mast-h + bleed
#let ring1 = (33in, 2.2in, 17in, 4.6in, -9deg)
#let ring2 = (27in, 3.6in, 25in, 7.2in, -7deg)
#place(top + left, box(width: MW, height: MH, clip: true, {
  place(rect(width: MW, height: MH, fill: space))
  // opaque nebula: blue glow top right, faint nova glow bottom left; outer stops are the band colour
  place(rect(width: MW, height: MH, fill: gradient.radial(glow, info.mix((space, 62%)), space,
    center: (84%, 18%), radius: 62%)))
  place(dx: -9in, dy: MH - 6in, ellipse(width: 20in, height: 12in, fill: gradient.radial(nova.mix((space, 62%)), space)))
  place(rect(width: MW, height: MH, fill: stars))
  for (cx, cy, a, b, rot) in (ring1, ring2) {
    place(orbit-path(orbit-pts(cx + bleed, cy + bleed, a, b, rot, 0deg, 360deg, n: 240), 1.5pt + mast-white))
  }
  // the one nova swoosh: a stretch of the inner ring, under the thesis
  let (cx, cy, a, b, rot) = ring1
  place(orbit-path(orbit-pts(cx + bleed, cy + bleed, a, b, rot, 72deg, 100deg, n: 60),
    (paint: nova, thickness: 6pt, cap: "round")))
}))
#place(top + left, dy: MH, rect(width: MW, height: bar-h, fill: bar-grad))
#let hero-mark(body) = box(text(fill: gradient.linear(gold, nova, relative: "parent"), weight: 800, body))
#let kick-y = 0.8in
#let title-y = 1.6in
// kicker row: white Galaxy logo + tracked mono kicker in gold
#let kicker = exempt(box(height: 0.7in, {
  box(baseline: -0.04in, image("assets/galaxy_logo_white.svg", height: 0.62in))
  h(0.35in)
  box(baseline: -0.12in, text(font: mono, weight: "bold", size: 36pt, tracking: 0.18em, fill: gold)[WORKFLOW FOUNDRY])
}))
#place(top + left, dx: 1.0in + bleed, dy: kick-y + bleed, kicker)
#context guard(kick-y + measure(kicker).height + 0.1in < title-y, message: "kicker runs into the title")
#put(1.0in, title-y, 41in, limit: 5.15in, what: "title")[
  #exempt[
    #set text(font: display, weight: 800, size: 120pt, tracking: -0.03em, fill: slip)
    #set par(leading: 30pt)
    #hero1 \
    #hero2.lead#hero-mark(hero2.mark)#hero2.tail
  ]
]
#put(20.2in, 3.55in, 22.3in, limit: 6.1in, what: "thesis",
  rotate(-1.5deg, reflow: false, text(font: hand, weight: "bold", size: 48pt, fill: tape-col)[#set par(leading: 0.22em)
    #thesis]))
#put(1.0in, 6.55in, 37.5in, limit: mast-h - 0.2in, what: "authors")[
  #exempt[
    #set par(leading: 0.3em)
    #text(font: sans, size: 42pt, weight: "bold", fill: slip, authors) \
    #text(font: sans, size: 28pt, fill: tape-col, affils)
  ]
]

// ---------- data ----------
#let c = d.cast
#let pn = d.pinned
#let vd = d.validated
#let ts = d.tested
#let rr = route.run

// ---------- the four receipts ----------
#let r-cast = (
  ..head(1, [CAST], [#c.cast_at.slice(5)], [skill build · foundry \@ #c.foundry]),
  rule(),
  row[#text(weight: "bold")[SKILL.md]][#c.skill],
  row[MOLD rev #c.revision][#c.hash],
  row[#c.refs refs][#c.upfront upfront · #(c.refs - c.upfront) on demand],
  rule(),
  signed(c.signed),
)
#let pin-row(p) = part(top: 0.09in, bottom: 0.07in, stack(spacing: 0.1in,
  one-line(what: "pin row", [#text(fill: ink-soft)[#p.owner/]#text(weight: "bold", p.tool)]),
  align(right, one-line(what: "pin row", [#p.version #text(fill: ink-soft)[\@]#p.changeset]))))
#let r-pinned = (
  ..head(2, [PINNED], [10-20 #pn.from–#pn.to], [Tool Shed changesets · phase #rr.loop_phase]),
  rule(),
  ..pn.pins.map(pin-row),
  rule(),
  signed(pn.signed),
)
#let r-validated = (
  ..head(3, [VALIDATED], [10-21 #vd.at], [replayed · gxwf #vd.cli · #vd.replayed]),
  rule(),
  part({
    set par(leading: 0.3em)
    one-line(what: "gxwf command")[\$ gxwf validate]
    one-line(what: "gxwf command")[#h(1.2em)galaxy-workflow.gxwf.yml]
    one-line(what: "gxwf command")[#h(1.2em)#"--connections --strict --json"]
  }),
  row[Tool state][#vd.tool_state.ok ok · #vd.tool_state.fail fail · #vd.tool_state.skip skip],
  row[Connections][#vd.connections.ok ok · #vd.connections.invalid invalid],
  row[map-over][all #vd.map_over_list steps over list],
  row[wall time][\< 1 s],
  rule(),
  signed(vd.signed),
)
#let r-tested = (
  ..head(4, [TESTED], [10-21 #ts.at], [planemo #ts.planemo · its JSON report]),
  rule(),
  row[planemo test][#ts.status],
  row[tests][#ts.summary.num_tests · failures #ts.summary.num_failures · errors #ts.summary.num_errors],
  row[Tool Shed repos, at the pins][#ts.installed],
  row[containers][#ts.containers],
  row[wall time][#ts.minutes min],
  rule(),
  jobs([#ts.jobs], tail: [ok · #(ts.jobs - ts.jobs_ok) failed]),
  signed(ts.signed),
)

// ---------- column 1: what it does ----------
#let mbox(tag, body, fill: tint, stroke: 2.5pt + pen) = block(width: 100%, inset: (x: 0.28in, y: 0.17in), radius: r-small,
  fill: fill, stroke: stroke, {
    set par(leading: 0.28em)
    text(font: mono, weight: "bold", size: 28pt, tracking: 0.08em, fill: pen, tag)
    linebreak()
    text(font: sans, size: 28pt, body)
  })
#let down(label) = block(width: 100%, height: 1.02in, inset: 0pt, spacing: 0pt, {
  place(top + left, dx: 0.9in, dy: 0.06in, line(start: (0pt, 0pt), end: (0pt, 0.62in), stroke: arrow-st(7pt)))
  place(top + left, dx: 0.9in - 0.22in, dy: 0.6in, polygon(fill: pen, (0in, 0in), (0.44in, 0in), (0.22in, 0.36in)))
  place(top + left, dx: 1.5in, dy: 0.12in, text(font: hand, weight: "bold", size: 40pt, fill: pen, label))
})
#let machine = context {
  let inner = stack(spacing: 0pt,
    mbox([KNOWLEDGE BASE], [notes, schemas, command manuals and patterns, written for people to read and review
      #v(0.04in)
      #pad(left: 0.4in, mbox([MOLD · ONE ACTION], fill: slip, [the exact references one action needs, plus its procedure]))]),
    down[cast: no model, same bytes],
    grid(columns: (1fr, 1fr), column-gutter: 0.3in,
      mbox([SKILL], [frozen, for the agent]),
      mbox([PROVENANCE], [a hash for every source used])),
    down[the agent runs it],
    mbox([GALAXY WORKFLOW], [checked by gxwf, run by Planemo]),
  )
  inner
}
#let card-what = card(1, [What it does], [
  #lead[The Galaxy Workflow Foundry helps coding agents turn a paper or a Nextflow pipeline into a #hl[native, tested Galaxy workflow].]
  Getting a workflow right is a knowledge problem, not a syntax problem: Galaxy's tools, collections and idioms change faster than model training data. So the Foundry keeps that knowledge in a wiki people can read and review [3], #hl[compiles it into agent skills], and lets programs, not the model, decide when a workflow is right. What it can't resolve, it writes down.

  _Native:_ Galaxy's own Tool Shed tools, pinned to exact revisions, on Galaxy collections.
  #penhead[Skills are binaries.]
  #machine
  #v(0.12in)
  #pen-text[#hl[Wrong skill? Fix the note, cast again.]]
])
#let card-kb = card(none, [What's inside], [
  #set par(leading: 0.2em)
  #let tally(n, what) = [#text(font: hand, weight: "bold", size: 72pt, fill: pen, n) #text(font: hand, size: 40pt, fill: pen, what)]
  #grid(columns: (1fr, 1fr), row-gutter: 0.12in, tally[420][notes], tally[56][Molds], tally[54][patterns], tally[69][skills])
  #v(0.1in)
  One note can feed many skills: fix it once, recast, and they all get the fix.
])
#let fig-cast = figure-slip(1, [CAST], [The Tool Shed search skill the DengueSeq run used in its draft loop: Mold revision #c.revision, #c.refs references, #hl[no model in the build].], r-cast)

// ---------- route card: columns 2-4 ----------
#let short = (
  "summarize-paper": [summarize],
  "summarize-nextflow": [summarize],
  "freeform-summary-to-workflow-brief": [write a brief],
  "nextflow-summary-to-workflow-brief": [write a brief],
  "workflow-brief-to-galaxy-interface": [interface],
  "workflow-brief-to-galaxy-data-flow": [data flow],
  "compare-against-iwc-exemplar": [compare \ to IWC],
  "workflow-brief-to-galaxy-template": [template],
  "advance-galaxy-draft-step": [draft loop],
  "test-data-resolution": [find \ test data],
  "workflow-brief-to-galaxy-test-plan": [test plan],
  "implement-galaxy-workflow-test": [write \ the test],
  "validate-galaxy-workflow": [validate],
  "run-workflow-test": [run \ the test],
  "debug-galaxy-workflow-output": [debug],
)
#let step-name(p) = p.at("mold", default: p.at("branch", default: none))
#let lane-text(lane) = lane.map(p => short.at(step-name(p))).join([ #sym.arrow ])
#let gates = (
  str(rr.loop_phase): (prog: [gxwf draft-validate], fig: [Fig. 1, 2]),
  str(rr.validate_phase): (prog: [gxwf validate], fig: [Fig. 3]),
  str(rr.test_phase): (prog: [planemo test], fig: [Fig. 4]),
)
#let route-w = 3 * cw + 2 * cg
#let route-inner = route-w - 1.0in
#let station(n, label, big: false, r: 0.42in) = {
  let gate = gates.at(str(n), default: none)
  (circle(radius: r, fill: if gate != none { ink } else { slip }, stroke: if gate != none { 6pt + gold } else { 4pt + pen }, inset: 0pt,
    align(center + horizon, text(font: sans, weight: 800, size: 34pt, fill: if gate != none { slip } else { pen }, str(n)))),
   gate)
}
#let route-diagram = context {
  let spine = route.spine
  guard(spine.len() == 11, message: "spine is not 11 phases")
  let loop-i = spine.position(p => p.at("loop", default: false))
  guard(loop-i + 1 == rr.loop_phase, message: "loop phase mismatch")
  let H = 7.55in
  box(width: route-inner, height: H, {
  let lane-w = 6.4in
  let lane-h = 1.62in
  let lane(tag, lane, y) = place(top + left, dx: 0pt, dy: y, block(width: lane-w, height: lane-h, inset: (x: 0.25in, y: 0.18in),
    radius: r-small, fill: tint, stroke: 2.5pt + pen, {
      set par(leading: 0.2em)
      text(font: display, weight: 800, size: 44pt, tracking: 0.02em, tag)
      linebreak()
      one-line(what: "lane text", text(font: sans, size: 28pt, lane-text(lane)))
    }))
  let rowA = 1.95in // spine row A centre line
  let rowB = 6.05in
  // two planning lanes and the reviewed brief
  let ly1 = rowA - lane-h - 0.25in
  let ly2 = rowA + 0.25in
  lane([PAPER], route.lanes.paper, ly1)
  lane([NEXTFLOW], route.lanes.nextflow, ly2)
  let bx = lane-w + 1.1in
  let bw = 4.3in
  let bh = 2.45in
  place(top + left, dx: bx, dy: rowA - bh / 2, block(width: bw, height: bh, inset: (x: 0.25in, y: 0.2in), radius: r-small,
    fill: gold, stroke: 2.5pt + gold-dark, {
      set par(leading: 0.22em)
      text(font: display, weight: 800, size: 40pt, tracking: 0.02em)[WORKFLOW \ BRIEF]
      v(0.06in)
      text(font: sans, size: 28pt)[a person reviews it before any build]
    }))
  arrow(lane-w + 0.1in, ly1 + lane-h / 2, bx - 0.12in, rowA - 0.35in, bend: -0.12)
  arrow(lane-w + 0.1in, ly2 + lane-h / 2, bx - 0.12in, rowA + 0.35in, bend: 0.12)
  // spine row A: phases 1..loop
  let ax0 = bx + bw + 1.15in
  let loop-w = 6.1in
  let loop-x = route-inner - loop-w
  let na = loop-i // stations before the loop
  let pitch-a = (loop-x - 0.55in - ax0) / (na - 0.5)
  let r = 0.42in
  let label-at(x, y, w, body) = place(top + left, dx: x - w / 2, dy: y, block(width: w, align(center, {
    set par(leading: 0.18em)
    text(font: sans, size: 28pt, body)
  })))
  place(top + left, dx: bx + bw, dy: rowA, line(start: (0pt, 0pt), end: (loop-x - bx - bw, 0pt), stroke: 4pt + pen))
  for i in range(na) {
    let x = ax0 + i * pitch-a
    let (dot, _) = station(i + 1, none)
    place(top + left, dx: x - r, dy: rowA - r, dot)
    let lb = short.at(step-name(spine.at(i)))
    guard(measure(text(font: sans, size: 28pt, lb)).width <= pitch-a - 0.2in, message: "station label too wide")
    label-at(x, rowA + r + 0.12in, pitch-a - 0.1in, lb)
  }
  // the loop station
  let lh = 2.7in
  let ly = rowA - lh / 2 + 0.25in
  // the loop station's nova orbit ring
  place(top + left, dx: loop-x - 0.45in, dy: ly - 0.5in, rotate(-5deg, reflow: false,
    ellipse(width: loop-w + 0.9in, height: lh + 1.0in, stroke: 2.5pt + nova)))
  place(top + left, dx: loop-x, dy: ly, block(width: loop-w, height: lh, inset: (x: 0.3in, top: 0.5in, bottom: 0.2in), radius: r-card,
    fill: slip, stroke: 4pt + pen, {
      set par(leading: 0.22em)
      box(baseline: 22%, station(rr.loop_phase, none, r: 0.3in).at(0))
      h(0.2em)
      text(font: sans, weight: "bold", size: 36pt, fill: pen)[#short.at(step-name(spine.at(loop-i)))]
      linebreak()
      text(font: sans, size: 28pt)[one step per pass until \ no step is a draft]
      linebreak()
      text(font: mono, weight: "bold", size: 28pt, hl(gates.at(str(rr.loop_phase)).prog))
    }))
  // loop arrow over the top of the loop station
  arrow(loop-x + loop-w - 1.0in, ly + 0.05in, loop-x + 1.0in, ly + 0.05in, bend: -0.12, th: 6pt)
  place(top + left, dx: loop-x + 1.45in, dy: ly - 0.92in, text(font: hand, weight: "bold", size: 36pt, fill: pen)[repeat])
  place(top + left, dx: loop-x + loop-w - 2.15in, dy: ly + lh + 0.36in, rotate(-4deg, reflow: false,
    text(font: hand, weight: "bold", size: 36pt, fill: pen, gates.at(str(rr.loop_phase)).fig)))
  // return line from the loop down to row B
  let bx0 = 0.55in
  let nb = spine.len() - na - 1
  let end-w = 3.6in
  let pitch-b = (route-inner - end-w - 0.9in - bx0) / (nb - 1)
  // elbow: loop foot -> down -> left along the gap between rows -> down onto station 6
  let ye = ly + lh + 0.62in
  let xl = loop-x + loop-w / 2 - 1.2in
  let rc = 0.55in
  place(top + left, curve(stroke: arrow-st(4pt), curve.move((xl, ly + lh)), curve.line((xl, ye - rc)),
    curve.quad((xl, ye), (xl - rc, ye)), curve.line((bx0 + rc, ye)), curve.quad((bx0, ye), (bx0, ye + rc)),
    curve.line((bx0, rowB - r - 0.12in))))
  place(top + left, dx: bx0 - 0.2in, dy: rowB - r - 0.46in, polygon(fill: pen, (0in, 0in), (0.4in, 0in), (0.2in, 0.34in)))
  place(top + left, dx: bx0, dy: rowB, line(start: (0pt, 0pt), end: (route-inner - end-w - bx0, 0pt), stroke: 4pt + pen))
  for j in range(nb) {
    let i = na + 1 + j
    let x = bx0 + j * pitch-b
    let (dot, gate) = station(i + 1, none)
    place(top + left, dx: x - r, dy: rowB - r, dot)
    let lb = short.at(step-name(spine.at(i)))
    guard(measure(text(font: sans, size: 28pt, lb)).width <= pitch-b - 0.2in, message: "station label too wide")
    label-at(x, rowB + r + 0.12in, pitch-b - 0.1in, lb)
    if gate != none {
      place(top + left, dx: x - pitch-b / 2 + 0.05in, dy: rowB - r - 1.17in, block(width: pitch-b - 0.1in, align(center, {
        set par(leading: 0.15em)
        text(font: hand, weight: "bold", size: 36pt, fill: pen, gate.fig)
        linebreak()
        text(font: mono, weight: "bold", size: 28pt, hl(gate.prog))
      })))
    }
  }
  // output
  place(top + left, dx: route-inner - end-w, dy: rowB - 0.85in, block(width: end-w, height: 1.7in, inset: (x: 0.25in, y: 0.18in), radius: r-small,
    fill: tint, stroke: 2.5pt + pen, {
      set par(leading: 0.2em)
      text(font: display, weight: 800, size: 36pt, tracking: 0.02em)[GALAXY \ WORKFLOW]
      linebreak()
      text(font: sans, size: 28pt)[with its tests]
    }))
  place(top + left, dx: route-inner - end-w - 0.36in, dy: rowB - 0.17in, polygon(fill: pen, (0in, 0in), (0.3in, 0.17in), (0in, 0.34in)))
  })
}
#let card-route = card(2, [How it works], w: route-w, aside-w: 20.6in,
  aside: [A route is a chain of Molds, each cast into a skill. A planning lane turns a paper or a Nextflow pipeline into a #hl[workflow brief]. Once a person has reviewed it, one shared spine of #route.spine.len() phases builds, checks and tests the Galaxy workflow. #hl[Filled stations are gates]: a program, not the model, signs each one.],
  route-diagram)

// ---------- column 2: inside the loop ----------
#let card-loop = card(3, [Inside the loop], [
  #penhead[Pinned, not named.]
  Phase #rr.loop_phase builds the workflow one step at a time. Each pass, `gxwf draft-next-step` picks the next unfinished step; the discover-shed-tool skill (Fig. 1) searches the Tool Shed and #hl[pins one wrapper to an exact changeset]; the agent fills in the step; `gxwf draft-validate` checks it against that tool's schema. The DengueSeq run took #rr.loop_iterations passes.
])
#let fig-pinned = figure-slip(2, [PINNED], [The seven tools the run pinned, as `gxwf tool-revisions` reported them. Planemo later installed exactly these.], r-pinned)
#let ledger-note = block(width: 100%, inset: (x: 0.15in), {
  penhead[Gaps are written down.]
  prose[The run's ledger closed #route.ledger.resolved of #route.ledger.entries requirements and left #route.ledger.open open, each stated in words for the reviewer: for example, that the source's filtered variant table is not reproduced, a cut the reviewed brief chose.]
})

// ---------- column 3: checked, then run ----------
#let card-check = card(4, [Checked, then run], [
  #penhead[Typed, not guessed.]
  In phase #rr.validate_phase, `gxwf validate` checks every parameter and every connection, collection map-over included, against the tools' real schemas. #hl[No job is queued], so an agent can repair in a tight loop.
])
#let fig-validated = figure-slip(3, [VALIDATED], [Phase #rr.validate_phase's check, replayed.], r-validated)
#let notrun = block(width: 100%, inset: (x: 0.15in), {
  penhead[The last check is a real run.]
  prose[gxwf checks the structure. Then Planemo installs the pinned tools in a real Galaxy and runs the workflow's test. #hl[That run is the validation]: real jobs, real outputs, checked against the expected ones.]
})
#let fig-tested = figure-slip(4, [TESTED], [Planemo's report of that run. One larger test case (about 178 MB of reads) was not run.], r-tested,
  stamp-over: (dx: 4.75in, dy: 2.93in, body: stamp(angle: -6deg, size: 56pt)[PASS]))

// ---------- column 4: rails, and how to use it ----------
#let card-rails = card(5, [Rails, not reminders.], feat: true, [
  The companion Orbit study ran agents on public Galaxy [1]. Its lesson: #hl[skills are guidance, not enforcement] [1]. What held were the rails. A connection check caught an agent's bad `tximport` wiring before anything ran, and Orbit's evidence gate now refuses by default [1].

  The Foundry is built the same way: the model drafts and repairs; gxwf and Planemo decide. Its compilation pipeline is described in [1]; here we show its knowledge base, provenance and checks. [1] also reports a 60-step workflow the Foundry compiled from an RNA-seq paper's methods text; comparing with the authors' data found a model choice the methods left out.
])
#let wide-w = colx.at(3) - colx.at(2) + cw
#let gs-qr = 3.3in
#let card-start = card(6, [Get started], w: wide-w, inset: 0.36in, head-in-body: true, {
  let scmd(body) = one-line(what: "command", exempt(text(font: mono, size: 24pt, weight: "semibold", tracking: -0.012em, body)))
  let tool(label, ..c) = block(above: 0.24in, below: 0pt, {
    block(below: 0.08in, text(weight: "bold", label))
    stack(spacing: 0.1in, ..c.pos().map(scmd))
  })
  grid(columns: (2 * gs-qr + 0.3in, 1fr), column-gutter: 0.5in, align: top, {
    block(below: 0.35in, { set par(leading: 0.12em); badge(6); h(0.3em); text(font: display, weight: 700, size: 72pt, tracking: -0.02em, fill: ink)[Get started] })
    grid(columns: (gs-qr, gs-qr), column-gutter: 0.3in,
      qr-tile("qr-foundry", [The Foundry], w: gs-qr), qr-tile("qr-preprint", [Preprint [1]], w: gs-qr))
  }, {
    v(-0.24in)
    tool([Claude Code], [/plugin marketplace add galaxyproject/foundry], [/plugin install foundry-skills\@galaxy-workflow-foundry])
    tool([Codex], [codex plugin marketplace add galaxyproject/foundry], [codex plugin add foundry-skills\@galaxy-workflow-foundry])
    tool([gxwf, the checker], [npm install -g \@galaxy-tool-util/cli])
    tool([From a paper: brief, review it, then build], [/foundry-skills:pipeline-paper-to-workflow-brief], [/foundry-skills:pipeline-workflow-brief-to-galaxy])
  })
})
#let refs = exempt(block(width: 100%, inset: (x: 0.1in), {
  set text(font: sans, size: 24pt, fill: ink-soft)
  set par(leading: 0.3em, hanging-indent: 1.0em, spacing: 0.4em)
  [Knowledge-base counts: galaxyproject/foundry main, 2026-10-24. Figures 1–4 and the ledger: Foundry run #d.run (2026-10-20), a Galaxy translation of DengueSeq [2]. Times UTC.

  [1] Baker D, …, Nekrutenko A. Verifiable Agentic Science on Public Infrastructure. bioRxiv (2026). doi:10.64898/2026.10.26.761864

  [2] Vogels CBF, Hill V, et al. DengueSeq. BMC Genomics 25:433 (2024).

  [3] Karpathy A. LLM wiki. gist.github.com/karpathy (2026).]
}))

// ---------- columns: measured stacks, each guarded against overflow ----------
// bottom line shared by columns 2-4 and the Get started card
#let bot = safe - 0.15in
#let column(i, y, items, what, spread: false, bottom: safe) = context {
  let g = gapv
  if spread {
    let used = items.map(it => measure(block(width: cw, it)).height).sum()
    g = calc.max(gapv, (bottom - y - used) / (items.len() - 1))
  }
  guard(g >= gapv - 0.01in, message: what + " items closer than gapv")
  let s = stack(spacing: g, ..items)
  let h = measure(block(width: cw, s)).height
  let x = colx.at(i)
  guard(y + h <= bottom + 0.01in, message: what + " overflows by " + repr((y + h - bottom).to-absolute()))
  place(top + left, dx: x + bleed, dy: y + bleed, block(width: cw, s))
  if debug {
    place(top + left, dx: x + bleed, dy: safe + 0.05in + bleed, text(size: 28pt, fill: red, weight: "bold")[slack #calc.round((safe - y - h).inches(), digits: 2) in])
  }
}

#column(0, y0, (card-what, fig-cast, card-kb, refs), "column 1", spread: true, bottom: bot)
#place(top + left, dx: colx.at(1) + bleed, dy: y0 + bleed, context {
  let h = measure(card-route).height
  guard(h <= span-h, message: "route card overflows by " + repr((h - span-h).to-absolute()))
  card-route
})
#column(1, y1, (card-loop, fig-pinned, ledger-note), "column 2", spread: true, bottom: bot)
#context {
  let gh = measure(card-start).height
  let gy = bot - gh
  column(2, y1, (card-check, fig-validated, notrun), "column 3", spread: true, bottom: gy - 2 * gapv)
  column(3, y1, (fig-tested, card-rails), "column 4", spread: true, bottom: gy - 2 * gapv)
  place(top + left, dx: colx.at(2) + bleed, dy: gy + bleed, card-start)
}
