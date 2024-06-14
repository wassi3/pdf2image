# process_pdfs.ps1 - PowerShell script that calls pdf2image.py for extracting images from all PDFs of a directory

param (
    [string]$pdfDirectory = "."
)

# Enable script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

# Get the specified directory
$searchDir = Resolve-Path -Path $pdfDirectory
Write-Host "Search directory: $searchDir"

# Get all PDF files in the specified directory and its subdirectories
$pdfFiles = Get-ChildItem -Path $searchDir -Recurse -Filter *.pdf

# Check if there are any PDF files
if ($pdfFiles.Count -eq 0) {
    Write-Host "No PDF files found in the specified directory."
} else {
    Write-Host "$($pdfFiles.Count) PDF files found in the specified directory."
}

# Loop through each PDF file and call the Python script
foreach ($file in $pdfFiles) {
    $relativePath = $file.FullName
    Write-Host "Processing file: $relativePath"
    #$command = "python .\script.py `"$relativePath`""
    Write-Host "Executing command: python .\pdf2image.py `"$relativePath`""
    $output = & python .\pdf2image.py "$relativePath" 2>&1
    Write-Host "Output: $output"
}

Write-Host "Script execution completed."
