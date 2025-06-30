#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基于黄金分割曲线的随机MIDI生成器
作者: AI Assistant
功能: 利用黄金分割比例和乐理知识生成随机MIDI音乐
"""

import random
import math
import time
import os
from typing import Dict, List, Optional
from music_theory import MusicTheory
from midi_generator import AdvancedMidiGenerator

class GoldenRatioMidiGenerator:
    def __init__(self):
        # 初始化音乐理论和MIDI生成器
        self.music_theory = MusicTheory()
        self.midi_gen = AdvancedMidiGenerator()
        
        # 黄金分割比例
        self.golden_ratio = self.music_theory.phi
        self.phi = self.golden_ratio
        
        # MIDI参数
        self.tempo = 120  # BPM
        self.duration = 60  # 秒
        self.instrument = 1  # 钢琴
        self.instrument_name = "钢琴"  # 乐器名称
        self.style = 'classical'  # 音乐风格
        self.scale = 'major'  # 音阶
        self.root_note = 60  # 根音 (C4)
        
        # 获取可用的乐器、风格和音阶
        self.instruments = self._get_available_instruments()
        self.styles = list(self.midi_gen.style_templates.keys()) if hasattr(self.midi_gen, 'style_templates') else ['classical', 'jazz', 'blues']
        self.scales = list(self.music_theory.scales.keys()) if hasattr(self.music_theory, 'scales') else ['major', 'minor', 'pentatonic_major']
    
    def _get_available_instruments(self) -> Dict[int, str]:
        """获取可用乐器列表"""
        instruments = {}
        for category, category_instruments in self.midi_gen.instrument_categories.items():
            instruments.update(category_instruments)
        return instruments
    
    def show_menu(self):
        """显示主菜单"""
        print("\n" + "="*50)
        print("🎵 黄金分割MIDI生成器 - 主菜单")
        print("="*50)
        print(f"当前设置:")
        print(f"  乐器: {self.instrument_name} (通道 {self.instrument})")
        print(f"  音乐风格: {self.style}")
        print(f"  音阶: {self.scale} ({self.root_note})")
        print(f"  速度: {self.tempo} BPM")
        print(f"  时长: {self.duration} 秒")
        print("\n选项:")
        print("1. 选择乐器")
        print("2. 选择音乐风格")
        print("3. 选择音阶")
        print("4. 设置根音")
        print("5. 设置速度 (BPM)")
        print("6. 设置时长")
        print("7. 🎵 生成音乐")
        print("8. 📚 黄金分割原理")
        print("9. 📖 音阶信息")
        print("10. 🎼 风格信息")
        print("0. 退出")
        print("="*50)
    
    def select_instrument(self):
        """选择乐器"""
        print("\n🎹 可用乐器分类:")
        categories = self.midi_gen.instrument_categories
        
        # 显示分类
        for i, (category, instruments) in enumerate(categories.items(), 1):
            print(f"{i}. {category.upper()} ({len(instruments)}种乐器)")
        
        try:
            cat_choice = int(input("\n请选择乐器分类 (1-{}): ".format(len(categories))))
            category_list = list(categories.keys())
            
            if 1 <= cat_choice <= len(category_list):
                selected_category = category_list[cat_choice - 1]
                instruments = categories[selected_category]
                
                print(f"\n{selected_category.upper()} 乐器:")
                for num, name in instruments.items():
                    print(f"{num}: {name}")
                
                choice = int(input("\n请选择乐器编号: "))
                if choice in instruments:
                    self.instrument = choice
                    print(f"已选择: {instruments[choice]}")
                else:
                    print("无效的乐器编号!")
            else:
                print("无效的分类选择!")
        except ValueError:
            print("请输入有效的数字!")
    
    def set_tempo(self):
        """设置速度"""
        try:
            tempo = int(input(f"请输入速度 (当前: {self.tempo} BPM, 建议范围: 60-200): "))
            if 30 <= tempo <= 300:
                self.tempo = tempo
                print(f"速度已设置为: {tempo} BPM")
            else:
                print("速度范围应在30-300之间!")
        except ValueError:
            print("请输入有效的数字!")
    
    def set_duration(self):
        """设置时长"""
        try:
            duration = int(input(f"请输入时长 (当前: {self.duration} 秒, 建议范围: 10-300): "))
            if 5 <= duration <= 600:
                self.duration = duration
                print(f"时长已设置为: {duration} 秒")
            else:
                print("时长范围应在5-600秒之间!")
        except ValueError:
            print("请输入有效的数字!")
    
    def select_style(self):
        """选择音乐风格"""
        print("\n🎼 选择音乐风格:")
        styles = list(self.midi_gen.style_templates.keys())
        
        for i, style in enumerate(styles, 1):
            template = self.midi_gen.style_templates[style]
            print(f"{i}. {style} - {template.get('description', '经典风格')}")
        
        try:
            choice = int(input(f"\n请选择风格 (1-{len(styles)}): "))
            if 1 <= choice <= len(styles):
                self.style = styles[choice - 1]
                print(f"✅ 已选择风格: {self.style}")
            else:
                print("❌ 无效选择!")
        except ValueError:
            print("❌ 请输入有效数字!")
    
    def select_scale(self):
        """选择音阶"""
        print("\n🎼 选择音阶类型:")
        scale_categories = {
            "传统音阶": ["major", "minor", "harmonic_minor", "melodic_minor"],
            "调式音阶": ["dorian", "phrygian", "lydian", "mixolydian", "aeolian", "locrian"],
            "五声音阶": ["pentatonic_major", "pentatonic_minor", "blues"],
            "特殊音阶": ["whole_tone", "diminished", "chromatic"],
            "世界音乐": ["arabic", "japanese", "indian_raga"]
        }
        
        print("\n音阶类别:")
        categories = list(scale_categories.keys())
        for i, category in enumerate(categories, 1):
            print(f"{i}. {category}")
        
        try:
            cat_choice = int(input(f"\n请选择类别 (1-{len(categories)}): "))
            if 1 <= cat_choice <= len(categories):
                selected_category = categories[cat_choice - 1]
                scales = scale_categories[selected_category]
                
                print(f"\n{selected_category}:")
                for i, scale in enumerate(scales, 1):
                    print(f"{i}. {scale}")
                
                scale_choice = int(input(f"\n请选择音阶 (1-{len(scales)}): "))
                if 1 <= scale_choice <= len(scales):
                    self.scale = scales[scale_choice - 1]
                    print(f"✅ 已选择音阶: {self.scale}")
                else:
                    print("❌ 无效选择!")
            else:
                print("❌ 无效选择!")
        except ValueError:
            print("❌ 请输入有效数字!")
    
    def set_root_note(self):
        """设置根音"""
        print("\n🎵 选择根音:")
        notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        
        for i, note in enumerate(notes, 1):
            print(f"{i:2d}. {note}")
        
        try:
            choice = int(input(f"\n请选择根音 (1-{len(notes)}): "))
            if 1 <= choice <= len(notes):
                # 计算MIDI音符号 (C4 = 60)
                self.root_note = 60 + (choice - 1)
                print(f"✅ 已设置根音: {notes[choice - 1]}")
            else:
                print("❌ 无效选择!")
        except ValueError:
            print("❌ 请输入有效数字!")
    
    def show_golden_ratio_info(self):
        """显示黄金分割原理"""
        print("\n📚 黄金分割原理")
        print("="*50)
        print("\n🌟 什么是黄金分割?")
        print(f"黄金分割比例 φ (phi) = {self.golden_ratio:.6f}")
        print("这是一个神奇的数学常数，在自然界和艺术中广泛存在。")
        
        print("\n🎼 黄金分割在音乐中的应用:")
        print("• 音符时值比例 - 使用φ控制音符长短关系")
        print("• 音程间隔 - 基于φ计算和谐的音程")
        print("• 旋律起伏 - φ周期控制音高变化")
        print("• 力度变化 - 正弦函数结合φ控制强弱")
        print("• 结构布局 - 斐波那契数列影响音符选择")
        
        print("\n📐 斐波那契数列与黄金分割:")
        fib = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
        print(f"数列: {fib}")
        print("相邻两项的比值逐渐趋向于黄金分割比例")
        
        print("\n🎯 本程序的黄金分割特色:")
        print("• 智能音程选择")
        print("• 自然的节奏变化")
        print("• 和谐的音乐结构")
        print("• 数学美学与音乐艺术的完美结合")
    
    def show_scale_info(self):
        """显示音阶信息"""
        print("\n📖 音阶理论知识")
        print("="*50)
        print("\n🎼 什么是音阶?")
        print("音阶是按照一定音程关系排列的音的序列，是音乐的基础。")
        print("不同的音阶具有不同的情感色彩和文化特征。")
        
        print("\n🌟 主要音阶类型:")
        print("\n• 大调音阶 (Major): 明亮、欢快的感觉")
        print("  音程模式: 全-全-半-全-全-全-半")
        print("\n• 小调音阶 (Minor): 忧郁、深沉的感觉")
        print("  音程模式: 全-半-全-全-半-全-全")
        
        print("\n• 调式音阶: 古典音乐中的七种调式")
        print("  - Dorian: 略带忧郁但不失希望")
        print("  - Phrygian: 神秘、异域风情")
        print("  - Lydian: 梦幻、飘渺")
        print("  - Mixolydian: 民谣、乡村风格")
        
        print("\n• 五声音阶: 东方音乐的特色")
        print("  - 大调五声: C-D-E-G-A (去掉4、7度)")
        print("  - 小调五声: A-C-D-E-G")
        print("  - 布鲁斯音阶: 加入蓝调音符")
        
        print("\n🌍 世界音乐音阶:")
        print("• 阿拉伯音阶: 四分音特色")
        print("• 日本音阶: 传统和风")
        print("• 印度拉格: 复杂的微分音")
        
        print("\n🎯 黄金分割在音阶中的应用:")
        print("• 音程比例接近黄金分割比")
        print("• 和谐音程的数学基础")
        print("• 旋律发展的自然规律")
    
    def show_style_info(self):
        """显示音乐风格信息"""
        print("\n🎼 音乐风格指南")
        print("="*50)
        
        for style_name, template in self.midi_gen.style_templates.items():
            print(f"\n🎵 {style_name.upper()}")
            print("-" * 30)
            print(f"描述: {template.get('description', '经典音乐风格')}")
            print(f"推荐音阶: {', '.join(template.get('scales', ['major']))}")
            print(f"常用和弦: {', '.join(template.get('chord_progressions', [['I', 'V', 'vi', 'IV']])[0])}")
            print(f"节奏特点: {template.get('rhythm_pattern', 'standard')}")
            print(f"速度范围: {template.get('tempo_range', [120, 140])[0]}-{template.get('tempo_range', [120, 140])[1]} BPM")
        
        print("\n🌟 风格选择建议:")
        print("• Classical: 适合学习和谐理论")
        print("• Jazz: 复杂和声，即兴特色")
        print("• Blues: 情感表达，简单有力")
        print("• Pop: 流行易懂，朗朗上口")
        print("• Ambient: 氛围音乐，放松冥想")
        print("• Electronic: 现代感，节奏强烈")
    
    def generate_music(self):
        """生成音乐"""
        print("\n🎵 正在生成基于黄金分割的MIDI音乐...")
        print(f"风格: {self.style}")
        print(f"音阶: {self.scale}")
        print(f"根音: {self.root_note}")
        print(f"速度: {self.tempo} BPM")
        print(f"时长: {self.duration} 秒")
        
        try:
            # 使用高级生成器创建完整作品
            midi_file, analysis = self.midi_gen.generate_complete_composition(
                style=self.style,
                duration_seconds=self.duration,
                tempo_bpm=self.tempo,
                scale_name=self.scale,
                root_note=self.root_note
            )
            
            # 保存文件
            filepath = self.midi_gen.save_midi_with_metadata(midi_file, analysis)
            
            print(f"\n✅ MIDI文件已生成!")
            print(f"📁 文件位置: {filepath}")
            print(f"📄 信息文件: {filepath.replace('.mid', '_info.txt')}")
            print(f"🎼 音符数量: {analysis.get('total_notes', 'N/A')}")
            print(f"🎯 黄金分割音程比例: {analysis.get('golden_ratio_percentage', 0):.1f}%")
            print(f"⏱️  黄金分割时值比例: {analysis.get('phi_duration_percentage', 0):.1f}%")
            
            return filepath
            
        except Exception as e:
            print(f"❌ 生成音乐时发生错误: {e}")
            return None
    
    def run(self):
        """运行主程序"""
        print("\n" + "="*60)
        print("🎵 欢迎使用黄金分割MIDI生成器 (高级版) 🎵")
        print("="*60)
        print("这个程序将使用黄金分割比例和乐理知识生成独特的音乐。")
        print("\n✨ 新功能:")
        print("• 多种音乐风格模板 (古典、爵士、布鲁斯、流行等)")
        print("• 丰富的音阶选择 (传统、调式、世界音乐)")
        print("• 智能和声生成")
        print("• 自动鼓轨添加")
        print("• 详细的黄金分割分析")
        print("• 完整的元数据导出")
        
        while True:
            self.show_menu()
            
            try:
                choice = input("请选择操作 (0-10): ").strip()
                
                if choice == '0':
                    print("\n🎵 感谢使用黄金分割MIDI生成器!")
                    print("愿音乐与数学的和谐伴随您! 再见! ✨")
                    break
                elif choice == '1':
                    self.select_instrument()
                elif choice == '2':
                    self.select_style()
                elif choice == '3':
                    self.select_scale()
                elif choice == '4':
                    self.set_root_note()
                elif choice == '5':
                    self.set_tempo()
                elif choice == '6':
                    self.set_duration()
                elif choice == '7':
                    self.generate_music()
                elif choice == '8':
                    self.show_golden_ratio_info()
                elif choice == '9':
                    self.show_scale_info()
                elif choice == '10':
                    self.show_style_info()
                else:
                    print("❌ 无效选择，请重试!")
                    
                input("\n按回车键继续...")
                
            except KeyboardInterrupt:
                print("\n\n程序被用户中断。再见! 🎵")
                break
            except Exception as e:
                print(f"❌ 发生错误: {e}")
                print("请检查依赖包是否正确安装: pip install -r requirements.txt")
                input("按回车键继续...")

if __name__ == "__main__":
    generator = GoldenRatioMidiGenerator()
    generator.run()