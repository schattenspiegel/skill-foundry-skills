# Verification matrix

Run tests with a cleared environment and temporary working directory. Cover
defaults, initializer input, environment names, nested values, dotenv,
secrets-directory files, CLI input when enabled, source collisions, malformed
complex values, missing required values, extra keys, custom-source failure, and
secret redaction. Assert typed values and error locations, not entire formatted
messages. Never read developer-machine environment or a real secrets directory.
