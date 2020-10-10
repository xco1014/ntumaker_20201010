# ntumaker_20201010

Add `./src/config.json` with this ewhich  following properties:
subscribe donataion event
|Variable|Type|Description|
|---|---|---|
|SOCKET_API_TOKEN|string|[Token to streamlabs](https://streamlabs.com/dashboard/#/settings/api-settings), which is used to subscribe donataion event|
|Verbose|boolean|Whether to show verbose log|
|pythonCmd|string|Command of python 3.x, usually are "python" or "python3"|

* example:
```json
{
  "SOCKET_API_TOKEN": "YOUR_SOCKET_API_TOKEN",
  "Verbose":false,
  "pythonCmd": "python"
}
```
