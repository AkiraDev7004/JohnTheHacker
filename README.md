# John the Hacker

## Overview
This tool automates account creation on any website by using Selenium to control a hidden Chrome browser and requests for API calls. It reads configuration from `config.json` and creates multiple accounts in rapid succession without leaving traces.

## Features
- **Stealth Mode**: Runs completely headless with no visible UI, making it invisible to users
- **Performance Optimized**: Uses Chrome's new headless engine for maximum speed
- **Configurable**: All settings stored in a simple JSON file
- **Random Suffix Generation**: Automatically appends random characters to account names

## Usage Instructions

### 1. Edit `config.json`
Modify the configuration file with your target website and base name:
```json
{
    "website": "https://example.com/signup",
    "name": "john_doe"
}
```

### 2. Run the Tool
Execute the Python script from a terminal:
```bash
python3 john_the_hacker.py
```

The tool will automatically:
- Open Chrome in hidden mode
- Navigate to your specified website
- Create accounts using `<name><random_suffix>` format
- Handle any errors gracefully and continue processing

### 3. Monitor Progress
Output includes real-time status messages showing which account is being created and whether it succeeded.

## Technical Details
- **Language**: Python 3.x
- **Dependencies**: Selenium, requests (install via pip)
- **Browser**: Google Chrome with headless mode enabled
- **Account Format**: Base name from config + random alphanumeric suffix

## Notes
This tool is designed for legitimate testing and automation purposes. Ensure you have proper authorization before creating accounts on any website.
