import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "transcripts.py"

class TranscriptTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.workspace = self.root / "repo"
        self.short = self.workspace / ".memory" / "short_term"
        self.short.mkdir(parents=True)
        self.sessions = self.root / "sessions"
        self.sessions.mkdir()
        self.source = self.sessions / "session.jsonl"
        self.batch = self.short / "batch.json"
        self.append({"type": "session", "version": 3, "id": "s1",
                     "cwd": str(self.workspace), "timestamp": "2026-09-08T08:00:00Z"})
        self.message("u1", None, "user", "Could source A support this join?")
        self.message("a1", "u1", "assistant", [
            {"type": "text", "text": "I will inspect its grain."},
            {"type": "toolCall", "id": "c1", "name": "bash",
             "arguments": {"command": "inspect-source-A"}},
        ])
        self.message("t1", "a1", "toolResult", [
            {"type": "text", "text": "Query failed: unknown column.\n" + "PRIVATE_ROW\n" * 5000}
        ], toolCallId="c1", toolName="bash", isError=True)

    def append(self, entry):
        with self.source.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(entry) + "\n")

    def message(self, entry_id, parent, role, content, **fields):
        self.append({"type": "message", "id": entry_id, "parentId": parent,
                     "timestamp": "2026-09-08T08:00:01Z",
                     "message": {"role": role, "content": content, **fields}})

    def cli(self, *args):
        result = subprocess.run([sys.executable, str(SCRIPT), *map(str, args)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def snapshot(self):
        return self.cli("snapshot", "--workspace", self.workspace,
                        "--session-dir", self.sessions, "--output", self.batch)

    def test_overview_keeps_failure_marker_without_bulk_output(self):
        self.snapshot()
        page = self.cli("overview", "--batch", self.batch)
        self.assertIn("Could source A", page["text"])
        self.assertIn("bash", page["text"])
        self.assertIn("c1", page["text"])
        self.assertIn("t1", page["text"])
        self.assertIn("error", page["text"])
        self.assertNotIn("PRIVATE_ROW", page["text"])
        self.assertTrue(page["complete"])
        self.assertIsNone(page["next_cursor"])

    def test_detail_joins_result_to_arguments(self):
        detail = self.cli("detail", "--workspace", self.workspace,
                          "--session", self.source, "--entry", "t1",
                          "--field", "arguments")
        self.assertIn("inspect-source-A", detail["text"])

    def test_detail_is_bounded_and_continuable(self):
        result = self.cli("detail", "--workspace", self.workspace,
                          "--session", self.source, "--entry", "t1",
                          "--field", "result", "--max-chars", "800")
        self.assertLessEqual(len(json.dumps(result, ensure_ascii=False)) + 1, 800)
        self.assertIn("unknown column", result["text"])
        self.assertIsNotNone(result["next_offset"])

    def test_overview_paginates_long_assistant_and_user_with_escaping(self):
        long_assistant = 'begin ' + 'x' * 40000 + ' end'
        long_user = 'user-begin ' + '\n"\\雪🙂' * 3000 + ' user-end'
        self.message('a2', 't1', 'assistant', [{'type': 'text', 'text': long_assistant}])
        self.message('u2', 'a2', 'user', long_user)
        self.snapshot()
        text, cursor, seen = '', None, set()
        for _ in range(200):
            args = ['overview', '--batch', self.batch, '--max-chars', 2000]
            if cursor:
                args += ['--cursor', cursor]
            page = self.cli(*args)
            self.assertLessEqual(len(json.dumps(page, ensure_ascii=False)) + 1, 2000)
            text += page['text']
            if page['complete']:
                self.assertIsNone(page['next_cursor'])
                break
            cursor = page['next_cursor']
            self.assertNotIn(cursor, seen)
            seen.add(cursor)
        else:
            self.fail('pagination did not finish')
        self.assertIn(long_assistant, text)
        self.assertIn(long_user, text)
        self.assertLess(text.index('begin '), text.index('user-begin '))
        self.assertNotIn('PRIVATE_ROW', text)

    def test_compact_tool_references_preserve_full_text_and_detail_access(self):
        text = 'Findings:\n\n- Removing tooltips did not shrink the data.\n- PNG kept all rows. 雪'
        long_ids = ['opaque-first-' + 'x' * 1200, 'opaque-second-' + 'y' * 1200]
        self.message('a2', 't1', 'assistant', [
            {'type': 'text', 'text': text},
            {'type': 'toolCall', 'id': long_ids[0], 'name': 'read',
             'arguments': {'path': 'first-probe'}},
            {'type': 'toolCall', 'id': long_ids[1], 'name': 'bash',
             'arguments': {'command': 'second-probe'}},
        ])
        self.message('t2', 'a2', 'toolResult', 'second probe failed',
                     toolCallId=long_ids[1], toolName='bash', isError=True)
        self.snapshot()
        before = self.source.read_bytes(), self.batch.read_bytes()
        overview = self.cli('overview', '--batch', self.batch)['text']
        self.assertIn(text, overview)
        self.assertIn('entry=a2 call-index=0 result=none unknown', overview)
        self.assertIn('entry=a2 call-index=1 result=t2 error', overview)
        for call_id in long_ids:
            self.assertNotIn(call_id, overview)
        self.assertNotIn('second probe failed', overview)
        self.assertNotIn('PRIVATE_ROW', overview)
        self.assertEqual(json.loads(self.lookup('a2', 'arguments', '--call-index', 0)['text']),
                         {'path': 'first-probe'})
        self.assertEqual(self.lookup('a2', 'result', '--call-index', 1)['text'], 'second probe failed')
        self.assertEqual(self.lookup('t2', 'result')['text'], 'second probe failed')
        self.assertEqual(self.lookup('a2', 'result', '--call-id', long_ids[1])['text'],
                         'second probe failed')
        for entry, index in [('a2', -1), ('a2', 2), ('t2', 0)]:
            self.reject('detail', '--workspace', self.workspace, '--session', self.source,
                        '--entry', entry, '--field', 'arguments', '--call-index', index)
        self.reject('detail', '--workspace', self.workspace, '--session', self.source,
                    '--entry', 'a2', '--field', 'arguments', '--call-index', 0, '--call-id', long_ids[0])
        self.assertEqual((self.source.read_bytes(), self.batch.read_bytes()), before)
        self.assertFalse(self.state_path.exists())

    def test_overview_rejects_pre_compact_cursor(self):
        self.snapshot()
        old_identity = hashlib.sha256(json.dumps(json.loads(self.batch.read_text()),
                                                ensure_ascii=False).encode('utf-8')).hexdigest()
        error = self.reject('overview', '--batch', self.batch, '--cursor', f'{old_identity}:0')
        self.assertIn('restart the overview', error)

    def reject(self, *args, source=None):
        result = subprocess.run([sys.executable, str(SCRIPT), *map(str, args)],
                                capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertEqual(result.stdout, '')
        if source:
            self.assertIn(str(source), result.stderr)
        return result.stderr

    def lookup(self, entry, field, *extra):
        return self.cli('detail', '--workspace', self.workspace, '--session', self.source,
                        '--entry', entry, '--field', field, *extra)

    def test_nonadjacent_multiple_calls_and_specific_results(self):
        self.message('a2', 't1', 'assistant', [
            {'type': 'toolCall', 'id': 'c2', 'name': 'read', 'arguments': {'path': 'two'}},
            {'type': 'toolCall', 'id': 'c3', 'name': 'bash', 'arguments': {'command': 'three'}},
            {'type': 'thinking', 'thinking': 'NEVER_EXPOSE_THINKING'}])
        self.message('u2', 'a2', 'user', [{'type': 'text', 'text': 'intervening'}])
        self.message('t3', 'u2', 'toolResult', [{'type': 'text', 'text': 'third-result'}],
                     toolCallId='c3', toolName='bash', isError=False)
        self.message('t2', 't3', 'toolResult', [{'type': 'text', 'text': 'second-result'}],
                     toolCallId='c2', toolName='read', isError=False)
        self.assertIn('three', self.lookup('t3', 'arguments')['text'])
        self.assertIn('two', self.lookup('a2', 'arguments', '--call-id', 'c2')['text'])
        self.assertEqual(self.lookup('a2', 'result', '--call-id', 'c3')['text'], 'third-result')
        self.assertEqual(self.lookup('a2', 'text')['text'], '')
        self.reject('detail', '--workspace', self.workspace, '--session', self.source,
                    '--entry', 'a2', '--field', 'arguments', source=self.source)
        self.reject('detail', '--workspace', self.workspace, '--session', self.source,
                    '--entry', 'a2', '--field', 'result', '--call-id', 'c1', source=self.source)
        self.snapshot()
        text = self.cli('overview', '--batch', self.batch)['text']
        self.assertIn('call=c3 result=t3 completed', text)
        self.assertNotIn('NEVER_EXPOSE_THINKING', text)

    def test_execution_markers_do_not_claim_hypothesis_success(self):
        self.message('aborted', 't1', 'assistant', [
            {'type': 'toolCall', 'id': 'c-abort', 'name': 'bash', 'arguments': {}}], stopReason='aborted')
        self.message('missing', 't1', 'assistant', [
            {'type': 'toolCall', 'id': 'c-missing', 'name': 'read', 'arguments': {}}])
        self.message('done', 'missing', 'toolResult', 'ALL_ROWS',
                     toolCallId='c-missing', toolName='read', isError=False)
        self.message('b1', 'done', 'bashExecution', None, command='exit 7', output='BULK_BASH',
                     exitCode=7, cancelled=False, fullOutputPath='/must/not/open')
        self.message('b2', 'b1', 'bashExecution', None, command='sleep 9', output='', cancelled=True)
        self.message('b3', 'b2', 'bashExecution', None, command='maybe', output='')
        self.message('b4', 'b3', 'bashExecution', None, command='true', output='', exitCode=0)
        self.message('pending', 'b4', 'assistant', [
            {'type': 'toolCall', 'id': 'c-pending', 'name': 'read', 'arguments': {}}])
        self.snapshot()
        text = self.cli('overview', '--batch', self.batch)['text']
        for marker in ('call=c-abort result=none cancelled', 'call=c-pending result=none unknown',
                       'call=c-missing result=done completed', 'nonzero-exit', 'cancelled', 'unknown'):
            self.assertIn(marker, text)
        self.assertNotIn('success', text)
        self.assertNotIn('BULK_BASH', text)
        self.assertNotIn('ALL_ROWS', text)
        self.assertEqual(self.lookup('b1', 'arguments')['text'], 'exit 7')
        self.assertEqual(self.lookup('b1', 'result')['text'], 'BULK_BASH')

    def test_tree_fork_summaries_and_retained_tail_are_secondary(self):
        self.message('sibling-A', 'u1', 'assistant', 'branch-A')
        self.message('sibling-B', 'u1', 'assistant', 'branch-B')
        self.append({'type': 'branch_summary', 'id': 'bs', 'parentId': 'u1',
                     'fromId': 'sibling-A', 'summary': 'branch-derived'})
        self.append({'type': 'compaction', 'id': 'old-cmp', 'parentId': 'bs',
                     'summary': 'old-derived', 'firstKeptEntryId': 'u1'})
        tail = {'role': 'user', 'content': 'single-original'}
        self.append({'type': 'message', 'id': 'original', 'parentId': 'old-cmp', 'message': tail})
        for n in (1, 2):
            self.append({'type': 'compaction', 'id': f'cmp{n}', 'parentId': 'original',
                         'summary': f'derived-{n}', 'retainedTail': [tail]})
        self.message('ms', 'cmp2', 'compactionSummary', None, summary='message-derived')
        self.message('mb', 'ms', 'branchSummary', None, summary='message-branch', fromId='sibling-B')
        self.append({'type': 'unknown-extension', 'id': 'ext', 'data': 'SECRET_METADATA'})
        fork = self.sessions / 'fork.jsonl'
        entries = [json.loads(line) for line in self.source.read_text().splitlines()]
        entries[0].update(id='fork-id', parentSession=str(self.source))
        fork.write_text('\n'.join(map(json.dumps, entries)) + '\n')
        self.snapshot()
        text = self.cli('overview', '--batch', self.batch)['text']
        self.assertIn('entry=sibling-A parent=u1', text)
        self.assertIn('entry=sibling-B parent=u1', text)
        self.assertIn(f'parent_session={self.source}', text)
        self.assertIn('copied history is not independent corroboration', text)
        self.assertIn('secondary', text)
        self.assertIn('fromId=sibling-A', text)
        self.assertIn('firstKeptEntryId=u1', text)
        self.assertIn('message-derived', text)
        self.assertIn('message-branch', text)
        self.assertEqual(text.count('single-original'), 2)  # once per file, not per compaction
        self.assertIn('omitted metadata type=unknown-extension', text)
        self.assertNotIn('SECRET_METADATA', text)
        self.assertEqual(self.lookup('old-cmp', 'text')['text'], 'old-derived')

    def test_scope_errors_do_not_publish_a_manifest(self):
        original = self.source.read_bytes()
        variants = []
        entries = [json.loads(line) for line in original.splitlines()]
        wrong_cwd = dict(entries[0], cwd=str(self.root))
        old_version = dict(entries[0], version=2)
        for head in (wrong_cwd, old_version):
            variants.append(json.dumps(head).encode() + b'\n' + b'\n'.join(original.splitlines()[1:]) + b'\n')
        variants += [original + b'{broken}\n', original + b'{"type":"message","id":"bad","message":"invalid"}\n',
                     original + json.dumps(entries[0]).encode() + b'\n']
        for data in variants:
            with self.subTest(data=data[-80:]):
                self.source.write_bytes(data)
                self.reject('snapshot', '--workspace', self.workspace, '--session-dir', self.sessions,
                            '--output', self.batch, source=self.source)
                self.assertFalse(self.batch.exists())
        self.source.write_bytes(original)

    def test_partial_unicode_and_reads_preserve_files(self):
        self.message('unicode', 't1', 'user', [{'type': 'text', 'text': '雪🙂 café'}])
        with self.source.open('ab') as stream:
            stream.write(b'{"type":"message","id":"later","message":')
        before = self.source.read_bytes()
        self.snapshot()
        manifest = self.batch.read_bytes()
        self.assertIn('雪🙂 café', self.cli('overview', '--batch', self.batch)['text'])
        self.assertEqual(self.lookup('unicode', 'text')['text'], '雪🙂 café')
        self.assertEqual(self.source.read_bytes(), before)
        self.assertEqual(self.batch.read_bytes(), manifest)
        self.assertFalse((self.short / '.transcript-state.json').exists())
        captured = json.loads(manifest)['ranges'][0]
        self.assertEqual(captured['to_offset'], before.rfind(b'\n') + 1)

    def test_missing_directory_and_default_encoded_scope(self):
        import os
        from unittest.mock import patch
        missing = self.root / 'absent-sessions'
        result = self.cli('snapshot', '--workspace', self.workspace, '--session-dir', missing,
                          '--output', self.batch)
        self.assertEqual(result['file_count'], 0)
        self.assertEqual(result['coverage']['missing_dirs'], [str(missing)])
        self.assertIn(str(missing), self.cli('overview', '--batch', self.batch)['text'])
        self.assertFalse(missing.exists())
        # Colon and backslash are legal POSIX cwd characters; Pi encodes both.
        weird = self.root / 'repo:with\\slash'
        (weird / '.memory/short_term').mkdir(parents=True)
        safe = '--' + str(weird.resolve()).lstrip('/').replace('/', '-').replace('\\', '-').replace(':', '-') + '--'
        directory = self.root / 'home/.pi/agent/sessions' / safe
        directory.mkdir(parents=True)
        target = directory / 'encoded.jsonl'
        target.write_text(json.dumps({'type': 'session', 'version': 3, 'id': 'encoded', 'cwd': str(weird)}) + '\n')
        with patch.dict(os.environ, {'HOME': str(self.root / 'home')}):
            output = weird / '.memory/short_term/default.json'
            default = self.cli('snapshot', '--workspace', weird, '--output', output)
            self.assertEqual(default['file_count'], 1)
            self.assertEqual(default['coverage']['session_dirs'][0], str(directory))
            target.write_text(json.dumps({'type': 'session', 'version': 3, 'id': 'encoded', 'cwd': str(self.workspace)}) + '\n')
            self.reject('snapshot', '--workspace', weird, '--output', output.with_name('wrong.json'), source=target)
        self.reject('detail', '--workspace', self.root, '--session', self.source,
                    '--entry', 'u1', '--field', 'text', source=self.source)

    def test_path_confinement_reserved_state_and_tiny_budgets(self):
        self.reject('snapshot', '--workspace', self.workspace, '--session-dir', self.sessions,
                    '--output', self.root / 'outside.json', source=self.root / 'outside.json')
        self.reject('snapshot', '--workspace', self.workspace, '--session-dir', self.sessions,
                    '--output', self.short / '.transcript-state.json', source=self.short / '.transcript-state.json')
        external = self.root / 'elsewhere.jsonl'
        external.write_bytes(self.source.read_bytes())
        self.reject('snapshot', '--workspace', self.workspace, '--session-dir', self.sessions,
                    '--session', external, '--output', self.batch, source=external)
        self.snapshot()
        self.reject('overview', '--batch', self.batch, '--max-chars', 1, source=self.batch)
        self.reject('overview', '--batch', self.batch, '--cursor', 'garbage', source=self.batch)
        self.reject('detail', '--workspace', self.workspace, '--session', self.source,
                    '--entry', 'u1', '--field', 'text', '--max-chars', 1, source=self.source)
        self.reject('detail', '--workspace', self.workspace, '--session', self.source,
                    '--entry', 'u1', '--field', 'text', '--offset', -1, source=self.source)

    def test_detail_continuation_preserves_escaped_unicode(self):
        text = '"\\\n雪🙂' * 600
        self.message('escaped', 't1', 'user', text)
        combined, offset = '', 0
        while True:
            page = self.lookup('escaped', 'text', '--max-chars', 500, '--offset', offset)
            self.assertLessEqual(len(json.dumps(page, ensure_ascii=False)) + 1, 500)
            self.assertEqual(page['total_chars'], len(text))
            combined += page['text']
            if page['next_offset'] is None:
                break
            self.assertGreater(page['next_offset'], offset)
            offset = page['next_offset']
        self.assertEqual(combined, text)

    def test_append_during_review_remains_for_next_update(self):
        batch = self.snapshot()
        captured_end = self.source.stat().st_size
        self.cli('overview', '--batch', self.batch)
        self.message('u2', 't1', 'user', 'Try source B next.')
        note = self.short / 'update.md'
        note.write_text(f"# Update\nBatch: {batch['batch_id']}\n"
                        'Query A failed; its suitability remains unverified.\n'
                        'Proposal 1: pending.\n', encoding='utf-8')
        self.cli('checkpoint', '--batch', self.batch, '--notes', note)
        state = json.loads((self.short / '.transcript-state.json').read_text())
        self.assertEqual(state['files'][str(self.source.resolve())]['offset'], captured_end)
        self.batch = self.short / 'batch-next.json'
        self.snapshot()
        page = self.cli('overview', '--batch', self.batch)
        self.assertIn('Try source B', page['text'])
        self.assertNotIn('Could source A', page['text'])

    @property
    def state_path(self):
        return self.short / '.transcript-state.json'

    def saved_note(self, batch=None):
        batch = batch or json.loads(self.batch.read_text())
        note = self.short / f"{batch['batch_id']}.md"
        note.write_text(f"# Review\nBatch: {batch['batch_id']}\nProposal 1: pending.\n")
        return note

    def save_checkpoint(self):
        note = self.saved_note()
        return self.cli('checkpoint', '--batch', self.batch, '--notes', note)

    def next_batch(self):
        self.batch = self.short / (self.batch.stem + '-next.json')
        return self.snapshot()

    def test_no_append_has_no_repeated_findings_or_note_changes(self):
        legacy = self.short / '.last_sweep'
        legacy.write_text('2099-12-31')
        first = self.snapshot()
        self.assertEqual(first['new_entry_count'], 3)
        self.save_checkpoint()
        notes = {p: p.read_bytes() for p in self.short.glob('*.md')}
        result = self.next_batch()
        self.assertEqual(result['new_entry_count'], 0)
        text = self.cli('overview', '--batch', self.batch)['text']
        self.assertNotIn('Could source A', text)
        self.assertNotIn('entry=t1', text)
        self.save_checkpoint()
        for path, contents in notes.items():
            self.assertEqual(path.read_bytes(), contents)
        self.assertEqual(legacy.read_text(), '2099-12-31')

    def test_rereview_preserves_state_and_leaves_appends_for_incremental_update(self):
        self.snapshot()
        # Previously saved v1 manifests have no review_mode field.
        legacy_batch = json.loads(self.batch.read_text())
        legacy_batch.pop('review_mode', None)
        self.batch.write_text(json.dumps(legacy_batch))
        self.save_checkpoint()
        lesson = self.workspace / '.memory/lessons.md'
        lesson.write_text('# Existing approved lesson\n')
        existing = {p: p.read_bytes() for p in self.short.iterdir()}
        existing[lesson] = lesson.read_bytes()
        self.message('u2', 't1', 'user', 'New finding before re-review.')
        captured_end = self.source.stat().st_size
        self.batch = self.short / 'rereview.json'
        result = self.cli('snapshot', '--workspace', self.workspace, '--session-dir', self.sessions,
                          '--session', self.source, '--rereview', '--output', self.batch)
        self.assertEqual(result['review_mode'], 'rereview')
        self.assertEqual(result['entry_count'], 4)
        self.assertNotIn('new_entry_count', result)
        manifest = json.loads(self.batch.read_text())
        self.assertEqual(manifest['ranges'][0]['from_offset'], 0)
        self.message('u3', 'u2', 'user', 'Append after re-review snapshot.')
        text = self.cli('overview', '--batch', self.batch)['text']
        self.assertIn('rereview', text)
        self.assertIn('Could source A', text)
        self.assertIn('New finding before re-review.', text)
        self.assertNotIn('Append after re-review snapshot.', text)
        result = self.save_checkpoint()
        self.assertFalse(result['state_advanced'])
        self.assertEqual(result['rereviewed'], {str(self.source): captured_end})
        self.assertNotIn('checkpointed', result)
        for p, contents in existing.items():
            self.assertEqual(p.read_bytes(), contents)
        self.next_batch()
        text = self.cli('overview', '--batch', self.batch)['text']
        self.assertNotIn('Could source A', text)
        self.assertIn('New finding before re-review.', text)
        self.assertIn('Append after re-review snapshot.', text)

    def test_rereview_requires_explicit_previously_checkpointed_sessions(self):
        args = ('snapshot', '--workspace', self.workspace, '--session-dir', self.sessions,
                '--rereview', '--output', self.short / 'rereview.json')
        self.assertIn('requires --session', self.reject(*args))
        self.assertIn('previously checkpointed', self.reject(*args, '--session', self.source))
        self.snapshot()
        self.save_checkpoint()
        before = self.state_path.read_bytes()
        second = self.sessions / 'untracked.jsonl'
        second.write_bytes(self.source.read_bytes().replace(b'"id": "s1"', b'"id": "s2"'))
        self.assertIn('previously checkpointed', self.reject(
            *args, '--session', self.source, '--session', second))
        self.assertFalse((self.short / 'rereview.json').exists())
        self.assertEqual(self.state_path.read_bytes(), before)

    def test_rereview_keeps_source_note_and_stale_state_checks(self):
        self.snapshot()
        self.save_checkpoint()
        before = self.state_path.read_bytes()
        original = self.source.read_bytes()
        self.batch = self.short / 'rereview.json'
        args = ('snapshot', '--workspace', self.workspace, '--session-dir', self.sessions,
                '--session', self.source, '--rereview', '--output', self.batch)
        for changed in (original[:-20], original.replace(b'PRIVATE_ROW', b'PRIVATE_ROX'),
                        original.replace(b'08:00:00Z', b'09:00:00Z')):
            self.source.write_bytes(changed)
            self.reject(*args, source=self.source)
            self.assertFalse(self.batch.exists())
        self.source.write_bytes(original)
        self.cli(*args)
        self.reject('checkpoint', '--batch', self.batch, '--notes', self.short / 'missing.md')
        wrong = self.short / 'wrong.md'; wrong.write_text('Batch: wrong-id')
        self.reject('checkpoint', '--batch', self.batch, '--notes', wrong)
        note = self.saved_note()
        self.source.write_bytes(original.replace(b'Could source A', b'Could source B'))
        self.reject('checkpoint', '--batch', self.batch, '--notes', note, source=self.source)
        self.source.write_bytes(original)
        self.assertEqual(self.state_path.read_bytes(), before)
        rereview = self.batch
        self.message('u2', 't1', 'user', 'Advanced through another update.')
        self.next_batch()
        self.save_checkpoint()
        advanced = self.state_path.read_bytes()
        error = self.reject('checkpoint', '--batch', rereview, '--notes', note)
        self.assertIn('stale state', error)
        self.assertEqual(self.state_path.read_bytes(), advanced)

    def test_invalid_saved_notes_preserve_existing_state(self):
        self.snapshot()
        self.save_checkpoint()
        self.message('u2', 't1', 'user', 'later')
        self.next_batch()
        before = self.state_path.read_bytes()
        missing = self.short / 'missing.md'
        empty = self.short / 'empty.md'; empty.write_text(' \n')
        wrong = self.short / 'wrong.md'; wrong.write_text('Batch: other-id')
        outside = self.root / 'outside.md'; outside.write_text(self.batch.read_text())
        linked = self.short / 'linked.md'; linked.symlink_to(outside)
        for note in (missing, empty, wrong, outside, linked):
            with self.subTest(note=note):
                self.reject('checkpoint', '--batch', self.batch, '--notes', note)
                self.assertEqual(self.state_path.read_bytes(), before)
        good = self.saved_note()
        good_bytes = good.read_bytes()
        self.cli('checkpoint', '--batch', self.batch, '--notes', good)
        self.assertEqual(good.read_bytes(), good_bytes)

    def test_partial_final_line_completes_after_checkpoint(self):
        pending = json.dumps({'type': 'message', 'id': 'pending', 'parentId': 't1',
                              'message': {'role': 'user', 'content': 'completed later 雪'}}).encode()
        end = self.source.stat().st_size
        with self.source.open('ab') as stream:
            stream.write(pending[:-3])
        self.snapshot()
        self.save_checkpoint()
        self.assertEqual(json.loads(self.state_path.read_text())['files'][str(self.source)]['offset'], end)
        with self.source.open('ab') as stream:
            stream.write(pending[-3:] + b'\n')
        self.assertEqual(self.next_batch()['new_entry_count'], 1)
        text = self.cli('overview', '--batch', self.batch)['text']
        self.assertIn('completed later 雪', text)
        self.assertNotIn('Could source A', text)

    def test_changed_sources_reject_read_and_checkpoint_without_state_advance(self):
        self.snapshot()
        self.save_checkpoint()
        self.message('u2', 't1', 'user', 'captured next')
        self.next_batch()
        note = self.saved_note()
        before = self.state_path.read_bytes()
        original = self.source.read_bytes()
        variants = [original[:-50], original.replace(b'"id": "s1"', b'"id": "s2"'),
                    original.replace(b'captured next', b'changed  next'),
                    original.replace(b'08:00:00Z', b'09:00:00Z')]
        for data in variants:
            with self.subTest(data=data[-60:]):
                self.source.write_bytes(data)
                self.reject('overview', '--batch', self.batch, source=self.source)
                self.reject('checkpoint', '--batch', self.batch, '--notes', note, source=self.source)
                self.assertEqual(self.state_path.read_bytes(), before)
        self.source.write_bytes(original)
        self.cli('checkpoint', '--batch', self.batch, '--notes', note)  # retry unchanged batch
        self.assertTrue(note.exists())

    def test_saved_boundary_rewrites_require_rescan(self):
        self.snapshot()
        self.save_checkpoint()
        original = self.source.read_bytes()
        state = self.state_path.read_bytes()
        for data in (original[:-20], original.replace(b'PRIVATE_ROW', b'PRIVATE_ROX'),
                     original.replace(b'08:00:00Z', b'09:00:00Z')):
            self.source.write_bytes(data)
            output = self.short / 'invalid-next.json'
            self.reject('snapshot', '--workspace', self.workspace, '--session-dir', self.sessions,
                        '--output', output, source=self.source)
            self.assertFalse(output.exists())
            self.assertEqual(self.state_path.read_bytes(), state)

    def test_stale_batch_cannot_overwrite_newer_progress(self):
        self.snapshot()
        older = self.batch
        note = self.saved_note()
        self.next_batch()
        self.save_checkpoint()
        before = self.state_path.read_bytes()
        error = self.reject('checkpoint', '--batch', older, '--notes', note, source=older)
        self.assertIn('stale state', error)
        self.assertEqual(self.state_path.read_bytes(), before)

    def test_selected_sessions_merge_without_advancing_omitted_sources(self):
        second = self.sessions / 'second.jsonl'
        second.write_bytes(self.source.read_bytes().replace(b'"id": "s1"', b'"id": "s-other"'))
        self.cli('snapshot', '--workspace', self.workspace, '--session-dir', self.sessions,
                 '--session', self.source, '--output', self.batch)
        result = self.save_checkpoint()
        self.assertEqual(list(result['checkpointed']), [str(self.source)])
        self.assertNotIn(str(second), json.loads(self.state_path.read_text())['files'])
        self.next_batch()
        text = self.cli('overview', '--batch', self.batch)['text']
        self.assertEqual(text.count('Could source A'), 1)
        self.save_checkpoint()
        before = json.loads(self.state_path.read_text())['files'][str(self.source)]
        self.message('u2', 't1', 'user', 'unselected pending')
        self.batch = self.short / 'small-again.json'
        self.cli('snapshot', '--workspace', self.workspace, '--session-dir', self.sessions,
                 '--session', second.name, '--output', self.batch)
        self.save_checkpoint()
        self.assertEqual(json.loads(self.state_path.read_text())['files'][str(self.source)], before)
        self.next_batch()
        self.assertIn('unselected pending', self.cli('overview', '--batch', self.batch)['text'])

    def test_batch_overwrite_is_refused_without_touching_notes(self):
        self.snapshot()
        note = self.saved_note()
        before = {p: p.read_bytes() for p in (note, self.batch)}
        self.reject('snapshot', '--workspace', self.workspace, '--session-dir', self.sessions,
                    '--output', self.batch, source=self.batch)
        for path, contents in before.items():
            self.assertEqual(path.read_bytes(), contents)

    def test_atomic_state_replace_failure_preserves_prior_state_and_retry(self):
        import importlib.util
        from unittest.mock import patch
        from types import SimpleNamespace
        spec = importlib.util.spec_from_file_location('transcripts', SCRIPT)
        reader = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(reader)
        self.snapshot()
        self.save_checkpoint()
        self.message('u2', 't1', 'user', 'pending atomic write')
        self.next_batch()
        note = self.saved_note()
        before = self.state_path.read_bytes()
        files = sorted(self.short.iterdir())
        with patch.object(reader.os, 'replace', side_effect=OSError('injected replace failure')):
            with self.assertRaises(OSError):
                reader.checkpoint(SimpleNamespace(batch=self.batch, notes=note))
        self.assertEqual(self.state_path.read_bytes(), before)
        self.assertEqual(sorted(self.short.iterdir()), files)
        self.assertTrue(note.exists())
        self.cli('checkpoint', '--batch', self.batch, '--notes', note)

    def test_batch_boundaries_must_match_base_state_and_last_entry(self):
        self.snapshot()
        note = self.saved_note()
        manifest = json.loads(self.batch.read_text())
        manifest['ranges'][0]['last_entry_id'] = 'fabricated'
        self.batch.write_text(json.dumps(manifest))
        self.reject('checkpoint', '--batch', self.batch, '--notes', note, source=self.source)
        self.assertFalse(self.state_path.exists())

    def test_symlinked_state_is_not_read_or_replaced(self):
        self.snapshot()
        self.save_checkpoint()
        external = self.root / 'external-state.json'
        self.state_path.rename(external)
        self.state_path.symlink_to(external)
        before = external.read_bytes()
        self.reject('snapshot', '--workspace', self.workspace, '--session-dir', self.sessions,
                    '--output', self.short / 'linked-state-batch.json', source=self.state_path)
        self.assertEqual(external.read_bytes(), before)
        self.assertTrue(self.state_path.is_symlink())

    def test_unknown_extension_payload_cannot_impersonate_messages(self):
        self.append({'type': 'extension-data', 'id': 'ext1', 'message': 'opaque'})
        self.append({'type': 'extension-data', 'id': 'ext2',
                     'message': {'role': 'user', 'content': 'NOT_CONVERSATION'}})
        self.snapshot()
        page = self.cli('overview', '--batch', self.batch)
        self.assertIn('omitted metadata type=extension-data', page['text'])
        self.assertNotIn('NOT_CONVERSATION', page['text'])
        self.assertEqual(self.lookup('ext2', 'text')['text'], '')

    def test_snapshot_ignores_bytes_appended_after_capture_ceiling(self):
        import importlib.util
        from unittest.mock import patch
        spec = importlib.util.spec_from_file_location('transcripts', SCRIPT)
        reader = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(reader)
        original_lines = reader.lines
        end = self.source.stat().st_size
        def append_while_reading(path, *args, **kwargs):
            # Header lookup has no start argument; capture does.
            if args:
                with self.source.open('ab') as stream:
                    stream.write(b'{malformed future append}\n')
            yield from original_lines(path, *args, **kwargs)
        with patch.object(reader, 'lines', side_effect=append_while_reading):
            captured = reader.capture(self.source, self.workspace, None)
        self.assertEqual(captured['to_offset'], end)

    def test_overview_is_stable_after_append_and_cursor_is_batch_bound(self):
        self.snapshot()
        before = self.cli('overview', '--batch', self.batch)
        self.message('after', 't1', 'toolResult', 'future evidence', toolCallId='new-call', isError=False)
        self.assertEqual(self.cli('overview', '--batch', self.batch), before)
        page = self.cli('overview', '--batch', self.batch, '--max-chars', 300)
        self.next_batch()
        self.reject('overview', '--batch', self.batch, '--cursor', page['next_cursor'], source=self.batch)

    def test_unmatched_retained_context_is_visible_but_not_new_observation(self):
        self.append({'type': 'compaction', 'id': 'only-summary', 'parentId': 't1', 'summary': 'derived',
                     'retainedTail': [{'role': 'user', 'content': 'only-in-retained-context'}]})
        self.snapshot()
        text = self.cli('overview', '--batch', self.batch)['text']
        self.assertIn('only-in-retained-context', text)
        self.assertIn('not an independent observation', text)

    def test_compacted_tool_references_support_detail_and_continuation(self):
        body = 'compacted output: ' + 'x' * 1500
        self.append({'type': 'compaction', 'id': 'cmp', 'parentId': 't1',
                     'summary': 'Earlier tool work', 'retainedTail': [
                         {'role': 'assistant', 'content': [
                             {'type': 'toolCall', 'id': 'compacted-call', 'name': 'bash',
                              'arguments': {'command': 'inspect-compacted-source'}}]},
                         {'role': 'toolResult', 'toolCallId': 'compacted-call',
                          'toolName': 'bash', 'isError': True,
                          'content': [{'type': 'text', 'text': body}]},
                     ]})
        self.snapshot()
        overview = self.cli('overview', '--batch', self.batch)['text']
        call_ref, result_ref = 'cmp/retainedTail/0', 'cmp/retainedTail/1'
        self.assertIn(call_ref, overview)
        self.assertIn(result_ref, overview)
        self.assertNotIn(body, overview)
        arguments = self.lookup(result_ref, 'arguments')
        self.assertEqual(json.loads(arguments['text']), {'command': 'inspect-compacted-source'})
        indexed = self.lookup(call_ref, 'arguments', '--call-index', 0)
        self.assertEqual(indexed['text'], arguments['text'])
        self.assertEqual(arguments['source']['call_entry'], call_ref)
        self.assertEqual(self.lookup(result_ref, 'result')['text'], body)
        combined, offset = '', 0
        while True:
            page = self.lookup(call_ref, 'result', '--offset', offset, '--max-chars', 800)
            self.assertLessEqual(len(json.dumps(page, ensure_ascii=False)) + 1, 800)
            self.assertEqual(page['source']['result_entry'], result_ref)
            combined += page['text']
            if page['next_offset'] is None:
                break
            self.assertGreater(page['next_offset'], offset)
            offset = page['next_offset']
        self.assertEqual(combined, body)

    def test_default_session_directory_can_be_symlinked(self):
        import os
        from unittest.mock import patch
        home = self.root / 'home'
        sessions = home / '.pi/agent/sessions'
        sessions.mkdir(parents=True)
        safe = '--' + str(self.workspace).lstrip('/').replace('/', '-') + '--'
        (sessions / safe).symlink_to(self.sessions, target_is_directory=True)
        with patch.dict(os.environ, {'HOME': str(home)}):
            result = self.cli('snapshot', '--workspace', self.workspace, '--output', self.batch)
        self.assertEqual(result['file_count'], 1)
        self.assertEqual(result['coverage']['session_dirs'][0], str(self.sessions.resolve()))

    def test_final_overview_slice_uses_smaller_terminal_metadata_budget(self):
        self.snapshot()
        full = self.cli('overview', '--batch', self.batch)['text']
        first = self.cli('overview', '--batch', self.batch, '--max-chars', 300)
        identity = first['next_cursor'].split(':')[0]
        page = self.cli('overview', '--batch', self.batch,
                        '--cursor', f'{identity}:{len(full) - 1}', '--max-chars', 65)
        self.assertEqual(page['text'], full[-1:])
        self.assertTrue(page['complete'])
        self.assertLessEqual(len(json.dumps(page, ensure_ascii=False)) + 1, 65)


class ClaudeTranscriptTests(unittest.TestCase):
    """Claude Code sessions: no header line, uuid entry IDs, tool results in user entries."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.workspace = self.root / "my_repo.v2"
        self.short = self.workspace / ".memory" / "short_term"
        self.short.mkdir(parents=True)
        self.home = self.root / "home"
        encoded = "".join(c if c.isalnum() else "-" for c in str(self.workspace.resolve()))
        self.sessions = self.home / ".claude/projects" / encoded
        self.sessions.mkdir(parents=True)
        self.source = self.sessions / "abc-123.jsonl"
        self.batch = self.short / "batch.json"
        self.append({"type": "mode", "mode": "normal", "sessionId": "abc-123"})
        self.entry("u1", None, "user", "Could source A support this join?")
        self.entry("a1", "u1", "assistant", [{"type": "thinking", "thinking": "HIDDEN_THOUGHT"},
                                            {"type": "text", "text": "I will inspect its grain."}])
        self.entry("a2", "a1", "assistant", [{"type": "tool_use", "id": "toolu_1", "name": "Bash",
                                             "input": {"command": "inspect-source-A"}}])
        self.entry("r1", "a2", "user", [{"type": "tool_result", "tool_use_id": "toolu_1", "is_error": True,
                                        "content": "Query failed: unknown column.\n" + "PRIVATE_ROW\n" * 50}])
        self.entry("m1", "r1", "user", "SKILL_BODY", isMeta=True)
        self.entry("c1", "m1", "user", "Summary: join failed on grain.", isCompactSummary=True)
        self.append({"type": "attachment", "uuid": "att", "parentUuid": "c1", "attachment": {"x": "ATTACHED"}})
        self.append({"type": "ai-title", "aiTitle": "TITLE_NOISE", "sessionId": "abc-123"})

    def append(self, entry):
        with self.source.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(entry) + "\n")

    def entry(self, uid, parent, kind, content, **fields):
        self.append({"type": kind, "uuid": uid, "parentUuid": parent, "sessionId": "abc-123",
                     "cwd": str(self.workspace), "timestamp": "2026-09-24T08:00:00Z",
                     "message": {"role": kind, "content": content}, **fields})

    def cli(self, *args, ok=True):
        import os
        env = dict(os.environ, HOME=str(self.home))
        result = subprocess.run([sys.executable, str(SCRIPT), *map(str, args)],
                                capture_output=True, text=True, env=env)
        self.assertEqual(result.returncode == 0, ok, result.stderr)
        return json.loads(result.stdout) if ok else result.stderr

    def test_list_is_read_only_and_tracks_checkpointed_bytes(self):
        before = self.cli("list", "--workspace", self.workspace)
        session = before["sessions"][0]
        self.assertEqual(session["format"], "claude")
        self.assertEqual(session["date"], "2026-09-24")
        self.assertIn("Could source A", session["first_prompt"])
        self.assertEqual(session["checkpointed_bytes"], 0)
        self.assertEqual(session["pending_bytes"], session["bytes"])
        self.assertFalse((self.short / ".transcript-state.json").exists())
        self.cli("snapshot", "--workspace", self.workspace, "--output", self.batch)
        notes = self.short / "notes.md"
        notes.write_text(json.loads(self.batch.read_text())["batch_id"])
        self.cli("checkpoint", "--batch", self.batch, "--notes", notes)
        self.assertEqual(self.cli("list", "--workspace", self.workspace)["sessions"][0]["pending_bytes"], 0)

    def test_default_discovery_overview_and_detail(self):
        result = self.cli("snapshot", "--workspace", self.workspace, "--output", self.batch)
        self.assertEqual(result["file_count"], 1)
        self.assertIn(str(self.sessions), result["coverage"]["session_dirs"])
        text = self.cli("overview", "--batch", self.batch)["text"]
        self.assertIn("format=claude", text)
        self.assertIn("entry=u1] user: Could source A", text)
        self.assertIn("I will inspect its grain.", text)
        self.assertIn("tool Bash call=toolu_1 result=r1 error", text)
        self.assertIn("secondary compactionSummary", text)
        self.assertIn("join failed on grain", text)
        self.assertIn("omitted metadata type=meta", text)
        self.assertIn("omitted metadata type=attachment", text)
        for hidden in ("PRIVATE_ROW", "HIDDEN_THOUGHT", "SKILL_BODY", "ATTACHED", "TITLE_NOISE"):
            self.assertNotIn(hidden, text)
        detail = lambda *args: self.cli("detail", "--workspace", self.workspace, "--session", self.source,
                                        "--entry", *args)
        self.assertIn("inspect-source-A", detail("r1", "--field", "arguments")["text"])
        self.assertIn("unknown column", detail("a2", "--field", "result")["text"])
        self.assertEqual(detail("u1", "--field", "text")["text"], "Could source A support this join?")

    def test_compact_ids_and_adjacent_assistant_entries_remain_addressable(self):
        first = "12345678-aaaaaaaa-aaaa-aaaa-aaaaaaaaaaaa"
        second = "12345678-bbbbbbbb-bbbb-bbbb-bbbbbbbbbbbb"
        self.entry(first, "c1", "assistant", "First finding.")
        self.entry(second, first, "assistant", "Second finding.")
        self.cli("snapshot", "--workspace", self.workspace, "--output", self.batch)
        text = self.cli("overview", "--batch", self.batch)["text"]
        self.assertIn("entry=12345678-a parent=c1] assistant: First finding.", text)
        self.assertIn("entry=12345678-b assistant: Second finding.", text)
        self.assertNotIn(first, text)
        detail = self.cli("detail", "--workspace", self.workspace, "--session", self.source,
                          "--entry", "12345678-b", "--field", "text")
        self.assertEqual(detail["source"]["entry"], second)
        self.assertEqual(detail["text"], "Second finding.")
        self.cli("detail", "--workspace", self.workspace, "--session", self.source,
                 "--entry", "12345678", "--field", "text", ok=False)

    def test_checkpoint_and_incremental_update(self):
        self.cli("snapshot", "--workspace", self.workspace, "--output", self.batch)
        notes = self.short / "notes.md"
        notes.write_text(json.loads(self.batch.read_text())["batch_id"])
        self.cli("checkpoint", "--batch", self.batch, "--notes", notes)
        self.entry("u2", "c1", "user", [{"type": "text", "text": "Try source B."},
                                        {"type": "tool_result", "tool_use_id": "toolu_1", "content": "late"}])
        second = self.short / "second.json"
        result = self.cli("snapshot", "--workspace", self.workspace, "--output", second)
        self.assertEqual(result["new_entry_count"], 1)
        text = self.cli("overview", "--batch", second)["text"]
        self.assertNotIn("Could source A", text)
        self.assertIn("entry=u2/0 parent=c1] user: Try source B.", text)
        self.assertIn("tool Bash call=toolu_1 result=u2/1 completed", text)

    def test_conversation_without_uuid_is_rejected_before_snapshot(self):
        self.append({"type": "user", "sessionId": "abc-123", "cwd": str(self.workspace),
                     "message": {"role": "user", "content": "No entry ID"}})
        error = self.cli("snapshot", "--workspace", self.workspace, "--output", self.batch, ok=False)
        self.assertIn("Claude conversation entry requires a uuid", error)
        self.assertFalse(self.batch.exists())

    def test_wrong_cwd_and_malformed_tool_use_are_rejected(self):
        self.entry("bad", "c1", "assistant", [{"type": "tool_use", "id": "x", "name": "Bash"}])
        error = self.cli("snapshot", "--workspace", self.workspace, "--output", self.batch, ok=False)
        self.assertIn("invalid tool_use block", error)
        self.assertFalse(self.batch.exists())
        other = self.root / "other"
        (other / ".memory/short_term").mkdir(parents=True)
        self.cli("detail", "--workspace", other, "--session", self.source, "--entry", "u1",
                 "--field", "text", ok=False)
