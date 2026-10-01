-- Home side covers when home_cover_margin > 0.
-- home_team_spread is from the home team's point of view:
--   negative = home favorite, positive = home underdog.
-- Pushes are excluded from cover rate. This extract has none.

-- 1. Cover rate by role
SELECT
    role,
    COUNT(*) AS games,
    SUM(home_covered) AS home_covers,
    ROUND(AVG(home_covered), 3) AS home_cover_rate,
    ROUND(AVG(home_cover_margin), 2) AS avg_cover_margin
FROM games
WHERE push = 0
GROUP BY role
ORDER BY games DESC;

-- 2. Home underdogs by spread bucket
SELECT
    CASE
        WHEN home_team_spread <= 3 THEN '0-3'
        WHEN home_team_spread <= 7 THEN '3-7'
        WHEN home_team_spread <= 14 THEN '7-14'
        WHEN home_team_spread <= 21 THEN '14-21'
        ELSE '21+'
    END AS points_received,
    COUNT(*) AS games,
    ROUND(AVG(home_covered), 3) AS home_cover_rate,
    ROUND(AVG(home_cover_margin), 2) AS avg_cover_margin
FROM games
WHERE role = 'home_dog' AND push = 0
GROUP BY 1
ORDER BY MIN(home_team_spread);

-- 3. Home underdogs by home conference
SELECT
    home_conference_abbreviation AS conference,
    COUNT(*) AS games,
    ROUND(AVG(home_covered), 3) AS home_cover_rate,
    ROUND(AVG(home_cover_margin), 2) AS avg_cover_margin
FROM games
WHERE role = 'home_dog' AND push = 0
GROUP BY 1
HAVING COUNT(*) >= 60
ORDER BY home_cover_rate DESC;
