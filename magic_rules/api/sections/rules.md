## /api/rules/read
### Request structure
Method(s): GET
*No payload or parameters required.*
### Call
```
curl -X GET http://127.0.0.1:5000/api/rules/read
```
### Response
```
{
  "test_tall": {
    "attribute": "height",
    "compare_value": "5",
    "concur": "_double_height",
    "name": "test_tall",
    "not_concur": "tall enough already",
    "operator": "<=",
    "type": "logic"
  }
}
```
## /api/rules/write
### Request structure
Method(s): POST
```
{
    "name": "",
    "object": "",
    "operator": ""
    "attribute": "",
    "compare_value": "",
    "concur_static": "",
    "concur_calc": "",
    "not_concur_calc": "",
    "not_concur_static": "",
}
```
### Call
```
curl -H "Content-Type: application/json" -X POST -d '{"name":"test_tall", "object":"animal", "operator":"<=", "attribute":"height", "compare_value":"5", "concur_static":"", "concur_calc":"_double_height", "not_concur_static":"tall enough already", "not_concur_calc":""}' http://127.0.0.1:5000/api/rules/write
```
### Response
```
{
  "test_tall": {
    "attribute": "height",
    "compare_value": "5",
    "concur": "_double_height",
    "name": "test_tall",
    "not_concur": "tall enough already",
    "operator": "<=",
    "type": "logic"
  }
}
```
