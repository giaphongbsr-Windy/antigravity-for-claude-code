# Hạn mức gói Google AI Plus

Anh Phong đang dùng **Google AI Plus** (tính đến 10/2026). Số liệu theo bảng gói Google One và blog bên thứ ba — đối chiếu lại trang gói của Google trước khi dựa vào con số.

| Dịch vụ | Hạn mức Plus | Cách xử lý |
|---|---|---|
| Antigravity / `agy` | "Limited", làm mới theo tuần như Free, không mua thêm credit | Chỉ delegate khi việc vượt rõ ngưỡng hoà vốn. Tier mặc định `flash`; `flash-lo` cho việc vặt; `pro` chỉ khi thật cần. Tránh fan-out nhiều agent con và `agy-handoff` cho việc nhỏ. |
| Google Flow | **200 credit/tháng** | Mỗi lần tạo: báo trước số credit dự kiến và chờ anh xác nhận. Thử prompt bằng ảnh trước khi làm video. Không bấm "Always approve". |
| NotebookLM (Gemini Notebook) | Hạn mức "More", notebook "Large" | Kênh rẻ nhất cho đọc/tổng hợp tài liệu → ưu tiên `nlm` thay vì đốt quota agy. |

- Wrapper trả **exit 10 / `AGY_SIGNAL` QUOTA_EXHAUSTED** → không thử lại liên tục; Claude tự làm phần việc đó và báo anh là quota agy tuần này đã hết.
- Đo thực tế 30/10/2026 (agy 1.4.11, gói Plus): `agy models` chỉ có Gemini 3.8 Flash (High/Medium/Low), Claude Sonnet/Opus 4.6, GPT-OSS 120B — **không có Argon/Pro**. Đã đặt `tier_pro = "Gemini 3.8 Flash (High)"` trong `~/.claude/settings.json` của WSL, nên `--tier pro` thực chất chạy Flash High. Không remap sang model Claude (mất ý nghĩa kiểm chéo khác hãng).
- Gemini 3.8 Flash headless hay tự đòi chạy lệnh shell khi prompt không chứa sẵn dữ liệu → bị từ chối (`PERMISSION_DENIED`, denied: command). Với việc chỉ đọc: đưa nội dung vào prompt (stdin `-`) và ghi rõ "không cần dùng tool"; chỉ dùng `--yolo` trên nhánh riêng khi thật cần.
- Exit 14 (model không có trong `agy models`) thường do gói Plus không có model của tier → remap `tier_pro`/`tier_flash` sang model mà `agy models` liệt kê (đặt trong `~/.claude/settings.json` → `pluginConfigs["antigravity@antigravity-for-claude-code"].options`).
