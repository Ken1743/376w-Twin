# The Exit Is Still There

A choose-your-own-adventure ethics game built with Twine (Harlowe 3.1.0), based on the ACM Code of Ethics case study [Dark UX Patterns](https://ethics.acm.org/code-of-ethics/using-the-code/case-dark-ux-patterns/).

You play an engineer at LearnLoop, a subscription learning app, who is asked to make the cancel button harder to find. Your choices lead to one of six endings, each followed by an epilogue that shows how users were affected.

## Team Nagano

| Member | Role |
|---|---|
| Fuka Nagata | User & UX perspective |
| Sora Watanabe | Business & product perspective |
| Kentaro Yamada | Overall structure, branching design, Twine build |

## Play

Open `game.html` in a browser. Keep the `assets/` folder next to it, because the character and background images are loaded from there.

- Click, Space, or Enter to advance the dialogue; number keys pick a choice; L opens the dialogue log.
- English is the default. Use the EN / 日本語 switch in the top-right corner to change languages.

## Files

| Path | Contents |
|---|---|
| `game.twee` | Story source (Twee 3): passages, story JavaScript, and stylesheet |
| `game.html` | Playable build |
| `assets/` | Character sprites (`m1`, `m2`, `w1`) and backgrounds (`bg/`) |
| `tools/build.py` | Rebuilds `game.html` from `game.twee` |

## Build

After editing `game.twee`, rebuild the HTML:

```sh
python3 tools/build.py
```

The script replaces only the story data in `game.html` and keeps the Harlowe engine, so Tweego is not required.

