"""game.twee から game.html を再生成する（Tweego がない環境用）。

game.html 内の Harlowe エンジン部分はそのまま使い、<tw-storydata> の中身だけを
game.twee の内容で置き換える。

使い方: python3 tools/build.py
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TWEE = ROOT / "game.twee"
HTML = ROOT / "game.html"

HEADER = re.compile(r"^:: *(?P<name>[^\[\{\n]+?) *(?:\[(?P<tags>[^\]]*)\])? *(?:\{[^}]*\})? *$", re.M)


def parse(source):
    passages = []
    matches = list(HEADER.finditer(source))
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(source)
        text = source[m.end():end].strip("\n").rstrip()
        passages.append((m.group("name").strip(), (m.group("tags") or "").split(), text))
    return passages


def build():
    passages = parse(TWEE.read_text(encoding="utf-8"))
    by_name = {name: (tags, text) for name, tags, text in passages}
    title = by_name["StoryTitle"][1].strip()
    data = json.loads(by_name["StoryData"][1])

    css = "\n".join(text for _, tags, text in passages if "stylesheet" in tags)
    js = "\n".join(text for _, tags, text in passages if "script" in tags)
    story = [(name, tags, text) for name, tags, text in passages
             if name not in ("StoryTitle", "StoryData") and not {"stylesheet", "script"} & set(tags)]

    pids = {name: i + 1 for i, (name, _, _) in enumerate(story)}
    parts = []
    for i, (name, tags, text) in enumerate(story):
        x, y = 100 + (i % 8) * 125, 100 + (i // 8) * 125
        parts.append(
            f'<tw-passagedata pid="{pids[name]}" name="{html.escape(name)}" tags="{html.escape(" ".join(tags))}" '
            f'position="{x},{y}" size="100,100">{html.escape(text)}</tw-passagedata>')

    storydata = (
        f'<tw-storydata name="{html.escape(title)}" startnode="{pids[data["start"]]}" creator="Tweego" '
        f'creator-version="2.1.1+81d1d71" ifid="{data["ifid"]}" zoom="1" format="{data["format"]}" '
        f'format-version="{data["format-version"]}" options="" hidden>'
        f'<style role="stylesheet" id="twine-user-stylesheet" type="text/twine-css">{css}</style>'
        f'<script role="script" id="twine-user-script" type="text/twine-javascript">{js}</script>'
        + "".join(parts) + "</tw-storydata>")

    if "</script" in js.lower():
        raise SystemExit("Story JavaScript に </script> を含めないでください")

    page = HTML.read_text(encoding="utf-8")
    start, end = page.index("<tw-storydata"), page.index("</tw-storydata>") + len("</tw-storydata>")
    page = page[:start] + storydata + page[end:]
    page = re.sub(r"<title>.*?</title>", f"<title>{html.escape(title)}</title>", page, count=1)
    HTML.write_text(page, encoding="utf-8")
    print(f"built {HTML.name}: {len(story)} passages")


if __name__ == "__main__":
    build()
