# Only files added or changed today. Previous project files remain in place.
SOURCES = {
'CreateProductRequest.java': '''package com.example.product;

public class CreateProductRequest {
    private String name;
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
            @RequestBody CreateProductRequest request) {
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
}
