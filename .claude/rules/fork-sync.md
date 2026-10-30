# Giữ fork dễ đồng bộ với upstream

- Remote `upstream` = `yuting0624/antigravity-for-claude-code`; đồng bộ bằng `git fetch upstream && git merge upstream/master` trên nhánh riêng, chạy lại `bash tests/run-tests.sh` sau khi merge.
- Thêm tính năng của fork vào `google-ai/` và `.claude/`, KHÔNG sửa `scripts/`, `skills/antigravity/`, `agents/`, `hooks/`, `commands/` trừ khi đang làm một bản sửa định gửi PR lên upstream.
- File upstream duy nhất fork cố ý sửa: `.claude-plugin/marketplace.json` (thêm entry plugin `google-ai`) và `CLAUDE.md` (mới). Khi merge xung đột ở đây, giữ cả entry của upstream lẫn của fork.
- Không bump version `antigravity` trong `plugin.json`/`SKILL.md` vì việc của fork; plugin `google-ai` có version riêng trong `google-ai/.claude-plugin/plugin.json`.
- Push lên `origin` (fork của anh Phong) chỉ khi anh đồng ý; không mở PR lên upstream nếu chưa được yêu cầu.
