"""
ASPICE Automotive Certification Dataset Generator for RAGAS Evaluation
Generates 100 evaluation samples with questions, contexts, answers, and ground truths
"""

import json
import random
from datetime import datetime
from typing import List, Dict, Any


class ASPICEDatasetGenerator:
    """Generate ASPICE automotive certification dataset for RAGAS evaluation."""
    
    def __init__(self):
        """Initialize ASPICE dataset generator."""
        self.certification_name = "ASPICE (Automotive SPICE)"
        self.full_name = "Automotive Software Process Improvement and Capability Determination"
        
        # ASPICE comprehensive knowledge base
        self.knowledge_base = self._build_knowledge_base()
        
        # Question templates
        self.question_templates = self._create_question_templates()
    
    def _build_knowledge_base(self) -> Dict[str, Any]:
        """Build comprehensive ASPICE knowledge base."""
        return {
            "basic_info": {
                "name": "ASPICE (Automotive SPICE)",
                "full_name": "Automotive Software Process Improvement and Capability Determination",
                "based_on": "ISO/IEC 15504",
                "maintained_by": "Automotive SIG Special Interest Group",
                "version": "ASPICE 3.1 (latest)",
                "purpose": "자동차 산업 소프트웨어 프로세스 평가 및 개선",
                "target": "자동차 전자시스템 공급업체 및 제조사"
            },
            
            "capability_levels": {
                "level_0": {"name": "Incomplete (불완전)", "description": "프로세스가 목표를 달성하지 못함"},
                "level_1": {"name": "Performed (수행)", "description": "프로세스가 수행되지만 목표가 달성되지 않을 수 있음"},
                "level_2": {"name": "Managed (관리)", "description": "프로세스가 정의된 목표를 달성하고 관리됨"},
                "level_3": {"name": "Established (확립)", "description": "프로세스가 정의되고 예측 가능한 결과 달성"},
                "level_4": {"name": "Predictable (예측 가능)", "description": "프로세스가 정량적 목표를 달성하고 통제됨"},
                "level_5": {"name": "Innovating (혁신)", "description": "프로세스가 지속적으로 개선됨"}
            },
            
            "process_categories": [
                {"name": "ACQ (Acquisition)", "korean": "조달", "description": "고객 요구사항 획득 및 공급업체 선정"},
                {"name": "SWE (Software Engineering)", "korean": "소프트웨어 엔지니어링", "description": "소프트웨어 요구사항, 설계, 테스트"},
                {"name": "SYS (Systems Engineering)", "korean": "시스템 엔지니어링", "description": "시스템 요구사항, 아키텍처, 통합"},
                {"name": "HWE (Hardware Engineering)", "korean": "하드웨어 엔지니어링", "description": "하드웨어 요구사항, 설계, 테스트"},
                {"name": "SUP (Support)", "korean": "지원", "description": "품질 보증, 형상 관리, 문서화"},
                {"name": "MAN (Management)", "korean": "관리", "description": "프로젝트 관리, 리스크 관리"},
                {"name": "CLU (Cluster)", "korean": "클러스터", "description": "조직 프로세스 개선"}
            ],
            
            "key_processes": {
                "SWE.1": {"name": "Requirements Elicitation", "korean": "요구사항 수집", "level_2_desc": "명확하고 검증 가능한 요구사항 정의"},
                "SWE.2": {"name": "System Requirements Analysis", "korean": "시스템 요구사항 분석", "level_2_desc": "요구사항의 일관성과 완전성 확인"},
                "SWE.3": {"name": "System Architecture Design", "korean": "시스템 아키텍처 설계", "level_2_desc": "시스템 구조와 인터페이스 정의"},
                "SWE.4": {"name": "Requirements Allocation", "korean": "요구사항 할당", "level_2_desc": "요구사항을 하위 시스템에 할당"},
                "SWE.5": {"name": "Software Requirements Analysis", "korean": "소프트웨어 요구사항 분석", "level_2_desc": "소프트웨어 요구사항의 명확성과 추적 가능성 확보"},
                "SWE.6": {"name": "Software Design", "korean": "소프트웨어 설계", "level_2_desc": "소프트웨어 구조와 컴포넌트 설계"},
                "SWE.7": {"name": "Integration and Qualification Testing", "korean": "통합 및 적합성 테스트", "level_2_desc": "통합 테스트와 요구사항 충족 검증"},
                "SWE.8": {"name": "Maintenance", "korean": "유지보수", "level_2_desc": "시스템 변경 관리와 유지보수 절차"}
            },
            
            "assessment_model": {
                "purpose": "조직의 프로세스 능력 평가",
                "scope": "전체 또는 일부 프로세스",
                "methods": ["온사이트 평가", "문서 검토", "인터뷰", "데모"],
                "duration": "보통 3-5일",
                "assessor": "인증된 ASPICE Assessors"
            },
            
            "related_standards": {
                "ISO_26262": "자동차 기능 안전 (Functional Safety)",
                "ISO_21434": "사이버 보안 (Cybersecurity)",
                "A_SPICE": "항공우주 SPICE (다른 분야)",
                "ISO_15504": "일반 프로세스 평가 표준"
            },
            
            "certification_levels": {
                "level_1": "자동차 산업에서 기대되는 최소 수준",
                "level_2": "대부분의 OEM이 요구하는 수준",
                "level_3": "고급 공급업체 수준",
                "level_4_5": "리딩 기업 수준 (매우 드뭄)"
            },
            
            "common_issues": [
                "요구사항의 명확성 부족",
                "추적 가능성 (Traceability) 미흡",
                "테스트 커버리지 부족",
                "문서화 불충분",
                "프로세스 준수 입증 부족",
                "품질 목표 미설정",
                "리스크 관리 미흡"
            ],
            
            "assessment_preparation": {
                "step1": "프로세스 준수 증거 수집",
                "step2": "프로세스 가이드라인 작성",
                "step3": "내부 프로세스 감사",
                "step4": "개선 계획 수립",
                "step5": "ASPICE 평가 수행"
            },
            
            "global_adoption": {
                "europe": "폭스바겐, BMW, 다임러 등 필수 인증",
                "korea": "현대차, 기아 등 ASPICE 준수 의무화",
                "usa": "일부 OEM에서 자발적 도입",
                "japan": "토요타, 혼다 등 자체적으로 적용"
            },
            
            "recent_trends": {
                "agile_aspice": "애자일 방법론과 ASPICE 조화",
                "devops": "DevOps 프로세스 평가",
                "cybersecurity": "사이버 보안 프로세스 평가 추가",
                "ai_ml": "AI/ML 시스템 평가 방법 개발"
            },
            
            "benefits": {
                "quality": "제품 품질 향상",
                "risk": "리스크 감소",
                "cost": "개발 비용 절감",
                "trust": "고객 신뢰 증대",
                "efficiency": "프로세스 효율화"
            },
            
            "challenges": {
                "documentation": "방대한 문서화 요구",
                "time": "준비 기간 길음",
                "cost": "인증 비용 부담",
                "expertise": "전문가 부족",
                "complexity": "표준의 복잡성"
            }
        }
    
    def _create_question_templates(self) -> List[Dict[str, str]]:
        """Create diverse question templates for ASPICE."""
        return [
            # 기본 정보 (15개)
            {"category": "basic_info", "question": "ASPICE의 정식 명칭은 무엇인가요?"},
            {"category": "basic_info", "question": "ASPICE는 어떤 표준을 기반으로 하나요?"},
            {"category": "basic_info", "question": "ASPICE의 주관리 기관은 어디인가요?"},
            {"category": "basic_info", "question": "ASPICE의 최신 버전은 무엇인가요?"},
            {"category": "basic_info", "question": "ASPICE의 목적은 무엇인가요?"},
            {"category": "basic_info", "question": "ASPICE 평가는 누가 수행하나요?"},
            {"category": "basic_info", "question": "ASPICE 인증은 어떤 분야에 적용되나요?"},
            {"category": "basic_info", "question": "ASPICE와 ISO 26262의 차이는 무엇인가요?"},
            {"category": "basic_info", "question": "ASPICE 평가는 보통 며칠 동안 진행되나요?"},
            {"category": "basic_info", "question": "자동차 제조사들이 ASPICE를 요구하는 이유는 무엇인가요?"},
            
            # 능력 등급 (15개)
            {"category": "capability_levels", "question": "ASPICE의 능력 등급은 몇 단계로 구성되어 있나요?"},
            {"category": "capability_levels", "question": "ASPICE Level 1의 특징은 무엇인가요?"},
            {"category": "capability_levels", "question": "대부분의 OEM이 요구하는 ASPICE 등급은 몇급인가요?"},
            {"category": "capability_levels", "question": "ASPICE Level 3의 정의는 무엇인가요?"},
            {"category": "capability_levels", "question": "자동차 산업에서 기대되는 최소 등급은 몇급인가요?"},
            {"category": "capability_levels", "question": "ASPICE Level 5는 어떤 조직이 달성하나요?"},
            {"category": "capability_levels", "question": "각 능력 등급의 주요 차이점은 무엇인가요?"},
            {"category": "capability_levels", "question": "ASPICE Level 2를 달성하려면 무엇이 필요한가요?"},
            {"category": "capability_levels", "question": "ASPICE 등급별 프로세스 성숙도의 차이는 무엇인가요?"},
            
            # 프로세스 카테고리 (20개)
            {"category": "process_categories", "question": "ASPICE의 주요 프로세스 카테고리는 몇 개인가요?"},
            {"category": "process_categories", "question": "SWE 프로세스 카테고리는 어떤 것을 포함하나요?"},
            {"category": "process_categories", "question": "ACQ.1 프로세스는 무엇을 담당하나요?"},
            {"category": "process_categories", "question": "SYS 엔지니어링 카테고리의 목적은 무엇인가요?"},
            {"category": "process_categories", "question": "MAN.3 프로세스는 어떤 관리 활동을 포함하나요?"},
            {"category": "process_categories", "question": "SUP 프로세스 카테고리의 주요 활동은 무엇인가요?"},
            {"category": "process_categories", "question": "ASPICE 평가 범위에 어떤 프로세스가 포함되나요?"},
            {"category": "process_categories", "question": "HWE 엔지니어링 카테고리는 무엇을 다루나요?"},
            {"category": "process_categories", "question": "CLU 클러스터 카테고리의 역할은 무엇인가요?"},
            
            # 핵심 프로세스 (20개)
            {"category": "key_processes", "question": "SWE.1 프로세스의 목적은 무엇인가요?"},
            {"category": "key_processes", "question": "SWE.2 시스템 요구사항 분석이 중요한 이유는 무엇인가요?"},
            {"category": "key_processes", "question": "SWE.3 아키텍처 설계의 주요 산출물은 무엇인가요?"},
            {"category": "key_processes", "question": "SWE.4 요구사항 할당은 언제 수행하나요?"},
            {"category": "key_processes", "question": "SWE.5 소프트웨어 요구사항 분석의 핵심 활동은 무엇인가요?"},
            {"category": "key_processes", "question": "SWE.6 소프트웨어 설계에서 고려해야 할 사항은 무엇인가요?"},
            {"category": "key_processes", "question": "SWE.7 통합 테스트의 중요성은 무엇인가요?"},
            {"category": "key_processes", "question": "SWE.8 유지보수 프로세스는 어떤 활동을 포함하나요?"},
            {"category": "key_processes", "question": "ASPICE 프로세스 간의 인터페이스는 어떻게 관리하나요?"},
            {"category": "key_processes", "question": "SWE 프로세스의 추적 가능성 요구사항은 무엇인가요?"},
            
            # 평가 및 인증 (15개)
            {"category": "assessment", "question": "ASPICE 평가는 어떤 방법으로 수행되나요?"},
            {"category": "assessment", "question": "ASPICE 평가 절차는 어떻게 진행되나요?"},
            {"category": "assessment", "question": "ASPICE 인증을 받기 위한 준비 단계는 무엇인가요?"},
            {"category": "assessment", "question": "ASPICE Assessor가 되려면 어떤 자격이 필요한가요?"},
            {"category": "assessment", "question": "ASPICE 평가의 주요 검증 항목은 무엇인가요?"},
            {"category": "assessment", "question": "ASPICE 평가 비용은 보통 얼마정도 드나요?"},
            {"category": "assessment", "question": "ASPICE 재평가 주기는 어떻게 되나요?"},
            {"category": "assessment", "question": "ASPICE 준수 입증을 위한 증거는 무엇을 포함하나요?"},
            {"category": "assessment", "question": "ASPICE 평가의 일반적인 실패 원인은 무엇인가요?"},
            
            # 관련 표준 (10개)
            {"category": "related_standards", "question": "ASPICE와 ISO 26262의 관계는 무엇인가요?"},
            {"category": "related_standards", "question": "ISO 21434는 ASPICE와 어떻게 연관되나요?"},
            {"category": "related_standards", "question": "자동차 기능 안전과 ASPICE의 통합 방법은 무엇인가요?"},
            {"category": "related_standards", "question": "사이버 보안이 ASPICE에 추가된 이유는 무엇인가요?"},
            {"category": "related_standards", "question": "ASPICE와 A-SPICE의 차이점은 무엇인가요?"},
            
            # 글로벌 채택 (5개)
            {"category": "global_adoption", "question": "유럽 자동차 제조사들의 ASPICE 요구 현황은 어떠한가요?"},
            {"category": "global_adoption", "question": "한국 자동차 산업의 ASPICE 도입 현황은 어떠한가요?"},
            {"category": "global_adoption", "question": "미국 자동차 제조사들은 ASPICE를 어떻게 사용하나요?"},
            {"category": "global_adoption", "question": "일본 자동차 기업들의 ASPICE 활용 방식은 무엇인가요?"},
            {"category": "global_adoption", "question": "ASPICE 인증이 글로벌 자동차 산업에서 차지하는 위상은 무엇인가요?"}
        ]
    
    def _generate_context_for_question(self, question_data: Dict[str, str]) -> List[str]:
        """Generate relevant context passages for a question."""
        category = question_data["category"]
        question = question_data["question"]
        
        contexts = []
        
        if category == "basic_info":
            contexts = [
                f"{self.certification_name}({self.full_name})은 {self.knowledge_base['basic_info']['based_on']} 표준을 기반으로 합니다.",
                f"이 인증은 {self.knowledge_base['basic_info']['maintained_by']}에서 관리하며, 현재 버전은 {self.knowledge_base['basic_info']['version']}입니다.",
                f"주 목적은 {self.knowledge_base['basic_info']['purpose']}이며, {self.knowledge_base['basic_info']['target']}를 대상으로 합니다."
            ]
        
        elif category == "capability_levels":
            contexts = [
                f"ASPICE는 {len(self.knowledge_base['capability_levels'])}단계 능력 등급 체계를 가집니다.",
                f"Level 2({self.knowledge_base['capability_levels']['level_2']['name']})는 {self.knowledge_base['capability_levels']['level_2']['description']}의 프로세스 수준입니다.",
                f"대부분의 자동차 제조사들은 Level 2 또는 그 이상을 요구합니다."
            ]
        
        elif category == "process_categories":
            contexts = [
                f"ASPICE는 {len(self.knowledge_base['process_categories'])}개의 주요 프로세스 카테고리로 구성됩니다.",
                f"SWE(소프트웨어 엔지니어링), SYS(시스템 엔지니어링), ACQ(조달) 등의 카테고리가 포함됩니다.",
                f"각 프로세스 카테고리는 다수의 프로세스(Process Attribute)로 세분화됩니다."
            ]
        
        elif category == "key_processes":
            process_name = self._extract_process_name(question)
            if process_name:
                process = self.knowledge_base['key_processes'].get(process_name)
                if process:
                    contexts = [
                        f"{process_name}: {process['name']} - {process['korean']}",
                        f"Level 2 요구사항: {process.get('level_2_desc', '프로세스 정의 및 실행')}",
                        f"이 프로세스는 소프트웨어 개발 생명주기의 핵심 활동입니다."
                    ]
            else:
                contexts = [
                    "SWE.1부터 SWE.8까지의 프로세스가 소프트웨어 엔지니어링을 정의합니다.",
                    "각 프로세스는 명확한 목적, 입력, 출력, 활동, 산출물을 가집니다.",
                    "추적 가능성(Traceability)이 모든 SWE 프로세스에서 핵심 요구사항입니다."
                ]
        
        elif category == "assessment":
            contexts = [
                f"ASPICE 평가는 {', '.join(self.knowledge_base['assessment_model']['methods'])} 방법으로 수행됩니다.",
                f"평가는 보통 {self.knowledge_base['assessment_model']['duration']} 동안 진행되며, {self.knowledge_base['assessment_model']['assessor']}가 수행합니다.",
                "준비, 문서 검토, 온사이트 평가, 피드백의 단계를 거칩니다."
            ]
        
        elif category == "related_standards":
            contexts = [
                f"ISO 26262는 {self.knowledge_base['related_standards']['ISO_26262']}를 다룹니다.",
                f"ISO 21434는 {self.knowledge_base['related_standards']['ISO_21434']}을 다룹니다.",
                "이 표준들은 자동차 전자시스템의 안전과 보안을 보장하기 위해 ASPICE와 함께 적용됩니다."
            ]
        
        elif category == "global_adoption":
            contexts = [
                f"{self.knowledge_base['global_adoption']['europe']}에서 ASPICE는 필수 인증입니다.",
                f"{self.knowledge_base['global_adoption']['korea']}에서도 ASPICE 준수가 의무화되고 있습니다.",
                f"{self.knowledge_base['global_adoption']['usa']}에서는 자발적으로 도입되고 있습니다."
            ]
        
        return contexts[:3]
    
    def _extract_process_name(self, question: str) -> str:
        """Extract process name from question."""
        for process_code in self.knowledge_base['key_processes']:
            if process_code in question:
                return process_code
        
        if "SWE" in question:
            return "SWE.1"  # Default to first process
        return ""
    
    def _generate_answer(self, question: str, contexts: List[str]) -> str:
        """Generate a realistic answer based on contexts."""
        if "정식 명칭" in question or "이름" in question:
            return "ASPICE는 'Automotive Software Process Improvement and Capability Determination'의 약자로, 자동차 소프트웨어 프로세스 개선 및 능력 결정을 의미합니다."
        
        elif "기반" in question or "표준" in question:
            return "ASPICE는 ISO/IEC 15504 표준을 기반으로 하며, 자동차 산업의 특성에 맞게 커스터마이징되었습니다."
        
        elif "버전" in question:
            return "현재 ASPICE의 최신 버전은 3.1입니다."
        
        elif "Level 2" in question or "2급" in question:
            return "ASPICE Level 2(관리)는 프로세스가 정의된 목표를 달성하고 관리되는 수준으로, 대부분의 자동차 제조사들이 기본적으로 요구하는 등급입니다."
        
        elif "능력 등급" in question or "몇 단계" in question:
            return "ASPICE는 0급부터 5급까지 6개의 능력 등급으로 구성되어 있습니다. 각 등급은 프로세스 성숙도를 나타냅니다."
        
        elif "SWE" in question:
            return "SWE(소프트웨어 엔지니어링)는 소프트웨어 요구사항 수집, 설계, 개발, 테스트, 유지보수의 전체 생명주기를 다루는 ASPICE의 핵심 프로세스 카테고리입니다."
        
        elif "평가" in question or "인증" in question:
            return "ASPICE 평가는 보통 3-5일 동안 진행되며, 문서 검토, 인터뷰, 온사이트 평가 등의 방법으로 조직의 프로세스 능력을 종합적으로 평가합니다."
        
        elif "ISO 26262" in question:
            return "ISO 26262는 자동차 기능 안전(Functional Safety) 표준으로, ASPICE와 함께 적용하여 소프트웨어 프로세스의 안전성을 보장합니다."
        
        elif "준수" in question or "요구" in question:
            return "자동차 제조사들은 ASPICE Level 2 이상의 프로세스 능력을 요구하며, 이는 품질과 신뢰성을 보장하기 위함입니다."
        
        elif "한국" in question:
            return "한국 자동차 산업에서는 현대차, 기아 등 주요 제조사들이 ASPICE 인증을 의무화하고 있으며, 1, 2차 협력업체들도 준수를 요구받고 있습니다."
        
        else:
            context_text = " ".join(contexts[:2])
            return f"{context_text} 이것이 {question.replace('?', '')}에 대한 답변입니다."
    
    def _generate_ground_truth(self, question: str) -> str:
        """Generate accurate ground truth answer."""
        ground_truths = {
            "정식 명칭": "Automotive Software Process Improvement and Capability Determination",
            "기반": "ISO/IEC 15504",
            "버전": "ASPICE 3.1",
            "능력 등급": "0급부터 5급까지 6단계",
            "Level 2": "관리(Managed) - 대부분 OEM이 요구하는 수준",
            "SWE": "소프트웨어 엔지니어링",
            "평가 기간": "보통 3-5일",
            "ISO 26262": "자동차 기능 안전 표준",
            "한국": "현대차, 기아 등이 ASPICE 준수 의무화"
        }
        
        for keyword, truth in ground_truths.items():
            if keyword in question:
                return truth
        
        return "ASPICE 프로세스 평가 및 개선에 관한 정확한 정보입니다."
    
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
                    "question_id": f"aspice_q_{i+1:03d}",
                    "generated_at": datetime.now().isoformat()
                }
            })
        
        return dataset
    
    def _expand_questions(self, target_count: int) -> List[Dict[str, str]]:
        """Expand question templates to reach target count."""
        expanded = []
        base_templates = self.question_templates.copy()
        
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
            "", "ASPICE의 ", "자동차 산업에서의 ",
            "소프트웨어 개발에서의 "
        ]
        
        suffixes = [
            "", "알려주세요", "설명해주세요", "정의해주세요"
        ]
        
        question = base["question"]
        
        if variation_num % 3 == 0:
            prefix = prefixes[variation_num % len(prefixes)]
            question = prefix + question
        elif variation_num % 3 == 1:
            suffix = suffixes[variation_num % len(suffixes)]
            question = question.replace("?", f"? {suffix}")
        
        return {
            "category": base["category"],
            "question": question
        }


def save_dataset(dataset: List[Dict[str, Any]], output_path: str):
    """Save dataset to JSON file."""
    import os
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
            "contexts": ["\n".join(item["contexts"])],
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
    """Main function to generate ASPICE dataset."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate ASPICE RAGAS evaluation dataset")
    parser.add_argument("--samples", type=int, default=100, help="Number of samples to generate")
    parser.add_argument("--output-dir", default="data/evaluation_datasets", help="Output directory")
    
    args = parser.parse_args()
    
    print("🚗 Generating ASPICE Automotive Certification Dataset for RAGAS Evaluation")
    print("=" * 60)
    
    # Initialize generator
    generator = ASPICEDatasetGenerator()
    
    # Generate dataset
    dataset = generator.generate_dataset(args.samples)
    
    # Save in different formats
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # JSON format
    json_path = f"{args.output_dir}/aspice_evaluation_dataset_{timestamp}.json"
    save_dataset(dataset, json_path)
    
    # RAGAS CSV format
    csv_path = f"{args.output_dir}/aspice_ragas_dataset_{timestamp}.csv"
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
