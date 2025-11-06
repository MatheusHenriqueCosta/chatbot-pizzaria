<#
  setup_deepseek.ps1
  - Pergunta pela DEEPSEEK_API_KEY de forma segura
  - Ativa o venv local (.venv)
  - Define a variável de ambiente na sessão atual
  - Opcional: pergunta e define DEEPSEEK_MODEL e DEEPSEEK_API_URL
  - Roda `python app.py` no ambiente virtual

  Uso: abra PowerShell na pasta do projeto e rode:
    .\setup_deepseek.ps1

  Observação: a chave não é enviada a ninguém; ela fica apenas na sessão do PowerShell.
#>

Write-Host "=== Setup Deepseek (sessão atual) ===" -ForegroundColor Cyan

# Ler a chave de forma segura
$secureKey = Read-Host "Insira sua DEEPSEEK_API_KEY (entrada oculta)" -AsSecureString
$ptr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureKey)
$apiKey = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($ptr)
[Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr)

if ([string]::IsNullOrWhiteSpace($apiKey)) {
    Write-Host "Chave vazia. Abortando." -ForegroundColor Red
    exit 1
}

# Opcional: ler modelo e endpoint
$model = Read-Host "DEEPSEEK_MODEL (pressione Enter para usar default 'deepseek/deepseek-r1:free')"
if ([string]::IsNullOrWhiteSpace($model)) { $model = 'deepseek/deepseek-r1:free' }

$apiUrl = Read-Host "DEEPSEEK_API_URL (pressione Enter para usar default 'https://openrouter.ai/api/v1/chat/completions')"
if ([string]::IsNullOrWhiteSpace($apiUrl)) { $apiUrl = 'https://openrouter.ai/api/v1/chat/completions' }

# Ativar venv se existir
$venvPath = Join-Path -Path (Get-Location) -ChildPath '.venv\Scripts\Activate.ps1'
if (Test-Path $venvPath) {
    Write-Host "Ativando venv..." -ForegroundColor Green
    . $venvPath
} else {
    Write-Host "Atenção: venv não encontrado em .venv. Verifique se você criou o ambiente virtual." -ForegroundColor Yellow
}

# Definir variáveis de ambiente na sessão atual
$env:DEEPSEEK_API_KEY = $apiKey
$env:DEEPSEEK_MODEL = $model
$env:DEEPSEEK_API_URL = $apiUrl

Write-Host "Variáveis definidas na sessão atual (DEEPSEEK_API_KEY oculto)." -ForegroundColor Green
Write-Host "DEEPSEEK_MODEL = $model" -ForegroundColor Green
Write-Host "DEEPSEEK_API_URL = $apiUrl" -ForegroundColor Green

# Iniciar a aplicação
Write-Host "Iniciando app.py... (será executado no terminal atual)" -ForegroundColor Cyan
python app.py

Write-Host "app.py finalizado (se saiu)." -ForegroundColor Cyan
