# Home dogs and the spread

Do college football home underdogs cover more often than the line says they should?

I tested that on **2,193 finished FBS games** from the 2023–2025 seasons that had a posted spread and were not on a neutral site. Home underdogs covered **50.4%** of the time. Home favorites covered **49.2%**. The side the market favored covered **49.3%**. That is a coin flip. The folk theory does not show up in the full sample.

The interesting part is where the sample splits, and where it does not survive a confidence interval.

## The question

A home underdog is a team playing at home and getting points. The claim you hear on Saturdays is that those teams are undervalued: the crowd, the routine, and the travel hit on the visitor are not fully priced in.

If that were true, home dogs would cover more than half the time, and the average cover margin would sit clearly above zero. A fair closing line should land near 50% once pushes are removed, because the price already includes the home edge.

This is not a betting system. It is a check on whether a common story survives the games.

## Result

| Slice | Games | Home cover rate | 95% interval | Avg cover margin |
| --- | ---: | ---: | --- | ---: |
| All home teams | 2,193 | 49.6% | 47.5–51.7% | +0.48 |
| Home favorites | 1,367 | 49.2% | 46.5–51.8% | +0.51 |
| Home underdogs | 826 | 50.4% | 47.0–53.8% | +0.43 |
| Home dogs getting 0–3 | 190 | 54.2% | 47.1–61.1% | +2.06 |
| ACC home dogs | 100 | 56.0% | 46.2–65.3% | +2.04 |
| Big Ten home dogs | 101 | 42.6% | 33.4–52.3% | −2.72 |
| SEC home dogs | 83 | 49.4% | 38.9–59.9% | +0.19 |

Cover margin is `home score − away score + home spread`. Positive means the home team beat the number. A home spread of −7.5 means the home team is laying 7.5. A home spread of +6.5 means it is getting 6.5.

Every interval above includes 50%. Short home dogs and ACC home dogs ran hot. Big Ten home dogs ran cold. None of those splits is large enough to call a market error. The honest finding is that the line already prices home field, and the leftovers are noise at this sample size.

## How a game is graded

`home_team_spread` is the home team's number.

- Home favorite: spread < 0
- Home underdog: spread > 0
- Home covers: `home_score + home_team_spread > away_score`
- Neutral-site games are out, because "home" is not meaningful there
- Both teams have to be FBS in that season's team file
- Pushes would be dropped from the rate. This extract has zero

## Reproduce

The cleaned file is already in `data/games.csv`. Queries are in `sql/cover_rates.sql`.

```bash
sqlite3 :memory: \
  ".mode column" \
  ".headers on" \
  ".import --csv data/games.csv games" \
  ".read sql/cover_rates.sql"
```

To rebuild the CSV from the public source files:

```bash
pip install -r requirements.txt
python src/build_dataset.py
```

## Data

Schedules, betting lines, and conference labels come from the public [sportsdataverse-data](https://github.com/sportsdataverse/sportsdataverse-data) releases (`espn_cfb_schedules`, `espn_cfb_betting`, `espn_cfb_teams`), which are built from ESPN. In that betting extract, a usable spread is only consistently present from 2023 on, so earlier seasons are not in the sample. Lines are whatever that release resolved as the game spread. They are not a guaranteed closing line from one book.

## What I would add next

- Grade the same games against the opening line, not just the posted spread, to see if the move is where the edge was.
- Split rest days and true road trips. A short-week visitor is a cleaner test of the travel story than conference label.
- Pre-register the ACC vs Big Ten contrast on 2026 games instead of reading it out of the same sample that suggested it.
