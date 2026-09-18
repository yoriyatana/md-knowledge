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

## Chuyển Evernote ENEX sang Markdown

Để tạo lại dữ liệu từ bản backup Evernote, đặt các file `.enex` vào
`raw_evernote/` rồi chạy:

```bash
.venv/bin/python tools/convert_evernote.py
```

Kết quả được tạo trước trong `raw_evernote_converted/` cùng báo cáo
`reports/evernote-conversion-report.json`. Công cụ giữ từng notebook thành thư mục,
chuyển ENML sang Markdown, giải mã resource nhúng và tạo link ảnh tương đối. Notebook
`Login Credentials` được bỏ qua để không đưa dữ liệu nhạy cảm vào vùng xử lý công khai.
Chỉ sau khi kiểm tra báo cáo và nội dung, mới đồng bộ kết quả vào `raw/`.

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

## Xây dựng kho kiến thức grouped theo manifest

Manifest deterministic chính thức nằm tại `reports/grouping-manifest.json`. Đây là
manifest version 3, với cấu trúc `Vendor -> Level 2 DocType -> Level 1 Domain ->
Level 3 Feature`. Tên thư mục và file generated luôn là lowercase kebab-case.
Các DocType cấp 2 cố định là:

- `index` — chỉ mục/source inventory được sinh tự động
- `concepts` — tài liệu khái niệm
- `configuration-guide` — tài liệu cấu hình
- `troubleshooting-guide` — tài liệu xử lý sự cố
- `install-maintenance-guide` — cài đặt/bảo trì
- `case-study` — case study

Mỗi group khai báo `vendor`, `level2_doctype`, `level1_domain`,
`level3_feature`; builder sinh `destination` theo mẫu
`vendor/doctype/domain/feature.md`. Dùng `configuration-guide` thống nhất,
không dùng `configuration-template`. Các source là đường dẫn tương đối bên trong
`formatted/`; nhóm index có thể dùng `source_directories`.

```bash
.venv/bin/python tools/build_grouped_knowledge.py plan
.venv/bin/python tools/build_grouped_knowledge.py build
```

`plan` kiểm tra tất cả nguồn có tồn tại và in kế hoạch. `build` tạo lại toàn bộ
`grouped/`, loại bỏ các block nội dung trùng nhau, sao chép ảnh và attachment được
tham chiếu với link tương đối đúng, tạo `grouped/index.md` và
`grouped/source-map.json`. Các note public chưa được consolidate vẫn được đưa vào
các nhóm `source-inventory/` theo thư mục nguồn để không bị bỏ sót; credentials
được loại trừ khỏi inventory. Thư mục `grouped/` là local-only cho đến khi nội
dung được review.
