-- 1. Overall Equipment Effectiveness (OEE)
SELECT
    machine_id,
    AVG((planned_production_time - downtime_minutes) / planned_production_time) * 100 AS availability_percentage,
    AVG(ideal_cycle_time * total_pieces) * 100 AS quality_percentage,
    AVG((planned_prodcution_time - downtime_minutes) / planned_production_time)
    * AVG((ideaml_cycle_time * total_pieces) / operating_time)
    * AVG(good_pieces / total_pieces) * 100 AS oee_score
FROM fact_production
GROUP BY machine_id
ORDER BY oee_score DESC;


-- 2. Inventory Turnover Analysis
SELECT 
    product_id,
    AVG(closing_stock) as avg_inventory,
    SUM(sold) as total_sold,
    SUM(sold) / AVG(closing_stock) as inventory_turnover_ratio
FROM fact_inventory
GROUP BY product_id
HAVING AVG(closing_stock) > 0
ORDER BY inventory_turnover_ratio DESC;
