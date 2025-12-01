#!/usr/bin/env python3
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from github import Github
from collections import Counter

USERNAME = os.environ["TARGET_USER"]
TOKEN = os.environ["GITHUB_TOKEN"]
OUT = "assets/activity_radar.svg"

EVENT_MAP = {
    "PushEvent": "Commits",
    "IssuesEvent": "Issues",
    "PullRequestEvent": "Pull requests",
    "PullRequestReviewEvent": "Code review"
}

gh = Github(TOKEN)
user = gh.get_user(USERNAME)

counts = Counter()
events = user.get_events()

for e in events:
    if e.type in EVENT_MAP:
        counts[EVENT_MAP[e.type]] += 1

# Ensure all categories exist
cats = ["Commits", "Issues", "Pull requests", "Code review"]
vals = [counts.get(c, 0) for c in cats]

total = sum(vals) or 1
perc = [v / total * 100 for v in vals]

commits, issues, prs, reviews = perc

def scale(v): return v / 100

x_left = -scale(commits)
x_right = scale(issues)
y_up = scale(reviews)
y_down = -scale(prs)

fig, ax = plt.subplots(figsize=(3,3))

ax.axhline(0, color="black", linewidth=0.6)
ax.axvline(0, color="black", linewidth=0.6)

ax.plot([x_left, x_right], [0, 0], linewidth=6)
ax.plot([0, 0], [y_down, y_up], linewidth=6)

ax.scatter([x_left, x_right, 0, 0],
           [0, 0, y_up, y_down], s=40)

ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
ax.axis("off")

fig.savefig(OUT, bbox_inches="tight")
print("Generated", OUT)
