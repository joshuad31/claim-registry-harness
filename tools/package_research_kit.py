"""Package the entire integrated research personality and refresh Cursor's always-on rules."""
import sys
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from claimreg.personality import PACKAGE, source_files  # noqa: E402


def package_files():
    return {"PERSONALITY.md": PACKAGE / "PERSONALITY.md", "INTEGRATION.json": PACKAGE / "INTEGRATION.json",
            **dict(source_files())}


FILES = package_files()  # compatibility for callers inspecting the export inventory


def write_cursor_rules(output=None):
    folder = Path(output) if output else ROOT / ".cursor" / "rules"
    files = package_files()
    # Materialize every body, not just @mentions (which Cursor does not inline).
    bodies = [(name, path.read_text(encoding="utf-8-sig")) for name, path in files.items()
              if name != "INTEGRATION.json"]
    folder.mkdir(parents=True, exist_ok=True)
    outputs = []
    for number, (name, body) in enumerate(bodies):
        dest = folder / f"claim-registry-personality-{number:02d}.mdc"
        header = ("---\ndescription: Standing Claim Registry research personality and complete supplied experience\n"
                  "alwaysApply: true\n---\n\n"
                  "Generated from agent/research-personality; edit the source and rebuild.\n"
                  "Apply PERSONALITY.md's interpretation of historical notes and role boundaries.\n"
                  f"Complete source file: {name}\n\n")
        # Keep the complete body, including its trailing whitespace, without leaving generated
        # rules with a whitespace-only end of file when the user expands a memory.
        dest.write_text(header + body + "\n<!-- End of complete source file. -->\n", encoding="utf-8")
        outputs.append(dest)
    return outputs


def build(output=None):
    output = Path(output) if output else ROOT / "dist" / "research-paper-converter-kit.zip"
    # Read all files first. A missing memory cannot destroy the previous ZIP.
    payloads = [(name, path.read_bytes()) for name, path in package_files().items()]
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_name(output.name + ".building")
    with ZipFile(temporary, "w", compression=ZIP_DEFLATED) as z:
        for name, data in payloads:
            info = ZipInfo("research-paper-converter/" + name, (2026, 11, 15, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            z.writestr(info, data)
    temporary.replace(output)
    return output


if __name__ == "__main__":
    print(f"Cursor always-on rules: {len(write_cursor_rules())}")
    print(build())
