# New Relic alert mute cli
This cli is based on python allows you to list, enable and disable muting rules for alerts. The purpose of this cli is to make it simple to setup recurring muting rules.

# Setup
You would first create a muting rule in the [one.newrelic.com](https://one.newrelic.com/). Then use nralertmute.py cli command to set recurring muting rule.
1. Enable at specified interval to mute alerts.
1. Disable at specified interval to unmute alerts.

## Create a muting rule
1. Once you login into New Relic, click Alerts & AI.
1. From the left navigation panel, click Muting rules and Add a rule.
1. On a Add muting rule page, enter Rule nane, Description, and select the account.
1. Build violation filter, you could add multiple violation conditions.
    For example:
    1. policyName contains MyApp
    1. conditionId equals 12345
1. Do not schedule your muting window.
1. Deselect Enable on save.
1. Click on Add rule to save the rule.

## nralertmute.py cli
1. After you fork the repo, chmod +x nralertmute.py
1. To see the cli help, type ./nralertmute.py -h
1. usage: nralertmute.py [-h] -a ACCOUNT -k APIKEY -m MUTING [-i ID] [-d]
    1. ACCOUNT: The New Relic account Id
    1. APIKEY: The personal apikey
    1. MUTING: The values could be:
        1. List - list all muting rules to find the muting rule id.
        1. Enable - enable muting rule, once enabled no alerts go out for this violation condition to a notification channel(s) linked to the policy.
        1. Disable - disable muting rule, after disabling alerts will start going out when critical incidents are created.
    1. d: If you would like to run the cli in a debug mode.

## Add CLI command in your scheduler program (cron job)
1. List all muting rules in your account:  
```./nralertmute.py -a newrelic-account-number -k personal-apikey -m list``` 
1. Enable muting rule: 
```./nralertmute.py -a newrelic-account-number -k personal-apikey -m enable -i muting-ruleId```
1. Disable muting rule: 
```./nralertmute.py -a newrelic-account-number -k personal-apikey -m disable -i muting-ruleId```
