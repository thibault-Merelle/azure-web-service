import logging


def log(func):
    def wrapper(*args, **kwargs):
        logging.info(f"Entering function {func.__name__}")
        result = func(*args, **kwargs)
        logging.info(f"Leaving function {func.__name__}")
        return result
    wrapper.__name__ = func.__name__    
    return wrapper