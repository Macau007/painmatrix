$times = @()
for ($i = 0; $i -lt 20; $i++) {
    $api = Invoke-RestMethod 'http://127.0.0.1:17888/api/state' -TimeoutSec 3
    $json = Get-Content 'C:\Users\Administrator\.openclaw\workspace\pain_state.json' | ConvertFrom-Json
    $t = Get-Date -Format 'HH:mm:ss'
    $times += "$t API=$($api.is_restless) JSON=$($json.is_restless) PG=$($api.is_restless)"
    Start-Sleep 1
}
$times | ForEach-Object { Write-Host $_ }
