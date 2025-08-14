# Example Pester test file with proper structure
Describe "Example Tests" {
    
    # The In command can be used here to temporarily change directory context
    In "C:\Users\nino1\curriculum-streamlit" {
        
        It "Should verify the current directory" {
            Get-Location | Should -Be "C:\Users\nino1\curriculum-streamlit"
        }
        
        It "Should check if main Python files exist" {
            Test-Path "analytics_dashboard.py" | Should -Be $true
            Test-Path "auth_system.py" | Should -Be $true
        }
        
        It "Should verify Python files are not empty" {
            (Get-Content "analytics_dashboard.py" | Measure-Object -Line).Lines | Should -BeGreaterThan 0
        }
    }
    
    # You can have multiple In blocks within the same Describe
    In "C:\Users\nino1" {
        
        It "Should be in the home directory" {
            Get-Location | Should -Be "C:\Users\nino1"
        }
        
        It "Should have access to curriculum-streamlit folder" {
            Test-Path "curriculum-streamlit" | Should -Be $true
        }
    }
}

# You can have multiple Describe blocks
Describe "Streamlit Application Tests" {
    
    In "C:\Users\nino1\curriculum-streamlit" {
        
        It "Should have required Python dependencies listed" {
            # Check if requirements.txt or similar exists
            $hasRequirements = (Test-Path "requirements.txt") -or (Test-Path "environment.yml") -or (Test-Path "pyproject.toml")
            $hasRequirements | Should -Be $true
        }
        
        It "Should contain Streamlit-related files" {
            $pythonFiles = Get-ChildItem -Filter "*.py" -File
            $streamlitFiles = $pythonFiles | Where-Object { (Get-Content $_.FullName -Raw) -match "streamlit|st\." }
            $streamlitFiles.Count | Should -BeGreaterThan 0
        }
    }
}
