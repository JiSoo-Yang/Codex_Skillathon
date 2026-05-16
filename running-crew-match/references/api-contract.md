# Running Crew Match API Contract

## Purpose

Use this contract when a deployed running-crew-match service is available.

The API is designed for lightweight recommendation calls and mirrors the bundled local demo matcher.

## Environment

- `RUNNING_CREW_MATCH_API_BASE_URL`: Base URL of the deployed API
- `RUNNING_CREW_MATCH_DATA_PATH`: Optional server-side override for custom data

## Endpoints

### `GET /health`

Returns a minimal service status.

Example response:

```json
{
  "status": "ok",
  "mode": "demo",
  "data_source": "/app/running-crew-match/assets/demo_crews.json"
}
```

### `POST /match`

Request body:

```json
{
  "region": "성수",
  "day": "평일",
  "time": "저녁",
  "level": "초보",
  "goal": "친목",
  "notes": "소규모",
  "limit": 3
}
```

Response body:

```json
{
  "mode": "demo",
  "data_source": "/app/running-crew-match/assets/demo_crews.json",
  "query": {
    "region": "성수",
    "day": "평일",
    "time": "저녁",
    "level": "초보",
    "goal": "친목",
    "notes": "소규모",
    "limit": 3
  },
  "assumptions": [],
  "count": 3,
  "results": [
    {
      "id": "seongsu-social-loop",
      "name": "Seongsu Social Loop",
      "area": "서울 성수",
      "schedule": "화/목 19:30",
      "level_fit": "수준: 초보, 친목형 / 목표: 친목, 루틴 형성, 5k",
      "reason": "지역 적합: 서울 성수; 요일 조건 일치: 평일; 시간대 조건 일치: 저녁",
      "source_url": "https://example.com/demo/seongsu-social-loop",
      "freshness_note": "Demo data only. Validate with live public sources before joining.",
      "participation_notes": "첫 참석은 가벼운 5k 기준",
      "description": "퇴근 후 가볍게 달리며 친목을 쌓는 초보자 친화형 모임",
      "score": 23,
      "match_mode": "strong"
    }
  ]
}
```

## Local test example

```bash
curl -X POST http://127.0.0.1:8000/match \
  -H 'Content-Type: application/json' \
  -d '{
    "region": "성수",
    "day": "평일",
    "time": "저녁",
    "level": "초보",
    "goal": "친목",
    "notes": "소규모",
    "limit": 3
  }'
```

## Notes

- 현재 번들 자산은 데모 데이터이므로, 응답을 실제 공개 크루 정보처럼 단정하면 안 된다.
- 실운영에서는 이 계약을 유지한 채 데이터 공급원만 교체하는 방식이 가장 안전하다.
