import sys
import os
from logging.config import fileConfig
from sqlalchemy import pool, create_engine
from alembic import context
from sqlmodel import SQLModel

# 1. Nastavení cesty - přidáme složku, kde je skutečně main.py a config.py
# Pokud je struktura /app/app/main.py, tak BASE_DIR musí být /app/app
BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app")
sys.path.insert(0, BASE_DIR)

# 2. Standardní importy (teď už je Python uvidí)
try:
    from main import Order
    from config import settings
except ImportError as e:
    print(f"Chyba: Nepodařilo se importovat moduly z {BASE_DIR}")
    raise e

# --- Zbytek Alembic konfigurace ---
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = SQLModel.metadata

def run_migrations_online() -> None:
    # Použijeme URL z našeho configu
    connectable = create_engine(settings.database_url)

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

# ... (zbytek souboru s run_migrations_offline a is_offline_mode)



def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = create_engine(settings.database_url)

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
