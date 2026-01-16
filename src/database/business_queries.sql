-- 1. Overall Equipment Effectiveness (OEE)
SELECT
    machine_id,
    AVG((planned_production_time - downtime_minutes) / planned_production_time) * 100 AS availability_percentage,