
  
    

    create or replace table `vertigo-games-case-2026`.`vertigo_analytics`.`daily_metrics`
      
    partition by event_date
    cluster by country, platform

    
    OPTIONS(
      labels=[('team', 'analytics'), ('domain', 'gaming_metrics')]
    )
    as (
      

/*
  daily_metrics.sql
  
  Aggregated model for business reporting - summarizes gameplay, monetization, 
  and performance signals per day, country, and platform.
  
  Source: Raw user-level daily metrics from BigQuery
  Grain: One row per (event_date, country, platform) combination
*/

WITH source_data AS (
    SELECT
        event_date,
        -- Handle NULL/empty country values
        COALESCE(NULLIF(TRIM(country), ''), 'UNKNOWN') AS country,
        UPPER(platform) AS platform,
        user_id,
        total_session_count,
        total_session_duration,
        match_start_count,
        match_end_count,
        victory_count,
        defeat_count,
        server_connection_error,
        iap_revenue,
        ad_revenue
    FROM `vertigo-games-case-2026`.`vertigo_raw`.`user_daily_metrics`
    WHERE event_date IS NOT NULL
),

-- Pre-aggregate to ensure we count each user only once per day/country/platform
daily_user_metrics AS (
    SELECT
        event_date,
        country,
        platform,
        user_id,
        SUM(total_session_count) AS user_sessions,
        SUM(total_session_duration) AS user_session_duration,
        SUM(match_start_count) AS user_matches_started,
        SUM(match_end_count) AS user_matches_ended,
        SUM(victory_count) AS user_victories,
        SUM(defeat_count) AS user_defeats,
        SUM(server_connection_error) AS user_server_errors,
        SUM(iap_revenue) AS user_iap_revenue,
        SUM(ad_revenue) AS user_ad_revenue
    FROM source_data
    GROUP BY event_date, country, platform, user_id
),

-- Final aggregation by date, country, platform
aggregated AS (
    SELECT
        event_date,
        country,
        platform,
        
        -- DAU: Daily Active Users (distinct users per day/country/platform)
        COUNT(DISTINCT user_id) AS dau,
        
        -- Revenue metrics
        SUM(user_iap_revenue) AS total_iap_revenue,
        SUM(user_ad_revenue) AS total_ad_revenue,
        
        -- Total revenue for ARPDAU calculation
        SUM(user_iap_revenue) + SUM(user_ad_revenue) AS total_revenue,
        
        -- Match metrics
        SUM(user_matches_started) AS matches_started,
        SUM(user_matches_ended) AS matches_ended,
        SUM(user_victories) AS total_victories,
        SUM(user_defeats) AS total_defeats,
        
        -- Session metrics
        SUM(user_sessions) AS total_sessions,
        SUM(user_session_duration) AS total_session_duration,
        
        -- Server errors
        SUM(user_server_errors) AS total_server_errors
        
    FROM daily_user_metrics
    GROUP BY event_date, country, platform
)

SELECT
    event_date,
    country,
    platform,
    
    -- Core metrics
    dau,
    
    -- Revenue metrics
    ROUND(total_iap_revenue, 2) AS total_iap_revenue,
    ROUND(total_ad_revenue, 2) AS total_ad_revenue,
    
    -- ARPDAU: Average Revenue Per Daily Active User
    ROUND(
        CASE 
            WHEN dau > 0 THEN total_revenue / dau 
            ELSE 0 
        END, 
        4
    ) AS arpdau,
    
    -- Match metrics
    matches_started,
    
    -- Match per DAU: Average matches started per daily active user
    ROUND(
        CASE 
            WHEN dau > 0 THEN CAST(matches_started AS FLOAT64) / dau 
            ELSE 0 
        END, 
        4
    ) AS match_per_dau,
    
    -- Win ratio: Victories / Matches ended
    ROUND(
        CASE 
            WHEN matches_ended > 0 THEN CAST(total_victories AS FLOAT64) / matches_ended 
            ELSE 0 
        END, 
        4
    ) AS win_ratio,
    
    -- Defeat ratio: Defeats / Matches ended  
    ROUND(
        CASE 
            WHEN matches_ended > 0 THEN CAST(total_defeats AS FLOAT64) / matches_ended 
            ELSE 0 
        END, 
        4
    ) AS defeat_ratio,
    
    -- Server error per DAU
    ROUND(
        CASE 
            WHEN dau > 0 THEN CAST(total_server_errors AS FLOAT64) / dau 
            ELSE 0 
        END, 
        4
    ) AS server_error_per_dau

FROM aggregated
    );
  