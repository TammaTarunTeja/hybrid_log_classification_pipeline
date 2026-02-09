import re

regex_patterns = {
    'HTTP Status': [
        r'^nova\.osapi_compute\.wsgi\.server.*'
    ],
    'Resource Usage': [
        r'^nova\.compute\.(claims|resource_tracker).*'
    ],
    'User Action': [
        r'^User User\d+ logged (in|out)\.',
        r'^Account with ID \d+ created by User\d+\.'
    ],
    'System Notification': [
        r'^Backup (started|ended|completed).*',
        r'^System updated to version [\d\.]+',
        r'^File .* uploaded successfully by user.*',
        r'^Disk cleanup completed successfully\.',
        r'^System reboot initiated by user.*'
    ],
    'Security Alert': [
        r'.*(Multiple|Repeated) (bad|failed|incorrect) login.*',
        r'^(Denied|Unauthorized|Invalid) login attempt.*',
        r'.*unauthorized API (access|request).*',
        r'.*(suspicious activity|compromised).*server.*',
        r'.*privilege escalation.*'
    ],
    'Critical Error': [
        r'^(Critical|Essential) system (unit|component|part) (error|malfunction|failure).*',
        r'^RAID array .* (multiple disk failures|disk crashes).*',
        r'.*kernel (panic|failure|malfunction).*',
        r'^System configuration (is no longer valid|is corrupted|failure).*'
    ],
    'Error': [
        r'.*(replication|synchronization) task failed.*shard.*',
        r'^Email service.*(experiencing issues|encountered a fault|failure).*',
        r'.*SSL certificate (validation|invalid).*',
        r'.*(Invalid|Input) (data )?format (mismatch|issue).*'
    ]
}

def regex_classifier(log_message):
    for label, patterns in regex_patterns.items():
        for pattern in patterns:
            if re.match(pattern, log_message):
                return label
    return 'Unknown'


# sample log messages for testing
if __name__ == "__main__":
    test_logs = [
        "nova.osapi_compute.wsgi.server started successfully.",
        "nova.compute.claims resource allocation failed.",
        "User User123 logged in.",
        "Backup started for server instance 456.",
        "Multiple bad login attempts detected from IP 192.168.1.100."
    ]
    for log in test_logs:
        label = regex_classifier(log)
        print(f"Log: '{log}' => Classified as: {label}")