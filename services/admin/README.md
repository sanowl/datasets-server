# Datasets server admin service

> Admin endpoints

## Configuration

The service can be configured using environment variables. They are grouped by scope.

### Admin service

Set environment variables to configure the application (`ADMIN_` prefix):

- `ADMIN_HF_ORGANIZATION`: the huggingface organization from which the authenticated user must be part of in order to access the protected routes, eg. "huggingface". If empty, the authentication is disabled. Defaults to None.
- `ADMIN_CACHE_REPORTS_NUM_RESULTS`: the number of results in /cache-reports/... endpoints. Defaults to `100`.
- `ADMIN_CACHE_REPORTS_WITH_CONTENT_NUM_RESULTS`: the number of results in /cache-reports-with-content/... endpoints. Defaults to `100`.
- `ADMIN_HF_TIMEOUT_SECONDS`: the timeout in seconds for the requests to the Hugging Face Hub. Defaults to `0.2` (200 ms).
- `ADMIN_HF_WHOAMI_PATH`: the path of the external whoami service, on the hub (see `HF_ENDPOINT`), eg. "/api/whoami-v2". Defaults to `/api/whoami-v2`.
- `ADMIN_MAX_AGE`: number of seconds to set in the `max-age` header on technical endpoints. Defaults to `10` (10 seconds).

### Uvicorn

The following environment variables are used to configure the Uvicorn server (`ADMIN_UVICORN_` prefix):

- `ADMIN_UVICORN_HOSTNAME`: the hostname. Defaults to `"localhost"`.
- `ADMIN_UVICORN_NUM_WORKERS`: the number of uvicorn workers. Defaults to `2`.
- `ADMIN_UVICORN_PORT`: the port. Defaults to `8000`.

### Prometheus

- `PROMETHEUS_MULTIPROC_DIR`: the directory where the uvicorn workers share their prometheus metrics. See https://github.com/prometheus/client_python#multiprocess-mode-eg-gunicorn. Defaults to empty, in which case every worker manages its own metrics, and the /metrics endpoint returns the metrics of a random worker.

### Storage

- `DATASETS_BASED_HF_DATASETS_CACHE`: storage directory where job runners that used `datasets` library store cache files.
- `DESCRIPTIVE_STATISTICS_CACHE_DIRECTORY`: storage directory where `split-descriptive-statistics` job runner stores temporal downloaded parquet files.
- `DUCKDB_INDEX_CACHE_DIRECTORY`: storage directory where `split-duckdb-index` job runner stores temporal downloaded parquet files.
Same directory is used for /search and /filter endpoint for temporal duckdb index files are downloaded.  

### Common

See [../../libs/libcommon/README.md](../../libs/libcommon/README.md) for more information about the common configuration.

## Endpoints

The admin service provides endpoints:

- `/healthcheck`: ensure the app is running
- `/metrics`: give info about the cache and the queue
- `/pending-jobs`: give the pending jobs, classed by queue and status (waiting or started)
- `/dataset-status`: give the dataset status including cache records and pending jobs.
- `/num-dataset-infos-by-builder-name`: give a report about number of datasets by builder name (parquet, csv, text, imagefolder, audiofolder, json, arrow and webdataset).
- `/recreate-dataset`: deletes all the cache entries related to a specific dataset, then run all the steps in order. It's a POST endpoint. Pass the requested parameters:
  - `dataset`: the dataset name
  - `priority`: `low` (default), `normal` or `high`

### Endpoints by processing step

- `/force-refresh{processing_step}`: force refresh cache entries for the processing step. It's a POST endpoint. Pass the requested parameters, depending on the processing step's input type:
  - `dataset`: `?dataset={dataset}`
  - `config`: `?dataset={dataset}&config={config}`
  - `split`: `?dataset={dataset}&config={config}&split={split}`
- `/cache-reports{processing_step}`: give detailed reports on the content of the cache for a processing step
- `/cache-reports-with-content{processing_step}`: give detailed reports on the content of the cache for a processing step, including the content itself, which can be heavy
