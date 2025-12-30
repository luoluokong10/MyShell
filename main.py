import os
import shutil
import argparse
import subprocess
from pathlib import Path


def is_windows() -> bool:
    return os.name == "nt"


def copy_tree(src: Path, dst: Path) -> None:
    if not src.exists():
        raise FileNotFoundError(f"Missing source directory: {src}")
    dst.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, dst, dirs_exist_ok=True)


def ensure_line(file_path: Path, line: str) -> None:
    if file_path.exists():
        content = file_path.read_text(encoding="utf-8")
        if line in content:
            return
        file_path.write_text(content + "\n" + line + "\n", encoding="utf-8")
    else:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(line + "\n", encoding="utf-8")


def update_git_submodules(path: Path) -> None:
    if not (path / ".gitmodules").exists():
        return

    try:
        subprocess.run(
            ["git", "submodule", "update", "--init", "--recursive"],
            cwd=path,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(
            f"Failed to update git submodules in {path}:\n{exc.stderr}"
        ) from exc


def install_zsh(repo_path: Path, target_dir: Path) -> None:
    update_git_submodules(repo_path)
    
    src = repo_path / "zsh"
    copy_tree(src, target_dir)

    zshrc = Path.home() / ".zshrc"
    ensure_line(zshrc, "ZSH_THEME=robbyrussell")
    ensure_line(zshrc, f"source {target_dir}/init.zsh")


def install_pwsh(repo_path: Path, profile_dir: Path) -> None:
    src = repo_path / "pwsh"
    target_dir = profile_dir / "pwsh"
    copy_tree(src, target_dir)

    profile_path = profile_dir / "Microsoft.PowerShell_profile.ps1"
    # !fix: fixed path is conflict with --pwsh-dir
    ensure_line(profile_path, ". (Join-Path $PSScriptRoot 'pwsh/init.ps1')")
    # !fix: but a full path looks terriable
    # init_path = target_dir / "init.ps1"
    # ensure_line(profile_path, f". {init_path}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Install MyShell files for the current platform."
    )
    parser.add_argument(
        "--zsh-dir",
        default=os.path.join(os.path.expanduser("~"), ".config", "zsh"),
        help="Target directory for zsh files (default: ~/.config/zsh)",
    )
    parser.add_argument(
        "--pwsh-dir",
        default=os.path.join(
            os.path.expanduser("~"), "Documents", "PowerShell"
        ),
        help="Target directory for PowerShell (default: ~/Documents/PowerShell)",
    )
    args = parser.parse_args()

    repo_path = Path(__file__).resolve().parent

    try:
        if is_windows():
            install_pwsh(repo_path, Path(args.pwsh_dir))
        else:
            install_zsh(repo_path, Path(args.zsh_dir))
    except (OSError, FileNotFoundError) as exc:
        print(f"Install failed: {exc}")
        return 1

    print("Done. Restart your shell.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())