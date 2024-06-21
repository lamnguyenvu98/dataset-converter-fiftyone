
class Registry:
    _registry = {'importer': {}, 'exporter': {}}

    @classmethod
    def register(cls, type):
        def decorator(class_to_register):
            if type not in cls._registry:
                raise ValueError(f"Invalid type: {type}. Expected 'importer' or 'exporter'.")
            cls._registry[type][class_to_register.__name__] = class_to_register
            return class_to_register
        return decorator

    @classmethod
    def get_instance(cls, type, dataset_type):
        if type not in cls._registry:
            raise ValueError(f"Invalid type: {type}. Expected 'importer' or 'exporter'.")
        if dataset_type in cls._registry[type]:
            return cls._registry[type][dataset_type]
        raise ValueError(f"{type}: {dataset_type} not found in registry")