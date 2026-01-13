# Установка зависимостей из vendor директории

Данный проект содержит предварительно загруженные зависимости в директории `vendor/`, что позволяет ускорить процесс установки.

## Быстрая установка

Для быстрой установки всех зависимостей выполните:

```bash
bash install-vendor-deps.sh
```

Или через npm:

```bash
npm run install-vendor
```

## Структура vendor директории

- `vendor/node_modules/` - предварительно загруженные npm пакеты
- `vendor/python_packages/` - предварительно загруженные Python пакеты в формате whl

## Установка вручную

Если вы хотите установить зависимости вручную:

### Node.js зависимости
```bash
# Создание символической ссылки вместо установки
ln -sf ../vendor/node_modules ./
```

### Python зависимости
```bash
pip install --find-links ./vendor/python_packages -r requirements.txt --no-index
```

## Обновление зависимостей

Если вам нужно обновить зависимости, просто удалите vendor директорию и переустановите пакеты:

```bash
rm -rf vendor/
mkdir -p vendor/{node_modules,python_packages}

# Загрузка Python пакетов
pip download -r requirements.txt -d vendor/python_packages/

# Установка Node.js пакетов и копирование
npm install
cp -r node_modules/* vendor/node_modules/
```

После этого используйте тот же скрипт установки `install-vendor-deps.sh` для использования подготовленных зависимостей.