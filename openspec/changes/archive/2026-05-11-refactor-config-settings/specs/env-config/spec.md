## ADDED Requirements

### Requirement: System SHALL load environment variables from .env file
The system SHALL use `pydantic-settings` to load configuration from environment variables. When a `.env` file exists at the project root, the system SHALL automatically read variables from it. Environment variables set in the OS shell SHALL take precedence over those in `.env`.

#### Scenario: Load from .env file
- **WHEN** a `.env` file exists at the project root with valid key-value pairs
- **THEN** the Settings class SHALL load those values as defaults

#### Scenario: OS environment variable overrides .env
- **WHEN** both `.env` and OS environment variables define the same key
- **THEN** the OS environment variable value SHALL be used

#### Scenario: Missing .env file
- **WHEN** no `.env` file exists at the project root
- **THEN** the Settings class SHALL use only OS environment variables and built-in defaults

### Requirement: System SHALL validate environment variable types
The Settings class SHALL use Pydantic type annotations to validate and convert environment variables. Boolean values SHALL accept `"true"`/`"1"`/`"yes"` and `"false"`/`"0"`/`"no"`. Integer values SHALL be parsed from strings. Invalid values SHALL raise a `ValidationError` on instantiation.

#### Scenario: Valid boolean conversion
- **WHEN** `DEBUG=true` is set in environment
- **THEN** `settings.DEBUG` SHALL be `True` (Python bool)

#### Scenario: Invalid integer raises error
- **WHEN** `PORT=notanumber` is set in environment
- **THEN** Settings instantiation SHALL raise `ValidationError`

### Requirement: System SHALL separate configuration into logical groups
The Settings class SHALL organize configuration into logical groups using Pydantic sub-models: `database` (DB connection), `app` (title, version, debug), `server` (host, port), and `security` (secret key, algorithm, token expiry). Each group SHALL use the corresponding prefix (e.g., `DATABASE_` for database settings, `APP_` for app settings, `SERVER_` for server settings, `SECURITY_` for security settings) in environment variable names.

#### Scenario: Database settings via prefix
- **WHEN** `DATABASE_URL=sqlite:///test.db` is set
- **THEN** `settings.database.URL` SHALL equal `"sqlite:///test.db"`

#### Scenario: App settings via prefix
- **WHEN** `APP_TITLE=MyAPI` and `APP_DEBUG=true` are set
- **THEN** `settings.app.TITLE` SHALL equal `"MyAPI"` and `settings.app.DEBUG` SHALL be `True`

### Requirement: System SHALL include security-related settings
The Settings class SHALL include fields for `SECRET_KEY`, `ALGORITHM` (default: `"HS256"`), and `ACCESS_TOKEN_EXPIRE_MINUTES` (default: `30`). When `SECRET_KEY` is not provided via environment, the system SHALL generate a warning at startup to remind the developer to set it in production.

#### Scenario: Default security values
- **WHEN** no security environment variables are set
- **THEN** `settings.security.ALGORITHM` SHALL equal `"HS256"` and `settings.security.ACCESS_TOKEN_EXPIRE_MINUTES` SHALL equal `30`

#### Scenario: Missing SECRET_KEY warning
- **WHEN** `SECURITY_SECRET_KEY` is not set in environment
- **THEN** the system SHALL log a warning at startup

### Requirement: System SHALL provide a .env.example template
The project SHALL include a `.env.example` file at the project root with documented placeholder values for all configurable settings. This file SHALL be committed to version control.

#### Scenario: .env.example exists
- **WHEN** the repository is cloned
- **THEN** `.env.example` SHALL exist at the project root with all documented settings

### Requirement: System SHALL exclude .env from version control
The actual `.env` file SHALL be listed in `.gitignore` to prevent accidental commit of sensitive information.

#### Scenario: .env not tracked
- **WHEN** `git status` is run
- **THEN** `.env` SHALL NOT appear in tracked files

### Requirement: main.py SHALL use settings from config
The `main.py` SHALL use `settings.APP_TITLE`, `settings.APP_VERSION`, `settings.SERVER_HOST`, and `settings.SERVER_PORT` from the Settings class instead of hardcoded values. The `uvicorn.run()` call SHALL use `settings.SERVER_HOST` and `settings.SERVER_PORT`.

#### Scenario: App metadata from settings
- **WHEN** the FastAPI app is created
- **THEN** its `title` SHALL come from `settings.app.TITLE` and `version` from `settings.app.VERSION`

#### Scenario: Server starts with configured host/port
- **WHEN** `uvicorn.run()` is called
- **THEN** it SHALL use `settings.server.HOST` and `settings.server.PORT`