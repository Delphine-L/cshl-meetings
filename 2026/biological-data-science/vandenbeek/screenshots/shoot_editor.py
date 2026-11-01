"""Screenshot the UDT tool editor for poster panel C and record line geometry for callouts."""
import json, sys
from playwright.sync_api import sync_playwright
P = sys.argv[1]; st = json.load(open(f"{P}/galaxy_state.json")); U = "http://localhost:8091"
with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    pg = b.new_page(viewport={"width": 760, "height": 1100}, device_scale_factor=6, locale="en-US")
    pg.goto(f"{U}/login/start"); pg.fill("input[name=login]", "poster@example.org"); pg.fill("input[name=password]", "posterpass123"); pg.keyboard.press("Enter"); pg.wait_for_timeout(3000)
    pg.goto(f"{U}/tools/editor/{st['tool']['uuid']}"); pg.wait_for_timeout(5000)
    pg.add_style_tag(content="#left, #right, .activity-bar, nav.activity-bar, .minimap, .decorationsOverviewRuler { display: none !important; } .monaco-editor .current-line { border: 0 !important; } .monaco-editor .cursors-layer { display: none !important; } #center button { visibility: hidden !important; }")
    pg.wait_for_timeout(1500)
    pg.mouse.click(5, 1095); pg.wait_for_timeout(800)
    # hover $(inputs.evalue) in shell_command to show Monaco's type hint
    ev = pg.evaluate("""() => { for (const line of document.querySelectorAll('.view-line')) {
        if (!line.textContent.includes('inputs.evalue')) continue;
        const w = document.createTreeWalker(line, NodeFilter.SHOW_TEXT); let n;
        while ((n = w.nextNode())) { const i = n.textContent.indexOf('evalue'); if (i >= 0) { const r = document.createRange(); r.setStart(n, i); r.setEnd(n, i + 6); const b = r.getBoundingClientRect(); return [b.x + b.width / 2, b.y + b.height / 2]; } } } }""")
    pg.mouse.move(ev[0], ev[1]); pg.wait_for_timeout(2500)
    assert pg.evaluate("() => [...document.querySelectorAll('.monaco-hover')].some(e => e.offsetParent && e.innerText.includes('evalue: number'))")
    geo = pg.evaluate("""() => { const c = document.querySelector('#center').getBoundingClientRect();
      const lines = [...document.querySelectorAll('.view-line')].map(e => e.getBoundingClientRect().top).sort((a,b)=>a-b);
      const m = document.querySelector('.monaco-editor').getBoundingClientRect();
      return {center: [c.x, c.y, c.width, c.height], monaco: [m.x, m.y, m.width, m.height], firstLineTop: lines[0], lineCount: lines.length,
              lineHeight: parseFloat(getComputedStyle(document.querySelector('.view-line')).height)}; }""")
    print(geo)
    x, y = geo["center"][0], geo["center"][1]
    bottom = geo["firstLineTop"] + 44 * geo["lineHeight"] + 3
    clip = {"x": x, "y": y, "width": 590, "height": bottom - y}
    pg.screenshot(path=f"{P}/shots/editor-c.png", clip=clip)
    json.dump({"clip": clip, "firstLineTop": geo["firstLineTop"] - y, "lineHeight": geo["lineHeight"], "pointer": [ev[0] - x, ev[1] - y]}, open(f"{P}/shots/editor-c.json", "w"), indent=1)
    b.close()
