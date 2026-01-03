# =============================================================================
# Recipe Management System - Automation Suite
# =============================================================================

$BaseUrl = "http://127.0.0.1:5000"
$DbPath = ".\instance\recipes.db"
$BackupPath = ".\backups"

# 1. Configure System Environment
function Configure-RecipeSystem {
    Write-Host "🏗️  Configuring Recipe System..." -ForegroundColor Cyan
    
    # Create directories
    if (!(Test-Path $BackupPath)) { New-Item -ItemType Directory -Force -Path $BackupPath | Out-Null }
    
    # Install Python dependencies if requirements.txt exists
    if (Test-Path "requirements.txt") {
        Write-Host "📦 Installing Python dependencies..."
        pip install -r requirements.txt
    } else {
        Write-Warning "requirements.txt not found."
    }

    Write-Host "✅ Configuration complete." -ForegroundColor Green
}

# 2. Seed Database with Sample Data
function Seed-RecipeDatabase {
    Write-Host "🌱 Seeding Database..." -ForegroundColor Cyan
    
    $recipes = @(
        @{
            title = "Classic Spaghetti Carbonara"
            description = "Roman pasta dish with eggs, cheese, bacon, and black pepper."
            ingredients = "Spaghetti`nEggs`nPecorino Romano`nGuanciale`nBlack Pepper"
            instructions = "Boil pasta.`nFry guanciale.`nMix eggs and cheese.`nCombine all off heat."
            cooking_time = 20
            difficulty = "Medium"
            cuisine = "Italian"
        },
        @{
            title = "Chicken Tikka Masala"
            description = "Roasted marinated chicken chunks in spiced curry sauce."
            ingredients = "Chicken`nYogurt`nTomato Puree`nGaram Masala`nCream"
            instructions = "Marinate chicken.`nGrill chicken.`nMake sauce.`nSimmer chicken in sauce."
            cooking_time = 45
            difficulty = "Hard"
            cuisine = "Indian"
        },
        @{
            title = "Avocado Toast"
            description = "Quick and healthy breakfast."
            ingredients = "Bread`nAvocado`nSalt`nChili Flakes"
            instructions = "Toast bread.`nMash avocado.`nSpread on toast.`nSeason."
            cooking_time = 5
            difficulty = "Easy"
            cuisine = "American"
        }
    )

    foreach ($r in $recipes) {
        try {
            $json = $r | ConvertTo-Json
            $response = Invoke-RestMethod -Uri "$BaseUrl/recipes" -Method Post -Body $json -ContentType "application/json"
            Write-Host "   + Added: $($r.title)" -ForegroundColor Gray
        } catch {
            Write-Error "Failed to add $($r.title). Is the server running?"
        }
    }
    Write-Host "✅ Seeding complete." -ForegroundColor Green
}

# 3. System Health Check
function Test-RecipeSystemHealth {
    Write-Host "🩺 Running Health Checks..." -ForegroundColor Cyan
    
    # API Check
    try {
        $health = Invoke-RestMethod -Uri "$BaseUrl/health" -Method Get -ErrorAction Stop
        Write-Host "   [PASS] API is online (Status: $($health.status))" -ForegroundColor Green
    } catch {
        Write-Host "   [FAIL] API is unreachable" -ForegroundColor Red
    }

    # DB File Check
    # Note: Flask creates 'instance' folder for db
    if (Test-Path ".\recipes.db") { 
        Write-Host "   [PASS] Database file found (Root)" -ForegroundColor Green 
    } elseif (Test-Path ".\instance\recipes.db") {
        Write-Host "   [PASS] Database file found (Instance)" -ForegroundColor Green
    } else {
        Write-Host "   [WARN] Database file not found yet" -ForegroundColor Yellow
    }

    # Disk Space
    $disk = Get-PSDrive C | Select-Object Used,Free
    Write-Host "   [INFO] Disk Free: $([math]::round($disk.Free/1GB, 2)) GB" -ForegroundColor Gray
}

# 4. Database Backup
function Backup-RecipeDatabase {
    Write-Host "💾 Starting Backup..." -ForegroundColor Cyan
    
    # Find DB (Flask 3.0+ usually puts it in /instance)
    $TargetDb = ".\instance\recipes.db"
    if (!(Test-Path $TargetDb)) { $TargetDb = ".\recipes.db" }

    if (Test-Path $TargetDb) {
        $timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
        $backupFile = "$BackupPath\recipes_backup_$timestamp.db"
        
        Copy-Item -Path $TargetDb -Destination $backupFile
        Write-Host "   + Backup created: $backupFile" -ForegroundColor Green
        
        # Retention Policy (Keep last 10)
        $backups = Get-ChildItem -Path $BackupPath -Filter "*.db" | Sort-Object CreationTime -Descending
        if ($backups.Count -gt 10) {
            $backups | Select-Object -Skip 10 | Remove-Item
            Write-Host "   - Cleaned up old backups" -ForegroundColor Yellow
        }
    } else {
        Write-Error "Database file not found to backup."
    }
}

# 5. Full Deployment (Simulated)
function Deploy-RecipeSystem {
    Write-Host "🚀 Deploying Recipe System..." -ForegroundColor Cyan
    Configure-RecipeSystem
    Start-Sleep -Seconds 2
    
    Write-Host "   Starting Backend (Background Process)..."
    # In a real scenario, use Start-Process or a Service manager
    # Start-Process python -ArgumentList "app.py" -WindowStyle Minimized
    
    Start-Sleep -Seconds 5
    Test-RecipeSystemHealth
    
    Write-Host "   Seeding initial data..."
    Seed-RecipeDatabase
    
    Write-Host "✅ Deployment Sequence Finished." -ForegroundColor Green
}

# Export functions for session use
Export-ModuleMember -Function *
