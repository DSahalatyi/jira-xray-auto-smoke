Disclaimer: This project is for educational or personal purposes only!

### Automated test execution creation script for XRAY Test Management
#### (Atlassian Jira extension)

For creating daily test runs (i.e. Smoke Test)

### Technologies
* Python 3
* Selenium 4

### Installation
```
cd ..\jira-xray-auto-smoke
pip install -r requirements.txt
```

### Usage
Before starting the script fill in .env file according to the .env.example
```
cd ..\jira-xray-auto-smoke
python main.py [-hl, --headless](run webdriver in headless mode), [-b, --build](specify build version, if not the latest), [-sconf, --skip_confirmation](create execution w/o confirmation from user)
```

### Workflow

[Fields] contain dynamic data

1. Open Test Plan web page
2. Open test execution creation window
3. Process 'General' tab
    - Retrieve latest build version from Jira (if not specified on launch)
    - Fill in the [Affected version] with the latest build version (if not specified on launch)
    - Fill in the [Summary] according to Template within .env file
    - Fill in the [Description] according to Teplate within .env file
4. Process 'Details' tab
    - Fill in [Test Environments]
    - Remove optional tests from the [Tests] select field
5. Create new test execution(s)
6. Share the executions links with your team via [MS Teams chat] (link to chat provided in .env)
