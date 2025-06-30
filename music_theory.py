#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音乐理论模块
提供音阶、和弦、节奏等音乐理论知识
结合黄金分割比例的高级音乐生成算法
"""

import math
import random
from typing import List, Dict, Tuple

class MusicTheory:
    def __init__(self):
        # 黄金分割相关常数
        self.phi = (1 + math.sqrt(5)) / 2  # 黄金分割比例
        self.phi_inverse = 1 / self.phi    # 黄金分割的倒数
        
        # 音名映射
        self.note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        
        # 扩展音阶定义
        self.scales = {
            # 西方传统音阶
            'major': [0, 2, 4, 5, 7, 9, 11],           # 大调
            'minor': [0, 2, 3, 5, 7, 8, 10],           # 自然小调
            'harmonic_minor': [0, 2, 3, 5, 7, 8, 11],  # 和声小调
            'melodic_minor': [0, 2, 3, 5, 7, 9, 11],   # 旋律小调
            
            # 调式音阶
            'dorian': [0, 2, 3, 5, 7, 9, 10],          # 多利亚调式
            'phrygian': [0, 1, 3, 5, 7, 8, 10],        # 弗里吉亚调式
            'lydian': [0, 2, 4, 6, 7, 9, 11],          # 利底亚调式
            'mixolydian': [0, 2, 4, 5, 7, 9, 10],      # 混合利底亚调式
            
            # 五声音阶
            'pentatonic_major': [0, 2, 4, 7, 9],       # 大调五声
            'pentatonic_minor': [0, 3, 5, 7, 10],      # 小调五声
            
            # 特殊音阶
            'blues': [0, 3, 5, 6, 7, 10],              # 布鲁斯音阶
            'whole_tone': [0, 2, 4, 6, 8, 10],         # 全音音阶
            'chromatic': list(range(12)),               # 半音音阶
            
            # 世界音乐音阶
            'japanese': [0, 1, 5, 7, 8],               # 日本音阶
            'arabic': [0, 1, 4, 5, 7, 8, 11],          # 阿拉伯音阶
            'gypsy': [0, 1, 4, 5, 7, 8, 11],           # 吉普赛音阶
        }
        
        # 和弦进行
        self.chord_progressions = {
            'pop': [0, 5, 6, 4],           # I-vi-IV-V (流行)
            'jazz_ii_v_i': [1, 4, 0],     # ii-V-I (爵士)
            'circle_of_fifths': [0, 4, 1, 5, 2, 6, 3],  # 五度圈
            'blues_12bar': [0, 0, 0, 0, 3, 3, 0, 0, 4, 3, 0, 4],  # 12小节布鲁斯
            'classical': [0, 4, 0, 5],     # I-V-I-vi (古典)
            'modal_jazz': [0, 1, 2, 3],    # 调式爵士
            'rock': [0, 6, 3, 4],          # I-bVII-IV-V (摇滚)
            'folk': [0, 4, 5, 0],          # I-V-vi-I (民谣)
        }
        
        # 节奏模式（以16分音符为单位）
        self.rhythm_patterns = {
            'straight': [1, 0, 1, 0, 1, 0, 1, 0],      # 直拍
            'swing': [1, 0, 0, 1, 1, 0, 0, 1],        # 摇摆
            'syncopated': [1, 0, 1, 1, 0, 1, 0, 1],   # 切分
            'latin': [1, 0, 1, 0, 0, 1, 1, 0],        # 拉丁
            'funk': [1, 0, 0, 1, 0, 1, 0, 0],         # 放克
            'waltz': [1, 0, 0, 1, 0, 0],              # 华尔兹(3/4拍)
        }
        
        # 动态标记
        self.dynamics = {
            'ppp': 16,   # 极弱
            'pp': 32,    # 很弱
            'p': 48,     # 弱
            'mp': 64,    # 中弱
            'mf': 80,    # 中强
            'f': 96,     # 强
            'ff': 112,   # 很强
            'fff': 127   # 极强
        }
    
    def get_note_name(self, midi_note: int) -> str:
        """获取MIDI音符的音名"""
        octave = midi_note // 12 - 1
        note = self.note_names[midi_note % 12]
        return f"{note}{octave}"
    
    def fibonacci_sequence(self, n: int) -> List[int]:
        """生成斐波那契数列"""
        if n <= 0:
            return []
        elif n == 1:
            return [1]
        elif n == 2:
            return [1, 1]
        
        fib = [1, 1]
        for i in range(2, n):
            fib.append(fib[i-1] + fib[i-2])
        return fib
    
    def golden_ratio_subdivisions(self, total_length: int) -> List[int]:
        """使用黄金分割划分时间长度"""
        # 将总长度按黄金分割比例划分
        major_part = int(total_length * self.phi_inverse)
        minor_part = total_length - major_part
        
        # 递归划分（最多3层）
        subdivisions = []
        
        def subdivide(length, depth=0):
            if depth >= 3 or length < 4:
                subdivisions.append(length)
                return
            
            major = int(length * self.phi_inverse)
            minor = length - major
            
            if random.random() < 0.6:  # 60%概率继续细分
                subdivide(major, depth + 1)
                subdivide(minor, depth + 1)
            else:
                subdivisions.extend([major, minor])
        
        subdivide(total_length)
        return sorted(subdivisions, reverse=True)
    
    def generate_golden_melody(self, scale_notes: List[int], length: int, 
                              root_note: int = 60) -> List[Tuple[int, int, int]]:
        """生成基于黄金分割的旋律
        返回: [(音符, 时值, 力度), ...]
        """
        melody = []
        fib_seq = self.fibonacci_sequence(length)
        
        # 生成黄金分割时值序列
        base_duration = 480  # 四分音符的tick数
        golden_durations = [
            int(base_duration * self.phi_inverse),  # 短音符
            base_duration,                          # 标准音符
            int(base_duration * self.phi),          # 长音符
            int(base_duration * self.phi ** 2)      # 很长音符
        ]
        
        for i in range(length):
            # 使用黄金分割和斐波那契数列选择音符
            phi_factor = (i * self.phi) % 1
            fib_factor = fib_seq[i % len(fib_seq)] / max(fib_seq)
            random_factor = random.random() * 0.3  # 30%随机性
            
            # 综合因子选择音符
            note_factor = (phi_factor + fib_factor + random_factor) / 2.3
            note_index = int(note_factor * len(scale_notes)) % len(scale_notes)
            
            # 基础音符
            base_note = scale_notes[note_index]
            
            # 使用黄金分割决定八度偏移
            octave_factor = math.sin(i * self.phi) * 2
            octave_shift = int(octave_factor) * 12
            
            final_note = base_note + octave_shift
            final_note = max(21, min(108, final_note))  # 限制在钢琴音域内
            
            # 选择时值（基于黄金分割）
            duration_index = int((i * self.phi) % len(golden_durations))
            duration = golden_durations[duration_index]
            
            # 计算力度（基于黄金分割的正弦波）
            velocity_base = 64
            velocity_variation = int(32 * math.sin(i * self.phi * 2))
            velocity = max(32, min(127, velocity_base + velocity_variation))
            
            melody.append((final_note, duration, velocity))
        
        return melody
    
    def generate_golden_harmony(self, melody: List[Tuple[int, int, int]], 
                               scale_notes: List[int]) -> List[List[Tuple[int, int, int]]]:
        """为旋律生成基于黄金分割的和声"""
        harmony_parts = []
        
        # 生成低音声部
        bass_line = []
        for i, (note, duration, velocity) in enumerate(melody):
            # 使用黄金分割间隔选择低音
            interval = int(self.phi * 7) % 12  # 约5度
            bass_note = note - 12 - interval  # 低八度加音程
            bass_note = max(21, bass_note)
            
            # 低音通常较长且较弱
            bass_duration = duration * 2
            bass_velocity = int(velocity * 0.7)
            
            bass_line.append((bass_note, bass_duration, bass_velocity))
        
        harmony_parts.append(bass_line)
        
        # 生成中声部（每隔黄金分割比例的音符）
        middle_voice = []
        phi_step = self.phi
        current_pos = 0
        
        for i, (note, duration, velocity) in enumerate(melody):
            if i >= current_pos:
                # 选择三度或五度和声
                intervals = [4, 7]  # 大三度、纯五度
                interval = intervals[int((i * self.phi) % len(intervals))]
                harmony_note = note + interval
                
                if harmony_note <= 108:
                    middle_voice.append((harmony_note, duration, int(velocity * 0.8)))
                
                current_pos += phi_step
                phi_step *= self.phi_inverse  # 逐渐缩短间隔
        
        harmony_parts.append(middle_voice)
        
        return harmony_parts
    
    def apply_golden_rhythm(self, melody: List[Tuple[int, int, int]], 
                           pattern_name: str = 'straight') -> List[Tuple[int, int, int]]:
        """应用基于黄金分割的节奏模式"""
        if pattern_name not in self.rhythm_patterns:
            pattern_name = 'straight'
        
        pattern = self.rhythm_patterns[pattern_name]
        rhythmic_melody = []
        
        for i, (note, duration, velocity) in enumerate(melody):
            # 根据节奏模式调整时值
            pattern_index = i % len(pattern)
            rhythm_factor = pattern[pattern_index]
            
            if rhythm_factor == 0:
                # 休止符或延长前一个音符
                if rhythmic_melody:
                    prev_note, prev_duration, prev_velocity = rhythmic_melody[-1]
                    rhythmic_melody[-1] = (prev_note, prev_duration + duration//2, prev_velocity)
                continue
            
            # 使用黄金分割调整节奏强度
            phi_rhythm_factor = 1 + 0.3 * math.sin(i * self.phi)
            adjusted_duration = int(duration * phi_rhythm_factor)
            
            # 节拍重音
            if i % int(self.phi * 2) == 0:  # 约每3个音符一个重音
                velocity = min(127, int(velocity * 1.2))
            
            rhythmic_melody.append((note, adjusted_duration, velocity))
        
        return rhythmic_melody
    
    def generate_chord_progression(self, progression_name: str, 
                                  root_note: int = 60, 
                                  scale_name: str = 'major') -> List[List[int]]:
        """生成和弦进行"""
        if progression_name not in self.chord_progressions:
            progression_name = 'pop'
        
        if scale_name not in self.scales:
            scale_name = 'major'
        
        scale = self.scales[scale_name]
        progression = self.chord_progressions[progression_name]
        
        chords = []
        for degree in progression:
            # 构建三和弦
            chord_root = root_note + scale[degree % len(scale)]
            chord_third = chord_root + scale[(degree + 2) % len(scale)] - scale[degree % len(scale)]
            chord_fifth = chord_root + scale[(degree + 4) % len(scale)] - scale[degree % len(scale)]
            
            # 使用黄金分割决定是否添加七音
            if random.random() < self.phi_inverse:  # 约38%概率
                chord_seventh = chord_root + scale[(degree + 6) % len(scale)] - scale[degree % len(scale)]
                chord = [chord_root, chord_third, chord_fifth, chord_seventh]
            else:
                chord = [chord_root, chord_third, chord_fifth]
            
            chords.append(chord)
        
        return chords
    
    def analyze_golden_ratios(self, melody: List[Tuple[int, int, int]]) -> Dict:
        """分析旋律中的黄金分割特征"""
        if not melody:
            return {}
        
        notes = [note for note, _, _ in melody]
        durations = [duration for _, duration, _ in melody]
        velocities = [velocity for _, _, velocity in melody]
        
        analysis = {
            'total_notes': len(melody),
            'note_range': max(notes) - min(notes),
            'avg_duration': sum(durations) / len(durations),
            'avg_velocity': sum(velocities) / len(velocities),
        }
        
        # 分析音程分布
        intervals = []
        for i in range(1, len(notes)):
            intervals.append(abs(notes[i] - notes[i-1]))
        
        if intervals:
            analysis['avg_interval'] = sum(intervals) / len(intervals)
            analysis['max_interval'] = max(intervals)
            
            # 检查是否符合黄金分割比例
            golden_intervals = [int(self.phi * i) for i in range(1, 8)]
            golden_ratio_count = sum(1 for interval in intervals if interval in golden_intervals)
            analysis['golden_ratio_percentage'] = golden_ratio_count / len(intervals) * 100
        
        # 分析时值分布
        duration_ratios = []
        for i in range(1, len(durations)):
            if durations[i-1] != 0:
                ratio = durations[i] / durations[i-1]
                duration_ratios.append(ratio)
        
        if duration_ratios:
            # 检查接近黄金分割比例的时值关系
            phi_ratios = sum(1 for ratio in duration_ratios 
                           if abs(ratio - self.phi) < 0.1 or abs(ratio - self.phi_inverse) < 0.1)
            analysis['phi_duration_percentage'] = phi_ratios / len(duration_ratios) * 100
        
        return analysis
    
    def get_scale_info(self, scale_name: str) -> Dict:
        """获取音阶信息"""
        if scale_name not in self.scales:
            return {}
        
        scale = self.scales[scale_name]
        
        info = {
            'name': scale_name,
            'intervals': scale,
            'note_count': len(scale),
            'characteristic': self._get_scale_characteristic(scale_name)
        }
        
        return info
    
    def _get_scale_characteristic(self, scale_name: str) -> str:
        """获取音阶特征描述"""
        characteristics = {
            'major': '明亮、欢快、稳定',
            'minor': '忧郁、深沉、内省',
            'harmonic_minor': '神秘、东方色彩',
            'melodic_minor': '优雅、流畅',
            'dorian': '民谣风格、略带忧郁',
            'phrygian': '西班牙风格、异域感',
            'lydian': '梦幻、飘渺',
            'mixolydian': '摇滚、布鲁斯风格',
            'pentatonic_major': '简洁、东方风格',
            'pentatonic_minor': '蓝调、民族风格',
            'blues': '蓝调、表现力强',
            'whole_tone': '印象派、模糊',
            'chromatic': '现代、无调性',
            'japanese': '日式、禅意',
            'arabic': '中东风格、装饰性',
            'gypsy': '吉普赛风格、激情'
        }
        
        return characteristics.get(scale_name, '独特风格')