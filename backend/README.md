# BACKEND

> MyPhone api

## Build Setup

``` bash
# python version
python3.8.5

# install dependencies
pip install requirements

# data migrate
python manage.py makemigrations [app]  # 生成迁移记录 默认所有
python manage.py migrate [app]  # 开始迁移

# serve start [default_port=8000]
python manage.py runserver [port]
```

## 环境报错问题

```markdown
ImportError: cannot import name 'SKIP_ADMIN_LOG' from 'import_export.admin'

因为admin.py更新后删除了两个文件，需要我们手动在其中添加如下代码：

文件路径：
python3.8/site-packages/import_export/admin.py

代码：
SKIP_ADMIN_LOG = getattr(settings, 'IMPORT_EXPORT_SKIP_ADMIN_LOG', False) 
TMP_STORAGE_CLASS = getattr(settings, 'IMPORT_EXPORT_TMP_STORAGE_CLASS', TempFolderStorage)
```