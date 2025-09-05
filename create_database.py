import sqlite3
import os
from werkzeug.security import generate_password_hash


def create_tables():
    # Remove existing database file for fresh start
    if os.path.exists('nexustrace.db'):
        os.remove('nexustrace.db')
    
    conn = sqlite3.connect('nexustrace.db')
    cursor = conn.cursor()
    
    print("Creating enhanced database schema with case management...")
    
    # Users table - Enhanced with roles and permissions
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            full_name TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'analyst',
            is_active BOOLEAN DEFAULT 1,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            preferences TEXT DEFAULT '{}'
        )
    ''')
    
    # Enhanced Cases table - Multi-analysis investigation management
    cursor.execute('''
        CREATE TABLE cases (
            case_id TEXT PRIMARY KEY,
            case_name TEXT NOT NULL,
            case_description TEXT,
            case_type TEXT DEFAULT 'incident_response',
            priority_level TEXT DEFAULT 'medium',
            status TEXT DEFAULT 'active',
            lead_investigator TEXT,
            created_by INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            closed_at TIMESTAMP NULL,
            case_metadata TEXT DEFAULT '{}',
            tags TEXT DEFAULT '[]',
            FOREIGN KEY (created_by) REFERENCES users (id)
        )
    ''')
    
    # Memory dumps table - Enhanced with better metadata
    cursor.execute('''
        CREATE TABLE memory_dumps (
            dump_id TEXT PRIMARY KEY,
            case_id TEXT NOT NULL,
            filename TEXT NOT NULL,
            filepath TEXT NOT NULL,
            file_size INTEGER,
            sha256_hash TEXT,
            md5_hash TEXT,
            upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            os_detected TEXT,
            os_selected TEXT,
            metadata TEXT DEFAULT '{}',
            analysis_status TEXT DEFAULT 'pending',
            FOREIGN KEY (case_id) REFERENCES cases (case_id) ON DELETE CASCADE
        )
    ''')
    
    # Analysis sessions table - Enhanced for case management
    cursor.execute('''
        CREATE TABLE analysis_sessions (
            session_id TEXT PRIMARY KEY,
            dump_id TEXT NOT NULL,
            case_id TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            session_data TEXT DEFAULT '{}',
            analysis_results TEXT,
            plugins_executed TEXT DEFAULT '[]',
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            session_status TEXT DEFAULT 'active',
            analysis_duration REAL DEFAULT 0,
            memory_optimized BOOLEAN DEFAULT 0,
            FOREIGN KEY (dump_id) REFERENCES memory_dumps (dump_id) ON DELETE CASCADE,
            FOREIGN KEY (case_id) REFERENCES cases (case_id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Case analyses relationship table - Links analyses to cases
    cursor.execute('''
        CREATE TABLE case_analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_id TEXT NOT NULL,
            session_id TEXT NOT NULL,
            analysis_role TEXT DEFAULT 'primary',
            system_identifier TEXT,
            analysis_order INTEGER DEFAULT 0,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (case_id) REFERENCES cases (case_id) ON DELETE CASCADE,
            FOREIGN KEY (session_id) REFERENCES analysis_sessions (session_id) ON DELETE CASCADE
        )
    ''')
    
    # Cross-case IoC correlation table
    cursor.execute('''
        CREATE TABLE case_iocs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_id TEXT NOT NULL,
            session_id TEXT NOT NULL,
            ioc_type TEXT NOT NULL,
            ioc_value TEXT NOT NULL,
            ioc_context TEXT,
            confidence_score REAL DEFAULT 0.5,
            first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            occurrence_count INTEGER DEFAULT 1,
            FOREIGN KEY (case_id) REFERENCES cases (case_id) ON DELETE CASCADE,
            FOREIGN KEY (session_id) REFERENCES analysis_sessions (session_id) ON DELETE CASCADE
        )
    ''')
    
    # Timeline correlation across dumps
    cursor.execute('''
        CREATE TABLE case_timeline (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_id TEXT NOT NULL,
            session_id TEXT NOT NULL,
            event_timestamp TIMESTAMP,
            event_type TEXT,
            event_description TEXT,
            system_identifier TEXT,
            risk_score INTEGER DEFAULT 0,
            correlation_group TEXT,
            event_metadata TEXT DEFAULT '{}',
            FOREIGN KEY (case_id) REFERENCES cases (case_id) ON DELETE CASCADE,
            FOREIGN KEY (session_id) REFERENCES analysis_sessions (session_id) ON DELETE CASCADE
        )
    ''')
    
    # Enhanced Plugin results table
    cursor.execute('''
        CREATE TABLE plugin_results (
            result_id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            plugin_name TEXT NOT NULL,
            result_data TEXT,
            execution_time REAL,
            success BOOLEAN DEFAULT 1,
            error_message TEXT,
            records_found INTEGER DEFAULT 0,
            records_truncated BOOLEAN DEFAULT 0,
            memory_usage REAL DEFAULT 0,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES analysis_sessions (session_id) ON DELETE CASCADE
        )
    ''')
    
    # Forensic analysis results table - IoCs, YARA, Risk Scores
    cursor.execute('''
        CREATE TABLE forensic_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            case_id TEXT NOT NULL,
            analysis_type TEXT NOT NULL,
            analysis_data TEXT NOT NULL,
            risk_score REAL DEFAULT 0,
            confidence REAL DEFAULT 0,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES analysis_sessions (session_id) ON DELETE CASCADE,
            FOREIGN KEY (case_id) REFERENCES cases (case_id) ON DELETE CASCADE
        )
    ''')
    
    # Export audit log
    cursor.execute('''
        CREATE TABLE export_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            case_id TEXT,
            user_id INTEGER NOT NULL,
            export_format TEXT NOT NULL,
            export_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            file_size INTEGER DEFAULT 0,
            export_metadata TEXT DEFAULT '{}',
            FOREIGN KEY (session_id) REFERENCES analysis_sessions (session_id),
            FOREIGN KEY (case_id) REFERENCES cases (case_id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Create indexes for performance
    print("Creating database indexes...")
    
    # Case management indexes
    cursor.execute('CREATE INDEX idx_case_analyses_case ON case_analyses (case_id, analysis_order)')
    cursor.execute('CREATE INDEX idx_case_iocs_value ON case_iocs (ioc_value)')
    cursor.execute('CREATE INDEX idx_case_iocs_type ON case_iocs (case_id, ioc_type)')
    cursor.execute('CREATE INDEX idx_case_timeline ON case_timeline (case_id, event_timestamp)')
    
    # Session and analysis indexes
    cursor.execute('CREATE INDEX idx_sessions_case ON analysis_sessions (case_id)')
    cursor.execute('CREATE INDEX idx_sessions_user ON analysis_sessions (user_id)')
    cursor.execute('CREATE INDEX idx_plugin_results_session ON plugin_results (session_id)')
    cursor.execute('CREATE INDEX idx_forensic_analysis_session ON forensic_analysis (session_id)')
    cursor.execute('CREATE INDEX idx_forensic_analysis_case ON forensic_analysis (case_id)')
    
    # Memory dump indexes  
    cursor.execute('CREATE INDEX idx_dumps_case ON memory_dumps (case_id)')
    cursor.execute('CREATE INDEX idx_dumps_hash ON memory_dumps (sha256_hash)')
    
    # Export log indexes
    cursor.execute('CREATE INDEX idx_export_log_user ON export_log (user_id)')
    cursor.execute('CREATE INDEX idx_export_log_timestamp ON export_log (export_timestamp)')
    
    # Create default users
    print("Creating default users...")
    
    # Admin user
    admin_hash = generate_password_hash('admin123')
    cursor.execute('''
        INSERT INTO users (username, email, full_name, password_hash, role)
        VALUES (?, ?, ?, ?, ?)
    ''', ('admin', 'admin@nexustrace.com', 'System Administrator', admin_hash, 'admin'))
    
    # Analyst user  
    analyst_hash = generate_password_hash('analyst123')
    cursor.execute('''
        INSERT INTO users (username, email, full_name, password_hash, role)
        VALUES (?, ?, ?, ?, ?)
    ''', ('analyst', 'analyst@nexustrace.com', 'Forensic Analyst', analyst_hash, 'analyst'))
    
    # Create sample case for demonstration
    cursor.execute('''
        INSERT INTO cases (case_id, case_name, case_description, case_type, priority_level, 
                          lead_investigator, created_by, case_metadata)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        'case_sample_001',
        'Sample Investigation Case',
        'Demonstration case for NexusTrace platform capabilities',
        'incident_response',
        'medium',
        'admin',
        1,
        '{"demo": true, "training": true}'
    ))
    
    conn.commit()
    conn.close()
    
    print("✅ Enhanced database schema created successfully!")
    print("🔧 Case management system enabled")
    print("📊 Forensic analysis tables configured")
    print("🔍 Cross-analysis correlation ready")
    print("📤 Export audit logging enabled")
    print()
    print("👤 Default users created:")
    print("   🔐 Admin: admin / admin123")
    print("   🕵️ Analyst: analyst / analyst123")
    print()
    print("📁 Sample case created: case_sample_001")


if __name__ == '__main__':
    create_tables()
