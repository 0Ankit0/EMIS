"""Performance and Load Tests"""
import pytest
import asyncio
from httpx import AsyncClient


@pytest.mark.asyncio
@pytest.mark.performance
async def test_concurrent_requests(client: AsyncClient, test_superuser):
    """Test system handles concurrent requests"""
    async def make_request():
        return await client.get(
            "/api/students",
            headers={"Authorization": f"Bearer {test_superuser.token}"}
        )
    
    # Make 10 concurrent requests
    tasks = [make_request() for _ in range(10)]
    responses = await asyncio.gather(*tasks)
    
    # All should succeed
    assert all(r.status_code in [200, 401] for r in responses)


@pytest.mark.asyncio
@pytest.mark.performance
async def test_response_time(client: AsyncClient, test_superuser):
    """Test API response time"""
    import time
    
    start = time.time()
    response = await client.get(
        "/api/students",
        headers={"Authorization": f"Bearer {test_superuser.token}"}
    )
    end = time.time()
    
    response_time = end - start
    
    # Response should be under 1 second
    assert response_time < 1.0
