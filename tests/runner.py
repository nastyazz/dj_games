"""This module implements a custom Django test runner for managing PostgreSQL schema creation."""

from types import MethodType
from typing import Any

from django.db import connections
from django.db.backends.base.base import BaseDatabaseWrapper
from django.test.runner import DiscoverRunner


def prepare_db(self):
    """Prepare the database by creating the 'games_data' schema if it does not exist."""
    self.connect()
    self.connection.cursor().execute('CREATE SCHEMA IF NOT EXISTS games_data;')


class PostgresSchemaRunner(DiscoverRunner):
    """Custom Django test runner for PostgreSQL schema management."""

    def setup_databases(self, **kwargs: Any) -> list[tuple[BaseDatabaseWrapper, str, bool]]:
        """
        Override the default database setup to prepare PostgreSQL databases.

        Args:
            **kwargs: Additional keyword arguments for setup.

        Returns:
            list: A list of tuples containing the prepared database connections.
        """
        for conn_name in connections:
            connection = connections[conn_name]
            connection.prepare_database = MethodType(prepare_db, connection)
        return super().setup_databases(**kwargs)
