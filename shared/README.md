# 강의 예제 원본과 실행 검증

교재의 상품 관리 주제를 적용한 독립 수업 예제입니다. 교재 본문·정답을 옮긴 코드가 아닙니다. 실제 교재의 요구와 다른 수업 정책은 각 날짜 자료에서 구분합니다.

- `product_sources.py`: 12일 정상/오류 API에서 14일 CRUD, 16일 JPA 기초, 19일 저장소 전환까지의 증분 Java 원본.
- `order_sources.py`: 23일 독립 주문 조회 실험. 전체 주문 API가 아닌 연관관계·영속성 컨텍스트·지연 로딩·N+1 관찰용입니다.
- `build_examples.py`: 공식 Initializr 프로젝트의 Gradle Wrapper를 그대로 복사해 날짜별 참조 프로젝트와 배포 ZIP을 조립합니다.
- `rehearse_http.py`: 빌드된 임시 프로젝트에서 HTTP 계약과 서버 재시작 후 저장 상태를 확인합니다. 18114/18116/18119 포트를 사용하고 시작한 프로세스를 정상 종료합니다.

## 재현

Python 3, Java 17, 공식 Initializr에서 생성한 Gradle 프로젝트의 Wrapper가 필요합니다. 다음 경로는 본인 환경에 맞게 지정합니다. 출력 폴더는 새 경로여야 하며 기존 프로젝트를 덮어쓰지 않습니다.

```sh
python3 shared/build_examples.py --output /tmp/course-examples \
  --wrapper-from /path/to/initializr-project
```

생성된 각 `product-api-14`, `product-api-16`, `product-api-19`, `order-query-lab` 폴더에서 `./gradlew clean build`를 실행합니다. Windows PowerShell에서는 `.\gradlew.bat clean build`를 사용합니다. `JAVA_HOME`은 Java 17로 설정합니다. 이후 저장소 루트에서:

```sh
python3 shared/rehearse_http.py --projects /tmp/course-examples
```

`--package-assets`는 검토된 참조 코드를 19일·23일 ZIP에 게시할 때만 조립 명령에 추가합니다. 학생은 본인 저장소를 먼저 커밋하고 ZIP과 비교합니다. 복구본으로 기존 코드·DB를 덮어쓰지 않습니다.

## 검증 결과 · 2026-10-27

Java 17 / Spring Boot 4.1.2 / Gradle Wrapper 9.8.2 / H2에서 실행했습니다.

| 단계 | 자동 테스트 | HTTP·재시작 확인 |
|---|---:|---:|
| 14일 메모리 CRUD | 9개 통과 | 43개 통과 |
| 16일 JPA 저장소 연습, API는 메모리 유지 | 13개 통과 | 43개 통과 |
| 19일 JPA 저장소로 API 전환 | 14개 통과 | 46개 통과 |
| 23일 독립 주문 조회 실험 | 4개 통과 | 동일한 주문·항목 내용, SELECT 4회 → 1회 |

확인 범위에는 생성/수정/삭제/조회, 400/404, 거부된 요청 후 원본 보존, 300자 이름, 실제 id와 Location, 재시작에 따른 메모리 초기화와 파일 DB 보존·삭제 반영이 포함됩니다. 테스트는 별도 메모리 DB를 사용합니다. N+1 횟수는 3주문·각2항목, seed 후 flush/clear 및 통계 초기화 조건에서 측정한 결과입니다. 모든 서비스에 같은 SQL 수가 나온다는 뜻은 아닙니다.

실행 예제와 H2 설정은 로컬 수업용입니다. 운영 서비스의 인증·인가·DB 설정을 대신하지 않습니다. 단축 URL 과제의 학생 답안이나 AI 생성 프론트 결과는 별도 검증 대상입니다.

## 공식 문서

- [Spring Boot 테스트와 JPA slice](https://docs.spring.io/spring-boot/reference/testing/spring-boot-applications.html)
- [Spring Data JPA 쿼리 메서드·JPQL](https://docs.spring.io/spring-data/jpa/reference/jpa/query-methods.html)
- [Hibernate ORM 영속성·연관관계·조회](https://docs.hibernate.org/orm/current/userguide/html_single/)

## DB·JPA 입문 보충

[DB 기초 화면](db-basics/) · [DB 멘티 작업지](db-basics/STUDENT-WORKSHEET.md) · [16일 첫 JPA 작업지](../2026-11-16/BEGINNER-WORKSHEET.md) · [23일 SQL·지연 로딩 작업지](../2026-11-23/BEGINNER-WORKSHEET.md)

독립 H2 메모리 SQL 연습은 기존 상품 API의 설정·Java·데이터를 바꾸지 않습니다. DB 기초 페이지 생성에는 작성 도구 markdown-it-py가 필요하며 `python3 shared/db-basics/build.py`로 HTML을 재생성합니다.
