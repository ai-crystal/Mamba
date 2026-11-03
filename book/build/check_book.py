# -*- coding: utf-8 -*-
"""书稿体检：结构完整性、引用、公式/代码块配对、AI 腔残留。"""
from __future__ import annotations

import glob
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

AI_PATTERNS = [
    (r"注意[，：]", "注意，"),
    (r"请记住", "请记住"),
    (r"关键在于", "关键在于"),
    (r"换句话说", "换句话说"),
    (r"一句话(概括|总结|：)", "一句话"),
    (r"值得停下来", "值得停下来"),
    (r"非常重要", "非常重要"),
    (r"极其重要", "极其重要"),
    (r"惊人", "惊人"),
    (r"这不是.{0,12}而是", "不是X而是Y"),
    (r"首先.{0,40}其次", "首先/其次"),
    (r"让我们", "让我们"),
]

# 每个文件必须仍然出现的关键数字（抽查信息是否被删）
KEY_NUMBERS = {
    "01": ["16384", "96.35"],
    "02": ["N^2L", "Delta"],
    "05": ["2n+1", "theta"],
    "09": ["2^{4N/3}"],
    "13": ["86.09", "96.35", "91.13"],
    "15": ["87.46", "98.58"],
    "17": ["18.3", "97.0"],
    "21": ["9.88", "8.71", "63.3"],
    "24": ["TN^2", "T^2N"],
    "25": ["6.1"],
    "27": ["8.26", "8.60", "5.95"],
    "32": ["10.24", "100.00", "0.90"],
}


def main():
    total_han = 0
    issues = []
    for f in sorted(glob.glob(str(ROOT / "*.md"))):
        p = Path(f)
        if p.name.startswith("_"):
            continue
        s = p.read_text(encoding="utf-8")
        han = len(re.findall(r"[\u4e00-\u9fff]", s))
        total_han += han
        h = {
            lv: len(re.findall(rf"^{'#' * lv} ", s, re.M))
            for lv in (1, 2, 3)
        }
        dd = s.count("$$")
        fences = len(re.findall(r"^```", s, re.M))
        links = re.findall(r"\]\(([^)]+)\)", s)
        imgs = len(re.findall(r"!\[", s))
        bold = len(re.findall(r"\*\*[^*\n]+\*\*", s))
        dash = s.count("——")
        ai = []
        for pat, name in AI_PATTERNS:
            n = len(re.findall(pat, s))
            if n:
                ai.append(f"{name}×{n}")

        if dd % 2:
            issues.append(f"{p.name}: $$ 数量为奇数")
        if fences % 2:
            issues.append(f"{p.name}: 代码围栏未闭合")
        for lk in links:
            if lk.startswith("http") or lk.startswith("#"):
                continue
            base = lk.split("#")[0]
            if base and not (ROOT / base).exists():
                issues.append(f"{p.name}: 死链 {lk}")

        key = p.name.split("-")[0]
        if key in KEY_NUMBERS:
            for num in KEY_NUMBERS[key]:
                if num not in s:
                    issues.append(f"{p.name}: 关键数字丢失 {num}")

        print(
            f"{p.name[:34]:36} 汉字{han:6} 粗{bold:4} 破{dash:3} 图{imgs:2} "
            f"H{h[1]}/{h[2]}/{h[3]}  {' '.join(ai)}"
        )

    print(f"\n总汉字：{total_han}")
    print(f"问题数：{len(issues)}")
    for it in issues:
        print("  !", it)


if __name__ == "__main__":
    main()
