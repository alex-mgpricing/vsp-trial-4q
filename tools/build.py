"""Dev helper: build the admin plugin zip, and a sample team plugin the way value-setup would."""
import datetime, os, re, shutil, sys, tempfile, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ADMIN = os.path.join(ROOT, "plugins", "cuvama-value-admin")
TEMPLATE = os.path.join(ADMIN, "skills", "value-setup", "assets", "team-plugin")
DIST = os.path.join(ROOT, "dist")


def zip_dir(src, out):
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for d, _, files in os.walk(src):
            for f in files:
                p = os.path.join(d, f)
                z.write(p, os.path.relpath(p, src).replace(os.sep, "/"))


def build_team(values, out):
    work = tempfile.mkdtemp()
    dst = os.path.join(work, "team")
    shutil.copytree(TEMPLATE, dst)
    for d, _, files in os.walk(dst):
        for f in files:
            if not f.endswith(".template"):
                continue
            p = os.path.join(d, f)
            text = open(p, encoding="utf-8").read()
            for k, v in values.items():
                text = text.replace("{{" + k + "}}", v)
            if "{{" in text:
                sys.exit(f"unfilled placeholder in {p}: {re.findall(r'{{[A-Z_]+}}', text)}")
            open(p[: -len(".template")], "w", encoding="utf-8", newline="\n").write(text)
            os.remove(p)
    zip_dir(dst, out)
    return dst


if __name__ == "__main__":
    os.makedirs(DIST, exist_ok=True)
    version = __import__("json").load(open(os.path.join(ADMIN, ".claude-plugin", "plugin.json")))["version"]
    zip_dir(ADMIN, os.path.join(DIST, f"cuvama-value-admin-{version}.zip"))
    sample = build_team({
        "COMPANY_NAME": "Example Co", "FOLDER_LINK": "https://example.sharepoint.com/sites/Sales/Shared%20Documents/Value",
        "DRIVE_ID": "b!example", "FOLDER_ITEM_ID": "01EXAMPLE", "CURRENCY": "USD",
        "GENERATED_AT": datetime.date.today().isoformat(),
        "VERSION": "1.0." + datetime.datetime.now().strftime("%Y%m%d%H%M"),
    }, os.path.join(DIST, "sample-team-plugin.zip"))
    print("built", os.listdir(DIST), "sample team dir:", sample)
