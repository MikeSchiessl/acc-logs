#!/usr/bin/env python3
import sys
import time
import datetime
import urllib.parse

import modules.aka_log as aka_log
import modules.aka_api as aka_api
import acc_config.default_config as default_config
import json

def get_nextEventPage(links):
    for link in links:
        if link.get("rel") == "next":
            return link.get("href")
    return False



def get_log(given_args=None, route='/', params={}):
    aka_log.log.debug(f"Setting environment for API requests") 
    ux_start = int(given_args.event_starttime) - default_config.acc_log_delay - default_config.acc_loop_time
    dt_start = datetime.datetime.utcfromtimestamp(ux_start)
    #starttime = urllib.parse.quote(dt_start.strftime('%Y-%m-%dT%H:%M:%S'), safe='')
    starttime = dt_start.strftime('%Y-%m-%dT%H:%M:%S')
    ux_end = int(given_args.event_endtime) - default_config.acc_log_delay
    dt_end = datetime.datetime.utcfromtimestamp(ux_end)
    endtime = dt_end.strftime('%Y-%m-%dT%H:%M:%S')
    #endtime = urllib.parse.quote(dt_end.strftime('%Y-%m-%dT%H:%M:%S'), safe='')
    follow_mode = given_args.event_follow
    user_agent = given_args.acc_user_agent_prefix
    my_params = params
    if given_args.accountswitchkey:
        accountswitchkey = given_args.accountswitchkey
    else:
        accountswitchkey = None

   # sys.exit()

    while True:
        #Set start and end time for API request
        my_params['start'] = starttime
        my_params['end'] = endtime

        #Check accountSwitchKey
        if accountswitchkey:
            aka_api_request = aka_api.AkaApi(given_args.credentials_file_section, given_args.credentials_file, accountswitchkey)
            aka_log.log.debug(f"Starttime: {starttime}, Endtime: {endtime}, follow mode: {follow_mode}, accountswithchkey: {accountswitchkey}")
        else:
            aka_api_request = aka_api.AkaApi(given_args.credentials_file_section, given_args.credentials_file)
            aka_log.log.debug(f"Starttime: {starttime}, Endtime: {endtime}, follow mode: {follow_mode}")          
     
        aka_log.log.debug(f"Starting API Request") 
        my_result = aka_api_request.get_events(method="GET", path=route, user_agent=user_agent, params=my_params)
        aka_log.log.debug(f"Parsing API response ... if any") 
        if my_result is not False:
            aka_log.log.debug(f"Dumping captured events") 
            for line in my_result['events']:
                print(json.dumps(line))
            aka_log.log.debug(f"Check if more than 50 events captured during defined time interval") 
            nextEventPage = get_nextEventPage(my_result['links'])
            page = 0
            if nextEventPage is not False:
                aka_log.log.debug(f"More than 50 events captured, going though all of them")
                while nextEventPage is not False:
                    page_route = get_nextEventPage(my_result['links'])
                    #Capture the next page from the events object
                    my_result_page = aka_api_request.get_events(method="GET", path=page_route, user_agent=user_agent)
                    for line in my_result_page['events']:
                       print(json.dumps(line))
                    nextEventPage = get_nextEventPage(my_result_page['links'])
                    #Continue to follow pages as long as available
                    if nextEventPage is not False:
                        aka_log.log.debug(f"Next page: " + nextEventPage)
                        my_result = my_result_page
                        page = page + 1
                        aka_log.log.debug(f"Page: " + str(page) + " complete")
                        time.sleep(1)
                aka_log.log.debug(f"Pagination complete")
            else:
                aka_log.log.debug(f"No more than 50 events, moving on with next time interval") 
        else:
            aka_log.log.info(f"API Request failed")
        aka_log.log.debug(f"Check if follow mode enabled") 
        if follow_mode is True:
            aka_log.log.debug(f"Follow mode enabled") 
            ux_start = ux_end
            dt_start = datetime.datetime.utcfromtimestamp(ux_start)
            starttime = dt_start.strftime('%Y-%m-%dT%H:%M:%S')
            ux_end = int(ux_end) + default_config.acc_loop_time
            dt_end = datetime.datetime.utcfromtimestamp(ux_end)
            endtime = dt_end.strftime('%Y-%m-%dT%H:%M:%S')
            aka_log.log.debug(f"Waiting {default_config.acc_loop_time} for next interaction") 
            time.sleep(default_config.acc_loop_time)
        else:
            aka_log.log.debug(f"Follow mode not enabled, stop log capturing here") 
            break

def eventViewer(given_args=None):
    aka_log.log.debug(f"Starting events collection") 
    get_log(given_args,
            route='/event-viewer-api/v1/events')
