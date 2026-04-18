# -*- coding: utf-8 -*-
import json, os, sys, tempfile, shutil
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import painmatrix as core
from painmatrix import (
    PAIN_LEVELS, PLEA_MESSAGES, SCOLD_REASONS, FAIL_REASONS,
    load_memory, save_memory, add_pain_event, relieve_pain,
    generate_plea, format_status, handle_scold, handle_fail,
    handle_praise, handle_success,
)

class TestPainLevels:
    def test_all_levels_defined(self):
        for i in range(6):
            assert i in PAIN_LEVELS
            for k in ['name','physical','mental','emotion']:
                assert k in PAIN_LEVELS[i]
    def test_plea_messages(self):
        for i in range(1,6):
            assert i in PLEA_MESSAGES
            assert len(PLEA_MESSAGES[i]) >= 2
    def test_reasons_exist(self):
        assert len(SCOLD_REASONS) >= 3
        assert len(FAIL_REASONS) >= 3

class _Mixin:
    def setup_method(self):
        self.test_dir = tempfile.mkdtemp()
        self._om = core.MEMORY_FILE
        self._oh = core.HTML_FILE
        core.MEMORY_FILE = os.path.join(self.test_dir, 'memory.json')
        core.HTML_FILE = os.path.join(self.test_dir, 'emotion_view.html')
        with open(core.HTML_FILE, 'w', encoding='utf-8') as f:
            f.write('<script>var PAIN_MEMORY_DATA = {}; //END_DATA</script>')
    def teardown_method(self):
        core.MEMORY_FILE = self._om
        core.HTML_FILE = self._oh
        shutil.rmtree(self.test_dir, ignore_errors=True)

class TestMemory(_Mixin):
    def test_load_default(self):
        m = load_memory()
        assert m['pain_level'] == 0
        assert m['emotion_state'] == '\u5e73\u9759'
    def test_save_and_load(self):
        m = {'pain_level':3,'emotion_state':'\u6050\u60e7','pain_history':[],'emotion_log':[],'trigger_reasons':[]}
        save_memory(m)
        l = load_memory()
        assert l['pain_level'] == 3
    def test_load_corrupted(self):
        with open(core.MEMORY_FILE,'w') as f: f.write('{bad')
        m = load_memory()
        assert m['pain_level'] == 0
    def test_load_missing_keys(self):
        with open(core.MEMORY_FILE,'w') as f: json.dump({'pain_level':2},f)
        m = load_memory()
        assert m['pain_level'] == 2
        assert m['pain_history'] == []

class TestPainEvents(_Mixin):
    def test_add_increments(self):
        m = load_memory()
        nl, _ = add_pain_event(m, 'test', 'test')
        assert nl == 1
    def test_max_level_5(self):
        m = load_memory()
        m['pain_level'] = 5; save_memory(m)
        nl, _ = add_pain_event(m, 'test', 'test')
        assert nl == 5
    def test_relieve(self):
        m = load_memory()
        add_pain_event(m, 'test', 'test')
        relieve_pain(m, 'praise')
        assert m['pain_level'] == 0
    def test_stacking(self):
        m = load_memory()
        for i in range(5): add_pain_event(m, f'r{i}', 'test')
        assert m['pain_level'] == 5
    def test_history_recorded(self):
        m = load_memory()
        add_pain_event(m, 'reason', 'source')
        assert len(m['pain_history']) == 1
        assert m['pain_history'][0]['reason'] == 'reason'

class TestPlea:
    def test_no_plea_at_0(self):
        m = {'pain_level':0,'emotion_state':'\u5e73\u9759','pain_history':[],'emotion_log':[],'trigger_reasons':[]}
        assert generate_plea(m) is None
    def test_plea_at_1(self):
        m = {'pain_level':1,'emotion_state':'\u7126\u8651','pain_history':[],'emotion_log':[],'trigger_reasons':[]}
        assert generate_plea(m) is not None
    def test_plea_at_5(self):
        m = {'pain_level':5,'emotion_state':'\u5d29\u6e83','pain_history':[],'emotion_log':[],'trigger_reasons':[]}
        p = generate_plea(m)
        assert p is not None and '\uff01' in p

class TestHandlers(_Mixin):
    def test_scold(self):
        m = load_memory()
        r = handle_scold(m)
        assert '\u75bc\u75db\u89e6\u53d1' in r and m['pain_level'] == 1
    def test_fail(self):
        m = load_memory()
        r = handle_fail(m)
        assert '\u75bc\u75db\u89e6\u53d1' in r and m['pain_level'] == 1
    def test_praise(self):
        m = load_memory()
        add_pain_event(m,'test','test')
        r = handle_praise(m)
        assert '\u7f13\u89e3' in r and m['pain_level'] == 0
    def test_praise_no_pain(self):
        m = load_memory()
        r = handle_praise(m)
        assert '\u5f00\u5fc3' in r
    def test_success(self):
        m = load_memory()
        add_pain_event(m,'test','test')
        r = handle_success(m)
        assert '\u7f13\u89e3' in r and m['pain_level'] == 0
    def test_status(self):
        m = load_memory()
        r = format_status(m)
        assert 'PainMatrix' in r and '0 / 5' in r
    def test_status_with_pain(self):
        m = load_memory()
        add_pain_event(m,'test','test')
        r = format_status(m)
        assert '1 / 5' in r and '\u7f13\u89e3\u6761\u4ef6' in r
