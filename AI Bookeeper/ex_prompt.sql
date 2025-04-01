SELECT p.product_name, SUM(s.revenue) AS total_revenue
FROM sales s
JOIN products p ON s.product_id = p.product_id
WHERE strftime('%Y-%m', s.sale_date) = strftime('%Y-%m', 'now')
GROUP BY p.product_name
ORDER BY total_revenue DESC
LIMIT 5;
