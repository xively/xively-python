# -*- coding: utf-8 -*-
"""
Data used to return in the responses.

"""

import requests


CREATE_FEED_JSON = b'''
{
  "title":"Xively Office environment",
  "website":"http://www.example.com/",
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

GET_FEED_61916 = b"{\"id\":61916,\"title\":\"Test Data Generator\",\"private\":\"false\",\"tags\":[\"data\",\"generated\",\"generator\",\"random\",\"sawtooth\",\"sine\",\"square\",\"test\",\"toggle\",\"triangle\",\"wave\"],\"description\":\"A constantly updating feed of test data for testing against.\\r\\n\\r\\nDatastreams are named by type and period. i.e. sawtooth60 is a sawtooth wave, which repeats every 60 seconds\\r\\n\\r\\nThe 'random' and 'toggle' datastreams are updated once per period.\\r\\n\\r\\nThe location follows a roughly sinusoidal orbit every 92 minutes reaching 51.6 deg. north latitude and -51.6 deg. south latitude.\\r\\n\\r\\nData is generated by a Node.js app running on Heroku: https://github.com/cosm/cosm_test_data_generator\",\"feed\":\"https://api.xively.com/v2/feeds/61916.json\",\"auto_feed_url\":\"https://api.xively.com/v2/feeds/61916.json\",\"status\":\"live\",\"updated\":\"2013-06-21T14:26:25.367987Z\",\"created\":\"2012-06-01T14:18:51.736718Z\",\"creator\":\"https://xively.com/users/paul\",\"version\":\"1.0.0\",\"datastreams\":[{\"id\":\"random3600\",\"current_value\":\"0.00411994\",\"at\":\"2013-06-21T14:00:00.113805Z\",\"max_value\":\"0.99902342\",\"min_value\":\"0.00297551\"},{\"id\":\"random5\",\"current_value\":\"0.85609216\",\"at\":\"2013-06-21T14:26:25.110520Z\",\"max_value\":\"1.0\",\"min_value\":\"0.0\"},{\"id\":\"random60\",\"current_value\":\"0.96102846\",\"at\":\"2013-06-21T14:26:00.109115Z\",\"max_value\":\"0.99998474\",\"min_value\":\"0.0\"},{\"id\":\"random900\",\"current_value\":\"0.77315938\",\"at\":\"2013-06-21T14:15:00.121434Z\",\"max_value\":\"0.99978637\",\"min_value\":\"0.00016785\"},{\"id\":\"sawtooth3600\",\"current_value\":\"0.44030806\",\"at\":\"2013-06-21T14:26:25.110520Z\",\"max_value\":\"0.99990694\",\"min_value\":\"2.639e-05\"},{\"id\":\"sawtooth60\",\"current_value\":\"0.41848333\",\"at\":\"2013-06-21T14:26:25.110520Z\",\"max_value\":\"0.99458333\",\"min_value\":\"0.00156667\"},{\"id\":\"sawtooth900\",\"current_value\":\"0.76123222\",\"at\":\"2013-06-21T14:26:25.110520Z\",\"max_value\":\"0.99962778\",\"min_value\":\"0.00010444\"},{\"id\":\"sine3600\",\"current_value\":\"-0.15682853\",\"at\":\"2013-06-21T14:26:25.110520Z\",\"max_value\":\"1.0\",\"min_value\":\"-1.0\"},{\"id\":\"sine60\",\"current_value\":\"0.02393713\",\"at\":\"2013-06-21T14:26:25.110520Z\",\"max_value\":\"1.0\",\"min_value\":\"-1.0\"},{\"id\":\"sine900\",\"current_value\":\"-0.58907566\",\"at\":\"2013-06-21T14:26:25.110520Z\",\"max_value\":\"1.0\",\"min_value\":\"-1.0\"},{\"id\":\"toggle3600\",\"current_value\":\"1\",\"at\":\"2013-06-21T13:28:45.111966Z\",\"max_value\":\"1.0\",\"min_value\":\"0.0\"},{\"id\":\"toggle5\",\"current_value\":\"0\",\"at\":\"2013-06-21T14:26:25.110520Z\",\"max_value\":\"1.0\",\"min_value\":\"0.0\"},{\"id\":\"toggle60\",\"current_value\":\"1\",\"at\":\"2013-06-21T14:26:00.109115Z\",\"max_value\":\"1.0\",\"min_value\":\"0.0\"},{\"id\":\"toggle900\",\"current_value\":\"0\",\"at\":\"2013-06-21T14:13:10.108706Z\",\"max_value\":\"1.0\",\"min_value\":\"0.0\"},{\"id\":\"triangle3600\",\"current_value\":\"0.88061611\",\"at\":\"2013-06-21T14:26:25.110520Z\",\"max_value\":\"0.99994778\",\"min_value\":\"5.278e-05\"},{\"id\":\"triangle60\",\"current_value\":\"0.83696666\",\"at\":\"2013-06-21T14:26:25.110520Z\",\"max_value\":\"0.99686667\",\"min_value\":\"0.00313333\"},{\"id\":\"triangle900\",\"current_value\":\"0.47753556\",\"at\":\"2013-06-21T14:26:25.110520Z\",\"max_value\":\"0.99979111\",\"min_value\":\"0.00020889\"}],\"location\":{\"disposition\":\"mobile\",\"name\":\"Orbit\",\"exposure\":\"outdoor\",\"domain\":\"physical\",\"ele\":\"370000\",\"lat\":9.821571348,\"lon\":-139.5979812}}"

GET_FEED_HISTORY_61916_DATASTREAM_RANDOM3600 = b"{\"id\":\"random3600\",\"current_value\":\"0.00411994\",\"at\":\"2013-06-21T14:00:00.113805Z\",\"max_value\":\"0.99902342\",\"min_value\":\"0.00297551\",\"version\":\"1.0.0\"}"
GET_FEED_HISTORY_61916_DATASTREAM_RANDOM5 = b"{\"id\":\"random5\",\"current_value\":\"0.85609216\",\"at\":\"2013-06-21T14:26:25.110520Z\",\"max_value\":\"1.0\",\"min_value\":\"0.0\",\"datapoints\":[{\"value\":\"0.38304723\",\"at\":\"2013-06-21T14:25:30.109017Z\"},{\"value\":\"0.59276722\",\"at\":\"2013-06-21T14:25:35.111401Z\"},{\"value\":\"0.36140993\",\"at\":\"2013-06-21T14:25:40.127913Z\"},{\"value\":\"0.62887007\",\"at\":\"2013-06-21T14:25:45.109497Z\"},{\"value\":\"0.58525978\",\"at\":\"2013-06-21T14:25:50.111327Z\"},{\"value\":\"0.48584726\",\"at\":\"2013-06-21T14:25:55.108562Z\"},{\"value\":\"0.96102846\",\"at\":\"2013-06-21T14:26:00.109115Z\"},{\"value\":\"0.68215457\",\"at\":\"2013-06-21T14:26:05.124915Z\"},{\"value\":\"0.38455787\",\"at\":\"2013-06-21T14:26:10.114177Z\"},{\"value\":\"0.06903182\",\"at\":\"2013-06-21T14:26:15.106108Z\"},{\"value\":\"0.55577935\",\"at\":\"2013-06-21T14:26:20.122268Z\"},{\"value\":\"0.85609216\",\"at\":\"2013-06-21T14:26:25.110520Z\"}],\"version\":\"1.0.0\"}"
GET_FEED_HISTORY_61916_DATASTREAM_RANDOM60 = b"{\"id\":\"random60\",\"current_value\":\"0.96102846\",\"at\":\"2013-06-21T14:26:00.109115Z\",\"max_value\":\"0.99998474\",\"min_value\":\"0.0\",\"datapoints\":[{\"value\":\"0.96102846\",\"at\":\"2013-06-21T14:26:00.109115Z\"}],\"version\":\"1.0.0\"}"
GET_FEED_HISTORY_61916_DATASTREAM_RANDOM900 = b"{\"id\":\"random900\",\"current_value\":\"0.77315938\",\"at\":\"2013-06-21T14:15:00.121434Z\",\"max_value\":\"0.99978637\",\"min_value\":\"0.00016785\",\"version\":\"1.0.0\"}"
GET_FEED_HISTORY_61916_DATASTREAM_SAWTOOTH3600 = b"{\"id\":\"sawtooth3600\",\"current_value\":\"0.44030806\",\"at\":\"2013-06-21T14:26:25.110520Z\",\"max_value\":\"0.99990694\",\"min_value\":\"2.639e-05\",\"datapoints\":[{\"value\":\"0.42503000\",\"at\":\"2013-06-21T14:25:30.109017Z\"},{\"value\":\"0.42641889\",\"at\":\"2013-06-21T14:25:35.111401Z\"},{\"value\":\"0.42780778\",\"at\":\"2013-06-21T14:25:40.127913Z\"},{\"value\":\"0.42919750\",\"at\":\"2013-06-21T14:25:45.109497Z\"},{\"value\":\"0.43058611\",\"at\":\"2013-06-21T14:25:50.111327Z\"},{\"value\":\"0.43197444\",\"at\":\"2013-06-21T14:25:55.108562Z\"},{\"value\":\"0.43336333\",\"at\":\"2013-06-21T14:26:00.109115Z\"},{\"value\":\"0.43475222\",\"at\":\"2013-06-21T14:26:05.124915Z\"},{\"value\":\"0.43614111\",\"at\":\"2013-06-21T14:26:10.114177Z\"},{\"value\":\"0.43753000\",\"at\":\"2013-06-21T14:26:15.106108Z\"},{\"value\":\"0.43891889\",\"at\":\"2013-06-21T14:26:20.122268Z\"},{\"value\":\"0.44030806\",\"at\":\"2013-06-21T14:26:25.110520Z\"}],\"version\":\"1.0.0\"}"
GET_FEED_HISTORY_61916_DATASTREAM_SAWTOOTH60 = b"{\"id\":\"sawtooth60\",\"current_value\":\"0.41848333\",\"at\":\"2013-06-21T14:26:25.110520Z\",\"max_value\":\"0.99458333\",\"min_value\":\"0.00156667\",\"datapoints\":[{\"value\":\"0.50180000\",\"at\":\"2013-06-21T14:25:30.109017Z\"},{\"value\":\"0.58513333\",\"at\":\"2013-06-21T14:25:35.111401Z\"},{\"value\":\"0.66846667\",\"at\":\"2013-06-21T14:25:40.127913Z\"},{\"value\":\"0.75185000\",\"at\":\"2013-06-21T14:25:45.109497Z\"},{\"value\":\"0.83516666\",\"at\":\"2013-06-21T14:25:50.111327Z\"},{\"value\":\"0.91846667\",\"at\":\"2013-06-21T14:25:55.108562Z\"},{\"value\":\"0.00180000\",\"at\":\"2013-06-21T14:26:00.109115Z\"},{\"value\":\"0.08513333\",\"at\":\"2013-06-21T14:26:05.124915Z\"},{\"value\":\"0.16846667\",\"at\":\"2013-06-21T14:26:10.114177Z\"},{\"value\":\"0.25180000\",\"at\":\"2013-06-21T14:26:15.106108Z\"},{\"value\":\"0.33513333\",\"at\":\"2013-06-21T14:26:20.122268Z\"},{\"value\":\"0.41848333\",\"at\":\"2013-06-21T14:26:25.110520Z\"}],\"version\":\"1.0.0\"}"
GET_FEED_HISTORY_61916_DATASTREAM_SAWTOOTH900 = b"{\"id\":\"sawtooth900\",\"current_value\":\"0.76123222\",\"at\":\"2013-06-21T14:26:25.110520Z\",\"max_value\":\"0.99962778\",\"min_value\":\"0.00010444\",\"datapoints\":[{\"value\":\"0.70567556\",\"at\":\"2013-06-21T14:25:35.111401Z\"},{\"value\":\"0.71123111\",\"at\":\"2013-06-21T14:25:40.127913Z\"},{\"value\":\"0.71679000\",\"at\":\"2013-06-21T14:25:45.109497Z\"},{\"value\":\"0.72234444\",\"at\":\"2013-06-21T14:25:50.111327Z\"},{\"value\":\"0.72789778\",\"at\":\"2013-06-21T14:25:55.108562Z\"},{\"value\":\"0.73345333\",\"at\":\"2013-06-21T14:26:00.109115Z\"},{\"value\":\"0.73900889\",\"at\":\"2013-06-21T14:26:05.124915Z\"},{\"value\":\"0.74456444\",\"at\":\"2013-06-21T14:26:10.114177Z\"},{\"value\":\"0.75012000\",\"at\":\"2013-06-21T14:26:15.106108Z\"},{\"value\":\"0.75567556\",\"at\":\"2013-06-21T14:26:20.122268Z\"},{\"value\":\"0.76123222\",\"at\":\"2013-06-21T14:26:25.110520Z\"}],\"version\":\"1.0.0\"}"
GET_FEED_HISTORY_61916_DATASTREAM_SINE3600 = b"{\"id\":\"sine3600\",\"current_value\":\"-0.15682853\",\"at\":\"2013-06-21T14:26:25.110520Z\",\"max_value\":\"1.0\",\"min_value\":\"-1.0\",\"datapoints\":[{\"value\":\"-0.24342916\",\"at\":\"2013-06-21T14:25:35.111401Z\"},{\"value\":\"-0.23484379\",\"at\":\"2013-06-21T14:25:40.127913Z\"},{\"value\":\"-0.22623490\",\"at\":\"2013-06-21T14:25:45.109497Z\"},{\"value\":\"-0.21761520\",\"at\":\"2013-06-21T14:25:50.111327Z\"},{\"value\":\"-0.20898022\",\"at\":\"2013-06-21T14:25:55.108562Z\"},{\"value\":\"-0.20032545\",\"at\":\"2013-06-21T14:26:00.109115Z\"},{\"value\":\"-0.19165503\",\"at\":\"2013-06-21T14:26:05.124915Z\"},{\"value\":\"-0.18296962\",\"at\":\"2013-06-21T14:26:10.114177Z\"},{\"value\":\"-0.17426990\",\"at\":\"2013-06-21T14:26:15.106108Z\"},{\"value\":\"-0.16555656\",\"at\":\"2013-06-21T14:26:20.122268Z\"},{\"value\":\"-0.15682853\",\"at\":\"2013-06-21T14:26:25.110520Z\"}],\"version\":\"1.0.0\"}"
GET_FEED_HISTORY_61916_DATASTREAM_SINE60 = b"{\"id\":\"sine60\",\"current_value\":\"-0.48509427\",\"at\":\"2013-06-21T14:26:30.114982Z\",\"max_value\":\"1.0\",\"min_value\":\"-1.0\",\"datapoints\":[{\"value\":\"-0.81572129\",\"at\":\"2013-06-21T14:25:35.111401Z\"},{\"value\":\"-0.99627805\",\"at\":\"2013-06-21T14:25:40.127913Z\"},{\"value\":\"-0.90281289\",\"at\":\"2013-06-21T14:25:45.109497Z\"},{\"value\":\"-0.56121744\",\"at\":\"2013-06-21T14:25:50.111327Z\"},{\"value\":\"-0.06550477\",\"at\":\"2013-06-21T14:25:55.108562Z\"},{\"value\":\"0.44839131\",\"at\":\"2013-06-21T14:26:00.109115Z\"},{\"value\":\"0.83902091\",\"at\":\"2013-06-21T14:26:05.124915Z\"},{\"value\":\"0.99899671\",\"at\":\"2013-06-21T14:26:10.114177Z\"},{\"value\":\"0.88434005\",\"at\":\"2013-06-21T14:26:15.106108Z\"},{\"value\":\"0.52657098\",\"at\":\"2013-06-21T14:26:20.122268Z\"},{\"value\":\"0.02393713\",\"at\":\"2013-06-21T14:26:25.110520Z\"},{\"value\":\"-0.48509427\",\"at\":\"2013-06-21T14:26:30.114982Z\"}],\"version\":\"1.0.0\"}"
GET_FEED_HISTORY_61916_DATASTREAM_SINE900 = b"{\"id\":\"sine900\",\"current_value\":\"-0.56013918\",\"at\":\"2013-06-21T14:26:30.114982Z\",\"max_value\":\"1.0\",\"min_value\":\"-1.0\",\"datapoints\":[{\"value\":\"-0.83249683\",\"at\":\"2013-06-21T14:25:35.111401Z\"},{\"value\":\"-0.81238550\",\"at\":\"2013-06-21T14:25:40.127913Z\"},{\"value\":\"-0.79124510\",\"at\":\"2013-06-21T14:25:45.109497Z\"},{\"value\":\"-0.76913195\",\"at\":\"2013-06-21T14:25:50.111327Z\"},{\"value\":\"-0.74606190\",\"at\":\"2013-06-21T14:25:55.108562Z\"},{\"value\":\"-0.72204967\",\"at\":\"2013-06-21T14:26:00.109115Z\"},{\"value\":\"-0.69713434\",\"at\":\"2013-06-21T14:26:05.124915Z\"},{\"value\":\"-0.67134708\",\"at\":\"2013-06-21T14:26:10.114177Z\"},{\"value\":\"-0.64472012\",\"at\":\"2013-06-21T14:26:15.106108Z\"},{\"value\":\"-0.61728678\",\"at\":\"2013-06-21T14:26:20.122268Z\"},{\"value\":\"-0.58907566\",\"at\":\"2013-06-21T14:26:25.110520Z\"},{\"value\":\"-0.56013918\",\"at\":\"2013-06-21T14:26:30.114982Z\"}],\"version\":\"1.0.0\"}"
GET_FEED_HISTORY_61916_DATASTREAM_TOGGLE3600 = b"{\"id\":\"toggle3600\",\"current_value\":\"1\",\"at\":\"2013-06-21T13:28:45.111966Z\",\"max_value\":\"1.0\",\"min_value\":\"0.0\",\"version\":\"1.0.0\"}"
GET_FEED_HISTORY_61916_DATASTREAM_TOGGLE5 = b"{\"id\":\"toggle5\",\"current_value\":\"1\",\"at\":\"2013-06-21T14:26:30.114982Z\",\"max_value\":\"1.0\",\"min_value\":\"0.0\",\"datapoints\":[{\"value\":\"0\",\"at\":\"2013-06-21T14:25:35.111401Z\"},{\"value\":\"1\",\"at\":\"2013-06-21T14:25:40.127913Z\"},{\"value\":\"0\",\"at\":\"2013-06-21T14:25:45.109497Z\"},{\"value\":\"1\",\"at\":\"2013-06-21T14:25:50.111327Z\"},{\"value\":\"0\",\"at\":\"2013-06-21T14:25:55.108562Z\"},{\"value\":\"1\",\"at\":\"2013-06-21T14:26:00.109115Z\"},{\"value\":\"0\",\"at\":\"2013-06-21T14:26:05.124915Z\"},{\"value\":\"1\",\"at\":\"2013-06-21T14:26:10.114177Z\"},{\"value\":\"0\",\"at\":\"2013-06-21T14:26:15.106108Z\"},{\"value\":\"1\",\"at\":\"2013-06-21T14:26:20.122268Z\"},{\"value\":\"0\",\"at\":\"2013-06-21T14:26:25.110520Z\"},{\"value\":\"1\",\"at\":\"2013-06-21T14:26:30.114982Z\"}],\"version\":\"1.0.0\"}"
GET_FEED_HISTORY_61916_DATASTREAM_TOGGLE60 = b"{\"id\":\"toggle60\",\"current_value\":\"1\",\"at\":\"2013-06-21T14:26:00.109115Z\",\"max_value\":\"1.0\",\"min_value\":\"0.0\",\"datapoints\":[{\"value\":\"1\",\"at\":\"2013-06-21T14:26:00.109115Z\"}],\"version\":\"1.0.0\"}"
GET_FEED_HISTORY_61916_DATASTREAM_TOGGLE900 = b"{\"id\":\"toggle900\",\"current_value\":\"0\",\"at\":\"2013-06-21T14:13:10.108706Z\",\"max_value\":\"1.0\",\"min_value\":\"0.0\",\"version\":\"1.0.0\"}"
GET_FEED_HISTORY_61916_DATASTREAM_TRIANGLE3600 = b"{\"id\":\"triangle3600\",\"current_value\":\"0.88339333\",\"at\":\"2013-06-21T14:26:30.114982Z\",\"max_value\":\"0.99994778\",\"min_value\":\"5.278e-05\",\"datapoints\":[{\"value\":\"0.85283778\",\"at\":\"2013-06-21T14:25:35.111401Z\"},{\"value\":\"0.85561556\",\"at\":\"2013-06-21T14:25:40.127913Z\"},{\"value\":\"0.85839500\",\"at\":\"2013-06-21T14:25:45.109497Z\"},{\"value\":\"0.86117222\",\"at\":\"2013-06-21T14:25:50.111327Z\"},{\"value\":\"0.86394889\",\"at\":\"2013-06-21T14:25:55.108562Z\"},{\"value\":\"0.86672667\",\"at\":\"2013-06-21T14:26:00.109115Z\"},{\"value\":\"0.86950444\",\"at\":\"2013-06-21T14:26:05.124915Z\"},{\"value\":\"0.87228222\",\"at\":\"2013-06-21T14:26:10.114177Z\"},{\"value\":\"0.87506000\",\"at\":\"2013-06-21T14:26:15.106108Z\"},{\"value\":\"0.87783778\",\"at\":\"2013-06-21T14:26:20.122268Z\"},{\"value\":\"0.88061611\",\"at\":\"2013-06-21T14:26:25.110520Z\"},{\"value\":\"0.88339333\",\"at\":\"2013-06-21T14:26:30.114982Z\"}],\"version\":\"1.0.0\"}"
GET_FEED_HISTORY_61916_DATASTREAM_TRIANGLE60 = b"{\"id\":\"triangle60\",\"current_value\":\"0.99640000\",\"at\":\"2013-06-21T14:26:30.114982Z\",\"max_value\":\"0.99686667\",\"min_value\":\"0.00313333\",\"datapoints\":[{\"value\":\"0.82973333\",\"at\":\"2013-06-21T14:25:35.111401Z\"},{\"value\":\"0.66306666\",\"at\":\"2013-06-21T14:25:40.127913Z\"},{\"value\":\"0.49630000\",\"at\":\"2013-06-21T14:25:45.109497Z\"},{\"value\":\"0.32966667\",\"at\":\"2013-06-21T14:25:50.111327Z\"},{\"value\":\"0.16306666\",\"at\":\"2013-06-21T14:25:55.108562Z\"},{\"value\":\"0.00360000\",\"at\":\"2013-06-21T14:26:00.109115Z\"},{\"value\":\"0.17026667\",\"at\":\"2013-06-21T14:26:05.124915Z\"},{\"value\":\"0.33693334\",\"at\":\"2013-06-21T14:26:10.114177Z\"},{\"value\":\"0.50360000\",\"at\":\"2013-06-21T14:26:15.106108Z\"},{\"value\":\"0.67026667\",\"at\":\"2013-06-21T14:26:20.122268Z\"},{\"value\":\"0.83696666\",\"at\":\"2013-06-21T14:26:25.110520Z\"},{\"value\":\"0.99640000\",\"at\":\"2013-06-21T14:26:30.114982Z\"}],\"version\":\"1.0.0\"}"
GET_FEED_HISTORY_61916_DATASTREAM_TRIANGLE900 = b"{\"id\":\"triangle900\",\"current_value\":\"0.46642667\",\"at\":\"2013-06-21T14:26:30.114982Z\",\"max_value\":\"0.99979111\",\"min_value\":\"0.00020889\",\"datapoints\":[{\"value\":\"0.58864889\",\"at\":\"2013-06-21T14:25:35.111401Z\"},{\"value\":\"0.57753778\",\"at\":\"2013-06-21T14:25:40.127913Z\"},{\"value\":\"0.56642000\",\"at\":\"2013-06-21T14:25:45.109497Z\"},{\"value\":\"0.55531111\",\"at\":\"2013-06-21T14:25:50.111327Z\"},{\"value\":\"0.54420444\",\"at\":\"2013-06-21T14:25:55.108562Z\"},{\"value\":\"0.53309333\",\"at\":\"2013-06-21T14:26:00.109115Z\"},{\"value\":\"0.52198222\",\"at\":\"2013-06-21T14:26:05.124915Z\"},{\"value\":\"0.51087111\",\"at\":\"2013-06-21T14:26:10.114177Z\"},{\"value\":\"0.49976000\",\"at\":\"2013-06-21T14:26:15.106108Z\"},{\"value\":\"0.48864889\",\"at\":\"2013-06-21T14:26:20.122268Z\"},{\"value\":\"0.47753556\",\"at\":\"2013-06-21T14:26:25.110520Z\"},{\"value\":\"0.46642667\",\"at\":\"2013-06-21T14:26:30.114982Z\"}],\"version\":\"1.0.0\"}"

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
    elif relative_url == 'feeds/61916':
        content = GET_FEED_61916
    elif relative_url == 'feeds/61916/datastreams/random5':
        content = GET_FEED_HISTORY_61916_DATASTREAM_RANDOM5
    elif relative_url == 'feeds/61916/datastreams/random60':
        content = GET_FEED_HISTORY_61916_DATASTREAM_RANDOM60
    elif relative_url == 'feeds/61916/datastreams/random900':
        content = GET_FEED_HISTORY_61916_DATASTREAM_RANDOM900
    elif relative_url == 'feeds/61916/datastreams/random3600':
        content = GET_FEED_HISTORY_61916_DATASTREAM_RANDOM3600
    elif relative_url == 'feeds/61916/datastreams/sawtooth60':
        content = GET_FEED_HISTORY_61916_DATASTREAM_SAWTOOTH60
    elif relative_url == 'feeds/61916/datastreams/sawtooth900':
        content = GET_FEED_HISTORY_61916_DATASTREAM_SAWTOOTH900
    elif relative_url == 'feeds/61916/datastreams/sawtooth3600':
        content = GET_FEED_HISTORY_61916_DATASTREAM_SAWTOOTH3600
    elif relative_url == 'feeds/61916/datastreams/triangle60':
        content = GET_FEED_HISTORY_61916_DATASTREAM_TRIANGLE60
    elif relative_url == 'feeds/61916/datastreams/triangle900':
        content = GET_FEED_HISTORY_61916_DATASTREAM_TRIANGLE900
    elif relative_url == 'feeds/61916/datastreams/triangle3600':
        content = GET_FEED_HISTORY_61916_DATASTREAM_TRIANGLE3600
    elif relative_url == 'feeds/61916/datastreams/sine60':
        content = GET_FEED_HISTORY_61916_DATASTREAM_SINE60
    elif relative_url == 'feeds/61916/datastreams/sine900':
        content = GET_FEED_HISTORY_61916_DATASTREAM_SINE900
    elif relative_url == 'feeds/61916/datastreams/sine3600':
        content = GET_FEED_HISTORY_61916_DATASTREAM_SINE3600
    elif relative_url == 'feeds/61916/datastreams/toggle5':
        content = GET_FEED_HISTORY_61916_DATASTREAM_TOGGLE5
    elif relative_url == 'feeds/61916/datastreams/toggle60':
        content = GET_FEED_HISTORY_61916_DATASTREAM_TOGGLE60
    elif relative_url == 'feeds/61916/datastreams/toggle900':
        content = GET_FEED_HISTORY_61916_DATASTREAM_TOGGLE900
    elif relative_url == 'feeds/61916/datastreams/toggle3600':
        content = GET_FEED_HISTORY_61916_DATASTREAM_TOGGLE3600
    if content:
        response._content = content
    return response
