-- H2 learning sandbox only. Run once per fresh dbBasics session.
-- lab_* tables are separate from the product API tables.
-- IDs are assigned manually in this paper-table exercise, not in the JPA API.
CREATE TABLE lab_products (
    id BIGINT PRIMARY KEY,
    name VARCHAR NOT NULL,
    price INTEGER NOT NULL CHECK (price >= 0)
);

INSERT INTO lab_products (id, name, price) VALUES (101, '노트', 3000);
INSERT INTO lab_products (id, name, price) VALUES (102, '펜', 1000);
INSERT INTO lab_products (id, name, price) VALUES (103, '무료', 0);
SELECT id, name, price FROM lab_products ORDER BY id;

-- Predict: pen and free sample, ordered by id.
SELECT id, name, price FROM lab_products
WHERE price <= 1000 ORDER BY id;

-- Change one row. WHERE identifies the target; it is not optional for this task.
UPDATE lab_products SET name = '공책', price = 2000 WHERE id = 101;
SELECT id, name, price FROM lab_products WHERE id = 101;

-- One transaction: observe a temporary change, then roll it back.
SET AUTOCOMMIT FALSE;
UPDATE lab_products SET price = 900 WHERE id = 101;
SELECT id, name, price FROM lab_products WHERE id = 101;
ROLLBACK;
SELECT id, name, price FROM lab_products WHERE id = 101;

-- One transaction: commit the change. This session is still a memory DB.
UPDATE lab_products SET price = 1500 WHERE id = 101;
COMMIT;
SET AUTOCOMMIT TRUE;
SELECT id, name, price FROM lab_products WHERE id = 101;

DELETE FROM lab_products WHERE id = 102;
SELECT id, name, price FROM lab_products ORDER BY id;
-- Final rows: (101, 공책, 1500), (103, 무료, 0).
-- COMMIT does not make an in-memory database survive closing the process.
