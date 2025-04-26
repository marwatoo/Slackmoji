import re

# Custom emoji mappings
CUSTOM_EMOJIS = {
    ":rain_cloud:": "🌧️",
    ":partly_sunny_rain:": "🌦️",
    ":snow_cloud:":"🌨️",
    # Add more custom mappings here
}

# Precompile the emoji pattern
EMOJI_PATTERN = re.compile(r':[a-zA-Z0-9_\-]+:')