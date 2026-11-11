#!/usr/bin/env python3
"""Дымовая проверка: добавление устройства во временный JSON-файл.
Использование: smoke_test.py <каталог_развертывания> <отчет>"""
import json
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


def run(cmd):
    res = subprocess.run(cmd, capture_output=True, text=True)
    return res.returncode, (res.stdout + res.stderr).strip()


def main():
    deploy_dir, report = Path(sys.argv[1]), Path(sys.argv[2])
    app = str(deploy_dir / "inventory.py")
    lines = ["Среда: test/inventory",
             "Время: " + datetime.now(timezone.utc).isoformat(),
             "Каталог: " + str(deploy_dir)]
    ok = True
    with tempfile.TemporaryDirectory() as tmp:
        data = str(Path(tmp) / "smoke.json")
        checks = [
            ("--help", [sys.executable, app, "--help"], 0),
            ("add", [sys.executable, app, "--file", data, "add",
                     "--name", "Smoke Router", "--serial", "SMOKE-001"], 0),
            ("duplicate", [sys.executable, app, "--file", data, "add",
                           "--name", "Other", "--serial", "smoke-001"], 2),
        ]
        for name, cmd, expected in checks:
            code, out = run(cmd)
            passed = code == expected
            ok = ok and passed
            lines.append("[%s] %s: код %d (ожидался %d)"
                         % ("OK" if passed else "FAIL", name, code, expected))
        try:
            stored = json.loads(Path(data).read_text(encoding="utf-8"))
            passed = stored == [{"name": "Smoke Router", "serial": "SMOKE-001"}]
        except (OSError, ValueError):
            passed = False
        ok = ok and passed
        lines.append("[%s] содержимое временного JSON" % ("OK" if passed else "FAIL"))
    lines.append("Результат: " + ("УСПЕХ" if ok else "ОШИБКА"))
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
