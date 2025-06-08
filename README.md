# 🔕 SilentMate

SilentMate는 시간표 기반 자동 무음 모드 전환 웹 앱입니다.  
수업 시간에 맞춰 자동으로 무음 모드로 전환되고, 사용자가 수동으로도 무음 설정을 변경할 수 있습니다.

---

## ✨ 주요 기능

- 📅 시간표 기반 자동 무음 모드
- 🔕 수동 무음 모드 전환 가능
- 🎯 현재 모드 상태 표시 (수업중 / 일반 모드)
- 🖥️ 웹 기반 UI 제공 (Flask)
- 💾 SQLite 데이터베이스 기반 저장

---

## 🧑‍🤝‍🧑 팀원 & 작업 브랜치

| 이름 | 역할 | Git Branch |
|------|------|------------|
| Kim Eunju | 전체 UI 정리 + README + 백엔드 일부 보조 | `feature/ui-readme` |
| Cho Yoonah | 시간표 입력 기능 개발 | `feature/schedule-ui` |
| Roh Hajin | 무음모드 타이머 로직 구현 | `feature/silent-timer` |
| Yoon Soyoung | 현재 상태 표시 및 설정 저장 | `feature/status-storage` |

---

## 💻 기술 스택

- Python 3.x
- Flask (웹 서버 및 라우팅)
- SQLite (DB 저장)
- GitHub (버전 관리 및 협업)
- HTML + CSS (웹 프론트엔드)

---

## 🚀 실행 방법

1️⃣ 프로젝트 클론

```bash
git clone git@github.com:azulnochea/SilentMate.git
cd SilentMate
