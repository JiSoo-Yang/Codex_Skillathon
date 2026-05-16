# Running Crew Match Usage Guide

안녕하세요. 이 문서는 `running-crew-match` 스킬을 직접 실행해보는 방법을 단계별로 설명합니다.

## 1. 로컬 CLI로 가장 빠르게 실행하기

아래 명령은 별도 패키지 설치 없이, 이 저장소 안의 데모 데이터로 바로 매칭 결과를 확인하는 가장 빠른 방법입니다.

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

예상 결과:

- JSON 형식의 추천 결과가 출력됩니다.
- `results` 안에 러닝 크루 후보가 2~3개 이상 보이면 정상입니다.
- 이 데이터는 데모 데이터이므로 실제 공개 크루 정보처럼 확정적으로 해석하면 안 됩니다.

## 2. 다른 조건으로 테스트해보기

예를 들어 잠실에서 주말 아침 하프 대비 모임을 보고 싶다면 이렇게 실행합니다.

```bash
cd /Users/jisu/Desktop/Skillathon/running-crew-match
python3 scripts/match_running_crews.py \
  --region "잠실" \
  --day "주말" \
  --time "아침" \
  --level "중급" \
  --goal "하프" \
  --limit 3 \
  --json
```

부산에서 여성 중심 소규모 모임을 보고 싶다면 이렇게 실행합니다.

```bash
cd /Users/jisu/Desktop/Skillathon/running-crew-match
python3 scripts/match_running_crews.py \
  --region "부산" \
  --day "주말" \
  --time "아침" \
  --level "초보" \
  --goal "친목" \
  --notes "여성 중심 소규모" \
  --limit 2 \
  --json
```

## 3. 로컬 API 서버로 실행하기

CLI 대신 HTTP API 형태로 실행해보고 싶다면 아래 서버를 띄웁니다.

```bash
cd /Users/jisu/Desktop/Skillathon/running-crew-match
python3 scripts/dev_server.py --host 127.0.0.1 --port 8000
```

서버가 정상 실행되면 아래와 비슷한 로그가 보입니다.

```text
RunningCrewMatch demo server on http://127.0.0.1:8000
Using data source: /Users/jisu/Desktop/Skillathon/running-crew-match/assets/demo_crews.json
```

## 4. 서버 상태 확인하기

다른 터미널에서 아래 명령으로 헬스체크를 합니다.

```bash
curl http://127.0.0.1:8000/health
```

정상 응답 예시:

```json
{
  "status": "ok",
  "mode": "demo",
  "data_source": "/Users/jisu/Desktop/Skillathon/running-crew-match/assets/demo_crews.json"
}
```

## 5. API로 직접 매칭 요청 보내기

성수 평일 저녁 초보 친목 러닝 크루 예시는 아래처럼 호출합니다.

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

부산 여성 중심 소규모 예시는 아래와 같습니다.

```bash
curl -X POST http://127.0.0.1:8000/match \
  -H 'Content-Type: application/json' \
  -d '{
    "region": "부산",
    "day": "주말",
    "time": "아침",
    "level": "초보",
    "goal": "친목",
    "notes": "여성 중심 소규모",
    "limit": 2
  }'
```

## 6. Brev 같은 배포 환경에서 접근하기

Brev에 올릴 때는 아래처럼 서버를 실행하면 됩니다.

```bash
python3 running-crew-match/scripts/dev_server.py --host 0.0.0.0 --port ${PORT:-8000}
```

배포가 끝나면 배포된 URL을 `RUNNING_CREW_MATCH_API_BASE_URL` 로 연결해서 스킬이 API 모드로 먼저 접근하도록 구성할 수 있습니다.

예시:

```bash
export RUNNING_CREW_MATCH_API_BASE_URL="https://your-running-crew-api.example.com"
```

이후 스킬은 우선 `POST /match` 를 호출하고, 배포된 API가 없을 때만 로컬 데모 모드나 공개 웹 확인 단계로 내려가면 됩니다.

## 7. 자주 보는 확인 포인트

- CLI 결과에 `results` 배열이 있으면 기본 동작은 정상입니다.
- `/health` 가 `status: ok` 를 반환하면 서버는 정상입니다.
- `/match` 결과에서 `freshness_note` 는 데모 데이터임을 알려주는 메모입니다.
- 실제 제출 데모에서는 "현재 버전은 데모 데이터 기반, 추후 라이브 데이터 소스로 확장 가능" 이라고 설명하면 자연스럽습니다.
