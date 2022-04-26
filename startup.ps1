$TargetFile = "$PSScriptRoot\ServiceInfo.exe"
$ShortcutFile = "$env:userprofile\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\ServiceInfo.lnk"
$WScriptShell = New-Object -ComObject WScript.Shell
$Shortcut = $WScriptShell.CreateShortcut($ShortcutFile)
$Shortcut.TargetPath = $TargetFile
$Shortcut.WorkingDirectory = $PSScriptRoot
$Shortcut.Save()

$bytes = [System.IO.File]::ReadAllBytes($ShortcutFile)
$bytes[0x15] = $bytes[0x15] -bor 0x20 #set byte 21 (0x15) bit 6 (0x20) ON
[System.IO.File]::WriteAllBytes($ShortcutFile, $bytes)