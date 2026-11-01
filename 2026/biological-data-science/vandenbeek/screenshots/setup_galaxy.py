"""Prepare a local Galaxy for the poster screenshots.

Creates the poster user, the two UDT roles, the Foldseek UDT, a history with placeholder datasets
and the example workflow, then writes galaxy_state.json for the shoot_*.py scripts.

Usage: python screenshots/setup_galaxy.py .   (from the poster directory; Galaxy on localhost:8091)
"""

import json
import sys
import time

import requests
import yaml

URL = "http://localhost:8091"
BOOT = {"x-api-key": "poster-bootstrap-key-0123456789"}  # bootstrap_admin_api_key in galaxy.yml.sample
P = sys.argv[1]

s = requests.Session()
users = s.get(f"{URL}/api/users", headers=BOOT, params={"f_email": "poster@example.org"}).json()
user = users[0] if users else s.post(
    f"{URL}/api/users", headers=BOOT, json={"username": "poster", "email": "poster@example.org", "password": "posterpass123"}
).json()
key = s.post(f"{URL}/api/users/{user['id']}/api_key", headers=BOOT).json()
H = {"x-api-key": key}

roles = [r["name"] for r in s.get(f"{URL}/api/roles", headers=BOOT).json()]
for role_type in ("user_tool_create", "user_tool_execute"):
    if f"UDT {role_type}" not in roles:
        s.post(f"{URL}/api/roles", headers=BOOT, json={"name": f"UDT {role_type}", "description": role_type, "role_type": role_type, "user_ids": [user["id"]]}).raise_for_status()

tool = s.post(f"{URL}/api/unprivileged_tools", headers=H, json={"src": "representation", "representation": yaml.safe_load(open(f"{P}/foldseek.yml"))})
tool.raise_for_status()

# Placeholder datasets: only their names appear in the tool-form screenshot.
history = s.post(f"{URL}/api/histories", headers=H, json={"name": "P. vivax structural families"}).json()
fasta = ">PVP01_0000010 hypothetical protein\nMKLLSIVLLAFAQCSSAEEDGKKPAAEEKPAEEKKPEESTKPS\n"
s.post(f"{URL}/api/tools/fetch", headers=H, json={"history_id": history["id"], "targets": [{"destination": {"type": "hdas"}, "elements": [
    {"src": "pasted", "paste_content": fasta, "name": "P. vivax proteomes (PvP01, PvW1, PvPAM).fasta", "ext": "fasta"},
    {"src": "pasted", "paste_content": "GGUF placeholder\n", "name": "prostt5-f16.gguf", "ext": "data"},
]}]}).raise_for_status()
for _ in range(60):
    contents = s.get(f"{URL}/api/histories/{history['id']}/contents", headers=H).json()
    if len(contents) == 2 and all(c["state"] == "ok" for c in contents):
        break
    time.sleep(2)

workflow = s.post(f"{URL}/api/workflows", headers=H, json={"workflow": yaml.safe_load(open(f"{P}/pvivax-foldseek.gxwf.yml"))})
workflow.raise_for_status()

json.dump({"api_key": key, "tool": tool.json(), "history_id": history["id"], "workflow": workflow.json()}, open(f"{P}/galaxy_state.json", "w"), indent=1)
print("tool", tool.json()["uuid"], "workflow", workflow.json()["id"])
