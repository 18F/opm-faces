## /api
### Request structure
Method(s): GET

*No payload or parameters required.*

### Call
```
curl -X GET http://127.0.0.1:5000/api
```
### Response
```
{
  "endpoints": [
    {
      "actions": [
        {
          "method": "GET",
          "route": "./read"
        },
        {
          "method": "POST",
          "route": "./write"
        }
      ],
      "route": "/prototypes"
    },
    {
      "actions": [
        {
          "method": "GET",
          "route": "./read"
        },
        {
          "method": "POST",
          "route": "./write"
        }
      ],
      "route": "/calculations"
    },
    {
      "actions": [
        {
          "method": "GET",
          "route": "./read"
        },
        {
          "method": "POST",
          "route": "./write"
        }
      ],
      "route": "/rules"
    },
    {
      "actions": [
        {
          "method": "GET",
          "route": "./read"
        },
        {
          "method": "POST",
          "route": "./write"
        }
      ],
      "route": "/data"
    }
  ]
}
```
