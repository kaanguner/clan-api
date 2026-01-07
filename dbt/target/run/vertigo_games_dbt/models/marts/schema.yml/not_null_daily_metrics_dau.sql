
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select dau
from `vertigo-games-case-2026`.`vertigo_analytics`.`daily_metrics`
where dau is null



  
  
      
    ) dbt_internal_test