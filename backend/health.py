from schemas import HealthResponse


async def health_check() -> HealthResponse:
    return HealthResponse()
