# 🚀 30초 빠른 실행 가이드 (Quick Start)

복잡한 설명 없이 바로 실행하고 싶다면 아래 3단계만 따라하세요.

### 1. 설치 (최초 1회)
터미널에 아래 명령어를 입력하여 필요한 프로그램을 설치합니다.
```bash
pip install -r requirements.txt
```

### 2. 키 설정 (최초 1회)
`.env` 파일을 열고 API 키를 입력합니다. (없으면 파일을 만드세요)
```ini
OPENAI_API_KEY=sk-... (여기에 키 붙여넣기)
```

### 3. 캐릭터 생성 실행
원하는 캐릭터의 **이름**과 **설명**을 적어서 실행합니다.

**기본 실행 (대화형)**:
```bash
python generate_character.py
```

**한방 실행 (명령어)**:
```bash
python generate_character.py --name "엘리아스" --request "달 기지에 홀로 남겨진 고독한 식물학자. 편지로만 지구와 소통함."
```

---
**결과물 확인**: `characters/엘리아스/` 폴더에 생성됩니다.
