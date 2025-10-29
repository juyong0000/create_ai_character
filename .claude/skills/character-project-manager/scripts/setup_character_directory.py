#!/usr/bin/env python3
"""
Create a structured directory for a new AI character project.

This script sets up a standardized folder structure for organizing character
creation workflows, including profile, background story, memory system, and review notes.

Usage:
    python setup_character_directory.py <character_name> [--base-dir <path>]

Example:
    python setup_character_directory.py "이서연"
    python setup_character_directory.py "MinJae Park" --base-dir /path/to/characters
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime


def sanitize_name(name: str) -> str:
    """
    Convert character name to a safe directory name.

    Examples:
        "이서연" -> "이서연"
        "Min Jae Park" -> "MinJaePark"
        "Anna-Marie" -> "Anna-Marie"
    """
    # Remove unsafe characters but keep Korean, alphanumeric, hyphens, underscores
    safe_chars = []
    for char in name:
        if char.isalnum() or char in ['-', '_'] or ord(char) > 127:  # Keep Unicode
            safe_chars.append(char)
        elif char == ' ':
            continue  # Remove spaces

    return ''.join(safe_chars)


def get_next_character_number(base_dir: Path) -> int:
    """Find the next available character number."""
    if not base_dir.exists():
        return 1

    existing_dirs = [d for d in base_dir.iterdir() if d.is_dir() and d.name.startswith('character-')]

    if not existing_dirs:
        return 1

    max_num = 0
    for dir_path in existing_dirs:
        try:
            # Extract number from "character-XXX-name" format
            parts = dir_path.name.split('-')
            if len(parts) >= 2:
                num = int(parts[1])
                max_num = max(max_num, num)
        except (ValueError, IndexError):
            continue

    return max_num + 1


def create_character_directory(character_name: str, base_dir: str = None) -> Path:
    """
    Create directory structure for a new character.

    Args:
        character_name: The name of the character
        base_dir: Base directory path (default: ./characters)

    Returns:
        Path to the created character directory
    """
    # Determine base directory
    if base_dir is None:
        base_dir = Path.cwd() / "characters"
    else:
        base_dir = Path(base_dir)

    # Create base directory if it doesn't exist
    base_dir.mkdir(parents=True, exist_ok=True)

    # Get next character number
    char_num = get_next_character_number(base_dir)

    # Sanitize character name
    safe_name = sanitize_name(character_name)

    # Create character directory name: character-001-이서연
    dir_name = f"character-{char_num:03d}-{safe_name}"
    char_dir = base_dir / dir_name

    # Create main directory
    char_dir.mkdir(exist_ok=True)

    # Create subdirectories
    (char_dir / "assets").mkdir(exist_ok=True)

    # Create placeholder files with timestamps
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    files_to_create = {
        "01-profile.md": f"""# 캐릭터 프로필: {character_name}

> 생성일: {timestamp}
> 상태: 작업 중

[character-profile-generator 스킬로 생성된 프로필이 여기에 저장됩니다]
""",
        "02-background-story.md": f"""# 백그라운드 스토리: {character_name}

> 생성일: {timestamp}
> 상태: 작업 중

[character-story-writer 에이전트가 작성한 상세 스토리가 여기에 저장됩니다]
""",
        "03-memory-system.md": f"""# 30개 기억 시스템: {character_name}

> 생성일: {timestamp}
> 상태: 작업 중

[character-memory-architect 에이전트가 설계한 기억 시스템이 여기에 저장됩니다]

## 메인 기억 (6개)

[메인 기억 목록]

## 서브 기억 (24개)

[서브 기억 목록]
""",
        "04-review-notes.md": f"""# 검수 및 피드백: {character_name}

> 생성일: {timestamp}
> 상태: 작업 중

[character-editorial-reviewer 에이전트의 검수 결과가 여기에 저장됩니다]

## 검수 이력

### [{timestamp}] 초기 생성
- 캐릭터 디렉토리 생성됨

""",
        "README.md": f"""# {character_name}

캐릭터 번호: {char_num:03d}
생성일: {timestamp}

## 파일 구조

- `01-profile.md` - 캐릭터 기본 프로필
- `02-background-story.md` - 상세 백그라운드 스토리
- `03-memory-system.md` - 30개 기억 시스템 설계
- `04-review-notes.md` - 검수 및 피드백 노트
- `assets/` - 이미지, 참고 자료 등

## 작업 진행 상태

- [ ] 캐릭터 디자인 (romantic-character-designer)
- [ ] 프로필 생성 (character-profile-generator)
- [ ] 백스토리 작성 (character-story-writer)
- [ ] 기억 시스템 설계 (character-memory-architect)
- [ ] 검수 (character-editorial-reviewer)
- [ ] 최종 완성

## 노트

[작업 중 특이사항이나 메모를 여기에 추가하세요]
"""
    }

    # Create files
    for filename, content in files_to_create.items():
        file_path = char_dir / filename
        if not file_path.exists():  # Don't overwrite existing files
            file_path.write_text(content, encoding='utf-8')

    return char_dir


def main():
    parser = argparse.ArgumentParser(
        description='Create a structured directory for a new AI character project'
    )
    parser.add_argument(
        'character_name',
        type=str,
        help='Name of the character (e.g., "이서연", "MinJae Park")'
    )
    parser.add_argument(
        '--base-dir',
        type=str,
        default=None,
        help='Base directory for characters (default: ./characters)'
    )

    args = parser.parse_args()

    try:
        char_dir = create_character_directory(args.character_name, args.base_dir)
        print(f"✅ Character directory created successfully!")
        print(f"📁 Location: {char_dir}")
        print(f"\n📋 Files created:")
        for file in sorted(char_dir.glob("*.md")):
            print(f"   - {file.name}")
        print(f"   - assets/ (directory)")

    except Exception as e:
        print(f"❌ Error creating character directory: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
