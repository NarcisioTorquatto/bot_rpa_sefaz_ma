$exclude = @("venv", "desafio_06_LG.zip")
$files = Get-ChildItem -Path . -Exclude $exclude
Compress-Archive -Path $files -DestinationPath "desafio_06_LG.zip" -Force