import pytest
import asyncio
import aiohttp
from typing import Generator, AsyncGenerator

@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def client() -> AsyncGenerator:
    """Async client fixture for making HTTP requests."""
    async with aiohttp.ClientSession() as session:
        yield session
