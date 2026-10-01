"""Rebuild data/games.csv from public sportsdataverse releases.

No API key. Source files are ESPN-derived schedules, betting lines, and team
metadata published by sportsdataverse/sportsdataverse-data.
"""

from pathlib import Path

import pandas as pd

SEASONS = (2023, 2024, 2025)
RELEASE = "https://github.com/sportsdataverse/sportsdataverse-data/releases/download"
OUT = Path(__file__).resolve().parents[1] / "data" / "games.csv"


def _url(tag: str, name: str) -> str:
    return f"{RELEASE}/{tag}/{name}"


def build(seasons=SEASONS) -> pd.DataFrame:
    frames = []
    for year in seasons:
        betting = pd.read_csv(_url("espn_cfb_betting", f"betting_{year}.csv"))
        schedule = pd.read_csv(_url("espn_cfb_schedules", f"cfb_schedule_{year}.csv"))
        teams = pd.read_csv(_url("espn_cfb_teams", f"cfb_teams_{year}.csv"))
        teams = teams[
            ["team_id", "conference_abbreviation", "is_fbs"]
        ].drop_duplicates("team_id")
        games = schedule.merge(betting, on=["game_id", "season", "week"], how="inner")
        games = games.merge(
            teams.add_prefix("home_"), left_on="home_id", right_on="home_team_id", how="left"
        )
        games = games.merge(
            teams.add_prefix("away_"), left_on="away_id", right_on="away_team_id", how="left"
        )
        frames.append(games)
    df = pd.concat(frames, ignore_index=True)
    df = df[
        (df.status == "STATUS_FINAL")
        & df.game_spread_available
        & df.home_team_spread.notna()
        & (df.home_is_fbs == True)
        & (df.away_is_fbs == True)
        & (~df.neutral_site.astype(bool))
    ].copy()
    df["home_margin"] = df.home_score - df.away_score
    df["home_cover_margin"] = (df.home_margin + df.home_team_spread).round(1)
    df["home_covered"] = (df.home_cover_margin > 0).astype(int)
    df["push"] = (df.home_cover_margin.abs() < 1e-6).astype(int)
    df["role"] = [
        "home_favorite" if spread < 0 else "home_dog" if spread > 0 else "pickem"
        for spread in df.home_team_spread
    ]
    keep = [
        "game_id",
        "season",
        "week",
        "game_date",
        "home_team",
        "away_team",
        "home_conference_abbreviation",
        "away_conference_abbreviation",
        "home_score",
        "away_score",
        "home_margin",
        "home_team_spread",
        "over_under",
        "home_cover_margin",
        "home_covered",
        "push",
        "role",
        "venue",
    ]
    return df[keep].sort_values(["season", "week", "game_id"])


if __name__ == "__main__":
    games = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    games.to_csv(OUT, index=False)
    print(f"wrote {len(games)} games to {OUT}")
