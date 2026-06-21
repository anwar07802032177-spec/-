# 🛠️ دليل تشغيل المشروع على macOS للتطوير

## المتطلبات
- Python 3.10 أو أحدث (تحقق: `python3 --version`)
- Git

إن لم يكن Python مثبّتاً، ثبّته عبر [Homebrew](https://brew.sh):
```bash
brew install python git
```

---

## خطوات التشغيل (أول مرة)

```bash
# 1. نسخ المشروع من GitHub
git clone https://github.com/anwar07802032177-spec/-.git jamaiti
cd jamaiti

# 2. إنشاء بيئة افتراضية
python3 -m venv venv

# 3. تفعيل البيئة الافتراضية
source venv/bin/activate

# 4. تثبيت الحزم
pip install -r requirements.txt

# 5. إنشاء قاعدة البيانات
python manage.py migrate

# 6. إنشاء مستخدم مدير (سيطلب اسماً وكلمة مرور)
python manage.py createsuperuser

# 7. تشغيل الخادم
python manage.py runserver
```

ثم افتح المتصفح على: **http://127.0.0.1:8000/**

---

## التشغيل اليومي (بعد أول مرة)

```bash
cd jamaiti
source venv/bin/activate
python manage.py runserver
```

لإيقاف الخادم: اضغط `Control + C`

---

## أوامر مفيدة أثناء التطوير

| الأمر | الوظيفة |
|-------|---------|
| `python manage.py runserver` | تشغيل الخادم |
| `python manage.py makemigrations` | إنشاء ترحيلات بعد تعديل النماذج |
| `python manage.py migrate` | تطبيق الترحيلات على قاعدة البيانات |
| `python manage.py createsuperuser` | إنشاء مستخدم إداري |
| `python manage.py shell` | صدفة بايثون تفاعلية |
| `deactivate` | الخروج من البيئة الافتراضية |

---

## ملاحظات مهمة

- **قاعدة البيانات** (`db.sqlite3`) و**البيئة الافتراضية** (`venv/`) غير مرفوعة على Git عمداً — كل مطوّر ينشئها محلياً.
- لوحة إدارة Django متاحة على: **http://127.0.0.1:8000/admin/**
- عند تعديل ملفات `models.py` نفّذ دائماً: `makemigrations` ثم `migrate`.

---

## بنية المشروع

```
jamaiti/      إعدادات المشروع (عربي + RTL)
accounts/     المصادقة ولوحة القيادة
members/      الأعضاء والاشتراكات
templates/    قوالب HTML عربية (Bootstrap 5 RTL)
requirements.txt   قائمة الحزم
```
