import requests
import json
import datetime
from rfeed import *

# used Postman to build the below request
url = "https://www.allelitewrestling.com/_api/cloud-data/v1/wix-data/collections/query"

payload = "{\"collectionName\":\"AEWEvents\",\"dataQuery\":{\"filter\":{\"$and\":[]},\"sort\":[{" \
          "\"fieldName\":\"sortByDate\",\"order\":\"ASC\"}],\"paging\":{\"offset\":0,\"limit\":30}},\"options\":{}," \
          "\"includeReferencedItems\":[],\"segment\":\"LIVE\",\"appId\":\"28829c14-24d7-456e-a628-dd1bb6da22fc\"} "
headers = {
    'authorization': 'wixcode-pub.7a83a60ebdf94fd81b6cdfb304defc1e5e9d0cfd.eyJpbnN0YW5jZUlkIjoiNmRjOGM0NTUtYzU2Yi00YjMzLTk3MTktYjdkZGJjODBiODJlIiwiaHRtbFNpdGVJZCI6IjliODczM2EzLWUyNGEtNDhlMC1iYmFlLWRlNzdlNTA0OTEyOCIsInVpZCI6bnVsbCwicGVybWlzc2lvbnMiOm51bGwsImlzVGVtcGxhdGUiOmZhbHNlLCJzaWduRGF0ZSI6MTY2MzM2MTc5ODk4NiwiYWlkIjoiNjIxN2M0OTYtYTgyNi00YmViLWIxMTMtZGFmZWU0ZjU1ODE1IiwiYXBwRGVmSWQiOiJDbG91ZFNpdGVFeHRlbnNpb24iLCJpc0FkbWluIjpmYWxzZSwibWV0YVNpdGVJZCI6IjQ3ZmI4M2NlLTA2ZTAtNDI5NC1iYmNiLTRjYTNhYTRlYmUxNyIsImNhY2hlIjpudWxsLCJleHBpcmF0aW9uRGF0ZSI6bnVsbCwicHJlbWl1bUFzc2V0cyI6Ikhhc0RvbWFpbixBZHNGcmVlLFNob3dXaXhXaGlsZUxvYWRpbmciLCJ0ZW5hbnQiOm51bGwsInNpdGVPd25lcklkIjoiYWMyMDQxNzAtMGZhMC00NWZlLWI5MDktMGIwOTVhYzUzYzE3IiwiaW5zdGFuY2VUeXBlIjoicHViIiwic2l0ZU1lbWJlcklkIjpudWxsfQ==',
    'Content-Type': 'text/plain',
    'Cookie': 'TS01b6f604=018d9e98b61683161bcf5460c44f5101eac363d474ef6616b6cada944b6748505b99487c0e6ce4e7f07b1a7aef3f10a8db16034e46; TS01e85bed=018d9e98b61683161bcf5460c44f5101eac363d474ef6616b6cada944b6748505b99487c0e6ce4e7f07b1a7aef3f10a8db16034e46; XSRF-TOKEN=1664376092|493UgdvF1xHF'
}

response = requests.request("POST", url, headers=headers, data=payload)
output = response.json()

# will use this number in order to iterate on the output for each item.
total_events = output['totalCount']
i = 0
items = []
nl = '\n'

# https://github.com/egorsmkv/rfeed
# this iterates on the output and then builds an rfeed Item object
# at the end it adds it to the list of rfeed items.
for event in range(total_events):
    try:
        # sometimes they will post the event and not have a ticket url poasted
        # if this occurs the link here will default to the event link.
        ticket_url = output['items'][i]['ticketsUrl']
    except:
        ticket_url = "https://www.allelitewrestling.com/aew-events"
    item = Item(
        title=output['items'][i]['eventName'],
        link=ticket_url,
        description=f"City: {output['items'][i]['city']}{nl}"
                    f"Date: {output['items'][i]['date']}{nl}"
                    f"{output['items'][i]['onSaleInfo']}",
        guid=Guid(output['items'][i]['eventName'])
    )
    items.append(item)
    i = i + 1

feed = Feed(
    title="AEW Events Tracker",
    link="https://www.allelitewrestling.com/aew-events",
    description="AEW Event Aggregator",
    language="en-US",
    lastBuildDate=datetime.datetime.now(),
    items=items
)

# writes the feed to an RSS file which can then be targeted by your rss feed reader
with open('path\\to\\rss\\feeds\\aew.rss', 'w') as f:
    f.write(feed.rss())
