# Chạy trên WSL

- `agy` và Claude Code dùng cho repo này chạy trong **WSL Ubuntu** (user `phongdg`), repo ở `~/antigravity-for-claude-code`.
- Không clone/chạy repo từ `/mnt/c` hay `/mnt/d`: agy đọc workspace qua cầu 9p, chậm ~10× (wrapper và `agy-doctor` sẽ cảnh báo).
- Không chạy `agy -p` từ Windows gốc (Git Bash/PowerShell): headless agy cần ConPTY, dễ treo rồi trả exit 12 (upstream issue #6).
- Từ Windows mở file repo qua `\\wsl.localhost\Ubuntu\home\phongdg\antigravity-for-claude-code`; chạy lệnh qua `wsl.exe -d Ubuntu -- bash -lc '...'`.
- `nlm` (NotebookLM CLI) thì ngược lại: cài và đăng nhập trên **Windows** (Python thuần, không vướng ConPTY), vì Claude Desktop/Cowork chạy trên Windows.
