# SLH Ground Station Journal

## 2026-08-21

- תחנת עבודה חדשה נוצרה ב-Termux.
- חבילות בסיסיות הותקנו.
- תיקיית העבודה נוצרה.
- GitHub עדיין לא מחובר.
- ממתין ל-URL של ה-repository ולהרשאות.

### Operating Rules

- Read-only first.
- Document before action.
- Snapshot before change.
- Verify after change.
- Commit small and clear.
- לעולם לא לשמור API keys או tokens בקוד.
- לעולם לא להציג secrets בצ'אט או בטרמינל.
- אין push ישירות ל-main.

## 2026-08-22 — Ground Station Verification

- Python verified: 3.13.13.
- Git verified: 2.54.0.
- GitHub remote verified: origin -> git@github.com:gold94guy-tech/slh-ground-station.git.
- Active branch verified: dev/ground-station.
- Working tree verified clean.
- GitHub SSH authentication verified for gold94guy-tech.
- .env verified to contain the required variable names without exposing secret values.
- .gitignore verified to protect .env, Python cache files, virtual environments, logs, and other local files.
- bot.py does not yet exist.
- Next planned step: create and verify the minimal Telegram bot.
