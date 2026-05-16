# Skillathon

This repository was prepared for the **May 16, 2026** event **"비개발자도 할 수 있는 AI 업무 자동화 MeetUp&Skillathon"**.

The meetup focused on practical AI automation for non-developers, Codex-based skill building, and hands-on experimentation with stronger agent workflows such as OpenClaw and NVIDIA NemoClaw. This project is my working skillathon submission and practice repository built in that context.

## What this project is about

The main project in this repository is `running-crew-match`, a demo skill that recommends Korean running crews based on:

- area
- preferred day and time
- running level
- running goal
- extra preferences such as small groups or women-friendly 분위기

The current version is designed as an **executable demo skill**, not just a documentation-only skill.

## What is included

- `running-crew-match/SKILL.md`
  The main skill definition and operating rules.
- `running-crew-match/assets/demo_crews.json`
  Bundled demo dataset for offline matching tests.
- `running-crew-match/scripts/match_running_crews.py`
  Local CLI entrypoint for testing the skill quickly.
- `running-crew-match/scripts/dev_server.py`
  Local HTTP API server for demo or deployment.
- `running-crew-match/references/usage-guide.md`
  Step-by-step guide for running the skill.
- `running-crew-match/references/api-contract.md`
  Request and response contract for the demo API.
- `running-crew-match/references/test-scenarios.md`
  Example prompts and expected behavior checks.

## Why this repo fits the event

This repository is meant to show how a skill can evolve:

1. from a simple `SKILL.md`
2. into a testable local CLI workflow
3. into a deployable API-backed demo
4. and eventually into a stronger automation flow connected to broader agent systems

That direction matches the event theme of making AI automation approachable and practical, even for people who are not full-time developers.

## Quick start

Run the local matcher:

```bash
cd /Users/jisu/Desktop/Skillathon/running-crew-match
python3 scripts/match_running_crews.py \
  --region "성수" \
  --day "평일" \
  --time "저녁" \
  --level "초보" \
  --goal "친목" \
  --notes "소규모" \
  --limit 3 \
  --json
```

Run the local API server:

```bash
cd /Users/jisu/Desktop/Skillathon/running-crew-match
python3 scripts/dev_server.py --host 127.0.0.1 --port 8000
```

For the full run guide, see:

- `running-crew-match/references/usage-guide.md`
