import time
from typing import Callable, Optional, Any
from functools import wraps


class RetryManager:
    """Retry utility for handling transient failures in automation"""
    
    def __init__(self, max_retries: int = 3, delay: float = 1.0, backoff: float = 2.0):
        """Initialize retry manager with configuration"""
        self.max_retries = max_retries
        self.delay = delay
        self.backoff = backoff
    
    def retry(self, func: Callable) -> Callable:
        """Decorator to add retry logic to a function"""
        @wraps(func)
        def wrapper(*args, **kwargs) -> Optional[Any]:
            last_exception = None
            current_delay = self.delay
            
            for attempt in range(self.max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < self.max_retries - 1:
                        print(f"Attempt {attempt + 1}/{self.max_retries} failed: {str(e)}. Retrying in {current_delay}s...")
                        time.sleep(current_delay)
                        current_delay *= self.backoff
                    else:
                        print(f"All {self.max_retries} attempts failed. Last error: {str(e)}")
            
            raise last_exception
        
        return wrapper
    
    def retry_with_condition(self, func: Callable, condition: Callable[[Exception], bool]) -> Callable:
        """Decorator to add retry logic with custom condition"""
        @wraps(func)
        def wrapper(*args, **kwargs) -> Optional[Any]:
            last_exception = None
            current_delay = self.delay
            
            for attempt in range(self.max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if not condition(e):
                        # Don't retry if condition is not met
                        raise
                    if attempt < self.max_retries - 1:
                        print(f"Attempt {attempt + 1}/{self.max_retries} failed: {str(e)}. Retrying in {current_delay}s...")
                        time.sleep(current_delay)
                        current_delay *= self.backoff
                    else:
                        print(f"All {self.max_retries} attempts failed. Last error: {str(e)}")
            
            raise last_exception
        
        return wrapper
    
    def execute_with_retry(self, func: Callable, *args, **kwargs) -> Optional[Any]:
        """Execute a function with retry logic without decorator"""
        last_exception = None
        current_delay = self.delay
        
        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                if attempt < self.max_retries - 1:
                    print(f"Attempt {attempt + 1}/{self.max_retries} failed: {str(e)}. Retrying in {current_delay}s...")
                    time.sleep(current_delay)
                    current_delay *= self.backoff
                else:
                    print(f"All {self.max_retries} attempts failed. Last error: {str(e)}")
        
        raise last_exception


def retry_on_failure(max_retries: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """Decorator factory for retry logic"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Optional[Any]:
            last_exception = None
            current_delay = delay
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        print(f"Attempt {attempt + 1}/{max_retries} failed: {str(e)}. Retrying in {current_delay}s...")
                        time.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        print(f"All {max_retries} attempts failed. Last error: {str(e)}")
            
            raise last_exception
        
        return wrapper
    return decorator
