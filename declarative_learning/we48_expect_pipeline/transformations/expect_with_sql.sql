create or refresh materialized view
workspace.default.get_silver_staff_sql
(
    constraint valid_age expect (age is not null) on violation drop row
)
as
select * from 
catalog_we48.logistics_db.silver_staff
;