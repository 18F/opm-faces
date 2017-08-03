## /api/prototypes/read
### Request structure
Method(s): GET
*No payload or parameters required.*
### Call
```
curl -X GET http://127.0.0.1:5000/api/prototypes/read
```
### Response
```
{
  "animal": {
    "height": null,
    "rules": [
      "test_tall"
    ],
    "type": "animal"
  }
}
```
## /api/prototypes/write
### Request structure
Method(s): POST
```
{
    "name": "",
    "attribute_0": "",
    "attribute_1": "",
    "attribute_2": "",
    "attribute_3": "",
    "attribute_4": "",
    ...
}
```
### Call
```
curl -H "Content-Type: application/json" -X POST -d '{"name":"animal","attribute_0":"height"}' http://127.0.0.1:5000/api/prototypes/write
```
### Response
```
{
  "animal": {
    "height": null,
    "rules": [],
    "type": "animal"
  }
}
```
