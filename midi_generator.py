#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MIDI生成器模块
提供高级MIDI文件生成功能
集成黄金分割算法和音乐理论
"""

import math
import random
import time
import os
from typing import List, Tuple, Dict, Optional
from mido import MidiFile, MidiTrack, Message, MetaMessage
from music_theory import MusicTheory

class AdvancedMidiGenerator:
    def __init__(self):
        self.music_theory = MusicTheory()
        self.phi = self.music_theory.phi
        
        # MIDI设置
        self.ticks_per_beat = 480
        self.default_tempo = 500000  # 120 BPM (微秒每拍)
        
        # 乐器分类
        self.instrument_categories = {
            'keyboard': {
                1: '大钢琴', 2: '明亮钢琴', 3: '电钢琴', 4: '酒吧钢琴',
                5: '电子钢琴1', 6: '电子钢琴2', 7: '大键琴', 8: '击弦古钢琴'
            },
            'guitar': {
                25: '尼龙吉他', 26: '钢弦吉他', 27: '爵士吉他', 28: '清音电吉他',
                29: '闷音电吉他', 30: '过载吉他', 31: '失真吉他', 32: '吉他和声'
            },
            'bass': {
                33: '原声贝斯', 34: '电贝斯(指奏)', 35: '电贝斯(拨奏)', 36: '无品贝斯',
                37: '击弦贝斯1', 38: '击弦贝斯2', 39: '合成贝斯1', 40: '合成贝斯2'
            },
            'strings': {
                49: '弦乐合奏1', 50: '弦乐合奏2', 51: '合成弦乐1', 52: '合成弦乐2',
                41: '小提琴', 42: '中提琴', 43: '大提琴', 44: '低音提琴'
            },
            'brass': {
                57: '小号', 58: '长号', 59: '大号', 60: '弱音小号',
                61: '法国号', 62: '铜管组', 63: '合成铜管1', 64: '合成铜管2'
            },
            'woodwind': {
                65: '高音萨克斯', 66: '中音萨克斯', 67: '次中音萨克斯', 68: '上低音萨克斯',
                73: '短笛', 74: '长笛', 75: '竖笛', 76: '排箫'
            },
            'synth': {
                81: '方波主音', 82: '锯齿波主音', 83: '汽笛主音', 84: '吉他主音',
                89: '温暖音色', 90: '多重合成', 91: '合唱音色', 92: '独奏音色'
            },
            'percussion': {
                128: '标准鼓组', 129: '房间鼓组', 130: '力量鼓组', 131: '电子鼓组'
            }
        }
        
        # 音乐风格模板
        self.style_templates = {
            'classical': {
                'scales': ['major', 'minor', 'harmonic_minor'],
                'progressions': ['classical', 'circle_of_fifths'],
                'tempo_range': (60, 120),
                'instruments': [1, 41, 42, 43, 73],
                'dynamics': ['p', 'mp', 'mf', 'f'],
                'rhythm': 'straight'
            },
            'jazz': {
                'scales': ['major', 'minor', 'dorian', 'mixolydian'],
                'progressions': ['jazz_ii_v_i', 'modal_jazz'],
                'tempo_range': (80, 160),
                'instruments': [1, 25, 33, 65, 57],
                'dynamics': ['mp', 'mf', 'f'],
                'rhythm': 'swing'
            },
            'blues': {
                'scales': ['blues', 'pentatonic_minor'],
                'progressions': ['blues_12bar'],
                'tempo_range': (70, 140),
                'instruments': [25, 33, 65, 57],
                'dynamics': ['mf', 'f', 'ff'],
                'rhythm': 'swing'
            },
            'pop': {
                'scales': ['major', 'minor', 'pentatonic_major'],
                'progressions': ['pop', 'folk'],
                'tempo_range': (90, 140),
                'instruments': [1, 25, 33, 81],
                'dynamics': ['mp', 'mf', 'f'],
                'rhythm': 'straight'
            },
            'ambient': {
                'scales': ['major', 'lydian', 'whole_tone'],
                'progressions': ['modal_jazz'],
                'tempo_range': (60, 90),
                'instruments': [89, 90, 49, 92],
                'dynamics': ['pp', 'p', 'mp'],
                'rhythm': 'straight'
            },
            'world': {
                'scales': ['pentatonic_major', 'japanese', 'arabic', 'gypsy'],
                'progressions': ['modal_jazz', 'folk'],
                'tempo_range': (80, 120),
                'instruments': [76, 73, 49, 33],
                'dynamics': ['p', 'mp', 'mf'],
                'rhythm': 'syncopated'
            }
        }
    
    def bpm_to_tempo(self, bpm: int) -> int:
        """将BPM转换为MIDI tempo (微秒每拍)"""
        return int(60000000 / bpm)
    
    def create_advanced_midi(self, 
                           melody_data: List[Tuple[int, int, int]],
                           harmony_data: Optional[List[List[Tuple[int, int, int]]]] = None,
                           style: str = 'classical',
                           tempo_bpm: int = 120,
                           key_signature: str = 'C',
                           time_signature: Tuple[int, int] = (4, 4)) -> MidiFile:
        """创建高级MIDI文件
        
        Args:
            melody_data: 主旋律数据 [(音符, 时值, 力度), ...]
            harmony_data: 和声数据 [[(音符, 时值, 力度), ...], ...]
            style: 音乐风格
            tempo_bpm: 速度
            key_signature: 调号 (升号数, 大小调标记)
            time_signature: 拍号 (分子, 分母)
        """
        
        mid = MidiFile(ticks_per_beat=self.ticks_per_beat)
        
        # 获取风格模板
        template = self.style_templates.get(style, self.style_templates['classical'])
        
        # 创建主旋律轨道
        melody_track = self._create_melody_track(
            melody_data, 
            template['instruments'][0], 
            tempo_bpm, 
            key_signature, 
            time_signature
        )
        mid.tracks.append(melody_track)
        
        # 创建和声轨道
        if harmony_data:
            for i, harmony_part in enumerate(harmony_data):
                if i < len(template['instruments']) - 1:
                    instrument = template['instruments'][i + 1]
                else:
                    instrument = template['instruments'][-1]
                
                harmony_track = self._create_harmony_track(
                    harmony_part, 
                    instrument, 
                    channel=i + 1
                )
                mid.tracks.append(harmony_track)
        
        # 添加鼓轨（如果风格需要）
        if style in ['jazz', 'blues', 'pop'] and len(melody_data) > 16:
            drum_track = self._create_drum_track(len(melody_data), template['rhythm'])
            mid.tracks.append(drum_track)
        
        return mid
    
    def _create_melody_track(self, 
                           melody_data: List[Tuple[int, int, int]], 
                           instrument: int, 
                           tempo_bpm: int,
                           key_signature: str,
                           time_signature: Tuple[int, int]) -> MidiTrack:
        """创建主旋律轨道"""
        track = MidiTrack()
        
        # 添加元信息
        track.append(MetaMessage('track_name', name='Melody', time=0))
        track.append(MetaMessage('set_tempo', tempo=self.bpm_to_tempo(tempo_bpm), time=0))
        track.append(MetaMessage('key_signature', key=key_signature, time=0))
        track.append(MetaMessage('time_signature', 
                               numerator=time_signature[0], 
                               denominator=time_signature[1], 
                               clocks_per_click=24, 
                               notated_32nd_notes_per_beat=8, 
                               time=0))
        
        # 设置乐器
        track.append(Message('program_change', channel=0, program=instrument-1, time=0))
        
        # 添加音符
        current_time = 0
        for note, duration, velocity in melody_data:
            # 音符开始
            track.append(Message('note_on', channel=0, note=note, velocity=velocity, time=current_time))
            # 音符结束
            track.append(Message('note_off', channel=0, note=note, velocity=0, time=duration))
            current_time = 0
        
        # 添加轨道结束标记
        track.append(MetaMessage('end_of_track', time=0))
        
        return track
    
    def _create_harmony_track(self, 
                            harmony_data: List[Tuple[int, int, int]],
                            instrument: int,
                            channel: int = 1) -> MidiTrack:
        """创建和声轨道"""
        track = MidiTrack()
        
        # 添加轨道名称
        track.append(MetaMessage('track_name', name=f'Harmony{channel}', time=0))
        
        # 设置乐器
        track.append(Message('program_change', channel=channel, program=instrument-1, time=0))
        
        # 设置音量（和声通常较轻）
        track.append(Message('control_change', channel=channel, control=7, value=80, time=0))
        
        # 添加音符
        current_time = 0
        for note, duration, velocity in harmony_data:
            # 和声音符通常较轻
            harmony_velocity = int(velocity * 0.7)
            
            track.append(Message('note_on', channel=channel, note=note, velocity=harmony_velocity, time=current_time))
            track.append(Message('note_off', channel=channel, note=note, velocity=0, time=duration))
            current_time = 0
        
        track.append(MetaMessage('end_of_track', time=0))
        return track
    
    def _create_drum_track(self, melody_length: int, rhythm_style: str = 'straight') -> MidiTrack:
        """创建鼓轨道"""
        track = MidiTrack()
        
        track.append(MetaMessage('track_name', name='Drums', time=0))
        
        # 鼓组使用通道9 (MIDI通道10)
        channel = 9
        
        # 基本鼓点映射
        drum_map = {
            'kick': 36,      # 底鼓
            'snare': 38,     # 军鼓
            'hihat': 42,     # 踩镲
            'open_hihat': 46, # 开踩镲
            'crash': 49,     # 碎音镲
            'ride': 51       # 叮叮镲
        }
        
        # 基础节拍模式
        beat_patterns = {
            'straight': [
                ('kick', 0, 100), ('hihat', 240, 60), ('snare', 480, 90), ('hihat', 720, 60)
            ],
            'swing': [
                ('kick', 0, 100), ('hihat', 160, 60), ('snare', 480, 90), ('hihat', 640, 60)
            ],
            'syncopated': [
                ('kick', 0, 100), ('hihat', 120, 60), ('snare', 360, 90), ('kick', 600, 80), ('hihat', 720, 60)
            ]
        }
        
        pattern = beat_patterns.get(rhythm_style, beat_patterns['straight'])
        
        # 生成鼓点（每4拍重复一次模式）
        beats_per_measure = 4
        ticks_per_measure = self.ticks_per_beat * beats_per_measure
        
        measures = max(1, melody_length // 8)  # 估算小节数
        
        current_time = 0
        for measure in range(measures):
            for drum, offset, velocity in pattern:
                drum_note = drum_map[drum]
                
                # 添加一些随机变化
                if random.random() < 0.1:  # 10%概率跳过
                    continue
                
                # 使用黄金分割调整力度
                phi_factor = math.sin(measure * self.phi) * 0.2 + 1
                adjusted_velocity = int(velocity * phi_factor)
                adjusted_velocity = max(30, min(127, adjusted_velocity))
                
                note_time = current_time + offset
                track.append(Message('note_on', channel=channel, note=drum_note, 
                                   velocity=adjusted_velocity, time=note_time - current_time))
                track.append(Message('note_off', channel=channel, note=drum_note, 
                                   velocity=0, time=120))  # 短促的鼓点
                
                current_time = note_time + 120
            
            # 移动到下一小节
            next_measure_time = (measure + 1) * ticks_per_measure
            if next_measure_time > current_time:
                current_time = next_measure_time
        
        track.append(MetaMessage('end_of_track', time=0))
        return track
    
    def generate_complete_composition(self, 
                                    style: str = 'classical',
                                    duration_seconds: int = 60,
                                    tempo_bpm: int = 120,
                                    scale_name: str = 'major',
                                    root_note: int = 60) -> Tuple[MidiFile, Dict]:
        """生成完整的音乐作品"""
        
        # 计算音符数量
        notes_per_second = tempo_bpm / 60 * 2  # 假设主要是八分音符
        total_notes = int(duration_seconds * notes_per_second)
        
        # 使用黄金分割划分乐曲结构
        structure_points = self.music_theory.golden_ratio_subdivisions(total_notes)
        
        # 生成主旋律
        scale_notes = [root_note + interval for interval in self.music_theory.scales[scale_name]]
        melody = self.music_theory.generate_golden_melody(scale_notes, total_notes, root_note)
        
        # 应用节奏模式
        template = self.style_templates.get(style, self.style_templates['classical'])
        melody = self.music_theory.apply_golden_rhythm(melody, template['rhythm'])
        
        # 生成和声
        harmony_parts = self.music_theory.generate_golden_harmony(melody, scale_notes)
        
        # 计算调号 (根据根音计算)
        # 将MIDI音符号映射到调号字符串
        key_map = {
            60: 'C',    # C
            61: 'C#',   # C#
            62: 'D',    # D
            63: 'Eb',   # D#/Eb
            64: 'E',    # E
            65: 'F',    # F
            66: 'F#',   # F#
            67: 'G',    # G
            68: 'Ab',   # G#/Ab
            69: 'A',    # A
            70: 'Bb',   # A#/Bb
            71: 'B'     # B
        }
        key_note = root_note % 12 + 60
        key_string = key_map.get(key_note, 'C')  # 默认C大调
        
        # 创建MIDI文件
        midi_file = self.create_advanced_midi(
            melody, 
            harmony_parts, 
            style, 
            tempo_bpm,
            key_signature=key_string  # 使用字符串格式的调号
        )
        
        # 分析信息
        analysis = self.music_theory.analyze_golden_ratios(melody)
        analysis.update({
            'style': style,
            'scale': scale_name,
            'root_note': self.music_theory.get_note_name(root_note),
            'tempo': tempo_bpm,
            'duration': duration_seconds,
            'structure_points': structure_points,
            'scale_info': self.music_theory.get_scale_info(scale_name)
        })
        
        return midi_file, analysis
    
    def save_midi_with_metadata(self, 
                               midi_file: MidiFile, 
                               analysis: Dict, 
                               filename: Optional[str] = None) -> str:
        """保存MIDI文件并生成元数据"""
        
        if filename is None:
            timestamp = int(time.time())
            style = analysis.get('style', 'unknown')
            scale = analysis.get('scale', 'unknown')
            filename = f"golden_{style}_{scale}_{timestamp}.mid"
        
        # 确保文件名以.mid结尾
        if not filename.endswith('.mid'):
            filename += '.mid'
        
        filepath = os.path.abspath(filename)
        midi_file.save(filepath)
        
        # 生成元数据文件
        metadata_file = filepath.replace('.mid', '_info.txt')
        with open(metadata_file, 'w', encoding='utf-8') as f:
            f.write("🎵 黄金分割MIDI生成器 - 作品信息\n")
            f.write("=" * 50 + "\n\n")
            
            f.write(f"文件名: {os.path.basename(filepath)}\n")
            f.write(f"生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"风格: {analysis.get('style', 'N/A')}\n")
            f.write(f"音阶: {analysis.get('scale', 'N/A')}\n")
            f.write(f"根音: {analysis.get('root_note', 'N/A')}\n")
            f.write(f"速度: {analysis.get('tempo', 'N/A')} BPM\n")
            f.write(f"时长: {analysis.get('duration', 'N/A')} 秒\n")
            f.write(f"总音符数: {analysis.get('total_notes', 'N/A')}\n")
            
            if 'scale_info' in analysis:
                scale_info = analysis['scale_info']
                f.write(f"\n音阶特征: {scale_info.get('characteristic', 'N/A')}\n")
            
            f.write(f"\n🌟 黄金分割分析:\n")
            f.write(f"音域: {analysis.get('note_range', 'N/A')} 半音\n")
            f.write(f"平均音程: {analysis.get('avg_interval', 'N/A'):.2f} 半音\n")
            f.write(f"黄金分割音程比例: {analysis.get('golden_ratio_percentage', 0):.1f}%\n")
            f.write(f"黄金分割时值比例: {analysis.get('phi_duration_percentage', 0):.1f}%\n")
            
            if 'structure_points' in analysis:
                f.write(f"\n结构划分点: {analysis['structure_points']}\n")
            
            f.write(f"\n黄金分割比例 φ = {self.phi:.10f}\n")
        
        return filepath
    
    def get_instrument_info(self, category: Optional[str] = None) -> Dict:
        """获取乐器信息"""
        if category and category in self.instrument_categories:
            return {category: self.instrument_categories[category]}
        return self.instrument_categories
    
    def get_style_info(self, style: Optional[str] = None) -> Dict:
        """获取风格信息"""
        if style and style in self.style_templates:
            return {style: self.style_templates[style]}
        return self.style_templates