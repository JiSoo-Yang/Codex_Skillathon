# Deploying the Demo API

## Goal

Deploy the bundled demo API so the skill can call a stable HTTP endpoint instead of shelling out locally.

## Recommended runtime

- Python 3.11+
- No external packages required for the bundled demo server

## Start command

```bash
python3 running-crew-match/scripts/dev_server.py --host 0.0.0.0 --port ${PORT:-8000}
```

## Health check

```bash
curl http://127.0.0.1:8000/health
```

## Match test

```bash
curl -X POST http://127.0.0.1:8000/match \
  -H 'Content-Type: application/json' \
  -d '{"region":"성수","day":"평일","time":"저녁","level":"초보","goal":"친목","limit":3}'
```

## Deployment notes

- Brev 같은 서비스에서는 `PORT` 환경변수를 우선 사용한다.
- 커스텀 데이터 파일을 쓰고 싶으면 `RUNNING_CREW_MATCH_DATA_PATH` 를 지정한다.
- 현재 서버는 데모용이므로, 실운영 전에는 인증, 로그, 데이터 갱신 정책을 별도로 보강해야 한다.
