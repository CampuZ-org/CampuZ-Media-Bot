API Documentation
Metrics Endpoint

URL: /metrics
Method: GET
Description: Provides Prometheus metrics for monitoring.
Metrics:
bot_cycle_duration_seconds: Duration of cycle.
bot_media_tact_duration_seconds: Duration of media tact.
bot_posts_published_total: Total posts published.
bot_posts_rejected_total: Total posts rejected.
bot_errors_total: Total errors.



Notes

No public API for bot control; all interactions via configuration files.
Telegram notifications for errors are sent to the admin (configured in config.yaml).

