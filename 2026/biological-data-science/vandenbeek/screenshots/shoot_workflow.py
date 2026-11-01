"""Screenshot the workflow editor canvas, clipped to the nodes, for poster panel B."""
import json, sys
from playwright.sync_api import sync_playwright
P = sys.argv[1]; st = json.load(open(f"{P}/galaxy_state.json")); U = "http://localhost:8091"
with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    pg = b.new_page(viewport={"width": 1100, "height": 900}, device_scale_factor=6, locale="en-US")
    pg.goto(f"{U}/login/start"); pg.fill("input[name=login]", "poster@example.org"); pg.fill("input[name=password]", "posterpass123"); pg.keyboard.press("Enter"); pg.wait_for_timeout(3000)
    pg.goto(f"{U}/workflows/edit?id={st['workflow']['id']}"); pg.wait_for_timeout(7000)
    pg.click("#activity-workflow-editor-attributes"); pg.mouse.move(1090, 890); pg.add_style_tag(content=".workflow-editor-toolbar { display: none !important; }"); pg.wait_for_timeout(2500)
    boxes = pg.evaluate("""() => [...document.querySelectorAll('[id^="wf-node-step-"]')].map(e => { const r = e.getBoundingClientRect(); return [r.left, r.top, r.right, r.bottom]; })""")
    print(len(boxes), "nodes")
    x0 = min(b[0] for b in boxes) - 30; y0 = min(b[1] for b in boxes) - 20
    x1 = max(b[2] for b in boxes) + 30; y1 = max(b[3] for b in boxes) + 20
    pg.screenshot(path=f"{P}/shots/workflow.png", clip={"x": x0, "y": y0, "width": x1 - x0, "height": y1 - y0})
    print("clip", round(x1 - x0), round(y1 - y0))
    b.close()
