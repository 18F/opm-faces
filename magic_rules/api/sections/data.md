## /api/rules/read
### Request structure
Method(s): GET
*No payload or parameters required.*
### Call
```
curl -X GET http://127.0.0.1:5000/api/data/read
```
### Response
```
[
  {
    "height": "4",
    "rules": [
      "test_tall"
    ],
    "test_tall": "8",
    "type": "animal"
  }
]
```

## /api/data/write
### Request structure
Method(s): POST
```
    {
        "type": "",
        ... # Any attributes available from the prototype.

    }
```
### Call
```
curl -H "Content-Type: application/json" -X POST -d '{"type":"animal","height":"4"}' http://127.0.0.1:5000/api/data/write
```
### Response
```
{
  "height": "4",
  "rules": [
    "test_tall"
  ],
  "test_tall": "8",
  "type": "animal"
}
```
