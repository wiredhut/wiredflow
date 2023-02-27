from datetime import datetime, timezone

# Information about current time zone
LOCAL_TIMEZONE = datetime.now(timezone.utc).astimezone().tzinfo
MAX_NUMBER_FAILURES_PER_PIPELINE = 2
FAILURES_BATCH_MINUTES = 5

WARM_START_CORE_SECONDS = 10
