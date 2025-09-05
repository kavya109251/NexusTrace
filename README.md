# NexusTrace

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-beta-orange.svg)]()

**Advanced Memory Forensics Analysis Platform**

NexusTrace is a comprehensive memory forensics analysis platform that provides automated threat detection, process tree visualization, IoC extraction, and multi-dump case management for digital forensic investigations.

![NexusTrace Dashboard](docs/images/dashboard.png)

## 🚀 Features

### Core Forensic Capabilities
- **🔍 IoC Extraction** - Automatic extraction of network, file, process, and registry indicators
- **🌳 Process Tree Visualization** - Interactive process hierarchy with threat analysis
- **⚡ Enhanced Risk Scoring** - Multi-factor intelligent threat assessment
- **🛡️ YARA Scanning** - Malware signature detection with custom rules
- **📊 Timeline Analysis** - Event correlation and attack reconstruction

### Investigation Workflow
- **📁 Case Management** - Multi-dump investigation with cross-system correlation
- **🔗 IoC Correlation** - Find threats across multiple memory dumps
- **📈 Comparative Analysis** - Identify most/least compromised systems
- **👥 Multi-user Support** - Collaborative investigation capabilities

### Export & Integration
- **📤 Multiple Export Formats** - MISP, STIX, JSON, CSV, HTML reports
- **🔌 API Integration** - RESTful API for automated workflows
- **📋 Professional Reports** - Executive summaries and technical findings
- **🎯 Threat Intelligence** - Direct integration with security platforms

## 📋 Requirements

### System Requirements
- **Python**: 3.8 or higher
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 50GB+ for memory dump storage
- **OS**: Windows, Linux, macOS

### Dependencies
- **Volatility3** - Memory analysis framework
- **YARA** - Pattern matching engine
- **Flask** - Web framework
- **SQLite** - Database (included with Python)

## 🛠️ Installation

### Option 1: Quick Setup (Recommended)
```bash
git clone https://github.com/your-repo/nexustrace.git
cd nexustrace
python setup_nexustrace.py
```

### Option 2: Manual Setup
## Step 1: Install Dependencies
```bash
Step 1: Install Dependencies
python -m venv nexustrace-env
source nexustrace-env/bin/activate  # Linux/Mac
or
nexustrace-env\Scripts\activate     # Windows

pip install -r requirements.txt
```

## Step 2: Initialize Database
```bash
python scripts/create_database.py
```

## Step 3: Create Required Directories
```bash
mkdir -p memory_dumps output/plugins output/dumps sessions \
         yara_rules/malware yara_rules/general yara_rules/custom \
         config logs
```

## Step 4: Set Up YARA Rules (Optional)
```bash
cat > yara_rules/malware/basic_rules.yar << 'EOF'
rule Suspicious_PowerShell_Commands
{
    meta:
        description = "Detects suspicious PowerShell command patterns"
        author = "NexusTrace"
        severity = "Medium"

    strings:
        $cmd1 = "powershell -enc" nocase
        $cmd2 = "powershell -encodedcommand" nocase
        $cmd3 = "invoke-expression" nocase
        $cmd4 = "downloadstring" nocase

    condition:
        any of ($cmd*)
}
EOF
```

## Step 5: Run NexusTrace
```bash
python web/app.py
```

## Open browser and navigate to:
```bash
http://localhost:5000
```

