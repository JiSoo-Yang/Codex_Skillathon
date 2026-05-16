---
name: running-crew-match
description: Find and recommend Korean running crews based on region, schedule, skill level, and running goals using public community information.
---

# Running Crew Match

## What this skill does

사용자의 지역, 선호 요일과 시간대, 러닝 수준, 목표를 바탕으로 한국 내 러닝 크루나 정기 러닝 모임 후보를 찾아 추천한다.

이 스킬은 가입 확정이나 자동 신청이 아니라, 공개 정보를 바탕으로 한 후보 탐색과 매칭 지원에 초점을 둔다.

## When to use

- "서울에서 초보자 러닝 크루 찾아줘"
- "성수 근처 평일 저녁 러닝 모임 추천해줘"
- "잠실에서 10k 준비하는 사람들 많은 크루 있을까?"
- "한강 근처 아침 러닝 크루 후보 알려줘"

## When not to use

- 참가 신청을 자동으로 완료해야 하는 경우
- 비공개 커뮤니티나 로그인 필수 정보에만 의존해야 하는 경우
- 실시간 위치 추적이나 안전 모니터링이 필요한 경우

## Inputs

- `region`: 지역 또는 세부 장소
- `day`: 선호 요일
- `time`: 선호 시간대
- `level`: 초보, 중급, 기록 지향 등 러닝 수준
- `goal`: 다이어트, 친목, 5k, 10k, 하프, 마라톤 준비 등
- `notes`: 혼자 뛰기 부담, 여성 중심 선호, 소규모 선호 같은 추가 조건

사용자가 일부 정보만 주면 가벼운 기본값을 추론해도 되지만, 무엇을 가정했는지는 답변에 짧게 밝힌다.

## Workflow

### 1. Match profile 정리

사용자의 지역, 일정, 러닝 수준, 목표를 먼저 정리한다.

핵심 정보가 빠졌다면 추천 품질에 가장 큰 영향을 주는 항목만 최소한으로 확인한다.

### 2. 공개 후보 탐색

아래처럼 공개적으로 확인 가능한 러닝 크루 정보를 우선 찾는다.

- Instagram profiles or posts
- Naver cafe or blog posts
- Meetup-style community pages
- Open Kakao community 안내 pages
- Public event pages for regular group runs

최근 활동 흔적, 지역 정보, 참여 방식이 보이는 소스를 우선한다.

### 3. 보수적으로 필터링

활동 중으로 보이고 사용자 조건과 맞는 후보만 남긴다.

우선순위는 다음과 같다.

- matching region
- matching day or time
- beginner friendliness or pace fit
- recent public activity
- clear participation instructions

### 4. 짧은 추천 리스트 제시

가능하면 3~5개의 후보를 추천한다.

각 후보마다 아래를 짧게 정리한다.

- crew or group name
- main area
- likely schedule
- fit for the user's goal or level
- why it matches
- source link

### 5. 애매한 경우 정직하게 처리

강한 후보가 없으면 억지로 단정하지 말고, 인접 지역이나 비슷한 시간대, 더 넓은 초보자용 옵션을 대안으로 제시한다.

## Output style

답변은 짧고 실용적으로 유지한다.

가능하면 정보의 최신성을 함께 적는다. 예:

- "최근 공개 활동이 확인된 편"
- "일정 정보가 오래되어 추가 확인이 필요함"

마지막에는 "이 후보부터 확인해보면 좋다" 같은 짧은 다음 행동을 덧붙인다.

## Done when

- 사용자가 검토할 만한 러닝 크루 후보 목록을 받았다
- 각 후보에 추천 이유와 출처가 붙어 있다
- 확인된 사실과 추론을 구분했다
- 오래되었거나 불확실한 정보는 명시했다

## Failure modes

- 요청 지역이 너무 넓거나 모호한 경우
- 공개 정보가 오래되었거나 매우 적은 경우
- 활동은 보이지만 일정 정보가 불명확한 경우
- 사용자 조건이 너무 좁아 공개 후보가 거의 없는 경우

## Notes

- 어떤 크루든 가입 보장을 단정해서 말하지 않는다.
- 페이스 규칙, 모임 시간, 참가비를 확인 없이 지어내지 않는다.
- 이 스킬의 1차 목적은 추천과 탐색 지원이다.
