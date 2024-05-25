from typing import TypedDict

from pydantic import BaseModel

PartialRouterConfig = TypedDict(
    "PartialRouterConfig", {"routerTrack": int, "routerFilter": int}
)


class Router(BaseModel):
    track_must_be_armed: bool = True
    router_exclusive: bool = False

    def to_ksem_config(self) -> PartialRouterConfig:
        return {
            "routerTrack": int(self.track_must_be_armed),
            "routerFilter": int(self.router_exclusive),
        }
