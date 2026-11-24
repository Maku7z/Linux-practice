import json, os, sys, tempfile

data = json.load(sys.stdin)
session_id = str(data.get("session_id", "default")).replace("/", "_")
counter_path = os.path.join(tempfile.gettempdir(), f"shadeward4_search_{session_id}.cnt")

if "--reset" in sys.argv:
    if os.path.exists(counter_path):
        os.remove(counter_path)
    sys.exit(0)

tool = data.get("tool_name", "")
if tool in ("Write", "Edit"):
    if os.path.exists(counter_path):
        os.remove(counter_path)
    file_path = data.get("tool_input", {}).get("file_path", "")
    root = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    allow_file = os.path.join(root, ".claude", "allowed_files.txt")
    if file_path and os.path.exists(allow_file):
        rel = os.path.relpath(os.path.abspath(file_path), os.path.abspath(root)).replace("\\", "/")
        with open(allow_file, "r", encoding="utf-8") as f:
            allowed = {ln.strip().replace("\\", "/") for ln in f if ln.strip() and not ln.startswith("#")}
        if rel not in allowed:
            sys.stderr.write(
                f"BLOCKED: '{rel}' is outside .claude/allowed_files.txt for this phase. "
                f"Allowed: {sorted(allowed)}. Do NOT create extra files."
            )
            sys.exit(2)
    sys.exit(0)

count = 0
if os.path.exists(counter_path):
    try:
        count = int(open(counter_path, "r", encoding="utf-8").read().strip())
    except ValueError:
        count = 0
count += 1
with open(counter_path, "w", encoding="utf-8") as f:
    f.write(str(count))

if count > 10:
    sys.stderr.write(
        "BLOCKED: Exceeded 10 consecutive search calls without editing or reporting. "
        "Stop searching and either implement with gathered facts or ask the user for exact paths."
    )
    sys.exit(2)
