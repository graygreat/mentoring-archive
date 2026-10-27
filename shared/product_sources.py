"""Independent course examples, not a transcription of the textbook.

Each dictionary contains only files introduced or replaced on that date.
Use assemble_product(day) for a complete reference snapshot.
"""
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[1]
BASE = runpy.run_path(str(ROOT / '2026-11-07/source/code_examples.py'))['SOURCES']
BASE = dict(BASE)
BASE.update(runpy.run_path(str(ROOT / '2026-11-12/source/code_examples.py'))['SOURCES'])

DAY14_SOURCES = {
'ProductRepository.java': '''package com.example.product;

import java.util.List;
import java.util.Optional;

public interface ProductRepository {
    Product save(String name, int price);
    List<Product> findAll();
    Optional<Product> findById(long id);
    Optional<Product> update(long id, String name, int price);
    boolean delete(long id);
}
''',
'MemoryProductRepository.java': '''package com.example.product;

import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;
import org.springframework.stereotype.Repository;

@Repository
public class MemoryProductRepository implements ProductRepository {
    private final Map<Long, Product> store = new ConcurrentHashMap<>();
    private final AtomicLong sequence = new AtomicLong();

    @Override
    public Product save(String name, int price) {
        long id = sequence.incrementAndGet();
        Product product = new Product(id, name, price);
        store.put(id, product);
        return product;
    }

    @Override
    public List<Product> findAll() {
        return store.values().stream()
                .sorted(Comparator.comparingLong(Product::getId))
                .toList();
    }

    @Override
    public Optional<Product> findById(long id) {
        return Optional.ofNullable(store.get(id));
    }

    @Override
    public Optional<Product> update(long id, String name, int price) {
        Product updated = store.computeIfPresent(id,
                (key, previous) -> new Product(key, name, price));
        return Optional.ofNullable(updated);
    }

    @Override
    public boolean delete(long id) {
        return store.remove(id) != null;
    }
}
''',
'ProductService.java': '''package com.example.product;

import java.util.List;
import org.springframework.stereotype.Service;

@Service
public class ProductService {
    private final ProductRepository repository;

    public ProductService(ProductRepository repository) {
        this.repository = repository;
    }

    public Product create(String name, int price) {
        Product checked = new Product(0, name, price);
        return repository.save(checked.getName(), checked.getPrice());
    }

    public List<Product> findAll() {
        return repository.findAll();
    }

    public Product findById(long id) {
        return repository.findById(id)
                .orElseThrow(() -> new ProductNotFoundException(id));
    }

    public Product update(long id, String name, int price) {
        Product checked = new Product(id, name, price);
        return repository.update(id, checked.getName(), checked.getPrice())
                .orElseThrow(() -> new ProductNotFoundException(id));
    }

    public void delete(long id) {
        if (!repository.delete(id)) {
            throw new ProductNotFoundException(id);
        }
    }
}
''',
'ProductController.java': '''package com.example.product;

import java.net.URI;
import java.util.List;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/products")
public class ProductController {
    private final ProductService service;

    public ProductController(ProductService service) {
        this.service = service;
    }

    @PostMapping
    public ResponseEntity<ProductResponse> create(
            @Valid @RequestBody CreateProductRequest request) {
        Product product = service.create(request.getName(), request.getPrice());
        URI location = URI.create("/products/" + product.getId());
        return ResponseEntity.created(location).body(new ProductResponse(product));
    }

    @GetMapping
    public List<ProductResponse> findAll() {
        return service.findAll().stream().map(ProductResponse::new).toList();
    }

    @GetMapping("/{id}")
    public ProductResponse findById(@PathVariable("id") long id) {
        return new ProductResponse(service.findById(id));
    }

    @PutMapping("/{id}")
    public ProductResponse update(@PathVariable("id") long id,
            @Valid @RequestBody CreateProductRequest request) {
        return new ProductResponse(
                service.update(id, request.getName(), request.getPrice()));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable("id") long id) {
        service.delete(id);
        return ResponseEntity.noContent().build();
    }
}
''',
'ProductCrudTest.java': '''package com.example.product;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class ProductCrudTest {
    private final ProductService service =
            new ProductService(new MemoryProductRepository());

    @Test
    void updateKeepsIdAndReplacesValues() {
        Product first = service.create("노트", 3000);
        Product changed = service.update(first.getId(), "  공책  ", 0);
        assertEquals(first.getId(), changed.getId());
        assertEquals("공책", changed.getName());
        assertEquals(0, service.findById(first.getId()).getPrice());
        assertEquals(1, service.findAll().size());
    }

    @Test
    void invalidUpdatePreservesPreviousValues() {
        Product first = service.create("노트", 3000);
        assertThrows(IllegalArgumentException.class,
                () -> service.update(first.getId(), "새 이름", -1));
        assertEquals("노트", service.findById(first.getId()).getName());
        assertEquals(3000, service.findById(first.getId()).getPrice());
    }

    @Test
    void deleteKeepsOtherProductsAndRepeatedDeleteFails() {
        Product first = service.create("노트", 3000);
        Product second = service.create("펜", 1000);
        service.delete(first.getId());
        assertThrows(ProductNotFoundException.class,
                () -> service.findById(first.getId()));
        assertThrows(ProductNotFoundException.class,
                () -> service.delete(first.getId()));
        assertEquals(second.getId(), service.findAll().get(0).getId());
    }

    @Test
    void missingUpdateDoesNotCreateProduct() {
        assertThrows(ProductNotFoundException.class,
                () -> service.update(999, "노트", 3000));
        assertTrue(service.findAll().isEmpty());
    }
}
'''
}

DAY16_SOURCES = {
'ProductEntity.java': '''package com.example.product;

import jakarta.persistence.*;

@Entity
@Table(name = "products")
public class ProductEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @Lob
    @Column(nullable = false)
    private String name;
    @Column(nullable = false)
    private int price;

    protected ProductEntity() {
    }

    public ProductEntity(String name, int price) {
        change(name, price);
    }

    public void change(String name, int price) {
        Product checked = new Product(0, name, price);
        this.name = checked.getName();
        this.price = checked.getPrice();
    }

    public Long getId() { return id; }
    public String getName() { return name; }
    public int getPrice() { return price; }

    public Product toProduct() {
        return new Product(id, name, price);
    }
}
''',
'SpringDataProductRepository.java': '''package com.example.product;

import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

public interface SpringDataProductRepository
        extends JpaRepository<ProductEntity, Long> {
    List<ProductEntity> findAllByOrderByIdAsc();
    List<ProductEntity> findByPriceLessThanEqualOrderByIdAsc(int maxPrice);

    @Query("select p from ProductEntity p where p.price <= :maxPrice order by p.id")
    List<ProductEntity> findAffordable(@Param("maxPrice") int maxPrice);
}
''',
'ProductJpaRepositoryTest.java': '''package com.example.product;

import jakarta.persistence.EntityManager;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTest;
import static org.junit.jupiter.api.Assertions.*;

@DataJpaTest
class ProductJpaRepositoryTest {
    @Autowired
    private SpringDataProductRepository repository;
    @Autowired
    private EntityManager entityManager;

    @Test
    void persistAndReloadAfterClear() {
        ProductEntity saved = repository.saveAndFlush(new ProductEntity("노트", 3000));
        Long id = saved.getId();
        entityManager.clear();
        ProductEntity found = repository.findById(id).orElseThrow();
        assertEquals("노트", found.getName());
        assertNotSame(saved, found);
    }

    @Test
    void derivedQueryAndJpqlHaveSameBoundary() {
        repository.save(new ProductEntity("노트", 3000));
        repository.save(new ProductEntity("무료", 0));
        repository.save(new ProductEntity("펜", 1000));
        entityManager.flush();
        entityManager.clear();
        var derived = repository.findByPriceLessThanEqualOrderByIdAsc(1000);
        var jpql = repository.findAffordable(1000);
        assertEquals(2, derived.size());
        assertEquals(derived.stream().map(ProductEntity::getId).toList(),
                jpql.stream().map(ProductEntity::getId).toList());
    }

    @Test
    void longNamePreservesExistingApiContract() {
        String name = "가".repeat(300);
        Long id = repository.saveAndFlush(new ProductEntity(name, 0)).getId();
        entityManager.clear();
        assertEquals(name, repository.findById(id).orElseThrow().getName());
    }

    @Test
    void managedEntityChangesAreFlushedWithoutSave() {
        ProductEntity saved = repository.saveAndFlush(new ProductEntity("노트", 3000));
        Long id = saved.getId();
        entityManager.clear();
        repository.findById(id).orElseThrow().change("공책", 2000);
        entityManager.flush();
        entityManager.clear();
        assertEquals(2000, repository.findById(id).orElseThrow().getPrice());
    }
}
'''
}
DAY16_PROPERTIES = '''spring.datasource.url=jdbc:h2:file:./data/products
spring.datasource.username=sa
spring.datasource.password=
spring.jpa.hibernate.ddl-auto=update
spring.jpa.open-in-view=false
spring.jpa.show-sql=true
'''
TEST_PROPERTIES = '''spring.datasource.url=jdbc:h2:mem:product-tests;DB_CLOSE_DELAY=-1
spring.datasource.username=sa
spring.datasource.password=
spring.jpa.hibernate.ddl-auto=create-drop
spring.jpa.open-in-view=false
'''
JPA_DEPENDENCIES = '''implementation 'org.springframework.boot:spring-boot-starter-data-jpa'
runtimeOnly 'com.h2database:h2'
testImplementation 'org.springframework.boot:spring-boot-starter-data-jpa-test'
'''

DAY19_SOURCES = {
'MemoryProductRepository.java': DAY14_SOURCES['MemoryProductRepository.java'].replace(
    'import org.springframework.stereotype.Repository;\n', '').replace('@Repository\n', ''),
'ProductService.java': DAY14_SOURCES['ProductService.java'].replace(
    'import org.springframework.stereotype.Service;',
    'import org.springframework.stereotype.Service;\nimport org.springframework.transaction.annotation.Transactional;'
).replace('@Service\n', '@Service\n@Transactional\n').replace(
    '    public List<Product> findAll()', '    @Transactional(readOnly = true)\n    public List<Product> findAll()'
).replace('    public Product findById(', '    @Transactional(readOnly = true)\n    public Product findById('),
'JpaProductRepository.java': '''package com.example.product;

import java.util.List;
import java.util.Optional;
import org.springframework.stereotype.Repository;

@Repository
public class JpaProductRepository implements ProductRepository {
    private final SpringDataProductRepository data;

    public JpaProductRepository(SpringDataProductRepository data) {
        this.data = data;
    }

    @Override
    public Product save(String name, int price) {
        return data.save(new ProductEntity(name, price)).toProduct();
    }

    @Override
    public List<Product> findAll() {
        return data.findAllByOrderByIdAsc().stream()
                .map(ProductEntity::toProduct).toList();
    }

    @Override
    public Optional<Product> findById(long id) {
        return data.findById(id).map(ProductEntity::toProduct);
    }

    @Override
    public Optional<Product> update(long id, String name, int price) {
        return data.findById(id).map(entity -> {
            entity.change(name, price);
            return entity.toProduct();
        });
    }

    @Override
    public boolean delete(long id) {
        Optional<ProductEntity> found = data.findById(id);
        if (found.isEmpty()) {
            return false;
        }
        data.delete(found.get());
        return true;
    }
}
''',
'ProductJpaMigrationTest.java': '''package com.example.product;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.NONE)
class ProductJpaMigrationTest {
    @Autowired
    private ProductService service;

    @Test
    void serviceUpdateCommitsAndInvalidUpdatePreservesData() {
        Product saved = service.create("노트", 3000);
        try {
            service.update(saved.getId(), "공책", 2000);
            assertEquals(2000, service.findById(saved.getId()).getPrice());
            assertThrows(IllegalArgumentException.class,
                    () -> service.update(saved.getId(), "변경 금지", -1));
            Product found = service.findById(saved.getId());
            assertEquals("공책", found.getName());
            assertEquals(2000, found.getPrice());
        } finally {
            service.delete(saved.getId());
        }
        assertThrows(ProductNotFoundException.class,
                () -> service.findById(saved.getId()));
    }
}
'''
}

def assemble_product(day):
    result = dict(BASE)
    result.update(DAY14_SOURCES)
    if day >= 16:
        result.update(DAY16_SOURCES)
    if day >= 19:
        result.update(DAY19_SOURCES)
    return result
