#!/usr/bin/env python3
"""
Mute and Unmute New Relic alerts on the command line
"""
import argparse
import hashlib
import requests
import json

GRAPHQL_URL = 'https://api.newrelic.com/graphql'

def gql_headers(api_key):
    return {'api-key': api_key, 'Content-Type': 'application/json'}

PARSER = argparse.ArgumentParser()
# account number
PARSER.add_argument("-a", "--account", required=True, help="new relic account number")
# personal api key
PARSER.add_argument("-k", "--apikey", required=True, help="personal api key")
# muting activity type
PARSER.add_argument("-m", "--muting", required=True, help="list, enable, disable")
# add a muting rule Id argument
PARSER.add_argument("-i", "--id", help="muting rule Id")
# Add a debug flag
PARSER.add_argument("-d", "--debug", help="debug mode",
                    action="store_true")
ARGV = PARSER.parse_args()
def debug_msg(*args):
    """prints the message if the debug option is set"""
    if ARGV.debug:
        print("DEBUG: {}".format("".join(args)))
debug_msg("Debug option is set")
debug_msg("New Relic account is - ", ARGV.account)
debug_msg("Personal api key is - ", ARGV.apikey)
debug_msg("Muting activity type is - ", ARGV.muting)

def validate_input(account, apikey, muting, ruleId):
  global gql_rule
  if (account and apikey and muting):
    if (muting.lower() == "list"):
      gql_rule = '''{
        actor {
          account(id: ''' + account + ''') {
            alerts {
              mutingRules {
                id
                name
              }
            }
          }
        }
      }'''
      return "act"
    elif (muting.lower() == "enable"):
      if (ruleId):
        gql_rule = '''mutation {
          alertsMutingRuleUpdate(accountId: ''' + account + ''', id: ''' + ARGV.id + ''', rule: {enabled: true}) {
            name
            enabled
          }
        }'''
        return "act"
      else:
        return "You have not entered a muting rule Id!"
    elif (muting.lower() == "disable"):
      if (ruleId):
        gql_rule = '''mutation {
          alertsMutingRuleUpdate(accountId: ''' + account + ''', id: ''' + ARGV.id + ''', rule: {enabled: false}) {
            name
            enabled
          }
        }'''
        return "act"
      else:
        return "You have not entered a muting rule Id!"
    else:
      return "You have not entered a muting rule action! (list, enable or disable)"
  else:
    return "You must enter account number, personal apikey and muting activity type (list, enable or disable)"

ret_value = validate_input(ARGV.account, ARGV.apikey, ARGV.muting, ARGV.id)
debug_msg("ret_value is - ", ret_value)
if (ret_value == "act"):
  payload = {'query': gql_rule, 'variables': ""}
  debug_msg("Payload is - ", gql_rule)
  response = requests.post(GRAPHQL_URL, headers=gql_headers(ARGV.apikey), data=json.dumps(payload))
  # print(response)
  print(json.dumps(response.json(), indent=2))
else:
    print(ret_value)