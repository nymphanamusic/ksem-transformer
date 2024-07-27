from __future__ import annotations

from typing import TypedDict

from pydantic import BaseModel

from ksem_transformer.models.ksem_json_types import KsemConfig

PartialRouterConfig = TypedDict(
    "PartialRouterConfig", {"routerTrack": int, "routerFilter": int}
)


class Router(BaseModel):
    track_must_be_armed: bool = True
    router_exclusive: bool = False

    @classmethod
    def from_ksem_config(cls, config: KsemConfig) -> Router:
        cfg = config["keySwitchManager"]
        return Router(
            track_must_be_armed=bool(cfg["routerTrack"]),
            router_exclusive=bool(cfg["routerFilter"]),
        )

    def to_ksem_config(self) -> PartialRouterConfig:
        return {
            "routerTrack": int(self.track_must_be_armed),
            "routerFilter": int(self.router_exclusive),
        }
