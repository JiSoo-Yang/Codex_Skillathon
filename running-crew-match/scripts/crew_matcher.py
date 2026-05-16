#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DEFAULT_DATA_PATH = Path(__file__).resolve().parent.parent / "assets" / "demo_crews.json"

DAY_ALIASES = {
    "월요일": "monday",
    "월요": "monday",
    "화요일": "tuesday",
    "화요": "tuesday",
    "수요일": "wednesday",
    "수요": "wednesday",
    "목요일": "thursday",
    "목요": "thursday",
    "금요일": "friday",
    "금요": "friday",
    "토요일": "saturday",
    "토요": "saturday",
    "일요일": "sunday",
    "일요": "sunday",
    "평일": "weekday",
    "주중": "weekday",
    "주말": "weekend",
}

TIME_ALIASES = {
    "아침": "morning",
    "오전": "morning",
    "새벽": "morning",
    "점심": "afternoon",
    "오후": "afternoon",
    "저녁": "evening",
    "퇴근후": "evening",
    "퇴근 후": "evening",
    "밤": "night",
    "야간": "night",
}

LEVEL_ALIASES = {
    "초보": "beginner",
    "입문": "beginner",
    "중급": "intermediate",
    "기록": "training",
    "훈련": "training",
    "레이스": "training",
}

GOAL_ALIASES = {
    "친목": "friendship",
    "다이어트": "weight_loss",
    "습관": "habit",
    "루틴": "habit",
    "5k": "5k",
    "5km": "5k",
    "10k": "10k",
    "10km": "10k",
    "하프": "half-marathon",
    "half": "half-marathon",
    "마라톤": "marathon",
    "풀코스": "marathon",
    "스피드": "speed",
    "기록향상": "speed",
}

NOTE_ALIASES = {
    "여성": "women-friendly",
    "여성중심": "women-friendly",
    "여성 중심": "women-friendly",
    "소규모": "small-group",
    "소수": "small-group",
    "한강": "riverside",
    "강변": "riverside",
    "야간": "night-run",
    "밤": "night-run",
    "퇴근후": "after-work",
    "퇴근 후": "after-work",
}

TAG_LABELS = {
    "monday": "월요일",
    "tuesday": "화요일",
    "wednesday": "수요일",
    "thursday": "목요일",
    "friday": "금요일",
    "saturday": "토요일",
    "sunday": "일요일",
    "weekday": "평일",
    "weekend": "주말",
    "morning": "아침",
    "afternoon": "오후",
    "evening": "저녁",
    "night": "밤",
    "beginner": "초보",
    "intermediate": "중급",
    "training": "기록 지향",
    "social": "친목형",
    "friendship": "친목",
    "weight_loss": "다이어트",
    "habit": "루틴 형성",
    "5k": "5k",
    "10k": "10k",
    "half-marathon": "하프 준비",
    "marathon": "마라톤 준비",
    "speed": "스피드 훈련",
    "women-friendly": "여성 친화",
    "small-group": "소규모",
    "riverside": "강변 코스",
    "night-run": "야간 러닝",
    "after-work": "퇴근 후",
}

MAJOR_REGION_TAGS = ["서울", "부산", "성남", "수원", "대구", "경기"]

REGION_TO_CITY = {
    "성수": "서울",
    "성동구": "서울",
    "잠실": "서울",
    "송파": "서울",
    "홍대": "서울",
    "합정": "서울",
    "마포": "서울",
    "강남": "서울",
    "역삼": "서울",
    "선릉": "서울",
    "건대": "서울",
    "광진": "서울",
    "여의도": "서울",
    "한강": "서울",
    "분당": "성남",
    "정자동": "성남",
    "탄천": "성남",
    "광교": "수원",
    "영통": "수원",
    "서면": "부산",
    "해운대": "부산",
    "광안리": "부산",
    "센텀": "부산",
    "민락": "부산",
    "수성": "대구",
    "신천": "대구",
}


def normalize_text(value: str | None) -> str:
    if not value:
        return ""
    return "".join(str(value).lower().split())


def canonical_tags(*values: str, alias_map: dict[str, str]) -> set[str]:
    combined = normalize_text(" ".join(value for value in values if value))
    tags: set[str] = set()
    for raw, canonical in alias_map.items():
        if normalize_text(raw) in combined:
            tags.add(canonical)
    return tags


def load_crews(data_path: str | Path | None = None) -> list[dict[str, Any]]:
    path = Path(data_path) if data_path else DEFAULT_DATA_PATH
    return json.loads(path.read_text(encoding="utf-8"))


def build_query(region: str = "", day: str = "", time: str = "", level: str = "", goal: str = "", notes: str = "") -> dict[str, Any]:
    return {
        "region": region.strip(),
        "day": day.strip(),
        "time": time.strip(),
        "level": level.strip(),
        "goal": goal.strip(),
        "notes": notes.strip(),
        "day_tags": canonical_tags(day, notes, alias_map=DAY_ALIASES),
        "time_tags": canonical_tags(time, notes, alias_map=TIME_ALIASES),
        "level_tags": canonical_tags(level, notes, alias_map=LEVEL_ALIASES),
        "goal_tags": canonical_tags(goal, notes, alias_map=GOAL_ALIASES),
        "note_tags": canonical_tags(notes, region, alias_map=NOTE_ALIASES),
    }


def tag_labels(tags: list[str] | set[str]) -> list[str]:
    return [TAG_LABELS.get(tag, tag) for tag in tags]


def overlap_score(requested: set[str], available: list[str], points: int, label: str) -> tuple[int, list[str]]:
    overlap = sorted(requested.intersection(available))
    if not overlap:
        return 0, []
    readable = ", ".join(tag_labels(overlap))
    return points * len(overlap), [f"{label} 일치: {readable}"]


def infer_city(region: str) -> str:
    normalized_region = normalize_text(region)
    for token, city in REGION_TO_CITY.items():
        if normalize_text(token) in normalized_region:
            return city
    for city in MAJOR_REGION_TAGS:
        if normalize_text(city) in normalized_region:
            return city
    return ""


def region_score(region: str, crew: dict[str, Any]) -> tuple[int, list[str]]:
    if not region:
        return 0, []

    normalized_region = normalize_text(region)
    exact_hits = [token for token in crew.get("region_tokens", []) if normalize_text(token) in normalized_region or normalized_region in normalize_text(token)]
    if exact_hits:
        return 10, [f"지역 적합: {crew['area']}"]

    inferred_city = infer_city(region)
    if inferred_city and inferred_city in crew.get("region_tokens", []):
        return 4, [f"같은 권역 후보: {inferred_city}"]

    return 0, []


def fit_summary(crew: dict[str, Any]) -> str:
    level_part = ", ".join(tag_labels(crew.get("level_tags", []))) or "정보 없음"
    goal_part = ", ".join(tag_labels(crew.get("goal_tags", []))) or "정보 없음"
    return f"수준: {level_part} / 목표: {goal_part}"


def summarize_reasons(reasons: list[str], crew: dict[str, Any]) -> str:
    if reasons:
        return "; ".join(reasons[:3])
    return crew.get("description", "조건과 완전히 일치하는 신호는 적지만 검토 가능한 후보")


def score_crew(query: dict[str, Any], crew: dict[str, Any]) -> dict[str, Any]:
    reasons: list[str] = []
    score = 0

    region_points, region_reasons = region_score(query["region"], crew)
    score += region_points
    reasons.extend(region_reasons)

    for requested_key, available_key, points, label in [
        ("day_tags", "day_tags", 3, "요일 조건"),
        ("time_tags", "time_tags", 2, "시간대 조건"),
        ("level_tags", "level_tags", 3, "수준 적합성"),
        ("goal_tags", "goal_tags", 3, "목표 적합성"),
        ("note_tags", "vibe_tags", 2, "추가 조건"),
    ]:
        gained, gained_reasons = overlap_score(query[requested_key], crew.get(available_key, []), points, label)
        score += gained
        reasons.extend(gained_reasons)

    match_mode = "strong" if score >= 8 else "fallback"
    return {
        "id": crew["id"],
        "name": crew["name"],
        "area": crew["area"],
        "schedule": crew["schedule_text"],
        "level_fit": fit_summary(crew),
        "reason": summarize_reasons(reasons, crew),
        "source_url": crew["source_url"],
        "freshness_note": crew["freshness_note"],
        "participation_notes": crew.get("participation_notes", ""),
        "description": crew.get("description", ""),
        "score": score,
        "match_mode": match_mode,
    }


def build_assumptions(query: dict[str, Any]) -> list[str]:
    assumptions: list[str] = []
    if not query["day"]:
        assumptions.append("요일 정보가 없어 모든 일정 후보를 함께 비교했다.")
    if not query["time"]:
        assumptions.append("시간대 정보가 없어 아침/저녁 후보를 함께 비교했다.")
    if not query["level"]:
        assumptions.append("러닝 수준 정보가 없어 초보/중급 후보를 함께 비교했다.")
    if not query["goal"]:
        assumptions.append("구체적인 목표 정보가 없어 친목과 훈련 후보를 함께 비교했다.")
    return assumptions


def match_crews(region: str = "", day: str = "", time: str = "", level: str = "", goal: str = "", notes: str = "", limit: int = 5, data_path: str | Path | None = None) -> dict[str, Any]:
    crews = load_crews(data_path)
    query = build_query(region=region, day=day, time=time, level=level, goal=goal, notes=notes)

    scored = [score_crew(query, crew) for crew in crews]
    scored.sort(key=lambda item: (-item["score"], item["name"]))

    trimmed = scored[: max(1, min(limit, 10))]
    return {
        "mode": "demo",
        "data_source": str(Path(data_path) if data_path else DEFAULT_DATA_PATH),
        "query": {
            "region": region,
            "day": day,
            "time": time,
            "level": level,
            "goal": goal,
            "notes": notes,
            "limit": limit,
        },
        "assumptions": build_assumptions(query),
        "count": len(trimmed),
        "results": trimmed,
    }
