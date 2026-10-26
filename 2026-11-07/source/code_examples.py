# Full reference code behind the read-only code viewer. Students create their own project.
SOURCES = {
'ProductApplication.java': '''package com.example.product;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class ProductApplication {
    public static void main(String[] args) {
        SpringApplication.run(ProductApplication.class, args);
    }
}
''',
'Product.java': '''package com.example.product;

public class Product {
    private final long id;
    private final String name;
    private final int price;

    public Product(long id, String name, int price) {
        if (name == null || name.isBlank()) {
            throw new IllegalArgumentException("상품명은 필수입니다");
        }
        if (price < 0) {
            throw new IllegalArgumentException("가격은 0 이상이어야 합니다");
        }
        this.id = id;
        this.name = name.strip();
        this.price = price;
    }

    public long getId() { return id; }
    public String getName() { return name; }
    public int getPrice() { return price; }
}
''',
'ProductRepository.java': '''package com.example.product;

import java.util.List;
import java.util.Optional;

public interface ProductRepository {
    Product save(String name, int price);
    List<Product> findAll();
    Optional<Product> findById(long id);
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
}
''',
'ProductNotFoundException.java': '''package com.example.product;

public class ProductNotFoundException extends RuntimeException {
    public ProductNotFoundException(long id) {
        super("상품을 찾을 수 없습니다: " + id);
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
        return repository.save(name, price);
    }

    public List<Product> findAll() {
        return repository.findAll();
    }

    public Product findById(long id) {
        return repository.findById(id)
                .orElseThrow(() -> new ProductNotFoundException(id));
    }
}
''',
'ProductServiceTest.java': '''package com.example.product;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class ProductServiceTest {
    private final ProductService service =
            new ProductService(new MemoryProductRepository());

    @Test
    void createAndFind() {
        Product saved = service.create("노트", 3000);
        assertEquals("노트", service.findById(saved.getId()).getName());
        assertEquals(1, service.findAll().size());
    }

    @Test
    void rejectInvalidPrice() {
        assertThrows(IllegalArgumentException.class,
                () -> service.create("노트", -1));
        assertTrue(service.findAll().isEmpty());
    }

    @Test
    void rejectMissingProduct() {
        assertThrows(ProductNotFoundException.class,
                () -> service.findById(999));
    }
}
''',
'TimingAspect.java': '''package com.example.product;

import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.springframework.stereotype.Component;

@Aspect
@Component
public class TimingAspect {
    @Around("execution(* com.example.product.ProductService.*(..))")
    public Object measure(ProceedingJoinPoint joinPoint) throws Throwable {
        long started = System.nanoTime();
        try {
            return joinPoint.proceed();
        } finally {
            long elapsedMs = (System.nanoTime() - started) / 1_000_000;
            System.out.println(joinPoint.getSignature().getName()
                    + " : " + elapsedMs + "ms");
        }
    }
}
''',
'CreateProductRequest.java': '''package com.example.product;

import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

public class CreateProductRequest {
    @NotBlank(message = "상품명은 필수입니다")
    private String name;
    @NotNull(message = "가격은 필수입니다")
    @Min(value = 0, message = "가격은 0 이상이어야 합니다")
    private Integer price;

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public Integer getPrice() { return price; }
    public void setPrice(Integer price) { this.price = price; }
}
''',
'ProductResponse.java': '''package com.example.product;

public class ProductResponse {
    private final long id;
    private final String name;
    private final int price;

    public ProductResponse(Product product) {
        this.id = product.getId();
        this.name = product.getName();
        this.price = product.getPrice();
    }

    public long getId() { return id; }
    public String getName() { return name; }
    public int getPrice() { return price; }
}
''',
'ProductController.java': '''package com.example.product;

import java.net.URI;
import java.util.List;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

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
}
''',
'ApiExceptionHandler.java': '''package com.example.product;

import java.util.Map;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class ApiExceptionHandler {
    @ExceptionHandler(ProductNotFoundException.class)
    public ResponseEntity<Map<String, String>> notFound(ProductNotFoundException ex) {
        return ResponseEntity.status(HttpStatus.NOT_FOUND)
                .body(Map.of("message", ex.getMessage()));
    }

    @ExceptionHandler({MethodArgumentNotValidException.class,
            HttpMessageNotReadableException.class})
    public ResponseEntity<Map<String, String>> invalidInput(Exception ex) {
        return ResponseEntity.badRequest()
                .body(Map.of("message", "요청값을 확인하세요"));
    }

    @ExceptionHandler(IllegalArgumentException.class)
    public ResponseEntity<Map<String, String>> invalidValue(IllegalArgumentException ex) {
        return ResponseEntity.badRequest()
                .body(Map.of("message", ex.getMessage()));
    }
}
'''
}

SOURCES['ProductWiringTest.java'] = """package com.example.product;

import org.junit.jupiter.api.Test;
import org.springframework.aop.support.AopUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.NONE)
class ProductWiringTest {
    @Autowired
    private ProductService service;

    @Test
    void injectedServiceUsesAopProxy() {
        assertTrue(AopUtils.isAopProxy(service));
        Product saved = service.create("연결 확인", 3000);
        Product found = service.findById(saved.getId());
        assertEquals("연결 확인", found.getName());
        assertEquals(3000, found.getPrice());
        assertTrue(service.findAll().stream()
                .anyMatch(product -> product.getId() == saved.getId()));
    }
}
"""
