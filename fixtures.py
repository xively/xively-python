# -*- coding: utf-8 -*-
"""
Data used to return in the responses.

"""

import requests


CREATE_FEED_JSON = b'''
{
  "title":"Xively Office environment",
  "website":"http://www.example.com/",
  "email":"info@example.com",
  "version":"1.0.0",
  "tags":[
      "Tag1",
      "Tag2"
  ],
  "location":{
    "disposition":"fixed",
    "ele":"23.0",
    "name":"office",
    "lat":51.5235375648154,
    "exposure":"indoor",
    "lon":-0.0807666778564453,
    "domain":"physical"
  },
  "datastreams":[
    {
      "current_value":"123",
      "max_value":"10000.0",
      "min_value":"-10.0",
      "tags":["humidity"],
      "id":"0"
    },
    {
      "current_value":"987",
      "max_value":"10000.0",
      "min_value":"-10.0",
      "tags":["humidity"],
      "id":"1"
    }
  ]
}
'''

GET_FEED_JSON = b'''
{
"description" : "test of manual feed snapshotting",
"feed" : "http://api.xively.com/v2/feeds/504.json",
"id" : 7021,
"status" : "frozen",
"title" : "Xively Office environment",
"website":"http://www.haque.co.uk/",
"email":"info@example.com",
"updated" : "2010-06-25T11:54:17.463771Z",
"created" : "2010-05-03T23:43:01.238734Z",
"version" : "1.0.0",
"creator" : "https://xively.com/users/hdr",
"auto_feed_url" : "https://api.xively.com/v2/feeds/7021",
"tags":[
    "Tag1",
    "Tag2"
],
"location":
{
  "disposition":"fixed",
  "ele":"23.0",
  "name":"office",
  "lat":51.5235375648154,
  "exposure":"indoor",
  "lon":-0.0807666778564453,
  "domain":"physical"
},
"datastreams" : [ {
  "at" : "2010-06-25T11:54:17.454020Z",
  "current_value" : "999",
  "id" : "3",
  "max_value" : "999.0",
  "min_value" : "7.0"
  },
  {
  "at" : "2010-06-24T10:05:49.000000Z",
  "current_value" : "0000017",
  "id" : "4",
  "max_value" : "19.0",
  "min_value" : "7.0"
  } ]
}
'''

GET_DEVICE_JSON = b'''
{
"description" : "test of manual feed snapshotting",
"feed" : "http://api.xively.com/v2/feeds/504.json",
"id" : 7021,
"status" : "frozen",
"title" : "Xively Office environment",
"website":"http://www.haque.co.uk/",
"updated" : "2010-06-25T11:54:17.463771Z",
"created" : "2010-05-03T23:43:01.238734Z",
"version" : "1.0.0",
"creator" : "https://xively.com/users/hdr",
"product_id": "EK0JEccOD_cVJUeD2eNw",
"device_serial": "ZEG9G6FAADJK",
"auto_feed_url" : "https://api.xively.com/v2/feeds/7021",
"tags":[
    "Tag1",
    "Tag2"
],
"location":
{
  "disposition":"fixed",
  "ele":"23.0",
  "name":"office",
  "lat":51.5235375648154,
  "exposure":"indoor",
  "lon":-0.0807666778564453,
  "domain":"physical"
},
"datastreams" : [ {
  "at" : "2010-06-25T11:54:17.454020Z",
  "current_value" : "999",
  "id" : "3",
  "max_value" : "999.0",
  "min_value" : "7.0"
  },
  {
  "at" : "2010-06-24T10:05:49.000000Z",
  "current_value" : "0000017",
  "id" : "4",
  "max_value" : "19.0",
  "min_value" : "7.0"
  } ]
}
'''

UPDATE_FEED_JSON = b'''
{
  "title":"Xively Office environment",
  "website":"http://www.haque.co.uk/",
  "version":"1.0.0",
  "tags":[
      "Tag1",
      "Tag2"
  ],
  "location":{
      "disposition":"fixed",
      "ele":"23.0",
      "name":"office",
      "lat":51.5235375648154,
      "exposure":"indoor",
      "lon":-0.0807666778564453,
      "domain":"physical"
  },
   "datastreams" : [ {
      "current_value" : "-333",
      "id" : "4"
    },
    { "current_value" : "211",
      "id" : "0",
      "max_value" : "20.0",
      "min_value" : "7.0"
    },
    { "current_value" : "312",
      "id" : "3",
      "max_value" : "999.0",
      "min_value" : "7.0"
    }
  ]
}
'''

LIST_FEEDS_JSON = b'''
{
  "totalResults":4299,
  "results":[
    {
      "feed":"http://api.xively.com/v2/feeds/5853.json",
      "title":"bridge19",
      "status":"live",
      "version":"1.0.0",
      "creator":"me",
      "website":"https://xively.com/users/hdr",
      "updated":"2010-06-08T09:30:21.472927Z",
      "created":"2010-05-03T23:43:01.238734Z",
      "location":{"domain":"physical"},
      "tags":[
          "Tag1",
          "Tag2"
      ],
      "datastreams":[
        {
          "max_value":"10000.0",
          "tags":["humidity"],
          "current_value":"435",
          "min_value":"-10.0",
          "at":"2010-07-02T10:21:57.101496Z",
          "id":"0"
        },
        {
          "max_value":"10000.0",
          "tags":["humidity"],
          "current_value":"herz",
          "min_value":"-10.0",
          "at":"2010-07-02T10:21:57.176209Z",
          "id":"1"
        }
      ]
    }
  ]
}
'''

GET_DATASTREAM_JSON = b'''
{
  "current_value":"100",
  "max_value":"10000.0",
  "at":"2010-07-02T10:16:19.270708Z",
  "min_value":"-10.0",
  "tags":[
    "humidity"
  ],
  "id":"1"
}
'''

CREATE_DATAPOINTS_JSON = b'''
{
  "datapoints":[
    {"at":"2010-05-20T11:01:43Z","value":"294"},
    {"at":"2010-05-20T11:01:44Z","value":"295"},
    {"at":"2010-05-20T11:01:45Z","value":"296"},
    {"at":"2010-05-20T11:01:46Z","value":"297"}
  ]
}
'''

GET_DATAPOINT_JSON = b'''
{
  "value":"297",
  "at":"2010-07-28T07:48:22.014326Z"
}
'''

HISTORY_DATASTREAM_JSON = b'''
{
  "max_value": "1.0",
  "current_value": "0.00334173",
  "min_value": "0.0",
  "at": "2013-01-04T10:30:00.119435Z",
  "version": "1.0.0",
  "datapoints": [
    {
      "value": "0.25741970",
      "at": "2013-01-01T14:14:55.118845Z"
    },
    {
      "value": "0.86826886",
      "at": "2013-01-01T14:29:55.123420Z"
    },
    {
      "value": "0.28586252",
      "at": "2013-01-01T14:44:55.111267Z"
    },
    {
      "value": "0.48122377",
      "at": "2013-01-01T14:59:55.126180Z"
    },
    {
      "value": "0.60897230",
      "at": "2013-01-01T15:14:55.121795Z"
    },
    {
      "value": "0.52898451",
      "at": "2013-01-01T15:29:55.105327Z"
    },
    {
      "value": "0.36369879",
      "at": "2013-01-01T15:44:55.115502Z"
    },
    {
      "value": "0.54204623",
      "at": "2013-01-01T15:59:55.111692Z"
    }
  ],
  "id": "random5"
}
'''

HISTORY_FEED_JSON = b'''
{
  "status": "live",
  "tags": [
    "data",
    "generated",
    "generator",
    "random",
    "sawtooth",
    "sine",
    "square",
    "test",
    "toggle",
    "triangle",
    "wave"
  ],
  "datastreams": [
    {
      "current_value": "-0.52858234",
      "datapoints": [
        {
          "value": "-0.36438789",
          "at": "2013-01-01T14:14:55.118845Z"
        },
        {
          "value": "-0.92348577",
          "at": "2013-01-01T14:29:55.123420Z"
        },
        {
          "value": "0.40271227",
          "at": "2013-01-01T14:44:55.111267Z"
        },
        {
          "value": "0.90677334",
          "at": "2013-01-01T14:59:55.126180Z"
        },
        {
          "value": "-0.44034308",
          "at": "2013-01-01T15:14:55.121795Z"
        },
        {
          "value": "-0.88850004",
          "at": "2013-01-01T15:29:55.105327Z"
        }
      ],
      "at": "2013-01-04T10:22:40.111636Z",
      "max_value": "1.0",
      "min_value": "-1.0",
      "id": "random5"
    },
    {
      "current_value": "0.90935832",
      "datapoints": [
        {
          "value": "-0.37776079",
          "at": "2013-01-01T14:14:55.118845Z"
        },
        {
          "value": "-0.99809959",
          "at": "2013-01-01T14:29:55.123420Z"
        },
        {
          "value": "-0.26099779",
          "at": "2013-01-01T14:44:55.111267Z"
        },
        {
          "value": "0.83106759",
          "at": "2013-01-01T14:59:55.126180Z"
        },
        {
          "value": "0.79286010",
          "at": "2013-01-01T15:14:55.121795Z"
        },
        {
          "value": "-0.32355670",
          "at": "2013-01-01T15:29:55.105327Z"
        }
      ],
      "at": "2013-01-04T10:22:40.111636Z",
      "max_value": "1.0",
      "min_value": "-1.0",
      "id": "random60"
    },
    {
      "current_value": "0.79187545",
      "datapoints": [
        {
          "value": "0.99688943",
          "at": "2013-01-01T14:14:55.118845Z"
        },
        {
          "value": "0.99999155",
          "at": "2013-01-01T14:29:55.123420Z"
        },
        {
          "value": "0.99620780",
          "at": "2013-01-01T14:44:55.111267Z"
        },
        {
          "value": "0.98556422",
          "at": "2013-01-01T14:59:55.126180Z"
        },
        {
          "value": "0.96813412",
          "at": "2013-01-01T15:14:55.121795Z"
        },
        {
          "value": "0.94403985",
          "at": "2013-01-01T15:29:55.105327Z"
        },
        {
          "value": "0.91341442",
          "at": "2013-01-01T15:44:55.115502Z"
        }
      ],
      "at": "2013-01-04T10:22:40.111636Z",
      "max_value": "1.0",
      "min_value": "-1.0",
      "id": "random900"
    }
  ],
  "description": "A test feed full of data for testing devices against.",
  "created": "2012-06-01T14:18:51.736718Z",
  "feed": "https://api.xively.com/v2/feeds/61916.json",
  "title": "Test Data Generator",
  "location": {
    "domain": "physical"
  },
  "version": "1.0.0",
  "private": "false",
  "creator": "https://xively.com/users/paul",
  "updated": "2013-01-04T10:22:40.342290Z",
  "id": 61916
}
'''

MOBILE_FEED_JSON = b'''
{
    "title": "Ship - HANJIN BELAWAN",
    "status": "live",
    "creator": "https://xively.com/users/dhunter",
    "location": {
        "waypoints": [
            {
                "at": "2012-06-01T12:25:05.999502Z",
                "lat": 24.9966,
                "lon": 55.06608
            },
            {
                "at": "2012-06-01T12:40:04.876604Z",
                "lat": 24.99647,
                "lon": 55.06635
            },
            {
                "at": "2012-06-01T12:55:05.907201Z",
                "lat": 24.99652,
                "lon": 55.0663
            },
            {
                "at": "2012-06-01T13:10:05.121031Z",
                "lat": 24.99655,
                "lon": 55.06627
            },
            {
                "at": "2012-06-01T13:25:04.082083Z",
                "lat": 24.99648,
                "lon": 55.06633
            },
            {
                "at": "2012-06-01T13:40:04.589002Z",
                "lat": 24.99648,
                "lon": 55.06635
            }
        ],
        "exposure": "outdoor",
        "domain": "physical",
        "disposition": "mobile",
        "lat": 24.9965,
        "lon": 55.06633
    },
    "datastreams": [
        {
            "at": "2012-06-01T13:55:05.013149Z",
            "datapoints": [],
            "tags": [
                "latitude"
            ],
            "max_value": "29.44627",
            "current_value": "24.9965",
            "id": "0",
            "min_value": "-34.06339"
        },
        {
            "at": "2012-06-01T13:55:05.013149Z",
            "datapoints": [],
            "tags": [
                "longitude"
            ],
            "max_value": "153.9353",
            "current_value": "55.06633",
            "id": "1",
            "min_value": "0.0"
        },
        {
            "at": "2012-06-01T13:55:05.013149Z",
            "datapoints": [],
            "tags": [
                "average speed"
            ],
            "unit": {
                "label": "knots"
            },
            "max_value": "20.8",
            "current_value": "14.3",
            "id": "2",
            "min_value": "5.2"
        },
        {
            "at": "2012-06-01T13:55:05.013149Z",
            "datapoints": [],
            "tags": [
                "last port"
            ],
            "current_value": "JEBEL ALI",
            "id": "3"
        },
        {
            "at": "2012-06-01T13:55:05.013149Z",
            "datapoints": [],
            "tags": [
                "destination"
            ],
            "current_value": "JEBEL ALI",
            "id": "4"
        }
    ],
    "created": "2009-12-08T19:00:05.304995Z",
    "feed": "https://api.xively.com/v2/feeds/3819.json",
    "private": "false",
    "id": 3819,
    "version": "1.0.0",
    "updated": "2012-06-01T13:55:05.170364Z"
}
'''

GET_TRIGGER_JSON = b'''
{
  "threshold_value":"15.0",
  "user":"xively",
  "notified_at":"",
  "url":"http:\/\/www.postbin.org\/1ijyltn",
  "trigger_type":"lt",
  "id":14,
  "environment_id":8470,
  "stream_id":"0"
}
'''

LIST_TRIGGERS_JSON = b'''
[
  {
    "trigger_type":"gt",
    "stream_id":"0",
    "url":"http:\/\/www.postbin.org\/1ijyltn",
    "environment_id":1233,
    "user":"xively",
    "threshold_value":"20.0",
    "notified_at":"",
    "id":13
  }
  ,
  {
    "trigger_type":"lt",
    "stream_id":"0",
    "url":"http:\/\/www.postbin.org\/1ijyltn",
    "environment_id":1233,
    "user":"xively",
    "threshold_value":"15.0",
    "notified_at":"",
    "id":14
  }
]
'''

CREATE_KEY_JSON = b'''
{
  "key":{
    "label":"sharing key",
    "private_access": true,
    "permissions":[
      {
        "access_methods":["put"],
        "source_ip": "128.44.98.129",
        "resources": [
          {
            "feed_id": 504
          }
        ]
      },
      {
        "access_methods": ["get"]
      }
    ]
  }
}
'''

LIST_KEYS_JSON = b'''
{"keys":[
  {
    "api_key":"CeWzga_cNja15kjwSVN5x5Mut46qj5akqKPvFxKIec0",
    "label": "sharing key 1",
    "permissions":[
      {
        "access_methods":["get"]
      }
    ]
  },
  {
    "api_key":"zR9eEw3WfrSY1-abcdefghasdfaoisdj109usasdf0a9sf",
    "label": "sharing key 2",
    "permissions":[
      {
        "access_methods":["put"],
        "source_ip":"123.12.123.123"
      }
    ]
  }
]}
'''

GET_KEY_JSON = b'''
{
  "key":{
    "api_key":"CeWzga_cNja15kjwSVN5x5Mut46qj5akqKPvFxKIec0",
    "label":"sharing key",
    "permissions":[
      {
        "access_methods":["get","put"]
      }
    ]
  }
}
'''


def handle_request(method, url, params=None, *args, **kwargs):
    response = requests.Response()
    response.status_code = 200
    relative_url = url.replace("http://api.xively.com/v2/", '')
    content = None
    if relative_url == 'feeds':
        response.headers['Location'] = url + '/7021'
    elif relative_url == 'feeds/7021':
        content = GET_FEED_JSON
    elif relative_url == 'triggers':
        response.headers['location'] = url + '/3'
    elif relative_url == 'feeds/7021/datastreams/':
        content = b'''
            {"version":"1.0.0",
             "datastreams": [{}]}
        '''.format(GET_DATASTREAM_JSON)
    elif relative_url == 'feeds/7021/datastreams/random5':
        content = HISTORY_DATASTREAM_JSON
    elif relative_url == 'keys':
        response.headers['Location'] = (
            url + '1nAYR5W8jUqiZJXIMwu3923Qfuq_lnFCDOKtf3kyw4g')
    if content:
        response._content = content
    return response
