## Context

目前 `config.py` 使用 Python 標準函式庫的 `os.getenv()` 來讀取環境變數，但存在以下問題：

1. **無環境變數檔案**：專案中沒有 `.env` 檔案，開發者無法直觀了解有哪些可設定的環境變數
2. **無型別驗證**：以 `os.getenv()` 取得的字串需手動轉型（如 `int(os.getenv("PORT", "8000"))`），容易因型別錯誤導致執行時期異常
3. **硬編碼與重複**：`main.py` 中再次寫死了 `title`、`version`、`host`、`port`，與 `config.py` 的預設值不一致
4. **缺乏安全設定**：沒有 `SECRET_KEY` 等 JWT 相關設定，日後實作認證仍需補上
5. **無環境區隔**：開發、測試、正式環境共用同一套預設值，缺乏管理機制

此設計文件說明如何以 `pydantic-settings` 取代既有實作，並建立完整的環境變數管理方案。

## Goals / Non-Goals

**Goals:**
- 以 `pydantic-settings` 取代手動 `os.getenv()` 呼叫
- 支援從 `.env` 檔案載入設定（OS 環境變數優先）
- 建立型別安全的 Settings class，含自動型別轉換與驗證
- 將設定依功能分類（database / app / server / security）
- 新增安全相關設定（SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES）
- 建立 `.env.example` 提供開發者參考
- 將 `.env` 加入 `.gitignore`
- 讓 `main.py` 從 `settings` 讀取 host/port/title/version

**Non-Goals:**
- 不支援多環境（dev/staging/prod）各自的 `.env` 檔案切換（未來可用 `ENV` 環境變數實作，但不在本次範圍）
- 不包含設定變更的熱載入（hot-reload）
- 不處理資料庫密碼等敏感資訊的加密儲存（僅不提交至版控）
- 不會改動現有 API 路由或資料庫連線邏輯

## Decisions

### Decision 1: 使用 pydantic-settings 取代 os.getenv()

**選擇**: `pydantic-settings` (BaseSettings + SettingsConfigDict)

**理由**:
- FastAPI 專案已依賴 Pydantic，`pydantic-settings` 為官方擴充套件，無需引入第三方套件
- 自動支援 `.env` 檔案載入、型別轉換、巢狀模型與 alias/prefix
- 比手動 `os.getenv()` + 型別轉換更安全且易於維護

**替代方案考量**:
- `python-decouple`：功能較簡單，但缺少型別驗證
- 自訂 Config Loader：沒有必要重新發明輪子

### Decision 2: 使用 Pydantic nested model + prefix 分群

**選擇**: 以 Pydantic nested model 搭配 `model_config["env_prefix"]` 區隔各群組

```python
class Settings(BaseSettings):
    database: DatabaseSettings  # 環境變數前綴: DATABASE_
    app: AppSettings           # 環境變數前綴: APP_
    server: ServerSettings     # 環境變數前綴: SERVER_
    security: SecuritySettings # 環境變數前綴: SECURITY_
```

**理由**:
- 語意清晰，透過 `settings.database.URL` 替代 `settings.DATABASE_URL`
- prefix 機制讓環境變數命名有規律（如 `DATABASE_URL`, `APP_TITLE`, `SERVER_HOST`）
- 避免單一 class 膨脹為大量扁平欄位

**替代方案考量**:
- 全部扁平化：所有欄位寫在同一個 class，變數名稱以 prefix 手動命名。物件導向性較差，不適合擴充
- 獨立多個 Settings class：載入邏輯需自行組合，增加複雜度

### Decision 3: 使用 SettingsConfigDict 設定 model 配置

**選擇**: 透過 `model_config` 指定 `env_file` 和 `env_file_encoding`

```python
model_config = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
    extra="ignore"
)
```

**理由**:
- `pydantic-settings` 原生支援 `.env` 載入，無需額外程式碼
- `extra="ignore"` 避免因環境變數中有不相干變數而噴錯
- OS 環境變數優先於 `.env` 是 `pydantic-settings` 預設行為

## Risks / Trade-offs

- **[相容性]** 既有 `settings.DATABASE_URL` 存取方式需改為 `settings.database.URL`
  - → 因目前僅在少數檔案中引用，影響範圍小，但仍需逐一確認
- **[新依賴]** 需新增 `pydantic-settings` 至相依套件
  - → `uv add pydantic-settings` 即可解決
- **[開發者習慣]** 開發者需記得複製 `.env.example` 為 `.env` 並填入實際值
  - → 在文件與 `.env.example` 中明確提醒
- **[SECRET_KEY 預設值]** 設定預設值可能會讓開發者在正式環境忘記設定
  - → 若未設定則在啟動時 log warning，並不給予預設值（設為 Optional[str] = None）