0..19 | ForEach-Object {
    $t = (Get-Date).ToString('HH:mm:ss')
    try {
        $d = Invoke-RestMethod 'http://127.0.0.1:17888/api/state' -TimeoutSec 3
        Write-Host "$t is_restless=$($d.is_restless) felt_pain=$($d.felt_pain)"
    } catch {
        Write-Host "$t ERROR: $_"
    }
    Start-Sleep 1
}
