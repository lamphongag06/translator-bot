# Translator Telegram Bot

## 🔁 Chức năng:
- Dịch mọi ngôn ngữ sang tiếng Việt.
- Dịch tiếng Việt sang tiếng Anh.
- Giữ định dạng khi nhận tin nhắn (gõ, dán, chuyển tiếp).
- Dịch được cả văn bản trong ảnh.

## 🚀 Triển khai
### 1. Cài thư viện
```bash
pip install -r requirements.txt
```

### 2. Chạy thử bot trên máy:
```bash
python translator_bot.py
```

### 3. Deploy lên Render:
- Tạo Web Service mới.
- Upload tất cả các file.
- Đảm bảo có `Procfile`, `requirements.txt` và `translator_bot.py`.

## 📌 Ghi chú
- Token bot đã được cài sẵn trong `translator_bot.py`
- OCR ảnh sử dụng thư viện `pytesseract`, cần `tesseract` được cài trên server nếu muốn chạy ảnh.
