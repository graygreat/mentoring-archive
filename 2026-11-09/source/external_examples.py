# Minimal external GET example for the existing Spring Boot 4.x / Java 17 project.
# Change each package declaration to a package below your own application class.
EXTERNAL_SOURCES = {
'DummyJsonProduct.java': '''package com.example.product;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import java.math.BigDecimal;

@JsonIgnoreProperties(ignoreUnknown = true)
public record DummyJsonProduct(
        Long id,
        String title,
        BigDecimal price,
        String category,
        String thumbnail,
        Integer stock) {
}
''',
'DummyJsonClient.java': '''package com.example.product;

import java.net.http.HttpClient;
import java.time.Duration;
import org.springframework.http.HttpStatus;
import org.springframework.http.client.JdkClientHttpRequestFactory;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClient;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestClientResponseException;
import org.springframework.web.server.ResponseStatusException;

@Component
public class DummyJsonClient {
    private final RestClient restClient;

    public DummyJsonClient() {
        HttpClient httpClient = HttpClient.newBuilder()
                .connectTimeout(Duration.ofSeconds(3))
                .build();
        JdkClientHttpRequestFactory factory =
                new JdkClientHttpRequestFactory(httpClient);
        factory.setReadTimeout(Duration.ofSeconds(5));

        this.restClient = RestClient.builder()
                .baseUrl("https://dummyjson.com")
                .requestFactory(factory)
                .build();
    }

    // Tests can supply a client connected to a local test server.
    DummyJsonClient(RestClient restClient) {
        this.restClient = restClient;
    }

    public DummyJsonProduct findById(long id) {
        if (id <= 0) {
            throw new ResponseStatusException(
                    HttpStatus.BAD_REQUEST, "상품 id는 양수여야 합니다");
        }

        try {
            DummyJsonProduct product = restClient.get()
                    .uri("/products/{id}", id)
                    .retrieve()
                    .body(DummyJsonProduct.class);

            if (product == null) {
                throw new ResponseStatusException(
                        HttpStatus.BAD_GATEWAY, "외부 상품 응답이 비어 있습니다");
            }
            return product;
        } catch (RestClientResponseException exception) {
            if (exception.getStatusCode().value() == 404) {
                throw new ResponseStatusException(
                        HttpStatus.NOT_FOUND, "외부 상품을 찾을 수 없습니다");
            }
            throw new ResponseStatusException(
                    HttpStatus.BAD_GATEWAY, "외부 상품 서버가 오류를 반환했습니다");
        } catch (RestClientException exception) {
            throw new ResponseStatusException(
                    HttpStatus.BAD_GATEWAY, "외부 상품 정보를 가져오지 못했습니다");
        }
    }
}
''',
'ExternalProductExampleController.java': '''package com.example.product;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/examples/external-products")
public class ExternalProductExampleController {
    private final DummyJsonClient client;

    public ExternalProductExampleController(DummyJsonClient client) {
        this.client = client;
    }

    @GetMapping("/{id}")
    public DummyJsonProduct findById(@PathVariable("id") long id) {
        return client.findById(id);
    }
}
''',
}
