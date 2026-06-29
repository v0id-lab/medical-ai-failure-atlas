#!/usr/bin/env python3
from __future__ import annotations

from leaderboard.app import demo


if __name__ == "__main__":
    if demo is None:
        raise SystemExit("Install Gradio with: python3 -m pip install -r requirements.txt")
    demo.launch()
