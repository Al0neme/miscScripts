param (
    [string]$file
)

if (-not $file) {
    Write-Host "Usage: .\$($MyInvocation.MyCommand) <file>"
    exit 1
}

$lines = Get-Content -Path $file

foreach ($line in $lines) {
    if ($line -match '^http?.*\.git$') {
        $repoName = [System.IO.Path]::GetFileNameWithoutExtension($line)

        if (Test-Path -Path $repoName) {
            Write-Host "Directory $repoName already exists, skipping clone."
        } else {
            Write-Host "Cloning Git repository: $line"
            git clone $line | Out-Null
            Write-Host "[+] ok"
        }

    } elseif ($line -match '^http') {
        $url, $dir = $line -split ' '

        if (-not (Test-Path -Path $dir)) {
            New-Item -ItemType Directory -Path $dir | Out-Null
            Write-Host "Created directory: $dir"
        }

        $fileName = [System.IO.Path]::GetFileName($url)
        if (Test-Path -Path (Join-Path -Path $dir -ChildPath $fileName)) {
            Write-Host "File $fileName already exists in $dir, skipping download."
        } else {
            Write-Host "Downloading $url to $dir"
            Invoke-WebRequest -Uri $url -OutFile (Join-Path -Path $dir -ChildPath $fileName) -ErrorAction Stop
            Write-Host "[+] ok"
        }
    } else {
        Write-Host "Skipping: $line (not a valid Git repo or URL)"
    }
}
