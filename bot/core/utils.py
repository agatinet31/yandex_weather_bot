import asyncio
from decimal import Decimal
from typing import Awaitable, Dict, Tuple


async def gather_dict(
    tasks: Dict[int, Awaitable[Decimal]]
) -> Dict[int, Decimal]:
    """Выполнения списка корутин."""

    async def mark(
        key: int, coroutine: Awaitable[Decimal]
    ) -> Tuple[int, Decimal]:
        return key, await coroutine

    return {
        key: result
        for key, result in await asyncio.gather(
            *(mark(key, coroutine) for key, coroutine in tasks.items())
        )
    }
