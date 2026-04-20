Get-NetTCPConnection -LocalPort 17888 -ErrorAction SilentlyContinue | Where-Object { $_.OwningProcess -ne 0 } | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue; Write-Host "killed" $_.OwningProcess }
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep 2
$r = Get-NetTCPConnection -LocalPort 17888 -ErrorAction SilentlyContinue | Where-Object { $_.OwningProcess -ne 0 }
if ($r) { Write-Host "still running:" $r.OwningProcess } else { Write-Host "17888 is clear" }
