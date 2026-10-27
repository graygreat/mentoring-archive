-- Optional preparation for the Nov 23 independent order lab.
-- Run once after starting a fresh dbBasics session, or after basics.sql.
CREATE TABLE lab_orders (
    id BIGINT PRIMARY KEY,
    label VARCHAR NOT NULL
);
CREATE TABLE lab_order_items (
    id BIGINT PRIMARY KEY,
    order_id BIGINT NOT NULL REFERENCES lab_orders(id),
    name VARCHAR NOT NULL
);
INSERT INTO lab_orders (id, label) VALUES
(201, '주문 1'), (202, '주문 2'), (203, '주문 3');
INSERT INTO lab_order_items (id, order_id, name) VALUES
(301, 201, '노트'), (302, 201, '펜'),
(303, 202, '노트'), (304, 202, '펜'),
(305, 203, '노트'), (306, 203, '펜');

-- An item points to its order. FK does not mean SQL automatically joins tables.
SELECT o.id AS order_id, o.label, i.id AS item_id, i.name
FROM lab_orders o
JOIN lab_order_items i ON i.order_id = o.id
ORDER BY o.id, i.id;
-- 6 result rows, with repeated order information. This is one SQL statement.
