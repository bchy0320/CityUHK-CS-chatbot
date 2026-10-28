"""Configuration loading for the CityU UG scraper.

Loads config/seeds.yaml into typed models so the rest of the pipeline can
rely on validated settings (URLs, patterns, fetch policy, area rules).
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field


class FetchPolicy(BaseModel):
    delay_seconds: float = 1.0
    timeout_seconds: float = 30.0
    user_agent: str = "CityU-UG-Scraper/0.1"
    respect_robots: bool = True
    max_retries: int = 2


class AreaRule(BaseModel):
    pattern: str
    area: str


class Source(BaseModel):
    name: str
    base_urls: list[str] = Field(default_factory=list)
    include_patterns: list[str] = Field(default_factory=list)
    exclude_patterns: list[str] = Field(default_factory=list)


class Config(BaseModel):
    vault_name: str = "CityUHK-Undergraduate-FAQ"
    default_area: str = "09_Undergraduate-General"
    fetch: FetchPolicy = Field(default_factory=FetchPolicy)
    area_rules: list[AreaRule] = Field(default_factory=list)
    sources: list[Source] = Field(default_factory=list)


def load_config(path: str | Path) -> Config:
    """Load and validate a seeds.yaml config file."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Config not found: {p}")
    data: dict[str, Any] = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    return Config.model_validate(data)