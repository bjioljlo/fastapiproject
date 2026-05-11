## Why

目前的 `config.py` 使用 `os.getenv()` 直接讀取環境變數，但專案中不存在 `.env` 檔案，導致所有設定值都只能依賴程式碼中的預設值，缺乏正式的管理機制。同時缺少型別驗證、環境區隔（dev/staging/prod）以及安全敏感資訊（如資料庫密碼）的保護機制。這在多人協作與部署時會造成設定混亂與安全風險。

## What Changes

- **採用 pydantic-settings**：取代 `os.getenv()`，以 Pydantic 模型進行環境變數讀取、型別驗證與自動轉換
- **建立 `.env` 機制**：支援從 `.env` 檔案載入設定，並提供 `.env.example` 作為範本
- **新增 `.env` 至 `.gitignore`**：避免將環境變數（含敏感資訊）提交至版本控制
- **設定分類重構**：將設定依用途拆分為 Database、App、Server、Security、Logging 等類別（但仍在同一個 Settings class 中，以 Pydantic model 的嵌套或 prefix 機制管理）
- **新增必要的設定欄位**：如 `SECRET_KEY`、`ALGORITHM`、`ACCESS_TOKEN_EXPIRE_MINUTES` 等安全相關設定，為未來 JWT 等功能做準備
- **移除 `config.py` 中對 `main.py` 的硬編碼**：`main.py` 中已重複定義 `title`、`version`、`host`、`port`，應統一從 `settings` 讀取

## Capabilities

### New Capabilities
- `env-config`: 基於 pydantic-settings 的環境變數管理系統，支援 `.env` 檔案載入、型別驗證、環境區隔

### Modified Capabilities
- （無既有 spec 需要修改）

## Impact

- 受影響檔案：
  - `src/fast_api_project/core/config.py` — 完全重寫
  - `src/fast_api_project/main.py` — 改用從 settings 讀取 host/port/title/version
  - `.gitignore` — 加入 `.env`
- 新增檔案：
  - `.env.example` — 環境變數範本（提交至版控）
  - `.env` — 實際環境變數（不提交至版控，由開發者自行建立）
- 新增依賴：`pydantic-settings`（或升級既有 `pydantic` 版本）
- 既有 `Settings` class 的公開 API 會變更，但由於目前僅在 `main.py` 中直接 `from config import settings`，影響範圍可控