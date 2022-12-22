from abc import ABC, abstractmethod


class RateAPI(ABC):
    @abstractmethod
    async def get_rate(self) -> float:
        pass

