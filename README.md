# Markdown Knowledge Organizer

Project lưu trữ file Markdown raw và bản đã chuẩn hóa.

## Cấu trúc

- `raw/`: đặt các file Markdown gốc, giữ nguyên nội dung.
- `formatted/`: kết quả được tạo tự động, giữ nguyên tên và cấu trúc thư mục.
- `reports/`: báo cáo JSON của mỗi lần chạy.
- `tools/reformat_markdown.py`: formatter batch, không tự sửa câu chữ.

## Cài đặt

Yêu cầu Python 3.10+ và Node.js 18+ nếu muốn chạy markdownlint cục bộ:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
npm install
```

## Reformat file

Đặt file `.md` vào `raw/`, sau đó chạy:

```bash
.venv/bin/python tools/reformat_markdown.py
```

Formatter sẽ chuẩn hóa line ending, khoảng trắng cuối dòng, dòng trống liên tiếp,
heading ATX và khoảng trắng sau marker của danh sách. Nội dung câu chữ được giữ nguyên.

## Kiểm tra

```bash
npm run lint
```

GitHub Actions cũng chạy formatter và markdownlint trên mỗi push hoặc pull request.

## MarkItDown

MarkItDown được khai báo như plugin tùy chọn để chuyển đổi các định dạng tài liệu
khác sang Markdown trước khi đưa vào `raw/`:

```bash
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/markitdown input.docx > raw/input.md
```
