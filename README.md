# Markdown Knowledge Organizer

Project lưu trữ file Markdown raw và bản đã chuẩn hóa.

## Cấu trúc

- `raw/`: đặt các file Markdown gốc, có thể chia thành nhiều thư mục con.
- `formatted/`: kết quả được tạo tự động, giữ nguyên tên, toàn bộ cấu trúc thư mục
  và các asset (ảnh, file đính kèm) tương ứng với `raw/`.
- `reports/`: báo cáo JSON của mỗi lần chạy.
- `tools/reformat_markdown.py`: formatter batch, không tự sửa câu chữ.
- `tools/group_markdown.py`: đề xuất nhóm theo embeddings và tạo tài liệu tổng hợp sau duyệt.

## Cài đặt

Yêu cầu Python 3.10+ và Node.js 18+ nếu muốn chạy markdownlint cục bộ:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
npm install
```

## Reformat file

Đặt file `.md` vào `raw/` hoặc bất kỳ thư mục con nào, sau đó chạy lệnh từ thư mục
gốc của project:

```bash
.venv/bin/python tools/reformat_markdown.py
```

Ví dụ `raw/classification/Concepts_Theory/topic.md` sẽ tạo thành
`formatted/classification/Concepts_Theory/topic.md`. Các file không phải `.md`
trong `raw/` được sao chép nguyên trạng để các link ảnh/file tương đối tiếp tục hoạt động.

Để loại trừ thư mục local-only khỏi kết quả public, dùng `--exclude-dir`:

```bash
.venv/bin/python tools/reformat_markdown.py --exclude-dir Login_Credentials
```

Thư mục `raw/Login_Credentials/` và kết quả tương ứng được giữ local và đã được
đưa vào `.gitignore`.

Formatter sẽ chuẩn hóa line ending, khoảng trắng cuối dòng, dòng trống liên tiếp,
heading ATX và khoảng trắng sau marker của danh sách. Nội dung câu chữ được giữ nguyên.

## Kiểm tra

```bash
npm run lint
```

GitHub Actions chạy markdownlint đệ quy trên các file `.md` trong cả `raw/` và
`formatted/` ở mỗi push hoặc pull request. Hãy chạy formatter cục bộ trước khi
commit để cập nhật `formatted/` và `reports/`.

## MarkItDown

MarkItDown được khai báo để chuyển đổi các định dạng tài liệu
khác sang Markdown trước khi đưa vào `raw/`:

```bash
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/markitdown input.docx > raw/input.md
```

MarkItDown được pin ở bản `0.1.7`. Không dùng extra `all` trong môi trường Python
3.14 trên macOS vì extra này kéo theo một số dependency tùy chọn chưa có wheel
tương thích.

## Gom nhóm theo chủ đề bằng local embeddings và Gemini

Đây là quy trình hai bước. Bước phân nhóm chạy local, miễn phí và không cần API
key. Model `all-MiniLM-L6-v2` được tải về máy và cache bởi
`sentence-transformers`:

```bash
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python tools/group_markdown.py propose --input formatted
```

Lệnh trên tạo `reports/group-proposals.json` và cache embeddings trong `.cache/`.
Hai file này là dữ liệu local/review nên không được commit lên GitHub.
Mở JSON, kiểm tra từng nhóm rồi đổi `approved` thành `true` cho nhóm muốn gom.
Chỉ bước viết lại/OCR dưới đây mới cần Gemini API key:

```bash
export GEMINI_API_KEY="..."
.venv/bin/python tools/group_markdown.py build
```

Kết quả được tạo trong `grouped/` (local-only mặc định vì nội dung được viết lại
bởi Gemini). Hệ thống giữ ngôn ngữ và thuật ngữ nguồn, gửi ảnh liên quan để OCR/mô
tả, yêu cầu tài liệu tổng hợp giữ phần Sources, và copy ảnh nguồn vào
`grouped/assets/<group-id>/`. Nếu muốn lưu kết quả lên GitHub, hãy kiểm tra thủ
công nội dung/OCR trước rồi bỏ `grouped/` khỏi `.gitignore`.
