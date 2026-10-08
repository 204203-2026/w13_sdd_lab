"""Deterministic offline required checks; network/browser work is bonus only."""
from __future__ import annotations
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time
import threading
from html.parser import HTMLParser
from urllib.parse import urlparse
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))
CONTRACT_HASH = "ffd867b4d9d84e48862bfffab82c2ec5c79a84a4573dc44a7ca3fa8db58cbc33"
PINS_HASH = "550c1789aa3f89242380ebd6cd625e27b3b8d6391bed9fd899de2fc6c49f2185"
REQUIRED = {
    "contract_intact": 0, "impl_original": 0,
    "spec_sections": 2, "spec_acs": 2,
    "review_file": 1, "review_crossref": 1, "review_applied": 2,
    "spec_frozen": 1, "ac_test_map": 2, "red_evidence": 2,
    "tests_green": 1, "grader_api": 2, "ui_static": 1,
    "tests_pass_correct": 1, "tests_catch_wrong": 2,
}
BONUS = {"ui_behaviour": 2, "edge_case_tests": 1,
         "review_round2": 1, "deployed": 2}
PLACEHOLDER = re.compile(r"\bTODO\b|\blorem\b|<\s*your\b", re.I)
AC_REF = re.compile(r"(?<![A-Za-z0-9])AC-(\d{1,2})(?!\d)")
GUARDED = {"grader_api", "ui_static", "tests_pass_correct", "tests_catch_wrong"}


def text(path):
    p = ROOT / path
    return p.read_text(encoding="utf-8") if p.is_file() else ""


def lf(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n")


def sha(path):
    return hashlib.sha256(lf(Path(path).read_bytes())).hexdigest()


def run(args, cwd=ROOT, env=None, timeout=60):
    return subprocess.run(args, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, timeout=timeout)


def section(source, heading):
    source = source.replace("\r\n", "\n")
    match = re.search(r"^##[ \t]+" + re.escape(heading) + r"[ \t]*:?[ \t]*$\n(.*?)(?=^##[ \t]+|\Z)",
                      source, re.M | re.S | re.I)
    return match.group(1).strip() if match else ""


def ac_lines(source=None):
    lines = re.findall(r"^[-*][ \t]+AC-(\d{1,2}):[ \t]*(.*?)[ \t]*$",
                       section(text("SPEC.md") if source is None else source, "Acceptance criteria"), re.M)
    return [(f"{int(number):02}", line) for number, line in lines]


def ac_refs(source):
    return {f"{int(number):02}" for number in AC_REF.findall(source)}


def ac_ids():
    return {number for number, _ in ac_lines()}


def tags(line):
    return re.findall(r"\[((?:EP|UI)-\d+)\]", line)


def contract():
    return json.loads(text("grading/contract.json"))


def lock():
    return json.loads(text("SPEC.lock"))


def functions():
    tree = ast.parse(text("tests/test_spec.py"))
    return [node for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name.startswith("test_")]


def git_file(ref, path):
    result = subprocess.run(["git", "show", f"{ref}:{path}"], cwd=ROOT,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
    if result.returncode:
        raise ValueError(f"missing {ref}:{path}")
    return lf(result.stdout)


def contract_intact():
    if os.environ.get("W13_CONTRACT_SHA256", CONTRACT_HASH) != CONTRACT_HASH:
        return False
    if sha(ROOT / "grading/contract.json") != CONTRACT_HASH:
        return False
    if sha(ROOT / "grading/contract.sha256") != PINS_HASH:
        return False
    pinned = {}
    for line in text("grading/contract.sha256").splitlines():
        digest, path = line.split(None, 1)
        pinned[path] = digest
    expected = {"grading/contract.json", "tests/conftest.py"} | {
        str(p.relative_to(ROOT)) for p in (ROOT / "grading/impls").glob("*.py")}
    if expected != set(pinned) or not all(sha(ROOT / p) == h for p, h in pinned.items()):
        return False
    present = {p.relative_to(ROOT) for p in (ROOT / "grading").rglob("*")
               if p.is_file() and "__pycache__" not in p.parts}
    allowed = {Path(p) for p in pinned if p.startswith("grading/")} | {
        Path("grading/contract.sha256"), Path("grading/CONTRACT.md"), Path("grading/brief_endpoints.txt")}
    return not (present - allowed) and os.environ.get("W13_REMOTE_CONTRACT", "ok") != "mismatch"


def normalized_tree(path):
    tree = ast.parse(Path(path).read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.body and isinstance(node.body[0], ast.Expr) \
                    and isinstance(node.body[0].value, ast.Constant) \
                    and isinstance(node.body[0].value.value, str):
                node.body.pop(0)
    identifiers = {}
    def rename(name):
        return identifiers.setdefault(name, f"v{len(identifiers)}")
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            node.id = rename(node.id)
        elif isinstance(node, ast.arg):
            node.arg = rename(node.arg)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            node.name = rename(node.name)
        elif isinstance(node, ast.alias) and node.asname:
            node.asname = rename(node.asname)
        elif isinstance(node, (ast.Global, ast.Nonlocal)):
            node.names = [rename(name) for name in node.names]
    return tree


def normalized(path):
    return hashlib.sha256(ast.dump(normalized_tree(path), include_attributes=False).encode()).hexdigest()


def impl_original():
    candidate = normalized(ROOT / "app/main.py")
    return all(candidate != normalized(p) for p in (ROOT / "grading/impls").glob("*.py"))


def spec_sections(source=None):
    source = text("SPEC.md") if source is None else source
    if not all(section(source, name) for name in ["Goal", "Acceptance criteria", "Edge cases", "Out of scope"]):
        return False
    if not any(line.strip() and not PLACEHOLDER.search(line)
               for line in section(source, "Goal").splitlines()):
        return False
    for name in ["Edge cases", "Out of scope"]:
        bullets = re.findall(r"^[-*][ \t]+(.+)$", section(source, name), re.M)
        if not any(item.strip() and not PLACEHOLDER.search(item) for item in bullets):
            return False
    return True


def spec_acs(source=None):
    lines = ac_lines(source)
    known = {item["id"] for group in contract().values() for item in group}
    return len(lines) >= 5 and [n for n, _ in lines] == [f"{i:02}" for i in range(1, len(lines) + 1)] \
        and all(len(line) >= 30 and not PLACEHOLDER.search(line) and set(tags(line)) <= known
                for _, line in lines)


def review_structure(path):
    source = text(path)
    return bool(section(source, "Verdict")) and all(
        len([item for item in re.findall(r"^\s*(?:[-*]|\d+[.)])\s+(.+)", section(source, name), re.M)
             if item.strip() and not PLACEHOLDER.search(item)]) >= 2
        for name in ["Ambiguities", "Missing edge cases"])


def review_file():
    return review_structure("REVIEW.md")


def review_crossref():
    cited = ac_refs(text("REVIEW.md"))
    return len(cited) >= 2 and cited <= ac_ids()


def is_ancestor(a, b):
    return run(["git", "merge-base", "--is-ancestor", a, b]).returncode == 0


def review_applied():
    if not is_ancestor("spec-draft", "spec-frozen"):
        return False
    draft_ref = run(["git", "rev-parse", "spec-draft"])
    frozen_ref = run(["git", "rev-parse", "spec-frozen"])
    if draft_ref.stdout.strip() == frozen_ref.stdout.strip():
        return False
    draft = git_file("spec-draft", "SPEC.md").decode("utf-8")
    lines = ac_lines(draft)
    if not lines or any(PLACEHOLDER.search(line) for _, line in lines):
        return False
    changes = section(text("SPEC.md"), "Changes after review")
    result = run(["git", "diff", "-w", "--ignore-blank-lines", "spec-draft", "spec-frozen", "--", "SPEC.md"])
    return bool(AC_REF.search(changes)) and result.returncode == 0 and bool(result.stdout.strip())


def spec_frozen():
    digest = lock()["spec_sha256"]
    return is_ancestor("spec-frozen", "HEAD") and digest == sha(ROOT / "SPEC.md") == hashlib.sha256(git_file("HEAD", "SPEC.md")).hexdigest() \
        == hashlib.sha256(git_file("spec-frozen", "SPEC.md")).hexdigest()


def ac_test_map():
    tree = ast.parse(text("tests/test_spec.py"))
    helpers = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)
               and not node.name.startswith("test_")}
    nodes = functions()
    lines = ac_lines()
    for number, _ in lines:
        valid = False
        for node in nodes:
            if not node.name.startswith(f"test_ac_{number}_"):
                continue
            # Keep existing one-level helper support; no literal method/path policy.
            called = {item.func.id for item in ast.walk(node)
                      if isinstance(item, ast.Call) and isinstance(item.func, ast.Name)}
            items = [item for part in [node] + [helpers[name] for name in called if name in helpers]
                     for item in ast.walk(part)]
            has_assert = any(isinstance(item, ast.Assert) for item in items)
            client_call = any(isinstance(item, ast.Call) and isinstance(item.func, ast.Attribute)
                              and isinstance(item.func.value, ast.Name) and item.func.value.id == "client"
                              for item in items)
            valid = valid or (has_assert and client_call)
        if not valid:
            return False
    return bool(lines)


RUN_IGNORES = {".git", ".venv", "results", "grading", "__pycache__", ".pytest_cache",
               ".w13-template", "pytest.ini", "tox.ini", "setup.cfg", "conftest.py"}


def suite_ignore(directory, names, root=None):
    ignored = set(names) & RUN_IGNORES
    # Instructor scratch can contain this copy destination; app/qa remains valid.
    if Path(directory).resolve() == Path(ROOT if root is None else root).resolve():
        ignored |= set(names) & {"qa"}
    return ignored


def run_suite(src: Path, main_source: str | None = None):
    tmp = Path(tempfile.mkdtemp(prefix="w13-run-")) / "tree"
    shutil.copytree(src, tmp, ignore=lambda directory, names: suite_ignore(directory, names, src))
    (tmp / "tests").mkdir(exist_ok=True)
    shutil.copy2(ROOT / "tests/conftest.py", tmp / "tests/conftest.py")
    if main_source is not None:
        backup(tmp / "app/main.py")
        (tmp / "app/main.py").write_text(main_source, encoding="utf-8")
    (tmp / "pytest.ini").write_text("[pytest]\n", encoding="utf-8")
    env = {key: value for key, value in os.environ.items()
           if key not in {"APP_MODULE", "PYTHONPATH", "PYTEST_ADDOPTS", "PYTEST_PLUGINS"}}
    env.update(PYTHONPATH=str(tmp), PYTHONDONTWRITEBYTECODE="1", UV_OFFLINE="1",
               UV_PYTHON_DOWNLOADS="never")
    return run([sys.executable, "-m", "pytest", "-q", "-rA", "-p", "no:cacheprovider",
                "-c", str(tmp / "pytest.ini"), "tests/test_spec.py"], cwd=tmp, env=env, timeout=120)


def all_failed(outcome):
    # Only pytest's final summary counts; assertion messages can contain "error".
    lines = [line.strip() for line in outcome.stdout.splitlines() if line.strip()]
    summary = lines[-1].strip("= ") if lines else ""
    counts = {status: int(count) for count, status in re.findall(
        r"\b(\d+) (failed|passed|errors?|skipped|xfailed|xpassed)\b", summary)}
    return outcome.returncode == 1 and counts.get("failed", 0) >= 1 \
        and all(value == 0 for status, value in counts.items() if status != "failed") \
        and not re.search(r"^(?:_+[ \t]+)?ERROR collecting\b", outcome.stdout, re.M)


def oracle(name):
    return (ROOT / "grading/impls" / f"{name}.py").read_text(encoding="utf-8")


def red_evidence():
    if not is_ancestor("spec-frozen", "tests-red") or not is_ancestor("tests-red", "HEAD"):
        return False
    directory = Path(tempfile.mkdtemp(prefix="w13-red-"))
    checkout = directory / "work"
    added = False
    try:
        result = run(["git", "worktree", "add", "--detach", str(checkout), "tests-red"])
        if result.returncode:
            return False
        added = True
        historic_lock = json.loads((checkout / "SPEC.lock").read_text(encoding="utf-8"))
        if sha(checkout / "tests/test_spec.py") != historic_lock.get("tests_sha256") \
                or historic_lock.get("tests_sha256") != lock().get("tests_sha256"):
            return False
        outcome = run_suite(checkout)
        return all_failed(outcome)
    finally:
        if added:
            # Preserve scratch evidence before removing the registered worktree.
            shutil.copytree(checkout, directory / "backup", symlinks=True)
            removed = run(["git", "worktree", "remove", "--force", str(checkout)])
            if removed.returncode:
                raise RuntimeError("worktree cleanup failed: " + removed.stdout)


def tests_green():
    expected = lock()["tests_sha256"]
    return sha(ROOT / "tests/test_spec.py") == expected \
        == hashlib.sha256(git_file("HEAD", "tests/test_spec.py")).hexdigest() \
        and run_suite(ROOT).returncode == 0


# Each probe set imports the app only in a fresh subprocess, never in the grader.
API_PROBE = '''
import importlib, json, shutil
from pathlib import Path
from datetime import datetime
from fastapi.testclient import TestClient
module = importlib.import_module("app.main")
with TestClient(module.app) as c:
    response = c.get("/api/notes")
    assert response.status_code == 200 and response.json() == []
    created = c.post("/api/notes", json={"title":"grader first", "body":"body text"})
    assert created.status_code == 201
    note = created.json()
    assert set(note) == {"id", "title", "body", "created_at"}
    assert isinstance(note["id"], (int, str)) and not isinstance(note["id"], bool)
    assert note["title"] == "grader first" and note["body"] == "body text"
    assert isinstance(note["created_at"], str)
    datetime.fromisoformat(note["created_at"].replace("Z", "+00:00"))
    second = c.post("/api/notes", json={"title":"grader second", "body":""})
    assert second.status_code == 201 and second.json()["id"] != note["id"]
    response = c.get("/api/notes")
    assert response.status_code == 200 and isinstance(response.json(), list)
    assert len(response.json()) == 2 and note in response.json()
    for title in ["", " ", "\\t\\n"]:
        assert c.post("/api/notes", json={"title":title, "body":"invalid"}).status_code == 422
    assert len(c.get("/api/notes").json()) == 2
    removed = c.delete("/api/notes/" + str(note["id"]))
    assert removed.status_code == 204 and removed.content == b""
    assert c.delete("/api/notes/" + str(note["id"])).status_code == 404
    assert c.get("/api/notes").json() == [second.json()]
    health = c.get("/api/health")
    assert health.status_code == 200
    assert health.json() == {"status":"ok", "spec":json.loads(Path("SPEC.lock").read_text(encoding="utf-8"))["spec_sha256"]}
    original = Path("SPEC.lock").read_text(encoding="utf-8")
    data = json.loads(original)
    data["spec_sha256"] = "request-time-probe"
    # This subprocess runs in an isolated copy; the student's lock is never edited.
    shutil.copy2("SPEC.lock", "SPEC.lock.bak_request_probe")
    Path("SPEC.lock").write_text(json.dumps(data), encoding="utf-8")
    assert c.get("/api/health").json()["spec"] == "request-time-probe"
'''


def grader_api():
    workspace = Path(tempfile.mkdtemp(prefix="w13-probe-"))
    shutil.copytree(ROOT, workspace, dirs_exist_ok=True,
                    ignore=lambda directory, names: suite_ignore(directory, names) | (set(names) & {"tests"}))
    outcome = run([sys.executable, "-c", API_PROBE], cwd=workspace,
                  env=dict(os.environ, PYTHONPATH=str(workspace)))
    if outcome.returncode:
        print(outcome.stdout[-1500:], file=sys.stderr)
    return outcome.returncode == 0


class Markup(HTMLParser):
    def __init__(self):
        super().__init__()
        self.selectors = set()
        self.repeated_item = False

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        self.selectors.add(attributes.get("data-testid"))
        if attributes.get("data-testid") == "note-item" and "v-for" in attributes:
            self.repeated_item = True


def ui_static():
    result = run([sys.executable, "-c", '''
from app.main import app
from fastapi.testclient import TestClient
with TestClient(app) as client:
    response = client.get("/")
    assert response.status_code == 200
    print(response.text)
'''])
    if result.returncode:
        return False
    markup = Markup()
    markup.feed(result.stdout)
    selectors = [item["testid"] for item in contract()["ui"]]
    return all(f'data-testid="{item}"' in result.stdout for item in selectors) \
        and markup.repeated_item and bool(re.search(r"fetch\s*\(\s*['\"`]/api/notes", result.stdout))


def tests_pass_correct():
    return (ROOT / "tests/test_spec.py").is_file() and run_suite(ROOT, oracle("correct")).returncode == 0


def tests_catch_wrong():
    if not (ROOT / "tests/test_spec.py").is_file():
        return 0
    earned = 0
    for name in ["wrong_status", "wrong_delete", "wrong_validation", "wrong_shape"]:
        outcome = run_suite(ROOT, oracle(name))
        if outcome.returncode == 1 and re.search(r"\b[1-9]\d* failed\b", outcome.stdout) \
                and not re.search(r"^(?:_+[ \t]+)?ERROR collecting\b", outcome.stdout, re.M):
            earned += 0.5
    return earned


def edge_case_tests():
    edge_ids = ac_refs(section(text("SPEC.md"), "Edge cases")) & ac_ids()
    return any((match := re.match(r"test_ac_(\d{2})_", node.name))
               and match.group(1) in ac_ids()
               and (node.name.startswith(f"test_ac_{match.group(1)}_edge_")
                    or match.group(1) in edge_ids) for node in functions())


def review_round2():
    cited = ac_refs(text("REVIEW2.md"))
    changes = section(text("SPEC.md"), "Changes after review")
    dated = re.findall(r"^###[^\n]*?(\d{4}-\d{2}-\d{2})", changes, re.M)
    return review_structure("REVIEW2.md") and len(cited) >= 2 and cited <= ac_ids() and len(dated) >= 2


def fetch_json(url, wall=10.0, limit=65536):
    result = []
    errors = []
    def fetch():
        try:
            with urlopen(url, timeout=wall) as response:
                body = response.read(limit + 1)
                if len(body) > limit:
                    raise ValueError("response exceeds size limit")
                result.append((response.status, json.loads(body)))
        except Exception as error:
            errors.append(error)
    worker = threading.Thread(target=fetch, daemon=True)
    worker.start()
    worker.join(wall)
    if worker.is_alive():
        raise TimeoutError("response exceeded wall-clock limit")
    if errors:
        raise errors[0]
    return result[0]


def deployed():
    match = re.search(r"https://[^\s<>\]\)\"']+", text("vercel_url.txt"))
    if not match:
        return False
    url = match.group(0).rstrip("/.,;")
    if not urlparse(url).hostname:
        return False
    status, data = fetch_json(url + "/api/health")
    ok = status == 200 and data.get("status") == "ok" and data.get("spec") == lock()["spec_sha256"]
    return {"url": url, "spec": data.get("spec")} if ok else False


def ui_behaviour():
    if not (os.environ.get("CI") and os.environ.get("W13_BROWSER_READY") == "1"):
        return False
    result = run(["uvx", "--offline", "--from", "playwright==1.55.0", "--with", "httpx==0.28.1",
                  "--with", "fastapi==0.116.1", "--with", "uvicorn==0.35.0",
                  "python", "grader/browser_probe.py"], timeout=45)
    return result.returncode == 0


def evaluate(name):
    maximum = (REQUIRED | BONUS)[name]
    try:
        if name in GUARDED and not (contract_intact() and impl_original()):
            outcome = False
        else:
            outcome = globals()[name]()
        full = outcome is True or isinstance(outcome, dict)
        earned = maximum if full else (outcome if isinstance(outcome, (int, float)) and not isinstance(outcome, bool) else 0)
        ok = full or (maximum > 0 and earned == maximum)
        row = {"name": name, "status": ("bonus" if ok else "todo") if name in BONUS else ("pass" if ok else "fail"),
               "points": earned, "max": maximum}
        if isinstance(outcome, dict):
            row.update(outcome)
        return row, ok
    except Exception as error:
        print(f"{name}: {error}", file=sys.stderr)
        return {"name": name, "status": "todo" if name in BONUS else "fail", "points": 0, "max": maximum}, False


def backup(path):
    if path.exists():
        shutil.copy2(path, path.with_name(path.name + ".bak_" + str(time.time_ns())))


def reports(required, bonus):
    for filename, rows, key, total in [("report.json", required, "score", sum(REQUIRED.values())),
                                       ("challenge_report.json", bonus, "bonus", sum(BONUS.values()))]:
        path = ROOT / "results" / filename
        path.parent.mkdir(exist_ok=True)
        backup(path)
        data = {key: sum(item["points"] for item in rows), "total" if key == "score" else "bonus_total": total, "results": rows}
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    if sys.argv[1] == "--red-preview":
        outcome = run_suite(ROOT)
        print(outcome.stdout)
        for line in outcome.stdout.splitlines():
            if line.startswith("PASSED "):
                print("passes on the current app: " + line.removeprefix("PASSED "))
        red = all_failed(outcome)
        if not red:
            print("NOT RED: require failed tests, zero passed and no collection errors")
        sys.exit(0 if red else 1)
    elif sys.argv[1] == "--reports":
        reports(json.loads(sys.argv[2]), json.loads(sys.argv[3]))
    else:
        row, ok = evaluate(sys.argv[1])
        print(json.dumps(row))
        sys.exit(0 if ok else 1)
