from datetime import datetime, timezone

# Information about current time zone
LOCAL_TIMEZONE = datetime.now(timezone.utc).astimezone().tzinfo
