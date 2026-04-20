$api = Invoke-RestMethod 'http://127.0.0.1:17888/api/state' -TimeoutSec 3
$json = Get-Content 'C:\Users\Administrator\.openclaw\workspace\pain_state.json' | ConvertFrom-Json
Write-Host "API  is_restless:" $api.is_restless "felt_pain:" $api.felt_pain
Write-Host "JSON is_restless:" $json.is_restless "felt_pain:" $json.felt_pain
Write-Host "JSON timestamp:" $json.timestamp
