from django.db.backends.signals import connection_created


def set_pragma(sender, connection, **kwargs):
    if connection.vendor == 'sqlite':
        cursor = connection.cursor()
        cursor.execute("PRAGMA journal_mode = WAL")
        cursor.execute("PRAGMA synchronous = normal")    # set cache_size in kilobytes
        cursor.execute("PRAGMA tmp_store = memory")
        cursor.execute("PRAGMA mmap_size = 30000000000")
        cursor.execute("PRAGMA cache_size = 1000000")


connection_created.connect(set_pragma)
