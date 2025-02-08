import pytest
import asyncio
import aiohttp
import time
from typing import List
from statistics import mean, median
from concurrent.futures import ThreadPoolExecutor

# Test configurations
BASE_URL = "http://localhost:8000"
CONCURRENT_USERS = [10, 25, 50]  # Different concurrency levels
REQUESTS_PER_USER = 10
TEST_ENDPOINTS = [
    "/health",
    "/api/v1/moderate/text",
    "/health/ready"
]

# Sample test data
TEXT_PAYLOAD = {
    "text": "This is a test message for load testing"
}

async def make_request(session: aiohttp.ClientSession, endpoint: str, payload: dict = None) -> float:
    """Make a single request and return the response time"""
    start_time = time.time()
    try:
        if payload:
            async with session.post(f"{BASE_URL}{endpoint}", json=payload) as response:
                await response.text()
        else:
            async with session.get(f"{BASE_URL}{endpoint}") as response:
                await response.text()
        return time.time() - start_time
    except Exception as e:
        print(f"Request failed: {e}")
        return -1

async def concurrent_requests(users: int, endpoint: str, payload: dict = None) -> List[float]:
    """Execute concurrent requests and return response times"""
    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(users * REQUESTS_PER_USER):
            tasks.append(make_request(session, endpoint, payload))
        return await asyncio.gather(*tasks)

def calculate_metrics(response_times: List[float]) -> dict:
    """Calculate performance metrics from response times"""
    valid_times = [t for t in response_times if t > 0]
    if not valid_times:
        return {
            "mean": 0,
            "median": 0,
            "min": 0,
            "max": 0,
            "success_rate": 0,
            "requests_per_second": 0
        }

    total_time = max(response_times)
    return {
        "mean": mean(valid_times),
        "median": median(valid_times),
        "min": min(valid_times),
        "max": max(valid_times),
        "success_rate": len(valid_times) / len(response_times) * 100,
        "requests_per_second": len(valid_times) / total_time if total_time > 0 else 0
    }

@pytest.mark.parametrize("users", CONCURRENT_USERS)
def test_health_endpoint_load(users):
    """Load test the health endpoint"""
    response_times = asyncio.run(concurrent_requests(users, "/health"))
    metrics = calculate_metrics(response_times)
    
    assert metrics["success_rate"] > 95, f"Health endpoint success rate below 95%: {metrics['success_rate']}%"
    assert metrics["mean"] < 0.5, f"Average response time too high: {metrics['mean']}s"
    print(f"\nHealth endpoint metrics (users={users}):")
    print(f"Mean: {metrics['mean']:.3f}s")
    print(f"Median: {metrics['median']:.3f}s")
    print(f"Success Rate: {metrics['success_rate']:.1f}%")
    print(f"Requests/second: {metrics['requests_per_second']:.1f}")

@pytest.mark.parametrize("users", CONCURRENT_USERS)
def test_moderation_endpoint_load(users):
    """Load test the text moderation endpoint"""
    response_times = asyncio.run(concurrent_requests(users, "/api/v1/moderate/text", TEXT_PAYLOAD))
    metrics = calculate_metrics(response_times)
    
    assert metrics["success_rate"] > 90, f"Moderation endpoint success rate below 90%: {metrics['success_rate']}%"
    assert metrics["mean"] < 2.0, f"Average response time too high: {metrics['mean']}s"
    print(f"\nModeration endpoint metrics (users={users}):")
    print(f"Mean: {metrics['mean']:.3f}s")
    print(f"Median: {metrics['median']:.3f}s")
    print(f"Success Rate: {metrics['success_rate']:.1f}%")
    print(f"Requests/second: {metrics['requests_per_second']:.1f}")

async def sustained_load_worker(duration: int, users: int) -> List[float]:
    """Worker function for sustained load testing"""
    start_time = time.time()
    response_times = []
    async with aiohttp.ClientSession() as session:
        while time.time() - start_time < duration:
            response_time = await make_request(session, "/health")
            response_times.append(response_time)
    return response_times

def test_sustained_load():
    """Test sustained load over a longer period"""
    DURATION = 60  # seconds
    CONCURRENT_USERS = 25
    
    response_times = asyncio.run(sustained_load_worker(DURATION, CONCURRENT_USERS))
    
    metrics = calculate_metrics(response_times)
    assert metrics["success_rate"] > 95, f"Sustained load test failed with {metrics['success_rate']}% success rate"
    print(f"\nSustained load test metrics ({DURATION}s duration):")
    print(f"Total requests: {len(response_times)}")
    print(f"Success Rate: {metrics['success_rate']:.1f}%")
    print(f"Requests/second: {metrics['requests_per_second']:.1f}")
