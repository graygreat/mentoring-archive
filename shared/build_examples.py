"""Assemble reproducible course reference projects from the slide source dictionaries.

Usage: python3 shared/build_examples.py --output /tmp/course-examples \
  --wrapper-from /path/to/an/official/Initializr/project
The Gradle Wrapper is copied unchanged; dependency versions are managed by Boot.
"""
from pathlib import Path
import argparse
import json
import shutil
import zipfile
from product_sources import assemble_product, DAY16_PROPERTIES, TEST_PROPERTIES
from order_sources import ORDER_SOURCES, ORDER_PROPERTIES

GRADLE_BASE = '''plugins {
    id 'java'
    id 'org.springframework.boot' version '4.1.2'
    id 'io.spring.dependency-management' version '1.1.7'
}
group = 'com.example'
version = '0.0.1-SNAPSHOT'
java { toolchain { languageVersion = JavaLanguageVersion.of(17) } }
repositories { mavenCentral() }
dependencies {
%s
}
tasks.named('test') { useJUnitPlatform() }
'''
PRODUCT_DEPS = '''    implementation 'org.springframework.boot:spring-boot-starter-webmvc'
    implementation 'org.springframework.boot:spring-boot-starter-validation'
    implementation 'org.springframework.boot:spring-boot-starter-aspectj'
    testImplementation 'org.springframework.boot:spring-boot-starter-test'
    testRuntimeOnly 'org.junit.platform:junit-platform-launcher' '''
JPA_DEPS = '''
    implementation 'org.springframework.boot:spring-boot-starter-data-jpa'
    runtimeOnly 'com.h2database:h2'
    testImplementation 'org.springframework.boot:spring-boot-starter-data-jpa-test' '''


def project(target, wrapper, sources, package, jpa=False, order=False):
    if target.exists():
        raise FileExistsError('Choose a fresh output directory: ' + str(target))
    target.mkdir(parents=True)
    for name in ['gradlew', 'gradlew.bat']:
        shutil.copy2(wrapper / name, target / name)
    shutil.copytree(wrapper / 'gradle', target / 'gradle')
    (target / 'settings.gradle').write_text("rootProject.name = '%s'\n" % target.name)
    deps = JPA_DEPS if order else PRODUCT_DEPS + (JPA_DEPS if jpa else '')
    if order:
        deps += "\n    testImplementation 'org.springframework.boot:spring-boot-starter-test'\n    testRuntimeOnly 'org.junit.platform:junit-platform-launcher'"
    (target / 'build.gradle').write_text(GRADLE_BASE % deps)
    (target / '.gitignore').write_text('.gradle/\nbuild/\ndata/\n.idea/\n*.iml\n.env\n')
    for name, source in sources.items():
        kind = 'test' if name.endswith('Test.java') else 'main'
        p = target / 'src' / kind / 'java' / Path(*package.split('.')) / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(source)
    if not order:
        p = target / 'src/test/java/com/example/product/ProductApplicationTests.java'
        p.write_text('''package com.example.product;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class ProductApplicationTests {
    @Test
    void contextLoads() {
    }
}
''')
    if jpa or order:
        p = target / 'src/main/resources/application.properties'
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(ORDER_PROPERTIES if order else DAY16_PROPERTIES)
        p = target / 'src/test/resources/application.properties'
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(ORDER_PROPERTIES if order else TEST_PROPERTIES)
    return target


def pack(source, dest, top_name, intro):
    dest.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(dest, 'w', zipfile.ZIP_DEFLATED) as z:
        for p in sorted(source.rglob('*')):
            relative = p.relative_to(source)
            if p.is_file() and not any(x in relative.parts for x in ['build', '.gradle', 'data']):
                z.write(p, str(Path(top_name) / relative))
        z.writestr(top_name + '/START-HERE.md', intro)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--wrapper-from', type=Path, required=True)
    parser.add_argument('--package-assets', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    for day in [14, 16, 19]:
        project(args.output / ('product-api-' + str(day)), args.wrapper_from,
                assemble_product(day), 'com.example.product', jpa=day >= 16)
    project(args.output / 'order-query-lab', args.wrapper_from,
            ORDER_SOURCES, 'com.example.orderlab', jpa=True, order=True)
    if args.package_assets:
        pack(args.output / 'product-api-16', root / '2026-11-19/assets/product-api-start.zip',
             'product-api', '''# 19일 복구용 출발 코드 · 16일 완료 상태

새 독립 저장소를 만들지 않습니다. 본인 product-api를 먼저 커밋/백업하세요.
필요한 파일을 비교해 복구하고 선택 검색 등 본인 기능을 보존합니다.
이 ZIP에는 중첩 .git, build, .gradle, DB 파일이 없습니다.

Java 17 / Spring Boot 4.1.2 / Gradle Wrapper 포함.
./gradlew test (Windows: .\\gradlew.bat test)
./gradlew bootRun (Windows: .\\gradlew.bat bootRun)

현재 API는 MemoryProductRepository를 사용합니다. Entity/Repository 테스트가
통과해도 API가 DB를 쓰는 것은 아닙니다. 19일 작업지에 따라 전환하세요.
./data DB 파일은 공유하지 않습니다. 테스트는 별도 메모리 DB를 사용합니다.
H2는 로컬 수업용입니다. 공개 운영 환경 설정이 아닙니다.
''')
        pack(args.output / 'order-query-lab', root / '2026-11-23/assets/order-query-lab.zip',
             'order-query-lab', '''# 23일 최소 주문 조회 실습 · 참고 구현 포함

책 주문 API 정답이 아닌 독립 학습 예제이며 전체 주문 CRUD는 요구하지 않습니다.
Java 17 / Spring Boot 4.1.2 / Gradle Wrapper 포함.
학습 저장소 안 order-query-lab/에 둡니다. 중첩 git init은 하지 않습니다.

1. 먼저 findAllByOrderByIdAsc로 읽고 항목 수를 더할 때 SQL 수를 예상합니다.
2. ./gradlew test --tests '*OrderQueryTest.lazyCollectionsProduceOnePlusNQueries' --info --rerun-tasks
3. 참고 findAllWithItems/@Query를 보기 전에 본인 개선안을 작성합니다.
4. ./gradlew test --tests '*OrderQueryTest' --info --rerun-tasks 후 SQL과 결과를 비교합니다.
5. ./gradlew test --tests '*PersistenceContextTest' --info --rerun-tasks
SQL 출력은 --info로 표시하고 --rerun-tasks로 반복 관찰을 보장합니다.
출력이 길면 build/reports/tests/test/index.html에서 해당 클래스의 Standard output을 확인합니다.
Windows는 ./gradlew 대신 .\\gradlew.bat 사용.

참고답안 fetch join과 검증 테스트가 포함됩니다. 메서드와 해당 테스트를 읽고
이유를 설명한 뒤 새 브랜치에서 직접 같은 동작을 구현하는 연습을 합니다.
3주문/6항목, seed flush/clear 후 초기화한 통계에서 기본4회→개선1회입니다.
이 수치는 이 실습 조건의 결과이며 모든 서비스의 보편적 수치가 아닙니다.
''')
    print(json.dumps({'output': str(args.output), 'assets': args.package_assets}))

if __name__ == '__main__':
    main()
