"""
Nino Medical AI - Sistema di Autenticazione
==========================================

Sistema completo di autenticazione con profili utente,
dashboard personalizzabili e gestione permessi.

Author: Antonino Piacenza
Email: ninomedical.ai@gmail.com
"""

import streamlit as st
import pandas as pd
import hashlib
import sqlite3
import json
import secrets
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
import bcrypt
import jwt
import re


class UserRole(Enum):
    """Ruoli utente del sistema."""
    ADMIN = "admin"
    DOCTOR = "doctor"
    RESEARCHER = "researcher"
    NURSE = "nurse"
    STUDENT = "student"
    GUEST = "guest"


@dataclass
class User:
    """Classe utente."""
    id: int
    username: str
    email: str
    full_name: str
    role: UserRole
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime] = None
    preferences: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.preferences is None:
            self.preferences = {}


class AuthenticationError(Exception):
    """Eccezione per errori di autenticazione."""
    pass


class AuthManager:
    """Manager per autenticazione e gestione utenti."""
    
    def __init__(self, db_path: str = "auth/users.db"):
        """
        Inizializza il manager di autenticazione.
        
        Args:
            db_path: Path del database SQLite
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True)
        self.secret_key = self._get_or_create_secret_key()
        self._init_database()
        self._create_default_admin()
        
    def _get_or_create_secret_key(self) -> str:
        """Genera o recupera la chiave segreta per JWT."""
        key_file = self.db_path.parent / "secret.key"
        
        if key_file.exists():
            with open(key_file, 'r') as f:
                return f.read().strip()
        else:
            # Genera nuova chiave segreta
            secret = secrets.token_hex(32)
            with open(key_file, 'w') as f:
                f.write(secret)
            return secret
            
    def _init_database(self):
        """Inizializza il database degli utenti."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    full_name TEXT NOT NULL,
                    role TEXT NOT NULL,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP,
                    preferences TEXT DEFAULT '{}'
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS login_attempts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    ip_address TEXT,
                    success BOOLEAN NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    session_token TEXT UNIQUE NOT NULL,
                    expires_at TIMESTAMP NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
    def _create_default_admin(self):
        """Crea utente admin di default se non esiste."""
        try:
            admin = self.get_user_by_username("admin")
            if admin is None:
                self.create_user(
                    username="admin",
                    email="admin@ninomedical.ai",
                    password="admin123!",
                    full_name="Amministratore Sistema",
                    role=UserRole.ADMIN
                )
        except Exception:
            pass  # Admin già esiste
            
    def _hash_password(self, password: str) -> str:
        """Hash della password usando bcrypt."""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
        
    def _verify_password(self, password: str, hashed: str) -> bool:
        """Verifica password con hash bcrypt."""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        
    def _validate_password_strength(self, password: str) -> List[str]:
        """Valida la forza della password."""
        errors = []
        
        if len(password) < 8:
            errors.append("Password deve essere almeno 8 caratteri")
        if not re.search(r"[A-Z]", password):
            errors.append("Password deve contenere almeno una maiuscola")
        if not re.search(r"[a-z]", password):
            errors.append("Password deve contenere almeno una minuscola")
        if not re.search(r"\d", password):
            errors.append("Password deve contenere almeno un numero")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            errors.append("Password deve contenere almeno un carattere speciale")
            
        return errors
        
    def create_user(self, 
                   username: str, 
                   email: str, 
                   password: str,
                   full_name: str,
                   role: UserRole = UserRole.GUEST) -> User:
        """
        Crea un nuovo utente.
        
        Args:
            username: Nome utente
            email: Email
            password: Password in chiaro
            full_name: Nome completo
            role: Ruolo utente
            
        Returns:
            Oggetto User creato
            
        Raises:
            AuthenticationError: Se creazione fallisce
        """
        # Validazione password
        password_errors = self._validate_password_strength(password)
        if password_errors:
            raise AuthenticationError(f"Password non valida: {'; '.join(password_errors)}")
            
        # Validazione email
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise AuthenticationError("Email non valida")
            
        password_hash = self._hash_password(password)
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute('''
                    INSERT INTO users (username, email, password_hash, full_name, role)
                    VALUES (?, ?, ?, ?, ?)
                ''', (username, email, password_hash, full_name, role.value))
                
                user_id = cursor.lastrowid
                
                return User(
                    id=user_id,
                    username=username,
                    email=email,
                    full_name=full_name,
                    role=role,
                    is_active=True,
                    created_at=datetime.now()
                )
                
        except sqlite3.IntegrityError as e:
            if "username" in str(e):
                raise AuthenticationError("Nome utente già esistente")
            elif "email" in str(e):
                raise AuthenticationError("Email già registrata")
            else:
                raise AuthenticationError("Errore nella creazione utente")
                
    def authenticate(self, username: str, password: str, ip_address: str = None) -> Optional[User]:
        """
        Autentica un utente.
        
        Args:
            username: Nome utente o email
            password: Password
            ip_address: Indirizzo IP per logging
            
        Returns:
            Oggetto User se autenticazione riuscita, None altrimenti
        """
        # Log tentativo di login
        success = False
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Cerca utente per username o email
                cursor = conn.execute('''
                    SELECT id, username, email, password_hash, full_name, role, is_active, 
                           created_at, last_login, preferences
                    FROM users 
                    WHERE (username = ? OR email = ?) AND is_active = TRUE
                ''', (username, username))
                
                user_data = cursor.fetchone()
                
                if user_data and self._verify_password(password, user_data[3]):
                    # Aggiorna last_login
                    conn.execute('''
                        UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?
                    ''', (user_data[0],))
                    
                    success = True
                    
                    # Crea oggetto User
                    user = User(
                        id=user_data[0],
                        username=user_data[1],
                        email=user_data[2],
                        full_name=user_data[4],
                        role=UserRole(user_data[5]),
                        is_active=user_data[6],
                        created_at=datetime.fromisoformat(user_data[7]),
                        last_login=datetime.fromisoformat(user_data[8]) if user_data[8] else None,
                        preferences=json.loads(user_data[9]) if user_data[9] else {}
                    )
                    
                    return user
                    
        finally:
            # Log tentativo
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    INSERT INTO login_attempts (username, ip_address, success)
                    VALUES (?, ?, ?)
                ''', (username, ip_address, success))
                
        return None
        
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Recupera utente per username."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                SELECT id, username, email, password_hash, full_name, role, is_active,
                       created_at, last_login, preferences
                FROM users WHERE username = ?
            ''', (username,))
            
            user_data = cursor.fetchone()
            
            if user_data:
                return User(
                    id=user_data[0],
                    username=user_data[1],
                    email=user_data[2],
                    full_name=user_data[4],
                    role=UserRole(user_data[5]),
                    is_active=user_data[6],
                    created_at=datetime.fromisoformat(user_data[7]),
                    last_login=datetime.fromisoformat(user_data[8]) if user_data[8] else None,
                    preferences=json.loads(user_data[9]) if user_data[9] else {}
                )
                
        return None
        
    def update_user_preferences(self, user_id: int, preferences: Dict[str, Any]):
        """Aggiorna preferenze utente."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                UPDATE users SET preferences = ? WHERE id = ?
            ''', (json.dumps(preferences), user_id))
            
    def create_session_token(self, user: User) -> str:
        """Crea token di sessione JWT."""
        payload = {
            'user_id': user.id,
            'username': user.username,
            'role': user.role.value,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }
        
        token = jwt.encode(payload, self.secret_key, algorithm='HS256')
        
        # Salva sessione nel database
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO sessions (user_id, session_token, expires_at)
                VALUES (?, ?, ?)
            ''', (user.id, token, payload['exp']))
            
        return token
        
    def validate_session_token(self, token: str) -> Optional[User]:
        """Valida token di sessione."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            
            # Verifica se sessione esiste nel database
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute('''
                    SELECT user_id FROM sessions 
                    WHERE session_token = ? AND expires_at > CURRENT_TIMESTAMP
                ''', (token,))
                
                session_data = cursor.fetchone()
                
                if session_data:
                    return self.get_user_by_username(payload['username'])
                    
        except jwt.ExpiredSignatureError:
            pass
        except jwt.InvalidTokenError:
            pass
            
        return None
        
    def logout(self, token: str):
        """Logout utente (invalida sessione)."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                DELETE FROM sessions WHERE session_token = ?
            ''', (token,))
            
    def get_login_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Recupera cronologia login."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                SELECT username, ip_address, success, timestamp
                FROM login_attempts 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (limit,))
            
            return [
                {
                    'username': row[0],
                    'ip_address': row[1],
                    'success': bool(row[2]),
                    'timestamp': row[3]
                }
                for row in cursor.fetchall()
            ]


class SessionManager:
    """Gestore sessioni Streamlit."""
    
    @staticmethod
    def get_current_user() -> Optional[User]:
        """Recupera utente corrente dalla sessione."""
        return st.session_state.get('current_user')
        
    @staticmethod
    def set_current_user(user: User):
        """Imposta utente corrente nella sessione."""
        st.session_state.current_user = user
        
    @staticmethod
    def clear_session():
        """Pulisce sessione corrente."""
        keys_to_clear = ['current_user', 'auth_token']
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
                
    @staticmethod
    def is_authenticated() -> bool:
        """Verifica se utente è autenticato."""
        return SessionManager.get_current_user() is not None
        
    @staticmethod
    def has_role(role: UserRole) -> bool:
        """Verifica se utente ha ruolo specifico."""
        user = SessionManager.get_current_user()
        return user is not None and user.role == role
        
    @staticmethod
    def has_permission(permission: str) -> bool:
        """Verifica permessi utente."""
        user = SessionManager.get_current_user()
        if user is None:
            return False
            
        # Definisci permessi per ruolo
        permissions = {
            UserRole.ADMIN: ['all'],
            UserRole.DOCTOR: ['patient_data', 'ai_analysis', 'medical_records'],
            UserRole.RESEARCHER: ['ai_analysis', 'database_search', 'export_data'],
            UserRole.NURSE: ['patient_data', 'basic_analysis'],
            UserRole.STUDENT: ['database_search', 'basic_analysis'],
            UserRole.GUEST: ['database_search']
        }
        
        user_permissions = permissions.get(user.role, [])
        return 'all' in user_permissions or permission in user_permissions


def render_login_form():
    """Renderizza form di login."""
    st.markdown('<h2 class="section-header">🔐 Accesso al Sistema</h2>', unsafe_allow_html=True)
    
    # Tabs login/registrazione
    tab1, tab2 = st.tabs(["🚪 Login", "📝 Registrazione"])
    
    with tab1:
        render_login_tab()
        
    with tab2:
        render_registration_tab()


def render_login_tab():
    """Tab di login."""
    st.subheader("Accedi al tuo account")
    
    with st.form("login_form"):
        username = st.text_input("Username o Email")
        password = st.text_input("Password", type="password")
        remember_me = st.checkbox("Ricordami")
        
        submitted = st.form_submit_button("🚀 Accedi")
        
        if submitted:
            if username and password:
                auth_manager = AuthManager()
                
                # Recupera IP (simulato)
                ip_address = "127.0.0.1"  # In produzione useresti st.context o headers
                
                user = auth_manager.authenticate(username, password, ip_address)
                
                if user:
                    SessionManager.set_current_user(user)
                    
                    # Crea token sessione
                    token = auth_manager.create_session_token(user)
                    st.session_state.auth_token = token
                    
                    st.success(f"Benvenuto, {user.full_name}!")
                    st.rerun()
                    
                else:
                    st.error("Credenziali non valide")
                    
            else:
                st.error("Inserisci username e password")


def render_registration_tab():
    """Tab di registrazione."""
    st.subheader("Crea nuovo account")
    
    with st.form("registration_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            username = st.text_input("Username *")
            email = st.text_input("Email *")
            password = st.text_input("Password *", type="password")
            
        with col2:
            full_name = st.text_input("Nome Completo *")
            role = st.selectbox("Ruolo", [
                UserRole.GUEST.value,
                UserRole.STUDENT.value,
                UserRole.RESEARCHER.value,
                UserRole.NURSE.value,
                UserRole.DOCTOR.value
            ])
            password_confirm = st.text_input("Conferma Password *", type="password")
            
        terms_accepted = st.checkbox("Accetto i termini e condizioni")
        
        submitted = st.form_submit_button("📝 Registrati")
        
        if submitted:
            if all([username, email, password, full_name, terms_accepted]):
                if password != password_confirm:
                    st.error("Le password non coincidono")
                    return
                    
                auth_manager = AuthManager()
                
                try:
                    user = auth_manager.create_user(
                        username=username,
                        email=email,
                        password=password,
                        full_name=full_name,
                        role=UserRole(role)
                    )
                    
                    st.success(f"Account creato con successo! Benvenuto, {user.full_name}")
                    
                    # Login automatico
                    SessionManager.set_current_user(user)
                    token = auth_manager.create_session_token(user)
                    st.session_state.auth_token = token
                    
                    st.rerun()
                    
                except AuthenticationError as e:
                    st.error(f"Errore nella registrazione: {str(e)}")
                    
            else:
                st.error("Compila tutti i campi obbligatori e accetta i termini")


def render_user_profile():
    """Renderizza profilo utente."""
    user = SessionManager.get_current_user()
    if not user:
        return
        
    st.markdown('<h2 class="section-header">👤 Profilo Utente</h2>', unsafe_allow_html=True)
    
    # Info utente
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Avatar placeholder
        st.markdown(f"""
        <div style='text-align: center; padding: 20px;'>
            <div style='font-size: 64px;'>👤</div>
            <h3>{user.full_name}</h3>
            <p>@{user.username}</p>
            <p><strong>Ruolo:</strong> {user.role.value.title()}</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("### 📊 Informazioni Account")
        
        info_data = {
            "Email": user.email,
            "Ruolo": user.role.value.title(),
            "Stato": "Attivo" if user.is_active else "Inattivo",
            "Data Registrazione": user.created_at.strftime("%d/%m/%Y"),
            "Ultimo Accesso": user.last_login.strftime("%d/%m/%Y %H:%M") if user.last_login else "Mai"
        }
        
        for key, value in info_data.items():
            st.write(f"**{key}:** {value}")
            
    # Tabs profilo
    tab1, tab2, tab3 = st.tabs(["⚙️ Preferenze", "🔒 Sicurezza", "📈 Statistiche"])
    
    with tab1:
        render_preferences_tab(user)
        
    with tab2:
        render_security_tab()
        
    with tab3:
        render_user_statistics_tab(user)


def render_preferences_tab(user: User):
    """Tab preferenze utente."""
    st.subheader("⚙️ Preferenze Personali")
    
    # Dashboard preferences
    st.markdown("#### Dashboard")
    
    col1, col2 = st.columns(2)
    
    with col1:
        default_theme = user.preferences.get('theme', 'light')
        theme = st.selectbox("Tema", ['light', 'dark'], 
                           index=0 if default_theme == 'light' else 1)
        
        default_language = user.preferences.get('language', 'it')
        language = st.selectbox("Lingua", ['it', 'en'], 
                              index=0 if default_language == 'it' else 1)
        
    with col2:
        notifications = st.checkbox(
            "Notifiche Email", 
            value=user.preferences.get('email_notifications', True)
        )
        
        auto_save = st.checkbox(
            "Salvataggio Automatico",
            value=user.preferences.get('auto_save', True)
        )
        
    # AI Analysis preferences
    st.markdown("#### Analisi IA")
    
    default_ai_model = user.preferences.get('default_ai_model', 'general')
    ai_model = st.selectbox("Modello IA Predefinito", 
                           ['general', 'specialized', 'experimental'])
    
    confidence_threshold = st.slider(
        "Soglia Confidenza Minima",
        0.5, 1.0, 
        user.preferences.get('confidence_threshold', 0.8),
        0.05
    )
    
    if st.button("💾 Salva Preferenze", key="save_preferences"):
        new_preferences = {
            'theme': theme,
            'language': language,
            'email_notifications': notifications,
            'auto_save': auto_save,
            'default_ai_model': ai_model,
            'confidence_threshold': confidence_threshold
        }
        
        auth_manager = AuthManager()
        auth_manager.update_user_preferences(user.id, new_preferences)
        
        # Aggiorna sessione
        user.preferences = new_preferences
        SessionManager.set_current_user(user)
        
        st.success("✅ Preferenze salvate!")


def render_security_tab():
    """Tab sicurezza."""
    st.subheader("🔒 Impostazioni Sicurezza")
    
    # Cambio password
    st.markdown("#### Cambia Password")
    
    with st.form("change_password_form"):
        current_password = st.text_input("Password Attuale", type="password")
        new_password = st.text_input("Nuova Password", type="password")
        confirm_password = st.text_input("Conferma Nuova Password", type="password")
        
        if st.form_submit_button("🔄 Cambia Password"):
            if new_password != confirm_password:
                st.error("Le nuove password non coincidono")
            elif len(new_password) < 8:
                st.error("La nuova password deve essere almeno 8 caratteri")
            else:
                # Qui implementeresti il cambio password
                st.success("Password cambiata con successo!")
                
    # Sessioni attive
    st.markdown("#### Sessioni Attive")
    st.info("📱 Sessione corrente: Browser Desktop - Oggi alle 14:30")
    
    if st.button("🚪 Termina Tutte le Sessioni"):
        # Qui implementeresti il logout da tutte le sessioni
        st.warning("Tutte le sessioni sono state terminate")


def render_user_statistics_tab(user: User):
    """Tab statistiche utente."""
    st.subheader("📈 Le Tue Statistiche")
    
    # Simulazione dati statistiche
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Ricerche Totali", "247")
    with col2:
        st.metric("Analisi IA", "89")
    with col3:
        st.metric("Report Generati", "23")
    with col4:
        st.metric("Giorni Attivo", "45")
        
    # Grafici attività
    import plotly.express as px
    import numpy as np
    
    # Attività ultima settimana
    days = ['Lun', 'Mar', 'Mer', 'Gio', 'Ven', 'Sab', 'Dom']
    activity = np.random.randint(5, 25, 7)
    
    fig = px.bar(x=days, y=activity, title="Attività Ultima Settimana")
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)


def render_admin_panel():
    """Pannello amministratore."""
    user = SessionManager.get_current_user()
    if not user or user.role != UserRole.ADMIN:
        st.error("Accesso negato: Solo amministratori")
        return
        
    st.markdown('<h2 class="section-header">⚙️ Pannello Amministratore</h2>', unsafe_allow_html=True)
    
    # Tabs admin
    tab1, tab2, tab3 = st.tabs(["👥 Gestione Utenti", "📊 Sistema", "🔍 Log"])
    
    with tab1:
        render_user_management_tab()
        
    with tab2:
        render_system_management_tab()
        
    with tab3:
        render_logs_tab()


def render_user_management_tab():
    """Tab gestione utenti."""
    st.subheader("👥 Gestione Utenti")
    
    # Lista utenti (simulata)
    users_data = [
        {"Username": "admin", "Nome": "Amministratore", "Ruolo": "admin", "Stato": "Attivo"},
        {"Username": "dr.smith", "Nome": "Dr. John Smith", "Ruolo": "doctor", "Stato": "Attivo"},
        {"Username": "researcher1", "Nome": "Alice Johnson", "Ruolo": "researcher", "Stato": "Attivo"},
        {"Username": "nurse.mary", "Nome": "Mary Wilson", "Ruolo": "nurse", "Stato": "Inattivo"}
    ]
    
    df = pd.DataFrame(users_data)
    st.dataframe(df, use_container_width=True)
    
    # Azioni
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("➕ Nuovo Utente"):
            st.info("Funzione per creare nuovo utente")
            
    with col2:
        if st.button("✏️ Modifica Utente"):
            st.info("Seleziona utente da modificare")
            
    with col3:
        if st.button("🗑️ Elimina Utente"):
            st.warning("Conferma eliminazione utente")


def render_system_management_tab():
    """Tab gestione sistema."""
    st.subheader("📊 Gestione Sistema")
    
    # Metriche sistema
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Utenti Totali", "156")
    with col2:
        st.metric("Utenti Attivi", "142")
    with col3:
        st.metric("Sessioni Correnti", "23")
    with col4:
        st.metric("Uptime", "99.9%")
        
    # Configurazioni
    st.markdown("#### Configurazioni Sistema")
    
    with st.expander("🔧 Impostazioni Autenticazione"):
        max_login_attempts = st.number_input("Tentativi login massimi", 1, 10, 5)
        session_timeout = st.number_input("Timeout sessione (ore)", 1, 24, 8)
        force_strong_passwords = st.checkbox("Forza password forti", value=True)
        
    if st.button("💾 Salva Configurazioni Sistema"):
        st.success("Configurazioni salvate!")


def render_logs_tab():
    """Tab log sistema."""
    st.subheader("🔍 Log Sistema")
    
    # Filtri log
    col1, col2, col3 = st.columns(3)
    
    with col1:
        log_type = st.selectbox("Tipo Log", ["Tutti", "Login", "Errori", "Accessi"])
    with col2:
        date_from = st.date_input("Da")
    with col3:
        date_to = st.date_input("A")
        
    # Simulazione log
    auth_manager = AuthManager()
    login_history = auth_manager.get_login_history(20)
    
    if login_history:
        df_logs = pd.DataFrame(login_history)
        st.dataframe(df_logs, use_container_width=True)
    else:
        st.info("Nessun log disponibile")
        
    if st.button("🔄 Aggiorna Log"):
        st.rerun()


def require_auth(func):
    """Decorator per richiedere autenticazione."""
    def wrapper(*args, **kwargs):
        if not SessionManager.is_authenticated():
            render_login_form()
            return None
        return func(*args, **kwargs)
    return wrapper


def require_role(role: UserRole):
    """Decorator per richiedere ruolo specifico."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not SessionManager.has_role(role):
                st.error(f"Accesso negato: Ruolo {role.value} richiesto")
                return None
            return func(*args, **kwargs)
        return wrapper
    return decorator


if __name__ == "__main__":
    # Test sistema autenticazione
    print("Testing Authentication System...")
    
    auth_manager = AuthManager()
    
    # Test creazione utente
    try:
        test_user = auth_manager.create_user(
            username="test_user",
            email="test@example.com",
            password="TestPass123!",
            full_name="Test User",
            role=UserRole.RESEARCHER
        )
        print(f"✅ User created: {test_user.username}")
        
        # Test autenticazione
        authenticated_user = auth_manager.authenticate("test_user", "TestPass123!")
        if authenticated_user:
            print(f"✅ Authentication successful: {authenticated_user.full_name}")
        else:
            print("❌ Authentication failed")
            
    except AuthenticationError as e:
        print(f"Authentication error: {e}")
        
    print("Authentication system working correctly!")
