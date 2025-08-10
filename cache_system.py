"""
Nino Medical AI - Sistema di Cache Avanzato
===========================================

Sistema di cache intelligente per ottimizzare le performance delle ricerche
sui database medici e dell'elaborazione IA.

Author: Antonino Piacenza
Email: ninomedical.ai@gmail.com
"""

import streamlit as st
import hashlib
import pickle
import json
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Callable
import diskcache as dc
import threading
import time
from dataclasses import dataclass
from functools import wraps
import psutil
import logging

# Configurazione logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class CacheStats:
    """Statistiche del cache."""
    hits: int = 0
    misses: int = 0
    size_mb: float = 0.0
    entries_count: int = 0
    
    @property
    def hit_rate(self) -> float:
        """Calcola hit rate."""
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0


class IntelligentCache:
    """Sistema di cache intelligente multi-livello."""
    
    def __init__(self, cache_dir: str = "cache", max_size_mb: int = 500):
        """
        Inizializza il sistema di cache.
        
        Args:
            cache_dir: Directory per il cache persistente
            max_size_mb: Dimensione massima cache in MB
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        
        # Cache persistente su disco
        self.disk_cache = dc.Cache(str(self.cache_dir / "disk_cache"), 
                                  size_limit=max_size_mb * 1024 * 1024)
        
        # Cache in memoria (LRU)
        self.memory_cache = {}
        self.memory_cache_order = []
        self.max_memory_entries = 100
        
        # Statistiche
        self.stats = CacheStats()
        
        # Thread per pulizia automatica
        self.cleanup_thread = threading.Thread(target=self._cleanup_worker, daemon=True)
        self.cleanup_thread.start()
        
    def _generate_key(self, func_name: str, args: tuple, kwargs: dict) -> str:
        """Genera chiave univoca per il cache."""
        key_data = {
            'func': func_name,
            'args': args,
            'kwargs': kwargs
        }
        
        key_string = json.dumps(key_data, sort_keys=True, default=str)
        return hashlib.sha256(key_string.encode()).hexdigest()
        
    def _cleanup_worker(self):
        """Worker thread per pulizia automatica cache."""
        while True:
            time.sleep(3600)  # Ogni ora
            self._cleanup_expired_entries()
            
    def _cleanup_expired_entries(self):
        """Rimuove entry scadute dal cache."""
        current_time = datetime.now()
        
        # Pulizia memory cache
        expired_keys = []
        for key in self.memory_cache:
            if 'expiry' in self.memory_cache[key]:
                if current_time > self.memory_cache[key]['expiry']:
                    expired_keys.append(key)
                    
        for key in expired_keys:
            del self.memory_cache[key]
            if key in self.memory_cache_order:
                self.memory_cache_order.remove(key)
                
        logger.info(f"Cleaned up {len(expired_keys)} expired cache entries")
        
    def _manage_memory_cache_size(self):
        """Gestisce dimensione memory cache (LRU eviction)."""
        while len(self.memory_cache) > self.max_memory_entries:
            oldest_key = self.memory_cache_order.pop(0)
            del self.memory_cache[oldest_key]
            
    def get(self, key: str, default: Any = None) -> Any:
        """Recupera valore dal cache."""
        # Prova prima memory cache
        if key in self.memory_cache:
            # Aggiorna ordine LRU
            self.memory_cache_order.remove(key)
            self.memory_cache_order.append(key)
            
            # Verifica scadenza
            entry = self.memory_cache[key]
            if 'expiry' in entry and datetime.now() > entry['expiry']:
                del self.memory_cache[key]
                self.memory_cache_order.remove(key)
            else:
                self.stats.hits += 1
                return entry['data']
                
        # Prova disk cache
        try:
            value = self.disk_cache[key]
            # Copia in memory cache per accesso veloce
            self.memory_cache[key] = {'data': value, 'timestamp': datetime.now()}
            self.memory_cache_order.append(key)
            self._manage_memory_cache_size()
            
            self.stats.hits += 1
            return value
        except KeyError:
            self.stats.misses += 1
            return default
            
    def set(self, key: str, value: Any, expiry_minutes: int = 60):
        """Salva valore nel cache."""
        expiry_time = datetime.now() + timedelta(minutes=expiry_minutes)
        
        # Memory cache
        entry = {
            'data': value,
            'timestamp': datetime.now(),
            'expiry': expiry_time
        }
        
        self.memory_cache[key] = entry
        if key in self.memory_cache_order:
            self.memory_cache_order.remove(key)
        self.memory_cache_order.append(key)
        self._manage_memory_cache_size()
        
        # Disk cache (solo per dati serializzabili)
        try:
            self.disk_cache.set(key, value, expire=expiry_minutes * 60)
        except Exception as e:
            logger.warning(f"Could not save to disk cache: {e}")
            
    def delete(self, key: str):
        """Rimuove entry dal cache."""
        # Memory cache
        if key in self.memory_cache:
            del self.memory_cache[key]
            self.memory_cache_order.remove(key)
            
        # Disk cache
        try:
            del self.disk_cache[key]
        except KeyError:
            pass
            
    def clear(self):
        """Pulisce tutto il cache."""
        self.memory_cache.clear()
        self.memory_cache_order.clear()
        self.disk_cache.clear()
        self.stats = CacheStats()
        
    def get_stats(self) -> CacheStats:
        """Ritorna statistiche cache."""
        self.stats.size_mb = self.disk_cache.volume() / (1024 * 1024)
        self.stats.entries_count = len(self.disk_cache)
        return self.stats


# Cache globale
_global_cache = IntelligentCache()


def cached(expiry_minutes: int = 60, use_args: bool = True, use_kwargs: bool = True):
    """
    Decorator per cache automatico delle funzioni.
    
    Args:
        expiry_minutes: Minuti prima della scadenza
        use_args: Include args nella chiave
        use_kwargs: Include kwargs nella chiave
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Genera chiave cache
            if use_args and use_kwargs:
                cache_key = _global_cache._generate_key(func.__name__, args, kwargs)
            elif use_args:
                cache_key = _global_cache._generate_key(func.__name__, args, {})
            elif use_kwargs:
                cache_key = _global_cache._generate_key(func.__name__, (), kwargs)
            else:
                cache_key = _global_cache._generate_key(func.__name__, (), {})
                
            # Prova a recuperare dal cache
            cached_result = _global_cache.get(cache_key)
            if cached_result is not None:
                return cached_result
                
            # Esegui funzione e salva risultato
            result = func(*args, **kwargs)
            _global_cache.set(cache_key, result, expiry_minutes)
            
            return result
        return wrapper
    return decorator


class SessionCache:
    """Cache specifico per sessione Streamlit."""
    
    @staticmethod
    def get(key: str, default: Any = None) -> Any:
        """Recupera da session state."""
        return st.session_state.get(key, default)
        
    @staticmethod
    def set(key: str, value: Any):
        """Salva in session state."""
        st.session_state[key] = value
        
    @staticmethod
    def delete(key: str):
        """Rimuove da session state."""
        if key in st.session_state:
            del st.session_state[key]
            
    @staticmethod
    def clear():
        """Pulisce session state."""
        for key in list(st.session_state.keys()):
            del st.session_state[key]


class PerformanceOptimizer:
    """Ottimizzatore di performance per l'app."""
    
    @staticmethod
    def get_system_info() -> Dict[str, Any]:
        """Recupera informazioni di sistema."""
        return {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_percent': psutil.disk_usage('/').percent,
            'cache_stats': _global_cache.get_stats()
        }
        
    @staticmethod
    def optimize_dataframe_loading():
        """Ottimizza caricamento dataframe."""
        # Configurazioni pandas ottimali
        import pandas as pd
        pd.set_option('display.max_columns', 50)
        pd.set_option('display.max_rows', 100)
        
    @staticmethod
    def lazy_load_modules():
        """Caricamento lazy dei moduli pesanti."""
        def load_tensorflow():
            import tensorflow as tf
            return tf
            
        def load_torch():
            import torch
            return torch
            
        return {
            'tensorflow': load_tensorflow,
            'torch': load_torch
        }


class DatabaseCacheManager:
    """Manager specifico per cache database medici."""
    
    def __init__(self, db_path: str = "cache/database_cache.db"):
        """Inizializza manager cache database."""
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True)
        self._init_database()
        
    def _init_database(self):
        """Inizializza database SQLite per cache."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS cache_entries (
                    key TEXT PRIMARY KEY,
                    data BLOB,
                    created_at TIMESTAMP,
                    expires_at TIMESTAMP,
                    source TEXT
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS search_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query TEXT,
                    source TEXT,
                    timestamp TIMESTAMP,
                    results_count INTEGER
                )
            ''')
            
    def cache_search_results(self, query: str, source: str, results: List[Dict]) -> str:
        """Cache risultati ricerca."""
        key = hashlib.sha256(f"{source}_{query}".encode()).hexdigest()
        
        with sqlite3.connect(self.db_path) as conn:
            # Salva risultati
            conn.execute('''
                INSERT OR REPLACE INTO cache_entries 
                (key, data, created_at, expires_at, source)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                key,
                pickle.dumps(results),
                datetime.now(),
                datetime.now() + timedelta(hours=24),
                source
            ))
            
            # Salva in search history
            conn.execute('''
                INSERT INTO search_history 
                (query, source, timestamp, results_count)
                VALUES (?, ?, ?, ?)
            ''', (query, source, datetime.now(), len(results)))
            
        return key
        
    def get_cached_results(self, query: str, source: str) -> Optional[List[Dict]]:
        """Recupera risultati cache."""
        key = hashlib.sha256(f"{source}_{query}".encode()).hexdigest()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                SELECT data, expires_at FROM cache_entries 
                WHERE key = ? AND expires_at > ?
            ''', (key, datetime.now()))
            
            result = cursor.fetchone()
            if result:
                return pickle.loads(result[0])
                
        return None
        
    def get_search_history(self, limit: int = 10) -> List[Dict]:
        """Recupera cronologia ricerche."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                SELECT query, source, timestamp, results_count 
                FROM search_history 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (limit,))
            
            return [
                {
                    'query': row[0],
                    'source': row[1],
                    'timestamp': row[2],
                    'results_count': row[3]
                }
                for row in cursor.fetchall()
            ]
            
    def cleanup_expired(self):
        """Rimuove entry scadute."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                DELETE FROM cache_entries WHERE expires_at < ?
            ''', (datetime.now(),))
            
            deleted_count = cursor.rowcount
            
        logger.info(f"Cleaned up {deleted_count} expired database cache entries")
        return deleted_count


def render_cache_management_page():
    """Renderizza pagina di gestione cache."""
    st.markdown('<h2 class="section-header">⚡ Gestione Cache e Performance</h2>', unsafe_allow_html=True)
    
    # Statistiche sistema
    system_info = PerformanceOptimizer.get_system_info()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("CPU", f"{system_info['cpu_percent']:.1f}%")
    with col2:
        st.metric("RAM", f"{system_info['memory_percent']:.1f}%")
    with col3:
        st.metric("Cache Hit Rate", f"{system_info['cache_stats'].hit_rate:.1%}")
    with col4:
        st.metric("Cache Size", f"{system_info['cache_stats'].size_mb:.1f} MB")
        
    # Controlli cache
    st.markdown("### 🗂️ Controlli Cache")
    
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        if st.button("🧹 Pulisci Cache", key="clear_cache"):
            _global_cache.clear()
            st.success("Cache pulito!")
            st.experimental_rerun()
            
    with col_b:
        if st.button("📊 Aggiorna Statistiche", key="refresh_stats"):
            st.experimental_rerun()
            
    with col_c:
        if st.button("🔄 Ottimizza Performance", key="optimize"):
            PerformanceOptimizer.optimize_dataframe_loading()
            st.success("Performance ottimizzata!")
            
    # Database cache manager
    db_cache = DatabaseCacheManager()
    
    st.markdown("### 📚 Cronologia Ricerche Database")
    search_history = db_cache.get_search_history(20)
    
    if search_history:
        history_df = pd.DataFrame(search_history)
        st.dataframe(history_df, use_container_width=True)
    else:
        st.info("Nessuna ricerca nella cronologia.")
        
    # Gestione cache database
    if st.button("🗑️ Pulisci Cache Database", key="clean_db_cache"):
        deleted = db_cache.cleanup_expired()
        st.success(f"Rimossi {deleted} record scaduti dal cache database!")


# Cache manager globale per database
db_cache_manager = DatabaseCacheManager()


if __name__ == "__main__":
    # Test sistema cache
    print("Testing Cache System...")
    
    cache = IntelligentCache()
    
    # Test set/get
    cache.set("test_key", {"data": "test_value"}, 5)
    result = cache.get("test_key")
    print(f"✅ Cache set/get: {result}")
    
    # Test decorator
    @cached(expiry_minutes=5)
    def expensive_function(x, y):
        time.sleep(0.1)  # Simula operazione costosa
        return x + y
        
    start_time = time.time()
    result1 = expensive_function(1, 2)
    first_call_time = time.time() - start_time
    
    start_time = time.time()  
    result2 = expensive_function(1, 2)
    second_call_time = time.time() - start_time
    
    print(f"✅ First call: {first_call_time:.3f}s, Second call: {second_call_time:.3f}s")
    print(f"✅ Cache speedup: {first_call_time/second_call_time:.1f}x")
    
    print("Cache system working correctly!")
