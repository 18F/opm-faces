## /api/calculations/read
### Request structure
Method(s): GET
*No payload or parameters required.*
### Call
```
curl -X GET http://127.0.0.1:5000/api/calculations/read
```
### Response
```
{
  "double_height": {
    "data": "2*__height__",
    "name": "double_height",
    "type": "calc"
  }
}
```
## /api/calculations/write
### Request structure
Method(s): POST
```
    {
        "object": "",
        "name": "",
        "contingent": "",
        "static_value_0": "",
        "attribute_value_0": "",
        "operator_value_0": "",
        "static_value_1": "",
        "attribute_value_1": "",
        "operator_value_1": "",
        "static_value_2": "",
        "attribute_value_2": "",
        "operator_value_2": "",
        "attribute_value_3": "",
        "static_value_3": "",
        "operator_value_3": "",
        "static_value_4": "",
        "attribute_value_4": "",
        "operator_value_4": "",
        "static_value_5": "",
        "attribute_value_5": "",
        ...
    }
```
### Call
```
curl -H "Content-Type: application/json" -X POST -d '{"name":"double_height", "object":"animal", "contingent": "TRUE", "static_value_0":"2", "attribute_value_0":"", "operator_value_0":"*","static_value_1":"", "attribute_value_1":"__height__"}' http://127.0.0.1:5000/api/calculations/write
```
### Response
```
{
  "data": "2*__height__",
  "name": "double_height",
  "type": "calc"
}
```
