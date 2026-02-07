

SELECT AVG(c.age) AS average_age
FROM customers c
WHERE c.customer_key IN (
    SELECT DISTINCT p.customer_key
    FROM purchases p
    INNER JOIN products pr ON p.product_key = pr.product_key
    WHERE pr.name = 'Smartwatch'
      AND SUBSTR(p.date, 1, 4) = '2024'
);
