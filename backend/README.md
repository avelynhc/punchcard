## How to run existing database migration files
- `docker compose up punchcard-migration`

## How to generate a new migration file
- `docker compose run punchcard-migration create -ext sql -dir /migrations -seq {NEW MIGRATION FILE NAME}`
