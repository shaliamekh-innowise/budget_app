from ports.external_api.rate_api import RateAPI


class FakeRateApi(RateAPI):
    async def get_rate(self) -> float:
        return 2.55
