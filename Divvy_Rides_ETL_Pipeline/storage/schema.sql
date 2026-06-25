-- DuckDB schema for Divvy pipeline

CREATE TABLE IF NOT EXISTS raw_rides (
    ride_id            VARCHAR PRIMARY KEY,
    rideable_type      VARCHAR,
    started_at         TIMESTAMP,
    ended_at           TIMESTAMP,
    start_station_name VARCHAR,
    start_station_id   VARCHAR,
    end_station_name   VARCHAR,
    end_station_id     VARCHAR,
    start_lat          DOUBLE,
    start_lng          DOUBLE,
    end_lat            DOUBLE,
    end_lng            DOUBLE,
    member_casual      VARCHAR
);

CREATE TABLE IF NOT EXISTS ingestion_log (
    id          INTEGER PRIMARY KEY,
    file_name   VARCHAR NOT NULL,
    rows_loaded INTEGER NOT NULL,
    started_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    finished_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status      VARCHAR DEFAULT 'success'
);

