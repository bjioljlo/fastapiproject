## 1. 安裝新依賴

- [x] 1.1 安裝 `pydantic-settings` 套件：執行 `uv add pydantic-settings`

## 2. 重寫 config.py

- [x] 2.1 建立 `DatabaseSettings` Pydantic model，包含 `URL` 欄位（環境變數前綴 `DATABASE_`，預設值沿用既有連線字串）
- [x] 2.2 建立 `AppSettings` Pydantic model，包含 `TITLE`、`VERSION`、`DEBUG` 欄位（環境變數前綴 `APP_`）
- [x] 2.3 建立 `ServerSettings` Pydantic model，包含 `HOST`、`PORT` 欄位（環境變數前綴 `SERVER_`）
- [x] 2.4 建立 `SecuritySettings` Pydantic model，包含 `SECRET_KEY` (Optional[str])、`ALGORITHM` (預設 `"HS256"`)、`ACCESS_TOKEN_EXPIRE_MINUTES` (預設 `30`) 欄位（環境變數前綴 `SECURITY_`）
- [x] 2.5 建立 `Settings(BaseSettings)` 主 class，含 `database`、`app`、`server`、`security` 四個群組（扁平欄位 + property 提供巢狀存取），並設定 `model_config` 載入 `.env` 且 `extra="ignore"`
- [x] 2.6 在 Settings 初始化完成後，若 `SECRET_KEY` 未設定則 log warning
- [x] 2.7 保留 `settings = Settings()` 單例實例

## 3. 更新 main.py

- [x] 3.1 匯入 `from fast_api_project.core.config import settings`
- [x] 3.2 使用 `settings.app.TITLE` 和 `settings.app.VERSION` 建立 FastAPI 實例
- [x] 3.3 使用 `settings.server.HOST` 和 `settings.server.PORT` 呼叫 `uvicorn.run()`

## 4. 建立環境變數檔案

- [x] 4.1 建立 `.env.example` 於專案根目錄，包含所有設定欄位的註解說明與範例值
- [x] 4.2 在 `.gitignore` 中加入 `.env` 條目

## 5. 驗證與測試

- [x] 5.1 確認 `uv run python -c "from fast_api_project.core.config import settings; print(settings)"` 可正常執行
- [x] 5.2 確認 `uv run uvicorn src.fast_api_project.main:app` 可正常啟動（透過 import 測試確認）
- [x] 5.3 確認無 `.env` 時使用預設值正常運作
- [x] 5.4 確認有 `.env` 時正確載入值
- [x] 5.5 確認 `git status` 顯示 `.env` 不被追蹤