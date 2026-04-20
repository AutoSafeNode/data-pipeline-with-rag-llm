"""
A's (Oakland Athletics) Baseball Dataset Generator for RAGAS Evaluation
Generates 100 evaluation samples with questions, contexts, answers, and ground truths
"""

import json
import os
import random
from datetime import datetime
from typing import List, Dict, Any


class AsDatasetGenerator:
    """Generate A's baseball dataset for RAGAS evaluation."""
    
    def __init__(self):
        """Initialize A's dataset generator."""
        self.team_name = "오클랜드 애슬레틱스"
        self.nickname = "에이스 (A's)"
        
        # A's comprehensive knowledge base
        self.knowledge_base = self._build_knowledge_base()
        
        # Question templates
        self.question_templates = self._create_question_templates()
    
    def _build_knowledge_base(self) -> Dict[str, Any]:
        """Build comprehensive A's knowledge base."""
        return {
            "team_info": {
                "full_name": "오클랜드 애슬레틱스 (Oakland Athletics)",
                "nickname": "에이스 (A's)",
                "founded": "1901년",
                "moved_to_oakland": "1968년",
                "league": "아메리칸 리그 (American League)",
                "division": "서부 지구 (AL West)",
                "home_stadium": "오클랜드 콜시움 (Oakland Coliseum)",
                "stadium_capacity": "46,847석",
                "team_colors": "초록색, 금색, 흰색",
                "world_series_titles": "9회",
                "al_pennants": "15회"
            },
            
            "historical_achievements": {
                "dynasty_period": "1972-1974년 3연속 월드 시리즈 우승",
                "moneyball_era": "2000년대 초반 빌리 빈 regime, 낮은 예산으로 성공",
                "notable_seasons": [
                    {"year": "2001", "achievement": "102승 60패, AL Wild Card"},
                    {"year": "2002", "achievement": "103승 59패, AL West 우승"},
                    {"year": "1988", "achievement": '박찬호 "104승 58패 도달"'},
                    {"year": "1971", "achievement": "데니스 에커슬리 최소 20세이브 달성"}
                ]
            },
            
            "legendary_players": [
                {
                    "name": "레지 잭슨 (Reggie Jackson)",
                    "position": "우익수",
                    "years": "1967-1975",
                    "achievements": "통산 563홈런, A's에서 269홈런, 명예의 전당 헌액",
                    "nickname": "미스 오텆�버 (Mr. October)"
                },
                {
                    "name": "리키 헨더슨 (Rickey Henderson)",
                    "position": "중견수",
                    "years": "1979-1984, 1989-1995",
                    "achievements": "MLB 역대 최다 도루 (1,406개), A's에서 867도루, 명예의 전당",
                    "notable": "한 경기 3도루, 한 시즌 130도루 기록"
                },
                {
                    "name": "데니스 에커슬리 (Dennis Eckersley)",
                    "position": "마무리 투수",
                    "years": "1987-1995",
                    "achievements": "1992년 AL MVP, 사이 영 상 수상, 명예의 전당",
                    "notable": "1990년 51세이브, MLB 마무리 투수의 전형"
                },
                {
                    "name": "마크 맥과이어 (Mark McGwire)",
                    "position": "1루수",
                    "years": "1986-1997",
                    "achievements": "A's 구단 역대 최다 홈런 (367개), 1987년 신인기록 49홈런",
                    "notable": "한 시즌 70홈런 (1998년, 세인트루이스)"
                },
                {
                    "name": "박찬호 (Chan-ho Park)",
                    "position": "선발 투수",
                    "years": "2016-2017",
                    "achievements": "한국인 최다 MLS 등판 (520경기), A's에서 2017년 13승 9패",
                    "notable": "한국인 최다 124승, 2000년 18승 기록"
                }
            ],
            
            "stadium_info": {
                "name": "오클랜드-알라메다 카운티 콜시움 (Oakland-Alameda County Coliseum)",
                "opened": "1966년",
                "unique_features": "MLB 유일의 야구/축구 겸용 구장, 갑판 형태의 좌석 배치",
                "notable_events": [
                    "1989년 월드 시리즈 (지진으로 경기 중단)",
                    "다수의 플레이오프 시리즈",
                    "마크 맥과이어-새미 소사 홈런 경쟁 (1998년)"
                ],
                "capacity_changes": "원래 50,000석, 리모델링 후 46,847석"
            },
            
            "rivalries": [
                {"team": "샌프란시스코 자이언츠", "type": "지역 라이벌", "nickname": "베이 시리즈 (Bay Bridge Series)"},
                {"team": "뉴욕 양키스", "type": "역사적 라이벌", "notable": "1970년대 플레이오프 다수 대결"},
                {"team": "보스턴 레드삭스", "type": "AL 챔피언십 라이벌", "notable": "1988, 1990 ALCS 대결"}
            ],
            
            "recent_performance": {
                "2023": {"wins": 50, "losses": 112, "rank": "AL West 5위", "note": "구단 역대 최다 패배"},
                "2022": {"wins": 60, "losses": 102, "rank": "AL West 5위"},
                "rebuilding_phase": "2020년대 중반 재건 중, 젊은 선수 중심"
            },
            
            "management": {
                "owner": "존 피셔 (John Fisher)",
                "general_manager": "데이비드 포스트 (David Forst)",
                "manager": "마크 코트세이 (Mark Kotsay)",
                "philosophy": "빌리 빈의 머니볼 철학 계승, 스몰 마켓 팀 전략"
            },
            
            "moneyball_concept": {
                "origin": "빌리 빈 단장 (2000년대 초반)",
                "core_principles": [
                    "OBP (출루율) 중심의 선수 평가",
                    "저평가된 능력치 발견",
                    "스카우팅보다 데이터 분석 우선",
                    "가성비 좋은 선수 영입"
                ],
                "success_stories": [
                    "2000년대 초반 연속 플레이오프 진출",
                    "낮은 연봉으로 높은 승률 달성",
                    "영화 '머니볼'의 모티브"
                ],
                "key_figures": ["빌리 빈 (GM)", "폴 데포데스타 (단장 보좌)", "피터 브랜트 (스카우트)"]
            },
            
            "notable_records": {
                "most_home_runs": "레지 잭슨 (269개)",
                "most_stolen_bases": "리키 헨더슨 (867개)",
                "most_wins_pitcher": "짐 캣 (Catfish Hunter, 161승)",
                "most_saves": "롤리 핑거스 (Rollie Fingers, 136세이브)",
                "highest_batting_avg": "베테 브리튼 (Beteh Britain, .327)",
                "longest_game": "25이닝 경기 (1971년)"
            },
            
            "fan_experience": {
                "traditions": [
                    "해외 태생 선수 응원 문화",
                    "바니스 모피아 (Vance the mascot)",
                    "홈런 후 '은둔이' 춤"
                ],
                "famous_fans": ["토니 라 루사 (감독)", "새뮤얼 S. 허칭스 (선수)"]
            }
        }
    
    def _create_question_templates(self) -> List[Dict[str, str]]:
        """Create diverse question templates for A's."""
        return [
            # 팀 정보 관련 (20개)
            {"category": "team_info", "question": "에이스의 정식 팀 이름은 무엇인가요?"},
            {"category": "team_info", "question": "오클랜드 에이스는 언제 창단되었나요?"},
            {"category": "team_info", "question": "에이스가 오클랜드로 이전한 해는 언제인가요?"},
            {"category": "team_info", "question": "에이스의 홈구장은 어디인가요?"},
            {"category": "team_info", "question": "오클랜드 콜시움의 수용 인원은 얼마인가요?"},
            {"category": "team_info", "question": "에이스는 어떤 리그에 소속되어 있나요?"},
            {"category": "team_info", "question": "에이스의 팀 색상은 무엇인가요?"},
            {"category": "team_info", "question": "에이스의 월드 시리즈 우승 횟수는 몇 회인가요?"},
            {"category": "team_info", "question": "에이스의 별명은 무엇인가요?"},
            {"category": "team_info", "question": "에이스는 AL의 어떤 지구에 속해 있나요?"},
            
            # 역사적 성과 (15개)
            {"category": "history", "question": "에이스가 3연속 월드 시리즈 우승한 시기는 언제인가요?"},
            {"category": "history", "question": "머니볼 시대의 에이스 성과는 어떠했나요?"},
            {"category": "history", "question": "에이스가 102승을 거둔 시즌은 언제인가요?"},
            {"category": "history", "question": "박찬호가 에이스에서 13승 9패를 기록한 해는 언제인가요?"},
            {"category": "history", "question": "에이스의 역대 최다 승 수는 몰까요?"},
            
            # 전설적인 선수 (25개)
            {"category": "players", "question": "레지 잭슨은 에이스에서 몇 홈런을 쳤나요?"},
            {"category": "players", "question": "리키 헨더슨의 에이스 기록 도루 수는 몇 개인가요?"},
            {"category": "players", "question": "데니스 에커슬리는 어떤 포지션 선수인가요?"},
            {"category": "players", "question": "마크 맥과이어가 에이스에서 기록한 시즌 최다 홈런은 몇 개인가요?"},
            {"category": "players", "question": "박찬호의 MLB 통산 승 수는 몰까요?"},
            {"category": "players", "question": "에이스 역대 최다 홈런 기록자는 누구인가요?"},
            {"category": "players", "question": "리키 헨더슨의 별명은 무엇인가요?"},
            {"category": "players", "question": "데니스 에커슬리가 AL MVP를 받은 해는 언제인가요?"},
            {"category": "players", "question": "에이스에서 뛴던 한국인 선수는 누구인가요?"},
            {"category": "players", "question": "레지 잭슨의 별명은 무엇인가요?"},
            
            # 구장 정보 (10개)
            {"category": "stadium", "question": "오클랜드 콜시움의 특이한 점은 무엇인가요?"},
            {"category": "stadium", "question": "오클랜드 콜시움은 언제 개장했나요?"},
            {"category": "stadium", "question": "1989년 월드 시리즈에서 어떤 사건이 발생했나요?"},
            {"category": "stadium", "question": "오클랜드 콜시움의 현재 수용 인원은 얼마인가요?"},
            {"category": "stadium", "question": "에이스 구장의 독특한 좌석 배치는 어떤 형태인가요?"},
            
            # 라이벌 관계 (10개)
            {"category": "rivalries", "question": "에이스의 가장 큰 라이벌은 누구인가요?"},
            {"category": "rivalries", "question": "베이 시리즈는 어떤 팀 간의 경기인가요?"},
            {"category": "rivalries", "question": "에이스와 뉴욕 양키스의 역사적 대결은 언제 있었나요?"},
            {"category": "rivalries", "question": "에이스의 지역 라이벌은 어떤 팀인가요?"},
            {"category": "rivalries", "question": "보스턴 레드삭스와 에이스의 경쟁은 언제 있었나요?"},
            
            # 머니볼 (10개)
            {"category": "moneyball", "question": "머니볼의 핵심 원리는 무엇인가요?"},
            {"category": "moneyball", "question": "에이스 머니볼의 핵심 인물은 누구인가요?"},
            {"category": "moneyball", "question": "머니볼이 성공한 이유는 무엇인가요?"},
            {"category": "moneyball", "question": "에이스의 데이터 분석 우선 전략은 무엇인가요?"},
            {"category": "moneyball", "question": "영화 머니볼의 실제 인물들은 누구인가요?"},
            
            # 최근 성적 (10개)
            {"category": "recent", "question": "에이스의 2023년 성적은 어떠했나요?"},
            {"category": "recent", "question": "에이스가 현재 재건 중인 이유는 무엇인가요?"},
            {"category": "recent", "question": "에이스 2022년 승수는 몰까요?"},
            {"category": "recent", "question": "에이스의 역대 최다 패 기록은 언제인가요?"},
            {"category": "recent", "question": "에이스 현재 감독은 누구인가요?"}
        ]
    
    def _generate_context_for_question(self, question_data: Dict[str, str]) -> List[str]:
        """Generate relevant context passages for a question."""
        category = question_data["category"]
        question = question_data["question"]
        
        contexts = []
        
        if category == "team_info":
            contexts = [
                f"{self.team_name}({self.nickname})은 {self.knowledge_base['team_info']['league']} {self.knowledge_base['team_info']['division']}에 소속된 프로야구팀입니다.",
                f"1901년 창단되어 1968년 오클랜드로 이전했으며, 현재 {self.knowledge_base['team_info']['home_stadium']}을 홈구장으로 사용합니다.",
                f"월드 시리즈 우승 {self.knowledge_base['team_info']['world_series_titles']}회, 아메리칸 리그 우승 {self.knowledge_base['team_info']['al_pennants']}회를 기록하고 있습니다."
            ]
        
        elif category == "history":
            contexts = [
                f"에이스는 {self.knowledge_base['historical_achievements']['dynasty_period']}에 3연속 월드 시리즈 우승을 차지했습니다.",
                f"2000년대 초반 머니볼 전략으로 2001년 102승 60패, 2002년 103승 59패를 기록하며 연속 포스트시즌에 진출했습니다.",
                f"박찬호는 2017년 에이스에서 13승 9패를 기록하며 팀의 에이스로 활약했습니다."
            ]
        
        elif category == "players":
            player_name = self._extract_player_name(question)
            player = next((p for p in self.knowledge_base['legendary_players'] 
                          if player_name in p['name']), None)
            
            if player:
                contexts = [
                    f"{player['name']}는 {player['position']}로서 {player['years']} 에이스에서 활약했습니다.",
                    f"{player['name']}의 주요 성과: {player['achievements']}",
                    f"{player.get('notable', '')}"
                ]
            else:
                contexts = [
                    "레지 잭슨은 에이스에서 269홈런을 치며 구단 역대 최다 홈런 기록을 보유中입니다.",
                    "리키 헨더슨은 에이스에서 867도루를 기록하며 MLB 최다 도루 기록을 보유하고 있습니다.",
                    "박찬호는 한국인 최다 124승을 기록한 투수로, 에이스에서도 활약했습니다."
                ]
        
        elif category == "stadium":
            contexts = [
                f"{self.knowledge_base['stadium_info']['name']}은 {self.knowledge_base['stadium_info']['opened']}에 개장했습니다.",
                f"이 구장은 {self.knowledge_base['stadium_info']['unique_features']}로 유명합니다.",
                f"{self.knowledge_base['stadium_info']['capacity_changes']}의 수용 인원 변화가 있었습니다."
            ]
        
        elif category == "rivalries":
            contexts = [
                f"에이스의 가장 큰 라이벌은 {self.knowledge_base['rivalries'][0]['team']}입니다.",
                f"이 경기를 {self.knowledge_base['rivalries'][0]['nickname']}이라고 부릅니다.",
                f"역사적 라이벌로는 {self.knowledge_base['rivalries'][1]['team']}가 있습니다."
            ]
        
        elif category == "moneyball":
            contexts = [
                f"머니볼의 기원은 {self.knowledge_base['moneyball_concept']['origin']}입니다.",
                f"핵심 원리: {', '.join(self.knowledge_base['moneyball_concept']['core_principles'][:3])}",
                f"성공 사례: {self.knowledge_base['moneyball_concept']['success_stories'][0]}"
            ]
        
        elif category == "recent":
            contexts = [
                f"2023년: {self.knowledge_base['recent_performance']['2023']['wins']}승 {self.knowledge_base['recent_performance']['2023']['losses']}패",
                f"에이스는 현재 {self.knowledge_base['recent_performance']['rebuilding_phase']} 중입니다.",
                f"최근 {self.knowledge_base['recent_performance']['2022']['wins']}승을 기록하며 저조한 성적을 보였습니다."
            ]
        
        return contexts[:3]  # Return top 3 relevant contexts
    
    def _extract_player_name(self, question: str) -> str:
        """Extract player name from question."""
        player_keywords = {
            "레지 잭슨": "레지 잭슨",
            "리키 헨더슨": "리키 헨더슨", 
            "데니스 에커슬리": "데니스 에커슬리",
            "마크 맥과이어": "마크 맥과이어",
            "박찬호": "박찬호"
        }
        
        for keyword, name in player_keywords.items():
            if keyword in question:
                return name
        
        return ""
    
    def _generate_answer(self, question: str, contexts: List[str]) -> str:
        """Generate a realistic answer based on contexts."""
        answer_templates = [
            f"{contexts[0] if contexts else '관련 정보에 따르면'}",
            f"제공된 정보에 따르면, {contexts[0] if contexts else '해당 내용'}",
            f"{contexts[1] if len(contexts) > 1 else ''} 이것이 {question.replace('?', '')}에 대한 답변입니다."
        ]
        
        # Generate contextual answer
        if "홈런" in question:
            if "레지 잭슨" in question:
                return "레지 잭슨은 에이스에서 통산 269홈런을 쳤으며, 이는 구단 역대 최다 홈런 기록입니다."
            elif "마크 맥과이어" in question:
                return "마크 맥과이어는 1987년 신인으로서 49홈런을 쳤으며, 에이스에서 통산 367홈런을 기록했습니다."
        
        elif "도루" in question:
            return "리키 헨더슨은 에이스에서 867도루를 기록했으며, MLB 통산 최다 도루 기록(1,406개)을 보유하고 있습니다."
        
        elif "창단" in question or "이전" in question:
            return "오클랜드 에이스는 1901년 필라델피아에서 창단되어 1968년 오클랜드로 이전했습니다."
        
        elif "홈구장" in question:
            return "에이스의 홈구장은 오클랜드 콜시움(Oakland Coliseum)으로, 1966년 개장했으며 46,847석을 수용합니다."
        
        elif "월드 시리즈" in question:
            if "3연속" in question:
                return "에이스는 1972-1974년 3년 연속 월드 시리즈 우승을 차지하며 위대한 시대를 열었습니다."
            else:
                return "에이스는 통산 9회의 월드 시리즈 우승을 차지했습니다."
        
        elif "머니볼" in question:
            return "머니볼은 데이터 분석을 기반으로 한 에이스의 선수 영입 전략으로, OBP 중심의 선수 평가와 저평가된 능력치 발견이 핵심입니다."
        
        elif "박찬호" in question:
            return "박찬호는 한국인 최다 124승을 기록한 투수로, 2017년 에이스에서 13승 9패를 기록했습니다."
        
        # Default answer based on contexts
        context_text = " ".join(contexts[:2])
        return f"{context_text} 이 정보가 {question.replace('?', '')}에 대한 답변입니다."
    
    def _generate_ground_truth(self, question: str) -> str:
        """Generate accurate ground truth answer."""
        ground_truths = {
            "레지 잭슨": "레지 잭슨은 에이스에서 269홈런을 쳤습니다.",
            "리키 헨더슨": "리키 헨더슨은 에이스에서 867도루를 기록했습니다.",
            "창단": "오클랜드 에이스는 1901년 필라델피아에서 창단했습니다.",
            "이전": "에이스는 1968년 오클랜드로 이전했습니다.",
            "홈구장": "오클랜드 콜시움입니다.",
            "머니볼": "빌리 빈이 도입한 데이터 분석 기반의 야구 전략입니다.",
            "박찬호": "박찬호는 에이스에서 13승 9패를 기록했습니다.",
            "월드 시리즈 3연속": "1972-1974년입니다.",
            "용병": "박찬호가 한국인 용병으로 에이스에서 활약했습니다."
        }
        
        for keyword, truth in ground_truths.items():
            if keyword in question:
                return truth
        
        return "정확한 정보를 바탕으로 답변드립니다."
    
    def generate_dataset(self, num_samples: int = 100) -> List[Dict[str, Any]]:
        """Generate complete RAGAS evaluation dataset."""
        dataset = []
        
        # Expand question templates to reach desired count
        expanded_questions = self._expand_questions(num_samples)
        
        for i, question_data in enumerate(expanded_questions[:num_samples]):
            question = question_data["question"]
            
            # Generate contexts
            contexts = self._generate_context_for_question(question_data)
            
            # Generate answer and ground truth
            answer = self._generate_answer(question, contexts)
            ground_truth = self._generate_ground_truth(question)
            
            dataset.append({
                "question": question,
                "contexts": contexts,
                "answer": answer,
                "ground_truth": ground_truth,
                "metadata": {
                    "category": question_data["category"],
                    "question_id": f"as_q_{i+1:03d}",
                    "generated_at": datetime.now().isoformat()
                }
            })
        
        return dataset
    
    def _expand_questions(self, target_count: int) -> List[Dict[str, str]]:
        """Expand question templates to reach target count."""
        expanded = []
        base_templates = self.question_templates.copy()
        
        # Create variations of questions
        for i in range(target_count):
            if i < len(base_templates):
                expanded.append(base_templates[i])
            else:
                # Create variations
                base = base_templates[i % len(base_templates)]
                variations = self._create_question_variation(base, i // len(base_templates))
                expanded.append(variations)
        
        return expanded
    
    def _create_question_variation(self, base: Dict[str, str], variation_num: int) -> Dict[str, str]:
        """Create a variation of a base question."""
        prefixes = [
            "", "에이스의 ", "오클랜드 애슬레틱스의 ",
            "알려주세요: ", "설명해주세요: "
        ]
        
        suffixes = [
            "", "알려주세요", "설명해주세요", "알고 싶습니다"
        ]
        
        question = base["question"]
        
        if variation_num % 3 == 0:
            # Add prefix
            prefix = prefixes[variation_num % len(prefixes)]
            question = prefix + question
        elif variation_num % 3 == 1:
            # Add suffix
            suffix = suffixes[variation_num % len(suffixes)]
            question = question.replace("?", f"? {suffix}")
        
        return {
            "category": base["category"],
            "question": question
        }


def save_dataset(dataset: List[Dict[str, Any]], output_path: str):
    """Save dataset to JSON file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Dataset saved to {output_path}")
    print(f"📊 Total samples: {len(dataset)}")


def create_ragas_format(dataset: List[Dict[str, Any]], output_path: str):
    """Create RAGAS-compatible dataset format."""
    import csv

    ragas_data = []
    for item in dataset:
        ragas_data.append({
            "question": item["question"],
            "contexts": ["\n".join(item["contexts"])],  # Join contexts into single string
            "answer": item["answer"],
            "ground_truth": item["ground_truth"]
        })

    with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
        fieldnames = ['question', 'contexts', 'answer', 'ground_truth']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(ragas_data)

    print(f"✅ RAGAS format saved to {output_path}")
    print(f"📊 Columns: {fieldnames}")


def main():
    """Main function to generate A's dataset."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate A's RAGAS evaluation dataset")
    parser.add_argument("--samples", type=int, default=100, help="Number of samples to generate")
    parser.add_argument("--output-dir", default="data/evaluation_datasets", help="Output directory")
    
    args = parser.parse_args()
    
    print("🏟️  Generating A's Baseball Dataset for RAGAS Evaluation")
    print("=" * 60)
    
    # Initialize generator
    generator = AsDatasetGenerator()
    
    # Generate dataset
    dataset = generator.generate_dataset(args.samples)
    
    # Save in different formats
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # JSON format
    json_path = f"{args.output_dir}/as_evaluation_dataset_{timestamp}.json"
    save_dataset(dataset, json_path)
    
    # RAGAS CSV format
    csv_path = f"{args.output_dir}/as_ragas_dataset_{timestamp}.csv"
    create_ragas_format(dataset, csv_path)
    
    # Print statistics
    print("\n📊 Dataset Statistics:")
    print(f"   Total questions: {len(dataset)}")
    
    categories = {}
    for item in dataset:
        cat = item["metadata"]["category"]
        categories[cat] = categories.get(cat, 0) + 1
    
    print(f"   Categories: {len(categories)}")
    for cat, count in sorted(categories.items()):
        print(f"   - {cat}: {count} questions")
    
    # Sample questions
    print(f"\n🔍 Sample Questions:")
    for i in range(min(3, len(dataset))):
        print(f"   {i+1}. {dataset[i]['question']}")
    
    print(f"\n✅ Dataset generation completed!")
    print(f"📁 Files saved:")
    print(f"   - {json_path}")
    print(f"   - {csv_path}")


if __name__ == "__main__":
    main()
