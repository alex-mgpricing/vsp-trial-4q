"""Dev helper: zip each plugin into dist/ for manual upload testing."""
import json, os, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "dist")

os.makedirs(DIST, exist_ok=True)
for name in os.listdir(os.path.join(ROOT, "plugins")):
    src = os.path.join(ROOT, "plugins", name)
    version = json.load(open(os.path.join(src, ".claude-plugin", "plugin.json")))["version"]
    out = os.path.join(DIST, f"{name}-{version}.zip")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for d, _, files in os.walk(src):
            for f in files:
                p = os.path.join(d, f)
                z.write(p, os.path.relpath(p, src).replace(os.sep, "/"))
    print("built", out)
