import threading

class MetaDataSingleton:
    """
    Singleton trzymający metadane API.
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, version="1.0", description="API with JWT auth"):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(MetaDataSingleton, cls).__new__(cls)
                # Inicjalizator, wypełnianie konstruktorów
                cls._instance.version = version
                cls._instance.description = description
            return cls._instance

    def get_metadata(self):
        return {"version": self.version, "description": self.description}
