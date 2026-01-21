"""
Shared Constants

Application-wide constants to avoid duplication.
"""

# Worker IDs
WORKER_IDS = ["W1", "W2", "W3", "W4", "W5", "W6"]

# Workstation IDs
WORKSTATION_IDS = ["S1", "S2", "S3", "S4", "S5", "S6"]

# Event types
EVENT_TYPE_WORKING = "working"
EVENT_TYPE_IDLE = "idle"
EVENT_TYPE_ABSENT = "absent"
EVENT_TYPE_PRODUCT_COUNT = "product_count"

EVENT_TYPES = [EVENT_TYPE_WORKING, EVENT_TYPE_IDLE, EVENT_TYPE_ABSENT, EVENT_TYPE_PRODUCT_COUNT]

# Time intervals
SEED_INTERVAL_MINUTES = 5

# Confidence thresholds
MIN_CONFIDENCE = 0.7
