# FastAPI Project with uv Tooling

一個使用現代 uv 工具的 FastAPI 項目，已從過時的結構遷移至符合當代最佳實踐的項目結構。

## 項目特色

- 使用 FastAPI 框架
- SQLAlchemy 2.0+ ORM
- uv 工具進行依賴管理和運行
- 模組化的路由結構（API v1 和 v2）
- 支援 MySQL 數據庫

## 安裝和運行

### 使用 uv 工具

1. 安裝 uv（如果尚未安裝）：
```bash
pip install uv
```

2. 安裝依賴：
```bash
uv sync
```

3. 開發模式運行：
```bash
uv run dev
```

4. 生產模式運行：
```bash
uv run start
```

### 使用傳統方式

1. 安裝依賴：
```bash
pip install -r requirements.txt
```

2. 運行應用：
```bash
python main.py
```

## 項目結構

```
FastAPI/
├── src/                      # 源代碼目錄
│   └── fast_api_project/     # 主要應用包
│       ├── __init__.py
│       ├── main.py          # 應用入口點
│       ├── core/           # 核心模組
│       │   ├── __init__.py
│       │   ├── config.py   # 配置設置
│       │   └── database.py # 數據庫配置
│       ├── models/         # 數據模型
│       │   ├── __init__.py
│       │   └── question.py # 數據模型
│       ├── api/            # API 路由
│       │   ├── __init__.py
│       │   ├── v1/        # API 版本 1
│       │   │   ├── __init__.py
│       │   │   ├── routers.py
│       │   │   └── endpoints/
│       │   │       ├── __init__.py
│       │   │       ├── blog.py
│       │   │       └── questions.py
│       │   └── v2/        # API 版本 2
│       │       ├── __init__.py
│       │       ├── routers.py
│       │       └── endpoints/
│       │           ├── __init__.py
│       │           ├── blog.py
│       │           └── questions.py
│       └── schemas/        # Pydantic 模式（預留）
├── tests/                  # 測試文件
├── pyproject.toml         # uv 配置文件
└── README.md              # 項目文檔
```

## API 端點

### 基礎端點
- `GET /` - 首頁

### API v1
- `GET /api/v1/questions/{question_id}` - 獲取問題
- `GET /api/v1/blog/{id}` - 獲取博客
- `GET /api/v1/blog/{id}/{comments}` - 獲取博客評論

### API v2
- `GET /api/v2/questions/{question_id}` - 獲取問題（v2）
- `GET /api/v2/blog/{id}` - 獲取博客（v2）
- `GET /api/v2/blog/{id}/{comments}` - 獲取博客評論（v2）

## 數據庫配置

默認配置使用 MySQL 數據庫：
- 主機：localhost
- 端口：3306
- 數據庫名：fastapi
- 用戶名：root
- 密碼：123456

如需修改配置，請編輯 `database.py` 文件中的 `URL_DATABASE` 變量。

## 開發工具

項目已配置以下開發工具：
- pytest - 測試框架
- black - 代碼格式化
- ruff - 代碼檢查

## 主要更新

此項目已從過時結構遷移至現代 uv 工具支持的結構：

1. 更新了 SQLAlchemy 至 2.0+ 版本
2. 使用 uv 工具進行依賴管理
3. 統一了導入路徑
4. 移除了 Flask 相關代碼
5. 添加了現代化的配置文件

## 貢獻

歡迎提交 Issue 和 Pull Request 來改進這個項目。