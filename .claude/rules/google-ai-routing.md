# Chọn công cụ Google AI nào

| Việc | Công cụ | Ghi chú |
|---|---|---|
| Hỏi đáp có trích dẫn từ tài liệu của anh, tổng hợp nhiều nguồn, Audio/Video Overview, slide, quiz, mind map | `nlm` (NotebookLM CLI/MCP, `jacob-bd/gemini-notebook-mcp-cli`) | Dùng skill do `nlm skill install` cài. Upload tài liệu nội bộ công ty, share notebook công khai → hỏi anh trước. |
| Web/Google search, deep research, đọc audio/video/ảnh, cross-model review, việc code hàng loạt | plugin `antigravity` (`agy-delegate`, `/antigravity:*`) | Chỉ trong Claude Code/WSL. Xem `quota-ai-plus.md`. |
| Tạo video/ảnh bằng Veo, Nano Banana trên Flow | skill `google-ai:google-flow` (trình duyệt) | Tốn credit Flow — luôn xác nhận trước. |
| Veo/Nano Banana/TTS/Lyria qua API | MCP genmedia của Google (`GoogleCloudPlatform/genmedia-creative-studio`) | **Chưa cài** — cần project GCP có billing. |

- Đã loại: `PleasePrompto/notebooklm-skill`/`-mcp` (archive 09/2026), `jamubc/gemini-mcp-tool` (trùng plugin antigravity), các MCP Flow cộng đồng (`google-labs-mcp`, `google-flow-automation`… — rất ít người dùng, bám vào phiên Chrome đăng nhập).
- Kết quả từ Gemini/NotebookLM là bằng chứng phải kiểm lại: số liệu, trích dẫn quan trọng thì đối chiếu nguồn gốc trước khi đưa cho anh.
- Claude Cowork không chạy được `agy`; ở Cowork chỉ dùng NotebookLM (skill zip của `nlm`) và Flow (trình duyệt).
