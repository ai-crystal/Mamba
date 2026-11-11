#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成全书插图。

逐章调用 book/code/chNN/figures.py，把 PNG 写到 book/images/chNN/。
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

CODE = Path(__file__).resolve().parent
BOOK = CODE.parent
sys.path.insert(0, str(CODE))

import common  # noqa: E402


def load(path: Path):
    spec = importlib.util.spec_from_file_location(path.parent.name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


def main() -> None:
    dirs = sorted(
        (p for p in CODE.iterdir() if p.is_dir() and (p / "figures.py").exists()),
        key=lambda p: (p.name != "front", p.name),
    )
    for d in dirs:
        common.CURRENT = BOOK / "images" / d.name
        common.CURRENT.mkdir(parents=True, exist_ok=True)
        mod = load(d / "figures.py")
        for fn in getattr(mod, "FIGURES", []):
            getattr(mod, fn)()
    print("done")


if __name__ == "__main__":
    main()
