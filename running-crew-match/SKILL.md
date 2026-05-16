---
name: running-crew-match
description: Use this skill to recommend Korean running crews by area, schedule, skill level, and running goal, starting with the bundled local demo matcher and optionally using a deployed API later.
---

# Running Crew Match

## What this skill does

사용자의 지역, 선호 요일과 시간대, 러닝 수준, 목표를 바탕으로 한국 내 러닝 크루 후보를 추천한다.

이 스킬은 현재 기준으로 두 가지 실행 모드를 지원한다.

- 로컬 데모 데이터 기반 추천
- 배포된 API 기반 추천

지금 단계의 기본 전제는 **로컬 실행 우선** 이다. 자동 가입이나 참가 확정이 아니라, 추천과 탐색 지원이 1차 목적이다.

## When to use

- "서울에서 초보자 러닝 크루 찾아줘"
- "성수 근처 평일 저녁 러닝 모임 추천해줘"
- "잠실에서 하프 준비하는 사람들 많은 크루 있을까?"
- "한강 근처 아침 러닝 모임 후보 알려줘"
- "러닝 크루 매칭 데모를 돌려봐"
- "이거 실행 어떻게 해보는거야?"

## When not to use

- 참가 신청을 자동으로 완료해야 하는 경우
- 최신 실시간 모집 공고를 반드시 보장해야 하는 경우
- 비공개 커뮤니티나 로그인 필수 정보에만 의존해야 하는 경우
- 실시간 위치 추적이나 안전 모니터링이 필요한 경우

## Inputs

- `region`: 지역 또는 세부 장소
- `day`: 선호 요일
- `time`: 선호 시간대
- `level`: 초보, 중급, 기록 지향 등 러닝 수준
- `goal`: 다이어트, 친목, 5k, 10k, 하프, 마라톤 준비 등
- `notes`: 여성 중심 선호, 소규모 선호, 혼자 뛰기 부담 같은 추가 조건
- `limit`: 반환 후보 수. 기본값은 5 이하로 유지한다.

핵심 정보가 빠졌다면 추천 품질에 가장 큰 영향을 주는 항목만 최소한으로 확인한다.

## If the user asks how to run this skill

사용자가 실행 방법, 테스트 방법, 배포 방법을 물으면 `references/usage-guide.md` 를 먼저 읽고, 그 안의 단계별 명령어를 바탕으로 안내한다.

가능하면 아래 순서로 설명한다.

- 로컬 CLI 실행
- 로컬 API 서버 실행
- `curl` 로 API 호출
- 필요할 때만 Brev 배포 후 `RUNNING_CREW_MATCH_API_BASE_URL` 연결

## Preferred execution order

### 1. Local demo mode

현재 기본 실행 경로는 로컬 데모 모드다.

이 레포를 직접 사용할 수 있으면 먼저 로컬 데모 매처를 사용한다.

```bash
python3 scripts/match_running_crews.py \
  --region "성수" \
  --day "평일" \
  --time "저녁" \
  --level "초보" \
  --goal "친목" \
  --notes "소규모" \
  --limit 5 \
  --json
```

- 이 모드는 `assets/demo_crews.json` 을 사용한다.
- 데모 데이터는 합성 예시 데이터이므로, 실제 공개 러닝 크루 정보처럼 단정해서 말하지 않는다.
- 결과를 보여줄 때는 필요하면 "데모 데이터 기준" 이라고 짧게 표시한다.
- 배포가 아직 준비되지 않은 단계에서는 이 모드를 기본값으로 본다.

### 2. API mode

`RUNNING_CREW_MATCH_API_BASE_URL` 가 설정되어 있고, 실제 배포된 엔드포인트가 준비된 경우에만 API 모드를 사용한다.

- `POST /match` 로 요청한다.
- 요청과 응답 형식은 `references/api-contract.md` 를 따른다.
- API 결과가 있으면 그 결과를 한국어로 요약해 추천한다.
- 로컬 모드보다 우선해야 하는 이유가 분명할 때만 API 모드를 앞세운다.

### 3. Live public search fallback

사용자가 최신 실제 크루 정보를 원하고, 로컬 데모 데이터나 배포된 API만으로는 충분하지 않을 때만 공개 웹 탐색으로 보완한다.

- 최신성이 중요한 경우 모집일과 최근 활동일을 확인한다.
- 확인된 사실과 추론을 구분한다.
- 오래된 정보는 오래되었다고 명시한다.

## Output style

답변은 짧고 실용적으로 유지한다.

가능하면 각 후보마다 아래를 포함한다.

- 크루 또는 모임 이름
- 주요 활동 지역
- 추정 가능한 일정
- 사용자 목표나 수준과 맞는 이유
- 출처 또는 데이터 출처
- 최신성 또는 데모 여부 메모

마지막에는 "이 후보부터 확인해보면 좋다" 같은 짧은 다음 행동을 덧붙인다.

## Done when

- 사용자가 검토할 만한 후보 목록을 받았다
- 각 후보에 추천 이유가 붙어 있다
- 로컬 데모 결과, API 결과, 실제 웹 확인 결과를 혼동하지 않는다
- 오래되었거나 불확실한 정보는 명시했다

## Failure modes

- 요청 지역이 너무 넓거나 모호한 경우
- 공개 정보가 오래되었거나 매우 적은 경우
- 활동은 보이지만 일정 정보가 불명확한 경우
- 사용자 조건이 너무 좁아 후보가 거의 없는 경우
- 데모 데이터만 있는 상태에서 실제 정보처럼 오해하게 만드는 경우
- 배포되지 않은 API를 기본 경로처럼 설명하는 경우

## Resources

- 실행 가이드: `references/usage-guide.md`
- API 요청과 응답 형식: `references/api-contract.md`
- 예시 입력과 기대 동작: `references/test-scenarios.md`
- 로컬 배포 힌트: `references/deploying-demo-api.md`
- 데모 데이터: `assets/demo_crews.json`
- 로컬 CLI: `scripts/match_running_crews.py`
- 로컬 API 서버: `scripts/dev_server.py`

## Notes

- 어떤 크루든 가입 보장을 단정해서 말하지 않는다.
- 참가비, 페이스 규칙, 모임 시간을 확인 없이 지어내지 않는다.
- 데모 데이터는 오프라인 검증용 자산이다.
- 현재 기본 흐름은 로컬 실행이며, API 모드는 배포 후 확장 단계로 본다.
- 실제 운영에서는 배포된 API 또는 최신 공개 소스를 우선할 수 있다.
