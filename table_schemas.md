# Table Schemas

This document outlines the schemas for the tables in the Gold Layer of the data warehouse.

---

### `dim_date`

The date dimension table.

| Column        | Data Type | Description                               |
|---------------|-----------|-------------------------------------------|
| `date_key`    | INT64     | Surrogate key for the date (e.g., 20230101) |
| `date`        | DATE      | The actual date.                          |
| `year`        | INT64     | The year of the date.                     |
| `quarter`     | INT64     | The quarter of the date (1-4).            |
| `month`       | INT64     | The month of the date (1-12).             |
| `week`        | INT64     | The week of the year.                     |
| `day_of_week` | INT64     | The day of the week (1=Sunday, 7=Saturday).|
| `is_weekend`  | BOOLEAN   | True if the day is a weekend.             |

---

### `dim_platform`

The platform dimension table.

| Column            | Data Type | Description                   |
|-------------------|-----------|-------------------------------|
| `platform_key`    | STRING    | Surrogate key for the platform. |
| `platform_name`   | STRING    | The name of the platform (e.g., ANDROID, IOS). |
| `platform_category`| STRING    | The category of the platform (e.g., Mobile). |

---

### `dim_country`

The country dimension table.

| Column        | Data Type | Description                   |
|---------------|-----------|-------------------------------|
| `country_key` | STRING    | Surrogate key for the country.  |
| `country_code`| STRING    | The country code (e.g., US, TR). |

---

### `dim_user`

The user dimension table (SCD Type 2).

| Column           | Data Type | Description                                  |
|------------------|-----------|----------------------------------------------|
| `user_key`       | STRING    | Surrogate key for a specific version of a user. |
| `user_id`        | STRING    | The natural key of the user.                 |
| `install_date`   | DATE      | The date the user installed the game.        |
| `first_platform` | STRING    | The first platform the user was seen on.     |
| `first_country`  | STRING    | The first country the user was seen in.      |
| `valid_from`     | TIMESTAMP | The timestamp when this version of the user record became valid. |
| `valid_to`       | TIMESTAMP | The timestamp when this version of the user record became invalid. (NULL for the current version) |
| `is_current`     | BOOLEAN   | True if this is the current version of the user record. |

---

### `fact_daily_user_activity`

The fact table containing daily user activities.

| Column                   | Data Type | Description                                  |
|--------------------------|-----------|----------------------------------------------|
| `activity_id`            | STRING    | Surrogate key for the daily activity record. |
| `user_key`               | STRING    | Foreign key to the `dim_user` table.         |
| `date_key`               | INT64     | Foreign key to the `dim_date` table.         |
| `platform_key`           | STRING    | Foreign key to the `dim_platform` table.     |
| `country_key`            | STRING    | Foreign key to the `dim_country` table.      |
| `session_count`          | INT64     | The number of sessions for the user on that day. |
| `session_duration_seconds`| INT64     | The total session duration in seconds.       |
| `matches_started`        | INT64     | The number of matches started.               |
| `matches_ended`          | INT64     | The number of matches ended.                 |
| `victories`              | INT64     | The number of victories.                     |
| `defeats`                | INT64     | The number of defeats.                       |
| `iap_revenue`            | FLOAT64   | In-app purchase revenue.                     |
| `ad_revenue`             | FLOAT64   | Ad revenue.                                  |
| `server_errors`          | INT64     | The number of server errors.                 |
| `created_at`             | DATE      | The date of the activity.                    |

---

### `daily_metrics`

The aggregated daily metrics table.

| Column              | Data Type | Description                                  |
|---------------------|-----------|----------------------------------------------|
| `event_date`        | DATE      | The date of the activity.                    |
| `country`           | STRING    | The country code.                            |
| `platform`          | STRING    | The platform name.                           |
| `dau`               | INT64     | Daily Active Users.                          |
| `total_iap_revenue` | FLOAT64   | Total in-app purchase revenue.               |
| `total_ad_revenue`  | FLOAT64   | Total ad revenue.                            |
| `arpdau`            | FLOAT64   | Average Revenue Per Daily Active User.       |
| `matches_started`   | INT64     | Total matches started.                       |
| `match_per_dau`     | FLOAT64   | Average matches started per DAU.             |
| `win_ratio`         | FLOAT64   | Ratio of victories to matches ended.         |
| `defeat_ratio`      | FLOAT64   | Ratio of defeats to matches ended.           |
| `server_error_per_dau`| FLOAT64   | Server connection errors per DAU.            |
