from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
from typing import Callable, TypeVar
import time

T = TypeVar("T")


def run_with_retries(
    operation: Callable[[], T],
    *,
    fallback: T,
    label: str,
    retries: int = 2,
    timeout_seconds: int = 30,
    backoff_seconds: float = 1.5,
) -> T:
    """
    Run a blocking operation with a timeout, retry, and fallback value.
    """

    for attempt in range(retries + 1):
        executor = ThreadPoolExecutor(max_workers=1)
        future = executor.submit(operation)

        try:
            return future.result(timeout=timeout_seconds)
        except FutureTimeoutError as exc:
            print(f"[{label}] timeout on attempt {attempt + 1}: {exc}")
        except Exception as exc:
            print(f"[{label}] error on attempt {attempt + 1}: {exc}")
        finally:
            executor.shutdown(wait=False, cancel_futures=True)

        if attempt < retries:
            time.sleep(backoff_seconds * (attempt + 1))

    return fallback