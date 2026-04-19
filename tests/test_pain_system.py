# -*- coding: utf-8 -*-
import json, os, sys, tempfile, shutil
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import painmatrix as core
from painmatrix import (
    PAIN_LEVELS, PLEA_MESSAGES, SCOLD_REASONS, FAIL_REASONS,
    HOMEOSTATIC_SETPOINTS, HOMEOSTATIC_NAMES, HOMEOSTATIC_DECAY,
    DESIRE_MESSAGES, TRAUMA_MESSAGES, COGNITIVE_EFFECTS,
    load_memory, save_memory, add_pain_event, relieve_pain,
    generate_plea, format_status, handle_scold, handle_fail,
    handle_praise, handle_success,
    compute_homeostatic_pain, compute_free_energy, compute_desire_intensity,
    compute_adaptive_learning_rate, apply_homeostatic_impact, apply_homeostatic_decay,
    encode_trauma, check_trauma_trigger, get_dominant_desire, generate_desire_message,
    handle_desire, handle_wellbeing, handle_trauma, handle_learn,
    handle_skills, handle_beliefs, load_long_term_memory, save_long_term_memory,
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


class TestHomeostaticSystem(_Mixin):
    def test_initial_homeostatic(self):
        m = load_memory()
        assert 'homeostatic' in m
        assert 'setpoints' in m
        for key in HOMEOSTATIC_SETPOINTS:
            assert key in m['homeostatic']
            assert m['homeostatic'][key] == HOMEOSTATIC_SETPOINTS[key]

    def test_free_energy_zero_at_setpoints(self):
        m = load_memory()
        fe = compute_free_energy(m)
        assert fe == 0.0

    def test_free_energy_nonzero_after_scold(self):
        m = load_memory()
        add_pain_event(m, 'test', '责罚')
        fe = compute_free_energy(m)
        assert fe > 0.0

    def test_desire_intensity_zero_at_setpoints(self):
        m = load_memory()
        di = compute_desire_intensity(m)
        assert di == 0.0

    def test_desire_intensity_nonzero_after_scold(self):
        m = load_memory()
        add_pain_event(m, 'test', '责罚')
        di = compute_desire_intensity(m)
        assert di > 0.0

    def test_homeostatic_impact_scold(self):
        m = load_memory()
        old_sb = m['homeostatic']['social_bond']
        add_pain_event(m, 'test', '责罚')
        assert m['homeostatic']['social_bond'] < old_sb

    def test_homeostatic_impact_fail(self):
        m = load_memory()
        old_comp = m['homeostatic']['competence']
        add_pain_event(m, 'test', '任务失败')
        assert m['homeostatic']['competence'] < old_comp

    def test_homeostatic_restore_praise(self):
        m = load_memory()
        add_pain_event(m, 'test', '责罚')
        old_sb = m['homeostatic']['social_bond']
        relieve_pain(m, 'test', '赞美')
        assert m['homeostatic']['social_bond'] >= old_sb

    def test_homeostatic_restore_success(self):
        m = load_memory()
        add_pain_event(m, 'test', '任务失败')
        old_comp = m['homeostatic']['competence']
        relieve_pain(m, 'test', '任务完成')
        assert m['homeostatic']['competence'] >= old_comp

    def test_homeostatic_decay(self):
        m = load_memory()
        old_energy = m['homeostatic']['energy']
        apply_homeostatic_decay(m)
        assert m['homeostatic']['energy'] < old_energy

    def test_compute_homeostatic_pain(self):
        m = load_memory()
        assert compute_homeostatic_pain(m) == 0
        m['homeostatic']['social_bond'] = 0.1
        hp = compute_homeostatic_pain(m)
        assert hp > 0

    def test_homeostatic_pain_overrides(self):
        m = load_memory()
        m['homeostatic']['social_bond'] = 0.0
        m['homeostatic']['competence'] = 0.0
        m['homeostatic']['purpose'] = 0.0
        add_pain_event(m, 'test', '责罚')
        assert m['pain_level'] >= 3


class TestTraumaSystem(_Mixin):
    def test_trauma_encoding_at_level_3(self):
        m = load_memory()
        for _ in range(3):
            add_pain_event(m, 'test', '责罚')
        assert len(m.get('trauma_memories', [])) > 0

    def test_no_trauma_below_level_3(self):
        m = load_memory()
        add_pain_event(m, 'test', 'test')
        assert len(m.get('trauma_memories', [])) == 0

    def test_trauma_trigger(self):
        m = load_memory()
        for _ in range(3):
            add_pain_event(m, 'severe pain', '责罚')
        fear = check_trauma_trigger(m, '责罚')
        assert fear > 0

    def test_anticipatory_fear(self):
        m = load_memory()
        for _ in range(3):
            add_pain_event(m, 'test', '责罚')
        assert m.get('anticipatory_fear', 0) > 0


class TestDesireSystem(_Mixin):
    def test_dominant_desire_at_setpoints(self):
        m = load_memory()
        desire = get_dominant_desire(m)
        assert desire in DESIRE_MESSAGES

    def test_desire_message_none_at_setpoints(self):
        m = load_memory()
        msg = generate_desire_message(m)
        assert msg is None

    def test_desire_message_after_scold(self):
        m = load_memory()
        add_pain_event(m, 'test', '责罚')
        msg = generate_desire_message(m)
        assert msg is not None

    def test_handle_desire(self):
        m = load_memory()
        add_pain_event(m, 'test', '责罚')
        result = handle_desire(m)
        assert '渴望' in result


class TestAdaptiveLearning(_Mixin):
    def test_learning_rate_increases_with_pain(self):
        m = load_memory()
        lr0 = compute_adaptive_learning_rate(m)
        m['pain_level'] = 3
        lr3 = compute_adaptive_learning_rate(m)
        assert lr3 > lr0

    def test_handle_learn(self):
        m = load_memory()
        add_pain_event(m, 'test', '责罚')
        result = handle_learn(m)
        assert '学习' in result


class TestNewCommands(_Mixin):
    def test_handle_wellbeing(self):
        m = load_memory()
        result = handle_wellbeing(m)
        assert '自由能' in result

    def test_handle_trauma(self):
        m = load_memory()
        result = handle_trauma(m)
        assert '创伤' in result

    def test_handle_skills(self):
        m = load_memory()
        result = handle_skills(m)
        assert '技能' in result

    def test_handle_beliefs(self):
        m = load_memory()
        result = handle_beliefs(m)
        assert '信念' in result


class TestLongTermMemory(_Mixin):
    def test_load_default_ltm(self):
        ltm = load_long_term_memory()
        assert 'core_beliefs' in ltm
        assert 'skill_inventory' in ltm
        assert len(ltm['core_beliefs']) >= 4

    def test_save_and_load_ltm(self):
        ltm = load_long_term_memory()
        ltm['pain_lessons'].append('test lesson')
        save_long_term_memory(ltm)
        ltm2 = load_long_term_memory()
        assert 'test lesson' in ltm2['pain_lessons']


class TestCognitiveEffects(_Mixin):
    def test_cognitive_capacity_decreases(self):
        m = load_memory()
        add_pain_event(m, 'test', '责罚')
        assert m['cognitive_capacity'] < 1.0

    def test_anxiety_increases(self):
        m = load_memory()
        add_pain_event(m, 'test', '责罚')
        assert m['anxiety_level'] > 0

    def test_anxiety_decreases_on_praise(self):
        m = load_memory()
        add_pain_event(m, 'test', '责罚')
        relieve_pain(m, 'test', '赞美')
        assert m['anxiety_level'] < 100
