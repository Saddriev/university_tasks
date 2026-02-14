
SELECT c.name
FROM customers c
WHERE c.customer_key IN (
    SELECT p.customer_key
    FROM purchases p
    INNER JOIN products pr ON p.product_key = pr.product_key
    WHERE pr.name = 'Laptop'
      AND SUBSTR(p.date, 1, 7) = '2024-03'
)
AND c.customer_key IN (
    SELECT p.customer_key
    FROM purchases p
    INNER JOIN products pr ON p.product_key = pr.product_key
    WHERE pr.name = 'Monitor'
      AND SUBSTR(p.date, 1, 7) = '2024-03'
)
ORDER BY c.name;
