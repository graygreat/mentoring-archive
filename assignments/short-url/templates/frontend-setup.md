# 프론트 기본 설정

| 항목 | 설정 |
| --- | --- |
| 사용 기술 | 순수 HTML·CSS·JavaScript만 사용 |
| 외부 의존성 | 외부 라이브러리·프레임워크·CDN 사용 금지. 프론트 빌드 도구·패키지 설치 없이 진행 |
| 파일 위치 | `src/main/resources/static/` 아래 `index.html`, `styles.css`, `app.js` |
| 실행 | Spring Boot 실행 후 `http://localhost:실제포트/`에서 접속 |
| API 연결 | 같은 origin에서 상대 경로의 `fetch` 사용. 경로·메서드·필드·응답 처리는 본인의 실제 API 명세 준수 |
| AI 활용 | 프롬프트는 본인이 자유롭게 작성. 비밀값·개인정보 입력 금지 |
| 활용 기록 | 사용 프롬프트·직접 수정한 내용·검증 결과를 `short-url/docs/ai-log.md`에 기록 |
