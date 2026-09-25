#!/usr/bin/env python3
"""Read Pi v3 and Claude Code transcripts without executing their contents or updating memory notes.

Snapshot writes a manifest; checkpoint writes progress except for explicit re-reviews.
All offsets are bytes at complete JSONL boundaries, not message timestamps.
Claude Code entries are normalized to the Pi message shape before rendering.
"""

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import uuid

VERSION = 1
STATE_NAME = ".transcript-state.json"


class Invalid(ValueError):
    pass


def fail(source, message):
    raise Invalid(f"{source}: {message}")


def encoded(value):
    return json.dumps(value, ensure_ascii=False)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def canonical(path):
    return Path(path).expanduser().resolve()


def workspace_path(path):
    workspace = canonical(path)
    if not workspace.is_dir():
        fail(workspace, "workspace is not a directory")
    return workspace


def short_dir(workspace):
    short = workspace / ".memory" / "short_term"
    if not short.is_dir() or short.resolve() != short:
        fail(short, "require an existing, workspace-local short_term directory (no symlink)")
    return short


def local_file(path, workspace):
    path = canonical(path)
    short = short_dir(workspace)
    if not path.is_relative_to(short) or path == short:
        fail(path, f"must be inside {short}")
    return path


def json_object(raw, source):
    try:
        value = json.loads(raw)
    except (ValueError, UnicodeError) as error:
        fail(source, f"invalid JSON: {error}")
    if not isinstance(value, dict):
        fail(source, "expected a JSON object")
    return value


def lines(path, start=0, end=None, *, defer_partial=False):
    """Stream complete lines, never parse a writer's unfinished trailing bytes."""
    with path.open("rb") as stream:
        stream.seek(start)
        while end is None or stream.tell() < end:
            offset = stream.tell()
            raw = stream.readline(-1 if end is None else end - offset)
            if not raw or not raw.endswith(b"\n"):
                if end is not None and not defer_partial:
                    fail(path, f"incomplete captured line at byte {offset}")
                break
            entry = json_object(raw, f"{path} byte {offset}")
            if not isinstance(entry.get("type"), str):
                fail(path, f"missing entry type at byte {offset}")
            if entry["type"] == "session" and offset != 0:
                fail(path, f"unexpected session header at byte {offset}")
            validate_entry(entry, f"{path} byte {offset}")
            yield stream.tell(), raw, entry


def validate_message(message, source):
    if not isinstance(message, dict) or not isinstance(message.get("role"), str):
        fail(source, "invalid message object/role")
    content = message.get("content")
    if content is not None and not isinstance(content, (str, list)):
        fail(source, "invalid message content")
    if isinstance(content, list):
        for block in content:
            if not isinstance(block, dict) or not isinstance(block.get("type"), str):
                fail(source, "invalid content block")
            if block["type"] == "text" and not isinstance(block.get("text"), str):
                fail(source, "invalid text block")
            if block["type"] == "toolCall" and not (
                    isinstance(block.get("id"), str) and isinstance(block.get("name"), str)
                    and isinstance(block.get("arguments"), dict)):
                fail(source, "invalid tool call")


def validate_entry(entry, source):
    if entry["type"] == "message":
        validate_message(entry.get("message"), source)
    if entry["type"] == "compaction" and "retainedTail" in entry:
        if not isinstance(entry["retainedTail"], list):
            fail(source, "invalid retainedTail")
        for message in entry["retainedTail"]:
            validate_message(message, source)


def header(path, workspace):
    first = next(lines(path), None)
    if first is None:
        fail(path, "missing complete session header")
    _, raw, entry = first
    if entry.get("type") != "session":
        # Claude Code has no header line; its first entry carrying a cwd is the launch cwd.
        for _, raw, entry in lines(path):
            if isinstance(entry.get("cwd"), str) and "sessionId" in entry:
                break
        else:
            fail(path, "unsupported transcript; require Pi v3 or Claude Code entries with cwd")
        head = {"id": entry.get("sessionId"), "cwd": entry["cwd"], "format": "claude"}
    elif entry.get("version") != 3:
        fail(path, "unsupported session header/version; require Pi v3")
    else:
        head = {"id": entry.get("id"), "cwd": entry.get("cwd"),
                "parentSession": entry.get("parentSession"), "format": "pi"}
    if not isinstance(head["id"], str) or not head["id"]:
        fail(path, "missing session id")
    cwd = head["cwd"]
    if not isinstance(cwd, str) or not Path(cwd).is_absolute() or canonical(cwd) != workspace:
        fail(path, f"header cwd {cwd!r} does not match workspace {workspace}")
    return head, sha(raw)


def entry_id(entry):
    return entry.get("id", entry.get("uuid"))


def validate_claude(message, source):
    if not isinstance(message.get("role"), str):
        fail(source, "invalid message role")
    content = message.get("content")
    if content is not None and not isinstance(content, (str, list)):
        fail(source, "invalid message content")
    for block in content if isinstance(content, list) else []:
        if not isinstance(block, dict) or not isinstance(block.get("type"), str):
            fail(source, "invalid content block")
        kind = block["type"]
        if (kind == "text" and not isinstance(block.get("text"), str)
                or kind == "tool_use" and not (isinstance(block.get("id"), str)
                                               and isinstance(block.get("name"), str)
                                               and isinstance(block.get("input"), dict))
                or kind == "tool_result" and not isinstance(block.get("tool_use_id"), str)):
            fail(source, f"invalid {kind} block")


def claude_entries(entry, names, source):
    """Map one Claude Code entry to Pi-shaped entries; each tool_result becomes a toolResult."""
    uid = entry.get("uuid")
    base = {"id": uid, "parentId": entry.get("parentUuid"), "timestamp": entry.get("timestamp")}
    message = entry.get("message")
    if entry["type"] not in ("user", "assistant") or not isinstance(message, dict):
        # Bookkeeping lines without a uuid (mode, titles, snapshots) are not conversation.
        return [dict(base, type=entry["type"])] if uid else []
    if not isinstance(uid, str) or not uid:
        fail(source, "Claude conversation entry requires a uuid")
    validate_claude(message, source)
    if entry.get("isMeta"):
        return [dict(base, type="meta")]
    content = message.get("content")
    if entry.get("isCompactSummary"):
        return [dict(base, type="message", message={"role": "compactionSummary",
                                                    "summary": visible(content)})]
    if entry["type"] == "assistant":
        blocks = content
        if isinstance(content, list):
            blocks = [{"type": "toolCall", "id": block["id"], "name": block["name"],
                       "arguments": block["input"]} if block["type"] == "tool_use" else block
                      for block in content]
            names.update((block["id"], block["name"]) for block in blocks if block["type"] == "toolCall")
        return [dict(base, type="message", message={"role": "assistant", "content": blocks})]
    if not isinstance(content, list):
        return [dict(base, type="message", message={"role": "user", "content": content})]
    results = [block for block in content if block["type"] == "tool_result"]
    rest = [block for block in content if block["type"] != "tool_result"]
    messages = [{"role": "user", "content": rest}] if rest or not results else []
    messages += [{"role": "toolResult", "toolCallId": block["tool_use_id"],
                  "toolName": names.get(block["tool_use_id"]), "content": block.get("content"),
                  "isError": block.get("is_error") is True} for block in results]
    return [dict(base, type="message", id=uid if len(messages) == 1 else f"{uid}/{index}",
                 message=message) for index, message in enumerate(messages)]


def entries(path, head, start=0, end=None, names=None):
    """Stream Pi-shaped entries; share `names` across calls to label later tool results."""
    names = {} if names is None else names
    for offset, _, entry in lines(path, start, end):
        if head["format"] == "pi":
            yield entry
        else:
            yield from claude_entries(entry, names, f"{path} before byte {offset}")


def boundary_line(path, offset):
    if not isinstance(offset, int) or isinstance(offset, bool) or offset < 0:
        fail(path, "invalid byte boundary")
    if offset == 0:
        return None
    # Seek backwards in chunks; retain only the final complete line for its anchor.
    with path.open("rb") as stream:
        if stream.seek(0, 2) < offset:
            fail(path, "source shrank; choose an explicit rescan")
        stream.seek(offset - 1)
        if stream.read(1) != b"\n":
            fail(path, "saved offset is not a complete-line boundary")
        position = offset - 1
        chunks = []
        while position:
            size = min(position, 8192)
            position -= size
            stream.seek(position)
            chunk = stream.read(size)
            split = chunk.rfind(b"\n")
            chunks.append(chunk[split + 1:] if split >= 0 else chunk)
            if split >= 0:
                break
        return b"".join(reversed(chunks)) + b"\n"


def boundary(path, offset):
    raw = boundary_line(path, offset)
    return sha(raw) if raw is not None else None


def load_state(workspace):
    path = short_dir(workspace) / STATE_NAME
    if path.is_symlink():
        fail(path, "processing state must not be a symlink")
    if not path.exists():
        return {"version": VERSION, "workspace": str(workspace), "files": {}}, None
    raw = path.read_bytes()
    state = json_object(raw, path)
    if (state.get("version") != VERSION or state.get("workspace") != str(workspace)
            or not isinstance(state.get("files"), dict)):
        fail(path, "invalid state version, workspace or files")
    for name, record in state["files"].items():
        if str(canonical(name)) != name or not isinstance(record, dict):
            fail(path, "invalid state file record")
        if not all(key in record for key in ("session_id", "offset", "last_entry_id", "anchor_sha256")):
            fail(path, f"incomplete state record for {name}")
    return state, sha(raw)


def capture(path, workspace, previous, *, rereview=False):
    if rereview and previous is None:
        fail(path, "re-review requires a previously checkpointed session; use a normal update first")
    head, head_hash = header(path, workspace)
    start = previous["offset"] if previous else 0
    anchor = boundary(path, start)
    if previous and (previous["session_id"] != head["id"] or previous["anchor_sha256"] != anchor
                     or previous.get("header_sha256", head_hash) != head_hash):
        fail(path, "saved boundary/header changed; choose an explicit rescan")
    if rereview:
        # Validate the saved boundary before capturing from zero; never reset state.
        start, anchor, previous = 0, None, None
    digest = hashlib.sha256()
    end, last_id, last_anchor, count = start, previous["last_entry_id"] if previous else None, anchor, 0
    # Freeze the upper bound before streaming. Appends are for the next snapshot.
    ceiling = path.stat().st_size
    names = {}
    for next_end, raw, entry in lines(path, start, ceiling, defer_partial=True):
        if head["format"] == "claude":
            claude_entries(entry, names, f"{path} before byte {next_end}")
        digest.update(raw)
        end, last_anchor = next_end, sha(raw)
        if entry["type"] != "session":
            last_id = entry_id(entry)
            count += 1
    return {"path": str(path), "session_id": head["id"], "format": head["format"],
            "parent_session": head.get("parentSession"), "header_sha256": head_hash,
            "from_offset": start, "to_offset": end, "prior_anchor_sha256": anchor,
            "range_sha256": digest.hexdigest(), "anchor_sha256": last_anchor,
            "last_entry_id": last_id, "new_entry_count": count}


def session_directories(workspace, session_dir):
    if session_dir:
        directories = [canonical(session_dir)]
    else:
        pi = "--" + re.sub(r"[/\\:]", "-", re.sub(r"^[/\\]", "", str(workspace))) + "--"
        claude = re.sub(r"[^A-Za-z0-9]", "-", str(workspace))
        directories = [canonical(Path.home() / ".pi/agent/sessions" / pi),
                       canonical(Path.home() / ".claude/projects" / claude)]
    directories = list(dict.fromkeys(directories))
    for directory in directories:
        if directory.exists() and not directory.is_dir():
            fail(directory, "session directory is not a directory")
    return directories


def session_sources(directories, selected=None):
    allowed = " or ".join(map(str, directories))
    if selected:
        sources = []
        for name in selected:
            if Path(name).is_absolute():
                path = canonical(name)
            else:
                found = [canonical(directory / name) for directory in directories
                         if (directory / name).is_file()]
                if len(found) > 1:
                    fail(name, f"ambiguous session name in {allowed}")
                path = found[0] if found else canonical(directories[0] / name)
            if path.parent not in directories or not path.is_file():
                fail(path, f"selected session must be a file directly inside {allowed}")
            sources.append(path)
    else:
        sources = [path for directory in directories if directory.exists()
                   for path in directory.glob("*.jsonl")]
    sources = sorted(set(canonical(path) for path in sources))
    for path in sources:
        if path.parent not in directories:
            fail(path, f"source escapes session directories {allowed}")
    return sources


def list_sessions(args):
    workspace = workspace_path(args.workspace)
    directories = session_directories(workspace, args.session_dir)
    state, _ = load_state(workspace)
    sessions = []
    for path in session_sources(directories):
        head, _ = header(path, workspace)
        first_prompt, date = None, None
        count = 0
        last_offset = 0
        for last_offset, _, raw in lines(path, defer_partial=True):
            if date is None and isinstance(raw.get("timestamp"), str):
                date = raw["timestamp"][:10]
            count += raw["type"] != "session"
            if first_prompt is None:
                for entry in claude_entries(raw, {}, path) if head["format"] == "claude" else [raw]:
                    message = entry_message(entry)
                    if message.get("role") == "user" and visible(message.get("content")).strip():
                        first_prompt = visible(message["content"]).strip().replace("\n", " ")[:160]
        previous = state["files"].get(str(path))
        sessions.append({"path": str(path), "date": date, "format": head["format"],
                         "bytes": last_offset, "entries": count, "first_prompt": first_prompt,
                         "checkpointed_bytes": previous["offset"] if previous else 0,
                         "pending_bytes": last_offset - (previous["offset"] if previous else 0)})
    return {"workspace": str(workspace), "session_dirs": list(map(str, directories)),
            "sessions": sessions}


def snapshot(args):
    workspace = workspace_path(args.workspace)
    output = local_file(args.output, workspace)
    if output == short_dir(workspace) / STATE_NAME:
        fail(output, "reserved processing state path is not a batch output")
    if output.exists():
        fail(output, "refusing to overwrite existing batch")
    if args.rereview and not args.session:
        fail(output, "--rereview requires --session selection")
    directories = session_directories(workspace, args.session_dir)
    sources = session_sources(directories, args.session)
    state, base = load_state(workspace)
    ranges = [capture(path, workspace, state["files"].get(str(path)), rereview=args.rereview)
              for path in sources]
    mode = "rereview" if args.rereview else "incremental"
    batch = {"version": VERSION, "batch_id": uuid.uuid4().hex, "workspace": str(workspace),
             "review_mode": mode,
             "created_at": datetime.now(timezone.utc).isoformat(), "base_state_sha256": base,
             "coverage": {"session_dirs": list(map(str, directories)), "workspace": str(workspace),
                          "missing_dirs": [str(item) for item in directories if not item.exists()],
                          "selected_only": bool(args.session)},
             "ranges": ranges}
    with output.open("x", encoding="utf-8") as stream:
        stream.write(encoded(batch) + "\n")
    count_key = "entry_count" if args.rereview else "new_entry_count"
    return {"batch_id": batch["batch_id"], "batch": str(output), "file_count": len(ranges),
            "review_mode": mode, count_key: sum(item["new_entry_count"] for item in ranges),
            "coverage": batch["coverage"]}


def load_batch(name):
    path = canonical(name)
    batch = json_object(path.read_bytes(), path)
    if batch.get("version") != VERSION:
        fail(path, "unsupported batch version")
    if batch.get("review_mode", "incremental") not in ("incremental", "rereview"):
        fail(path, "unsupported review mode")
    workspace = workspace_path(batch.get("workspace", ""))
    local_file(path, workspace)
    if not isinstance(batch.get("ranges"), list) or not batch.get("batch_id"):
        fail(path, "invalid batch")
    seen = set()
    for item in batch["ranges"]:
        source = canonical(item["path"])
        if str(source) != item["path"] or str(source) in seen:
            fail(path, f"noncanonical or duplicate source range: {source}")
        seen.add(str(source))
        head, head_hash = header(source, workspace)
        if head["id"] != item["session_id"] or head_hash != item["header_sha256"]:
            fail(source, "captured header changed")
        if boundary(source, item["from_offset"]) != item["prior_anchor_sha256"]:
            fail(source, "prior boundary anchor changed")
        if item["to_offset"] < item["from_offset"]:
            fail(source, "reversed captured range")
        last_raw = boundary_line(source, item["to_offset"])
        last_entry = json_object(last_raw, source) if last_raw else {}
        last_id = entry_id(last_entry) if last_entry.get("type") != "session" else None
        if last_id != item["last_entry_id"]:
            fail(source, "captured last_entry_id does not match boundary")
        digest = hashlib.sha256()
        count = 0
        for _, raw, entry in lines(source, item["from_offset"], item["to_offset"]):
            digest.update(raw)
            count += entry["type"] != "session"
        if digest.hexdigest() != item["range_sha256"]:
            fail(source, "captured bytes changed; choose an explicit rescan")
        if count != item["new_entry_count"]:
            fail(source, "captured entry count changed")
        if (sha(last_raw) if last_raw else None) != item["anchor_sha256"]:
            fail(source, "captured boundary changed")
    return batch


def visible(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(block["text"] for block in content
                         if isinstance(block, dict) and block.get("type") == "text"
                         and isinstance(block.get("text"), str))
    return ""


def entry_message(entry):
    return entry["message"] if entry["type"] == "message" else {}


def retained_entries(entry):
    if entry["type"] == "compaction":
        for index, message in enumerate(entry.get("retainedTail", [])):
            yield {"type": "message", "id": f"{entry.get('id')}/retainedTail/{index}",
                   "parentId": entry.get("id"), "message": message}


def detail_entries(path, head):
    for entry in entries(path, head):
        yield entry
        yield from retained_entries(entry)


def calls(entry):
    message = entry_message(entry)
    content = message.get("content", [])
    if message.get("role") != "assistant" or not isinstance(content, list):
        return []
    return [block for block in content if isinstance(block, dict) and block.get("type") == "toolCall"]


def status(message):
    if message.get("cancelled") is True:
        return "cancelled"
    if message.get("isError") is True:
        return "error"
    code = message.get("exitCode")
    if isinstance(code, int) and not isinstance(code, bool):
        return "completed" if code == 0 else "nonzero-exit"
    if message.get("isError") is False:
        return "completed"
    return "unknown"


def render_entry(entry, result_refs, previous_id=None, compact=lambda value: value):
    parent = entry.get('parentId')
    parent_ref = f" parent={compact(parent)}" if parent and parent != previous_id else ""
    prefix = f"[{entry.get('timestamp')} entry={compact(entry.get('id'))}{parent_ref}] "
    message = entry_message(entry)
    role = message.get("role")
    if role in ("user", "assistant"):
        yield prefix + role + ": " + visible(message.get("content")) + "\n"
        for index, call in enumerate(calls(entry)):
            # Opaque provider IDs can be hundreds of characters. Keep them for
            # joins, but expose a usable entry/index reference instead.
            ref = (f"call={call['id']}" if len(call['id']) <= 80 else
                   f"entry={compact(entry.get('id'))} call-index={index}")
            refs = result_refs.get(call.get("id"), [])
            if refs:
                for result_id, outcome in refs:
                    yield f"tool {call.get('name')} {ref} result={compact(result_id)} {outcome}\n"
            else:
                outcome = "cancelled" if message.get("stopReason") == "aborted" else "unknown"
                yield f"tool {call.get('name')} {ref} result=none {outcome}\n"
    elif role == "toolResult":
        call_id = message.get("toolCallId")
        ref = f"call={call_id} " if isinstance(call_id, str) and len(call_id) <= 80 else ""
        yield prefix + f"tool {message.get('toolName')} {ref}result={compact(entry.get('id'))} {status(message)}; body omitted\n"
    elif role == "bashExecution":
        yield prefix + f"bashExecution {status(message)}; command/output omitted\n"
    elif entry["type"] in ("compaction", "branch_summary") or role in ("compactionSummary", "branchSummary"):
        summary = entry if entry["type"] != "message" else message
        yield (prefix + f"secondary {role or entry['type']} fromId={summary.get('fromId')} "
               + f"firstKeptEntryId={summary.get('firstKeptEntryId')}: " + str(summary.get("summary", "")) + "\n")
    else:
        yield prefix + f"omitted metadata type={entry['type']} role={role}\n"


def overview_text(batch):
    if batch.get("review_mode") == "rereview":
        yield "Review mode: rereview; incremental progress will not advance\n"
    yield "Coverage: " + encoded(batch["coverage"]) + "\n"
    for item in batch["ranges"]:
        path = Path(item["path"])
        yield f"Session {path} id={item['session_id']} format={item.get('format', 'pi')}\n"
        if item.get("parent_session"):
            yield f"parent_session={item['parent_session']}; copied history is not independent corroboration\n"
        result_refs, originals, names, ids = {}, set(), {}, set()
        head = {"format": item.get("format", "pi")}
        # Retain compact references only, never tool bodies. Do not inspect future appends.
        for entry in entries(path, head, 0, item["to_offset"], names):
            if isinstance(entry.get("id"), str):
                ids.add(entry["id"])
            message = entry_message(entry)
            if entry["type"] == "message":
                originals.add(sha(encoded(message).encode("utf-8")))
            if message.get("role") == "toolResult":
                result_refs.setdefault(message.get("toolCallId"), []).append((entry.get("id"), status(message)))
        def compact(value):
            if not isinstance(value, str) or len(value) < 24:
                return value
            size = 8
            while any(other != value and other.startswith(value[:size]) for other in ids):
                size += 1
            return value[:size]

        previous_id = None
        assistant_run = False
        for entry in entries(path, head, item["from_offset"], item["to_offset"], names):
            if entry["type"] == "session":
                continue
            message = entry_message(entry)
            # Claude streams a single reply across adjacent assistant records.
            # Keep each entry reference visible while eliding repeated timestamps.
            merge = (head["format"] == "claude" and assistant_run
                     and message.get("role") == "assistant" and not calls(entry)
                     and bool(visible(message.get("content"))))
            if merge:
                yield f"  entry={compact(entry.get('id'))} assistant: {visible(message['content'])}\n"
            else:
                yield from render_entry(entry, result_refs, previous_id, compact)
            assistant_run = (head["format"] == "claude" and message.get("role") == "assistant")
            previous_id = entry.get("id")
            if entry["type"] == "compaction" and "retainedTail" in entry:
                yield "retainedTail: secondary embedded context; exact original/repeated copies omitted\n"
                for retained in retained_entries(entry):
                    fingerprint = sha(encoded(retained["message"]).encode("utf-8"))
                    if fingerprint not in originals:
                        originals.add(fingerprint)
                        yield "secondary retainedTail (not an independent observation): "
                        yield from render_entry(retained, {}, compact=compact)


def bounded(text, offset, budget, make_result, source):
    if offset < 0 or offset > len(text):
        fail(source, "offset outside text")
    # The terminal response drops its cursor, so its size is not monotonic with
    # an unfinished slice. Test it separately before binary-searching partials.
    if len(text) - offset <= budget:
        terminal = make_result(text[offset:], len(text))
        if len(encoded(terminal)) + 1 <= budget:
            return terminal
    low, high = 0, min(len(text) - offset - 1, max(0, budget))
    best = None
    while low <= high:
        size = (low + high) // 2
        result = make_result(text[offset:offset + size], offset + size)
        if len(encoded(result)) + 1 <= budget:
            best = (size, result)
            low = size + 1
        else:
            high = size - 1
    if best is None or (best[0] == 0 and offset < len(text)):
        fail(source, "max-chars too small for metadata and forward progress")
    return best[1]


def overview(args):
    batch = load_batch(args.batch)
    text = "".join(overview_text(batch))
    # Text offsets from the earlier verbose rendering must not silently skip
    # content after this display-format change. Batch/state formats are unchanged.
    identity = sha(("overview-v4\n" + encoded(batch)).encode("utf-8"))
    offset = 0
    if args.cursor:
        parts = args.cursor.split(":")
        if len(parts) != 2 or parts[0] != identity or not parts[1].isdigit():
            fail(args.batch, "invalid cursor or batch/overview format changed; keep notes and restart the overview without --cursor")
        offset = int(parts[1])
    return bounded(text, offset, args.max_chars,
                   lambda part, end: {"text": part,
                                      "next_cursor": f"{identity}:{end}" if end < len(text) else None,
                                      "complete": end == len(text)}, args.batch)


def detail(args):
    workspace = workspace_path(args.workspace)
    path = canonical(args.session)
    head, _ = header(path, workspace)
    found = None
    for entry in detail_entries(path, head):
        if isinstance(entry.get("id"), str) and entry["id"].startswith(args.entry) and entry["type"] != "session":
            if found is not None:
                fail(path, f"ambiguous entry {args.entry}")
            found = entry
    if found is None:
        fail(path, f"entry {args.entry} not found")
    full_entry_id = found["id"]
    message = entry_message(found)
    role = message.get("role")
    own_calls = calls(found)
    call_id = args.call_id or message.get("toolCallId")
    if args.call_index is not None:
        if not 0 <= args.call_index < len(own_calls):
            fail(path, f"entry {args.entry}: call-index must select a tool call in an assistant entry")
        call_id = own_calls[args.call_index]["id"]
    if call_id is None and len(own_calls) == 1:
        call_id = own_calls[0].get("id")
    if args.call_id and not (args.call_id == message.get("toolCallId") or
                             any(call.get("id") == args.call_id for call in own_calls)):
        fail(path, f"entry {args.entry}: call-id is not associated with requested entry")
    source = {"session": str(path), "session_id": head["id"], "entry": full_entry_id,
              "field": args.field, "call_id": call_id}
    if args.field == "text":
        if found["type"] in ("compaction", "branch_summary"):
            text = str(found.get("summary", ""))
        elif role in ("compactionSummary", "branchSummary"):
            text = str(message.get("summary", ""))
        else:
            text = visible(message.get("content"))
    elif role == "bashExecution":
        text = str(message.get("command" if args.field == "arguments" else "output", ""))
    else:
        if call_id is None:
            fail(path, f"entry {args.entry}: require an unambiguous call-id or call-index")
        matches = []
        for entry in detail_entries(path, head):
            if args.field == "arguments":
                matches.extend((entry["id"], encoded(call.get("arguments", {})))
                               for call in calls(entry) if call.get("id") == call_id)
            else:
                result = entry_message(entry)
                if result.get("role") == "toolResult" and result.get("toolCallId") == call_id:
                    matches.append((entry["id"], visible(result.get("content"))))
        # Prefer the requested context over copied compaction history.
        context = full_entry_id.rpartition("/retainedTail/")[0]
        scoped = [match for match in matches if match[0].rpartition("/retainedTail/")[0] == context]
        if scoped:
            matches = scoped
        elif matches and all(text == matches[0][1] for _, text in matches):
            matches = matches[:1]
        if len(matches) != 1:
            fail(path, f"entry {args.entry}: missing or ambiguous {args.field} for call {call_id}")
        source["call_entry" if args.field == "arguments" else "result_entry"] = matches[0][0]
        text = matches[0][1]
    return bounded(text, args.offset, args.max_chars,
                   lambda part, end: {"text": part, "total_chars": len(text),
                                      "next_offset": end if end < len(text) else None, "source": source}, path)


def checkpoint(args):
    batch = load_batch(args.batch)
    workspace = workspace_path(batch["workspace"])
    note = local_file(args.notes, workspace)
    if note.suffix.lower() != ".md":
        fail(note, "review notes must be Markdown")
    text = note.read_text(encoding="utf-8")
    if not text.strip() or batch["batch_id"] not in text:
        fail(note, "require nonempty saved review notes containing this batch_id")
    state, fingerprint = load_state(workspace)
    if fingerprint != batch["base_state_sha256"]:
        fail(args.batch, "stale state: another update advanced progress; reconcile before checkpoint")
    if batch.get("review_mode") == "rereview":
        for item in batch["ranges"]:
            previous = state["files"].get(item["path"])
            if (previous is None or item["from_offset"] != 0
                    or item["to_offset"] < previous["offset"]
                    or previous["session_id"] != item["session_id"]):
                fail(item["path"], "re-review must include the previously checkpointed history from byte zero")
        return {"batch_id": batch["batch_id"], "state_advanced": False,
                "rereviewed": {item["path"]: item["to_offset"] for item in batch["ranges"]}}
    checkpointed = {}
    for item in batch["ranges"]:
        previous = state["files"].get(item["path"])
        if item["from_offset"] != (previous["offset"] if previous else 0) or item["prior_anchor_sha256"] != (
                previous["anchor_sha256"] if previous else None):
            fail(item["path"], "batch range does not start at base state boundary")
        if previous and previous["session_id"] != item["session_id"]:
            fail(item["path"], "batch session_id differs from base state")
        record = {"session_id": item["session_id"], "offset": item["to_offset"],
                  "last_entry_id": item["last_entry_id"], "anchor_sha256": item["anchor_sha256"],
                  "header_sha256": item["header_sha256"]}
        state["files"][item["path"]] = record
        checkpointed[item["path"]] = item["to_offset"]
    target = short_dir(workspace) / STATE_NAME
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=target.parent,
                                         prefix=STATE_NAME + ".", suffix=".tmp", delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(encoded(state) + "\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, target)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return {"checkpointed": checkpointed, "batch_id": batch["batch_id"]}


def parser():
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="command", required=True)
    listing = commands.add_parser("list", help="read-only session inventory for the selected workspace")
    listing.add_argument("--workspace", required=True)
    listing.add_argument("--session-dir")
    snap = commands.add_parser("snapshot")
    snap.add_argument("--workspace", required=True)
    snap.add_argument("--output", required=True)
    snap.add_argument("--session-dir")
    snap.add_argument("--session", action="append")
    snap.add_argument("--rereview", action="store_true",
                      help="capture selected previously checkpointed sessions from the start without advancing progress")
    view = commands.add_parser("overview")
    view.add_argument("--batch", required=True)
    view.add_argument("--cursor")
    view.add_argument("--max-chars", type=int, default=16000)
    lookup = commands.add_parser("detail")
    lookup.add_argument("--workspace", required=True)
    lookup.add_argument("--session", required=True)
    lookup.add_argument("--entry", required=True)
    lookup.add_argument("--field", choices=("text", "arguments", "result"), required=True)
    selector = lookup.add_mutually_exclusive_group()
    selector.add_argument("--call-id", help="full tool call ID")
    selector.add_argument("--call-index", type=int,
                          help="zero-based tool-call index within the selected assistant entry")
    lookup.add_argument("--offset", type=int, default=0)
    lookup.add_argument("--max-chars", type=int, default=4000)
    save = commands.add_parser("checkpoint")
    save.add_argument("--batch", required=True)
    save.add_argument("--notes", required=True)
    return root


def main():
    args = parser().parse_args()
    try:
        result = {"list": list_sessions, "snapshot": snapshot, "overview": overview, "detail": detail,
                  "checkpoint": checkpoint}[args.command](args)
        print(encoded(result))
    except (Invalid, OSError, KeyError, TypeError, ValueError) as error:
        source = getattr(args, "batch", None) or getattr(args, "session", None) or args.workspace
        print(f"{source}: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
