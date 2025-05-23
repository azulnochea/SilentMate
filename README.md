# 🔕 SilentMate

SilentMate is an open-source app that automatically switches your device to silent mode during scheduled times like lectures or meetings.  
It helps users maintain digital etiquette without worrying about forgetting to mute their phone.

---

## ✨ Features

- Add/edit/delete scheduled silent times
- Automatically switch to silent mode during the set period
- Restore sound mode after the time ends
- Display current mode status (e.g. “Now in silent mode”)
- Simple and clear UI

---

## 🧑‍🤝‍🧑 Team Members & Branches

| Name | Role | Git Branch |
|------|------|------------|
| Kim Eunju | 전체 UI 정리 + README + 백엔드 일부 보조 | `feature/ui-readme` |
| Cho Yoonah | 시간표 입력 기능 개발 | `feature/schedule-ui` |
| Roh Hajin | 무음모드 타이머 로직 구현 | `feature/silent-timer` |
| Yoon Soyoung | 현재 상태 표시 및 설정 저장 | `feature/status-storage` |

---

## 💻 Tech Stack

- Python with Tkinter *(or HTML/JS if using web)*
- GitHub for version control & collaboration
- JSON for local storage (optional)

---

## 🧭 How to Run (Python example)

```bash
git clone git@github.com:your-id/SilentMate.git
cd SilentMate
python3 main.py

