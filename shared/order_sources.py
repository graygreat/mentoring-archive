"""Minimal independent JPA learning lab; not the textbook order API solution."""
ORDER_SOURCES = {
'OrderLabApplication.java': '''package com.example.orderlab;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class OrderLabApplication {
    public static void main(String[] args) {
        SpringApplication.run(OrderLabApplication.class, args);
    }
}
''',
'PurchaseOrder.java': '''package com.example.orderlab;

import java.util.ArrayList;
import java.util.List;
import jakarta.persistence.*;

@Entity
@Table(name = "purchase_orders")
public class PurchaseOrder {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String label;
    @OneToMany(fetch = FetchType.LAZY, cascade = CascadeType.ALL)
    @JoinColumn(name = "order_id")
    private List<OrderItem> items = new ArrayList<>();

    protected PurchaseOrder() {
    }

    public PurchaseOrder(String label) {
        this.label = label;
    }

    public void addItem(String name) {
        items.add(new OrderItem(name));
    }

    public void rename(String label) { this.label = label; }
    public Long getId() { return id; }
    public String getLabel() { return label; }
    public List<OrderItem> getItems() { return items; }
}
''',
'OrderItem.java': '''package com.example.orderlab;

import jakarta.persistence.*;

@Entity
@Table(name = "order_items")
public class OrderItem {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String name;

    protected OrderItem() {
    }

    public OrderItem(String name) {
        this.name = name;
    }

    public Long getId() { return id; }
    public String getName() { return name; }
}
''',
'OrderQueryRepository.java': '''package com.example.orderlab;

import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

public interface OrderQueryRepository extends JpaRepository<PurchaseOrder, Long> {
    List<PurchaseOrder> findAllByOrderByIdAsc();

    @Query("select distinct o from PurchaseOrder o left join fetch o.items order by o.id")
    List<PurchaseOrder> findAllWithItems();
}
''',
'OrderQueryTest.java': '''package com.example.orderlab;

import jakarta.persistence.EntityManager;
import org.hibernate.SessionFactory;
import org.hibernate.stat.Statistics;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTest;
import static org.junit.jupiter.api.Assertions.*;

@DataJpaTest(properties = "spring.jpa.properties.hibernate.generate_statistics=true")
class OrderQueryTest {
    @Autowired
    private OrderQueryRepository repository;
    @Autowired
    private EntityManager entityManager;
    private Statistics statistics;

    @BeforeEach
    void seedAndClear() {
        for (int i = 1; i <= 3; i++) {
            PurchaseOrder order = new PurchaseOrder("주문 " + i);
            order.addItem("노트");
            order.addItem("펜");
            repository.save(order);
        }
        entityManager.flush();
        entityManager.clear();
        statistics = entityManager.getEntityManagerFactory()
                .unwrap(SessionFactory.class).getStatistics();
        statistics.clear();
    }

    @Test
    void lazyCollectionsProduceOnePlusNQueries() {
        var orders = repository.findAllByOrderByIdAsc();
        int totalItems = orders.stream().mapToInt(o -> o.getItems().size()).sum();
        long selects = statistics.getPrepareStatementCount();
        assertEquals(3, orders.size());
        assertEquals(6, totalItems);
        assertEquals(java.util.List.of("주문 1", "주문 2", "주문 3"),
                orders.stream().map(PurchaseOrder::getLabel).toList());
        assertTrue(orders.stream().allMatch(order ->
                order.getItems().stream().map(OrderItem::getName).sorted().toList()
                        .equals(java.util.List.of("노트", "펜"))));
        assertEquals(4, selects);
        System.out.println("lazy-select-count=" + selects);
    }

    @Test
    void fetchJoinLoadsSameResultInOneQuery() {
        var orders = repository.findAllWithItems();
        int totalItems = orders.stream().mapToInt(o -> o.getItems().size()).sum();
        long selects = statistics.getPrepareStatementCount();
        assertEquals(3, orders.size());
        assertEquals(6, totalItems);
        assertEquals(java.util.List.of("주문 1", "주문 2", "주문 3"),
                orders.stream().map(PurchaseOrder::getLabel).toList());
        assertTrue(orders.stream().allMatch(order ->
                order.getItems().stream().map(OrderItem::getName).sorted().toList()
                        .equals(java.util.List.of("노트", "펜"))));
        assertEquals(1, selects);
        System.out.println("fetch-select-count=" + selects);
    }
}
''',
'PersistenceContextTest.java': '''package com.example.orderlab;

import jakarta.persistence.EntityManager;
import org.hibernate.Hibernate;
import org.hibernate.LazyInitializationException;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTest;
import org.springframework.transaction.PlatformTransactionManager;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.transaction.support.TransactionTemplate;
import static org.junit.jupiter.api.Assertions.*;

@DataJpaTest
class PersistenceContextTest {
    @Autowired
    private OrderQueryRepository repository;
    @Autowired
    private EntityManager entityManager;
    @Autowired
    private PlatformTransactionManager transactionManager;

    @Test
    void sameContextKeepsIdentityAndFlushWritesChanges() {
        PurchaseOrder saved = repository.saveAndFlush(new PurchaseOrder("처음"));
        Long id = saved.getId();
        entityManager.clear();
        PurchaseOrder first = repository.findById(id).orElseThrow();
        assertSame(first, repository.findById(id).orElseThrow());
        first.rename("변경");
        entityManager.flush();
        entityManager.clear();
        PurchaseOrder reloaded = repository.findById(id).orElseThrow();
        assertNotSame(first, reloaded);
        assertEquals("변경", reloaded.getLabel());
    }

    @Test
    @Transactional(propagation = Propagation.NOT_SUPPORTED)
    void uninitializedCollectionCannotLoadAfterContextCloses() {
        TransactionTemplate tx = new TransactionTemplate(transactionManager);
        Long id = tx.execute(status -> {
            PurchaseOrder order = new PurchaseOrder("분리 실험");
            order.addItem("노트");
            return repository.saveAndFlush(order).getId();
        });
        try {
            PurchaseOrder detached = tx.execute(status ->
                    repository.findById(id).orElseThrow());
            assertFalse(Hibernate.isInitialized(detached.getItems()));
            assertThrows(LazyInitializationException.class,
                    () -> detached.getItems().size());
        } finally {
            tx.executeWithoutResult(status -> repository.deleteById(id));
        }
    }
}
'''
}
ORDER_PROPERTIES = '''spring.datasource.url=jdbc:h2:mem:order-lab;DB_CLOSE_DELAY=-1
spring.datasource.username=sa
spring.datasource.password=
spring.jpa.hibernate.ddl-auto=create-drop
spring.jpa.open-in-view=false
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.generate_statistics=true
'''
