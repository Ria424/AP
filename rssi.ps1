chcp 437
$signalLine = netsh wlan show interfaces | Select-String "Signal"
if ($signalLine) {
    $signalPercent = [int]($signalLine -replace '[^\d]', '')
    $rssi = ($signalPercent / 2) - 100
    Write-Host "Wi-Fi Signal Strength: $signalPercent% ($rssi dBm)"
} else {
    Write-Host "No Wi-Fi connection detected."
}
