# Claude Code 상태줄(statusLine) 설정 정리

작성일: 2026-10-23

## 표시 예시

```
Sonnet 5.5 | 261023_15_claude | main *3 | ctx 63% | $0.43 | 1h23m | +120/-8
```

## 항목 설명

| 항목 | 의미 | 표시 조건 / 색 |
|---|---|---|
| 모델명 | 현재 사용 중인 모델 | 항상 (청록) |
| 폴더명 | 작업 중인 디렉터리 이름 | 항상 (파랑) |
| 브랜치 `*N` | git 브랜치와 변경된 파일 수 | git 저장소 안에서만 (브랜치 초록, 변경 수 노랑) |
| `ctx N%` | 컨텍스트 창 사용률 | 50% 미만 초록, 50~79% 노랑, 80% 이상 빨강 |
| `$0.43` | 세션 누적 비용(USD) | 데이터가 있을 때 |
| `1h23m` | 세션 경과 시간 | 데이터가 있을 때 |
| `+120/-8` | 추가/삭제된 코드 줄 수 | 변경이 있을 때 |

## 관련 파일

- `~/.claude/settings.json`: `statusLine` 항목이 스크립트를 가리킵니다.

  ```json
  "statusLine": { "type": "command", "command": "bash ~/.claude/statusline-command.sh" }
  ```

- `~/.claude/statusline-command.sh`: 상태줄을 만드는 bash 스크립트입니다. Claude Code가 stdin으로 넘겨주는 JSON을 읽습니다. `jq`가 있으면 쓰고, 없으면 `sed`로 파싱합니다. Windows에서는 Git Bash로 실행됩니다.

## 동작 방식

1. Claude Code가 응답이 끝날 때마다 스크립트를 실행하고 세션 정보를 JSON으로 넘깁니다.
2. 스크립트는 모델, 경로, 컨텍스트, 비용, 시간, 줄 수를 꺼냅니다.
3. git 정보는 `git status --porcelain`으로 읽고, 락을 잡지 않도록 `GIT_OPTIONAL_LOCKS=0`을 사용합니다.
4. 값이 없는 항목은 생략해서 줄이 깨지지 않게 합니다.

## 추가로 넣을 수 있는 항목

- 속도 제한(rate limit) 사용량
- effort 레벨, 출력 스타일
- Claude Code 버전
- 항목별 on/off를 위한 환경 변수

## 문제 해결

- **상태줄이 안 보임**: `bash ~/.claude/statusline-command.sh < 샘플.json`으로 직접 실행해 오류를 확인합니다.
- **한 항목만 안 나옴**: 해당 값이 JSON에 아직 없는 경우입니다. `jq` 설치 여부도 확인합니다.
- **상태줄을 끄고 싶음**: `settings.json`에서 `statusLine` 항목을 지웁니다. 스크립트 파일은 남겨도 됩니다.
- **상태줄 설정 후 Shift+Tab/숫자패드가 안 되는 문제**가 있었습니다. 원인이 상태줄인지는 확인되지 않았고, 재발하면 `statusLine`을 빼고 재시작해 비교합니다.
