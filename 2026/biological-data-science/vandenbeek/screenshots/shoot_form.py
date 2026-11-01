"""Screenshot the tool form Galaxy generates for the Foldseek UDT (poster panel F)."""

import json
import sys

from playwright.sync_api import sync_playwright

P = sys.argv[1]
st = json.load(open(f"{P}/galaxy_state.json"))
U = "http://localhost:8091"
with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    pg = b.new_page(viewport={"width": 1600, "height": 1000}, device_scale_factor=6, locale="en-US")
    pg.goto(f"{U}/login/start")
    pg.fill("input[name=login]", "poster@example.org")
    pg.fill("input[name=password]", "posterpass123")
    pg.keyboard.press("Enter")
    pg.wait_for_timeout(4000)
    pg.request.put(f"{U}/history/set_as_current?id={st['history_id']}")
    pg.goto(f"{U}/?tool_uuid={st['tool']['uuid']}")
    pg.wait_for_timeout(5000)
    # Chromium renders number inputs with the OS decimal separator; show the raw value instead.
    pg.evaluate("document.querySelectorAll('input[type=number]').forEach(e => { const v = e.value; e.type = 'text'; e.value = v; })")
    pg.wait_for_timeout(500)
    pg.screenshot(path=f"{P}/shots/form.png", clip={"x": 403.33, "y": 50, "width": 883.33, "height": 400})
    b.close()
