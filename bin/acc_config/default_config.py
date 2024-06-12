#!/usr/bin/env python3

# Generic Settings
## CLI default loglevel
default_log_level = 'DEBUG'
## CLI available loglevels
log_levels_available = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
## How often do we want to retry an auth before failing
max_auth_attempts = 3

## Event Viewer
### Event Viewer events per page
acc_page_size = 10000
### Event Viewer Delay from $now to ensure 100% of logs are received on the backend (time in seconds)
acc_log_delay = 1200
### Loop time in seconds
acc_loop_time = 10