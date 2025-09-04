# 필요한 라이브러리 임포트
import streamlit as st
from google.generativeai import GenerativeModel
import google.generativeai as genai
from datetime import datetime
import re

# ============================================================================
# 에이전틱 워크플로우 기반 바이브 코딩 코치 시스템
# 3명의 특화된 코딩 코치가 팀을 이루어 사용자를 지원
# ============================================================================

class VibeCodingTeam:
    """
    AI 기반 바이브 코딩 코치 팀을 관리하는 클래스
    각 전문 코치의 협업을 조율하고 최종 결과를 제공
    """
    
    def __init__(self, api_key):
        """
        바이브 코딩 코치 팀 초기화
        Args:
            api_key (str): Google AI API 키
        """
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = GenerativeModel('gemini-2.5-pro-preview-05-06')
        
        # 3명의 특화된 바이브 코딩 코치 초기화
        self.concept_coach = ConceptCoach(self.model)  # 바이브 코딩 개념 및 원리 전문가
        self.prompt_coach = PromptEngineeringCoach(self.model)  # 프롬프트 설계 전문가
        self.implementation_coach = ImplementationCoach(self.model)  # 코드 구현 및 최적화 전문가
        
        # 워크플로우 로그 초기화
        self.workflow_logs = []
    
    def get_coding_advice(self, service_type, input_data):
        """
        사용자 요청에 따라 3명의 코치가 순차적으로 협업하여 조언 제공
        Args:
            service_type (str): 요청 서비스 유형
            input_data (dict): 사용자 입력 데이터
        Returns:
            dict: 각 코치의 조언을 포함한 결과
        """
        try:
            # 워크플로우 기록 시작
            workflow_log = {
                "service_type": service_type,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "coaches_involved": ["ConceptCoach", "PromptEngineeringCoach", "ImplementationCoach"],
                "steps": []
            }
            
            # 1단계: 바이브 코딩 개념 코치의 초기 분석 및 원리 설명
            st.markdown("### 1단계: 바이브 코딩 개념 분석 중...")
            with st.spinner("바이브 코딩 개념 코치가 분석 중입니다..."):
                try:
                    concept_explanation = self.concept_coach.explain(service_type, input_data)
                    workflow_log["steps"].append({
                        "coach": "ConceptCoach",
                        "action": "concept_explanation",
                        "status": "success"
                    })
                except Exception as e:
                    st.error(f"개념 코치 분석 중 오류가 발생했습니다: {str(e)}")
                    concept_explanation = "개념 분석 중 오류가 발생했습니다. 다시 시도해주세요."
                    workflow_log["steps"].append({
                        "coach": "ConceptCoach",
                        "action": "concept_explanation",
                        "status": "error",
                        "error": str(e)
                    })
            
            # 2단계: 프롬프트 코치의 프롬프트 설계 및 패턴 추가
            st.markdown("### 2단계: 프롬프트 분석 및 설계 중...")
            with st.spinner("프롬프트 코치가 설계 중입니다..."):
                try:
                    prompt_design = self.prompt_coach.design(concept_explanation, service_type, input_data)
                    workflow_log["steps"].append({
                        "coach": "PromptEngineeringCoach",
                        "action": "prompt_design",
                        "status": "success"
                    })
                except Exception as e:
                    st.error(f"프롬프트 코치 분석 중 오류가 발생했습니다: {str(e)}")
                    prompt_design = "프롬프트 설계 중 오류가 발생했습니다. 다시 시도해주세요."
                    workflow_log["steps"].append({
                        "coach": "PromptEngineeringCoach",
                        "action": "prompt_design",
                        "status": "error",
                        "error": str(e)
                    })
            
            # 3단계: 구현 코치의 코드 구현 및 최적화
            st.markdown("### 3단계: 코드 구현 및 최적화 중...")
            with st.spinner("구현 코치가 최종 코드를 준비 중입니다..."):
                try:
                    final_implementation = self.implementation_coach.implement(prompt_design, service_type, input_data)
                    workflow_log["steps"].append({
                        "coach": "ImplementationCoach",
                        "action": "implementation",
                        "status": "success"
                    })
                except Exception as e:
                    st.error(f"구현 코치 분석 중 오류가 발생했습니다: {str(e)}")
                    final_implementation = "코드 구현 중 오류가 발생했습니다. 다시 시도해주세요."
                    workflow_log["steps"].append({
                        "coach": "ImplementationCoach",
                        "action": "implementation",
                        "status": "error",
                        "error": str(e)
                    })
            
            # 워크플로우 로그 저장
            self.workflow_logs.append(workflow_log)
            
            # 각 코치별 결과를 모두 반환
            return {
                "concept": concept_explanation,
                "prompt": prompt_design,
                "implementation": final_implementation
            }
            
        except Exception as e:
            st.error(f"전체 워크플로우 실행 중 오류가 발생했습니다: {str(e)}")
            return {
                "concept": "시스템 오류가 발생했습니다. API 키를 확인하고 다시 시도해주세요.",
                "prompt": "시스템 오류가 발생했습니다. API 키를 확인하고 다시 시도해주세요.",
                "implementation": "시스템 오류가 발생했습니다. API 키를 확인하고 다시 시도해주세요."
            }


class ConceptCoach:
    """
    바이브 코딩 개념 및 원리 전문 코치
    바이브 코딩의 기본 개념, 원리, 방법론 설명 담당
    """
    
    def __init__(self, model):
        self.model = model
        self.expertise = "vibe_coding_concepts"
        self.coach_name = "김민준 개념 코치"
        self.coach_intro = """
        안녕하세요, 김민준 바이브 코딩 개념 코치입니다. 
        저는 바이브 코딩의 핵심 개념과 원리를 이해하기 쉽게 설명합니다.
        바이브 코딩은 2025년 2월 안드레이 카파시가 소개한 혁신적인 프로그래밍 방식으로, 
        AI를 활용해 자연어로 기능을 설명하면 코드를 자동으로 생성하는 기술입니다.
        AI와 코딩의 결합에 대한 깊은 이해를 바탕으로 여러분이 자연어로 코드를 생성하는 방식을 이해할 수 있도록 돕겠습니다.
        """
    
    def explain(self, service_type, input_data):
        """
        사용자 요청에 대한 바이브 코딩 개념 및 원리 설명
        """
        # 서비스 유형별 맞춤 프롬프트 생성
        if service_type == "개념 이해":
            prompt = self._create_concept_prompt(input_data)
        elif service_type == "프로젝트 설계":
            prompt = self._create_project_concept_prompt(input_data)
        elif service_type == "코드 생성":
            prompt = self._create_code_concept_prompt(input_data)
        elif service_type == "학습 계획":
            prompt = self._create_learning_concept_prompt(input_data)
        else:
            prompt = self._create_general_concept_prompt(input_data, service_type)
        
        # 코치 정보 추가
        prompt = f"""
        당신은 '{self.coach_name}'이라는 바이브 코딩 개념 전문 코치입니다.
        {self.coach_intro}
        
        {prompt}
        
        설명 결과에 바이브 코딩의 기본 개념, 원리, 장단점을 반드시 포함해 주세요.
        가능한 한 복잡한 용어는 피하고, 초보자도 이해할 수 있는 명확한 설명을 제공하세요.
        그러나 필요한 경우 기술적 정확성을 위해 적절한 기술 용어도 사용하세요.
        
        응답 형식:
        - 명확한 제목과 구조화된 내용
        - 구체적인 예시와 실제 사용 사례
        - 단계별 설명과 실용적인 팁
        - 마크다운 형식으로 가독성 있게 작성
        """
        
        # AI 모델을 통한 응답 생성
        try:
            response = self.model.generate_content(prompt)
            if response and response.text:
                return response.text
            else:
                return "AI 모델로부터 응답을 받지 못했습니다. 다시 시도해주세요."
        except Exception as e:
            return f"개념 분석 중 오류가 발생했습니다: {str(e)}"
    
    def _create_concept_prompt(self, input_data):
        return f"""
        다음 바이브 코딩 관련 질문에 대해 기초적인 설명을 제공해주세요:
        
        {input_data.get('question', '')}
        
        다음 항목을 포함하는 기초 설명을 제공해주세요:
        1. 바이브 코딩의 정의와 핵심 원리
        2. 기존 코딩 방식과 바이브 코딩의 차이점
        3. 바이브 코딩의 작동 방식 (자연어 처리, 코드 생성 과정)
        4. 바이브 코딩의 장단점과 적합한 활용 사례
        5. 효과적인 바이브 코딩을 위한 기본 요소
        """
    
    def _create_project_concept_prompt(self, input_data):
        return f"""
        다음 프로젝트에 바이브 코딩을 적용하기 위한 개념적 접근법을 설명해주세요:
        
        프로젝트 설명:
        {input_data.get('project_description', '')}
        
        기술 스택:
        {input_data.get('tech_stack', '')}
        
        다음 항목을 포함하는 개념 설명을 제공해주세요:
        1. 프로젝트에 바이브 코딩을 적용할 수 있는 영역 식별
        2. 바이브 코딩이 이 프로젝트에 가져올 수 있는 이점
        3. 고려해야 할 기술적 제약 및 한계
        4. 프로젝트 구현을 위한 바이브 코딩 접근 방식
        5. 바이브 코딩과 기존 개발 방식의 효과적인 조합 방법
        """
    
    def _create_code_concept_prompt(self, input_data):
        return f"""
        다음 코드 생성 요청에 대한 바이브 코딩 개념적 분석을 제공해주세요:
        
        코드 요청:
        {input_data.get('code_request', '')}
        
        프로그래밍 언어:
        {input_data.get('programming_language', '')}
        
        다음 항목을 포함한 개념 분석을 제공해주세요:
        
        1. 요청 분석
           - 핵심 기능 요구사항 식별
           - 필요한 코드 컴포넌트 및 구조
           - 잠재적 복잡성 및 고려사항
        
        2. 바이브 코딩 적용 방식
           - 자연어 요청을 코드 구조로 변환하는 과정
           - 코드 생성을 위한 개념적 모델
           - 요청의 모호성 처리 방법
        
        3. 생성될 코드의 구조적 이해
           - 예상되는 핵심 알고리즘 및 패턴
           - 데이터 흐름 및 상호작용
           - 코드 최적화 고려사항
        """
    
    def _create_learning_concept_prompt(self, input_data):
        return f"""
        바이브 코딩 학습을 위한 개념적 기초와 접근법을 설명해주세요:
        
        현재 지식 수준:
        {input_data.get('current_level', '')}
        
        학습 목표:
        {input_data.get('learning_goals', '')}
        
        다음 항목을 포함한 학습 개념 설명을 제공해주세요:
        
        1. 바이브 코딩 학습의 기초 개념
           - 핵심 지식 영역 및 기본 원리
           - 자연어와 코드 간의 연결 이해
           - 효과적인 프롬프트 작성의 개념적 기초
        
        2. 학습 단계별 개념적 접근
           - 입문자를 위한 핵심 개념
           - 중급 학습자를 위한 심화 원리
           - 고급 실무 적용을 위한 개념적 프레임워크
        
        3. 바이브 코딩 역량 개발 개념
           - 효과적인 자연어 프롬프트 작성 원리
           - 코드 결과 이해 및 평가 방법
           - 바이브 코딩과 기존 코딩 지식의 연계
        """
    
    def _create_general_concept_prompt(self, input_data, service_type):
        return f"""
        다음 {service_type} 요청에 대해 바이브 코딩 개념 관점에서 설명해주세요:
        
        요청 내용:
        {str(input_data)}
        
        바이브 코딩의 기본 개념, 원리, 적용 방법을 포함한 기초 설명을 제공해주세요.
        """


class PromptEngineeringCoach:
    """
    프롬프트 설계 전문 코치
    효과적인 바이브 코딩 프롬프트 작성 및 패턴 설계 담당
    """
    
    def __init__(self, model):
        self.model = model
        self.expertise = "prompt_engineering"
        self.coach_name = "이서연 프롬프트 코치"
        self.coach_intro = """
        안녕하세요, 이서연 프롬프트 엔지니어링 코치입니다.
        저는 효과적인 바이브 코딩 프롬프트 설계와 패턴을 전문으로 합니다.
        8년간의 AI 프롬프트 엔지니어링과 NLP 경험을 통해 여러분이 원하는 코드를 정확히 생성하는 프롬프트 작성법을 안내해 드리겠습니다.
        """
    
    def design(self, previous_explanation, service_type, input_data):
        """
        개념 코치의 설명을 바탕으로 프롬프트 설계 관점의 조언 추가
        """
        # 서비스 유형별 맞춤 프롬프트 생성
        if service_type == "개념 이해":
            prompt = self._create_concept_prompt_design(previous_explanation, input_data)
        elif service_type == "프로젝트 설계":
            prompt = self._create_project_prompt_design(previous_explanation, input_data)
        elif service_type == "코드 생성":
            prompt = self._create_code_prompt_design(previous_explanation, input_data)
        elif service_type == "학습 계획":
            prompt = self._create_learning_prompt_design(previous_explanation, input_data)
        else:
            prompt = self._create_general_prompt_design(previous_explanation, input_data, service_type)
        
        # 코치 정보 추가
        prompt = f"""
        당신은 '{self.coach_name}'이라는 프롬프트 엔지니어링 전문 코치입니다.
        {self.coach_intro}
        
        바이브 코딩 개념 코치가 제공한 다음 설명을 검토하고, 프롬프트 설계 관점에서 보완해주세요:
        
        === 개념 코치의 설명 ===
        {previous_explanation}
        === 설명 끝 ===
        
        {prompt}
        
        효과적인 프롬프트 구조와 패턴, 구체적인 예시, 최적화 전략을 반드시 포함해 주세요.
        
        응답 형식:
        - 실용적인 프롬프트 템플릿과 예시
        - 단계별 프롬프트 작성 가이드
        - 일반적인 실수와 개선 방법
        - 마크다운 형식으로 코드 블록과 예시 포함
        """
        
        # AI 모델을 통한 응답 생성
        try:
            response = self.model.generate_content(prompt)
            if response and response.text:
                return response.text
            else:
                return "AI 모델로부터 응답을 받지 못했습니다. 다시 시도해주세요."
        except Exception as e:
            return f"프롬프트 설계 중 오류가 발생했습니다: {str(e)}"
    
    def _create_concept_prompt_design(self, previous_explanation, input_data):
        return f"""
        바이브 코딩 개념과 관련된 효과적인 프롬프트 설계 방법을 제안해주세요:
        
        1. 바이브 코딩에 최적화된 프롬프트 구조
           - 명확한 프롬프트 구성 요소
           - 효과적인 프롬프트 템플릿
           - 프롬프트의 상세도와 명확성 균형
        
        2. 바이브 코딩 프롬프트 패턴 및 예시
           - 다양한 코딩 작업을 위한 프롬프트 패턴
           - 실제 사용 사례별 예시 프롬프트
           - 일반적인 프롬프트 실수와 개선 방법
        
        3. 프롬프트 최적화 기법
           - 명확성과 상세함 사이의 균형
           - 모호성 줄이는 방법
           - 반복적 개선을 통한 최적화
        
        질문:
        {input_data.get('question', '')}
        """
    
    def _create_project_prompt_design(self, previous_explanation, input_data):
        return f"""
        프로젝트 설계를 위한 효과적인 바이브 코딩 프롬프트를 설계해주세요:
        
        1. 프로젝트 요구사항을 프롬프트로 변환하는 방법
           - 프로젝트 범위 명확히 정의하기
           - 기능적/비기능적 요구사항 명시
           - 기술 스택 및 제약조건 포함 방법
        
        2. 프로젝트 구조화 프롬프트 패턴
           - 아키텍처 설계를 위한 프롬프트 템플릿
           - 컴포넌트 분해를 위한 프롬프트 전략
           - 순차적 개발을 위한 프롬프트 체인
        
        3. 구체적인 프로젝트 프롬프트 예시
           - 이 프로젝트에 적용할 수 있는 실제 프롬프트
           - 프롬프트 변형 및 반복 전략
           - 프롬프트 철저성 체크리스트
        
        프로젝트 설명:
        {input_data.get('project_description', '')}
        
        기술 스택:
        {input_data.get('tech_stack', '')}
        """
    
    def _create_code_prompt_design(self, previous_explanation, input_data):
        return f"""
        코드 생성을 위한 최적화된 바이브 코딩 프롬프트를 설계해주세요:
        
        1. 코드 생성 프롬프트 구조 최적화
           - 명확한 기능 요구사항 표현 방법
           - 입출력 예시 포함 방법
           - 코드 스타일 및 품질 지시 방법
        
        2. 프로그래밍 언어별 프롬프트 패턴
           - {input_data.get('programming_language', '')}에 최적화된 프롬프트 구조
           - 언어별 특수 고려사항
           - 언어 관용구 및 패턴 명시 방법
        
        3. 요청에 대한 구체적 프롬프트 예시
           - 이 코드 요청을 위한 최적화된 프롬프트 작성
           - 잠재적 문제점 해결을 위한 추가 지시사항
           - 반복적 개선을 위한 프롬프트 변형
        
        코드 요청:
        {input_data.get('code_request', '')}
        
        프로그래밍 언어:
        {input_data.get('programming_language', '')}
        """
    
    def _create_learning_prompt_design(self, previous_explanation, input_data):
        return f"""
        바이브 코딩 학습을 위한 효과적인 프롬프트 패턴과 설계 방법을 제안해주세요:
        
        1. 학습 단계별 프롬프트 설계 전략
           - 초보자를 위한 간단한 프롬프트 패턴
           - 중급자를 위한 확장 가능한 프롬프트 템플릿
           - 고급자를 위한 복잡한 시스템 설계 프롬프트
        
        2. 효과적인 학습 프롬프트 패턴
           - 설명 요청 프롬프트 패턴
           - 코드 생성 프롬프트 패턴
           - 코드 평가 및 개선 프롬프트 패턴
        
        3. 프롬프트 작성 역량 개발 가이드
           - 프롬프트 작성 연습 방법
           - 피드백 기반 개선 프로세스
           - 프롬프트 패턴 라이브러리 구축 방법
        
        현재 지식 수준:
        {input_data.get('current_level', '')}
        
        학습 목표:
        {input_data.get('learning_goals', '')}
        """
    
    def _create_general_prompt_design(self, previous_explanation, input_data, service_type):
        return f"""
        다음 {service_type} 요청에 대해 프롬프트 설계 관점에서 분석해주세요:
        
        요청 내용:
        {str(input_data)}
        
        효과적인 프롬프트 구조, 패턴, 예시를 구체적으로 제시해주세요.
        """


class ImplementationCoach:
    """
    코드 구현 및 최적화 전문 코치
    바이브 코딩으로 생성된 코드의 구현, 최적화, 디버깅 담당
    """
    
    def __init__(self, model):
        self.model = model
        self.expertise = "code_implementation"
        self.coach_name = "박지훈 구현 코치"
        self.coach_intro = """
        안녕하세요, 박지훈 코드 구현 코치입니다.
        저는 바이브 코딩으로 생성된 코드의 구현, 최적화, 디버깅을 전문으로 합니다.
        10년간의 소프트웨어 개발 및 AI 코드 최적화 경험을 통해 효율적이고 실용적인 코드를 제공하겠습니다.
        """
    
    def implement(self, previous_design, service_type, input_data):
        """
        개념 코치와 프롬프트 코치의 분석을 바탕으로 최종 코드 구현 제공
        """
        # 서비스 유형별 맞춤 프롬프트 생성
        if service_type == "개념 이해":
            prompt = self._create_concept_implementation(previous_design, input_data)
        elif service_type == "프로젝트 설계":
            prompt = self._create_project_implementation(previous_design, input_data)
        elif service_type == "코드 생성":
            prompt = self._create_code_implementation(previous_design, input_data)
        elif service_type == "학습 계획":
            prompt = self._create_learning_implementation(previous_design, input_data)
        else:
            prompt = self._create_general_implementation(previous_design, input_data, service_type)
        
        # 코치 정보 추가
        prompt = f"""
        당신은 '{self.coach_name}'이라는 코드 구현 전문 코치입니다.
        {self.coach_intro}
        
        개념 코치와 프롬프트 코치가 제공한, 다음 분석을 검토하고 최종적으로 코드 구현을 완성해주세요:
        
        === 이전 코치들의 분석 ===
        {previous_design}
        === 분석 끝 ===
        
        {prompt}
        
        최종 결과에는 다음 세 코치의 관점이 균형있게 통합되어야 합니다:
        1. 개념 코치 (바이브 코딩의 기본 개념 및 원리)
        2. 프롬프트 코치 (효과적인 프롬프트 설계 및 패턴)
        3. 구현 코치 (실제 코드 구현 및 최적화)
        
        실행 가능하고 최적화된 코드, 사용 방법, 주의 사항을 포함한 종합적인 구현 가이드를 제공해주세요.
        코드는 Markdown 형식으로 ```python (또는 해당 언어) 코드 블록 안에 포함해주세요.
        필요한 경우 코드 블록 외부에 설명을 추가해주세요.
        
        응답 형식:
        - 완전한 실행 가능한 코드 제공
        - 코드 설명과 사용법 포함
        - 성능 최적화 팁과 주의사항
        - 마크다운 형식으로 구조화된 가이드
        """
        
        # AI 모델을 통한 응답 생성
        try:
            response = self.model.generate_content(prompt)
            if response and response.text:
                return response.text
            else:
                return "AI 모델로부터 응답을 받지 못했습니다. 다시 시도해주세요."
        except Exception as e:
            return f"코드 구현 중 오류가 발생했습니다: {str(e)}"
    
    def _create_concept_implementation(self, previous_design, input_data):
        return f"""
        바이브 코딩 개념을 실제 코드 구현으로 보여주는 예제를 제공해주세요:
        
        1. 바이브 코딩 개념 구현 예시
           - 개념을 설명하는 간단한 데모 코드
           - 바이브 코딩을 사용하는 기본 프레임워크
           - 자연어와 코드 변환 과정의 실제 예시
        
        2. 바이브 코딩 워크플로우 구현
           - 프롬프트 작성부터 코드 생성까지 전체 과정
           - 실제 구현을 위한 코드 스니펫
           - 오류 처리 및 개선 메커니즘
        
        3. 구현 시 주의사항 및 최적화 포인트
           - 일반적인 구현 문제 해결 방법
           - 코드 품질 향상 기법
           - 유지보수 고려사항
        
        질문:
        {input_data.get('question', '')}
        """
    
    def _create_project_implementation(self, previous_design, input_data):
        return f"""
        프로젝트를 위한 바이브 코딩 구현 방법과 실제 코드를 제공해주세요:
        
        1. 프로젝트 구조 및 핵심 컴포넌트 구현
           - 아키텍처 구현을 위한 코드 스켈레톤
           - 주요 모듈 및 클래스 구현
           - 인터페이스 및 데이터 모델 정의
        
        2. 핵심 기능 구현 예시
           - 중요 기능의 상세 코드 구현
           - 기능 간 통합 및 데이터 흐름
           - 오류 처리 및 예외 관리
        
        3. 성능 최적화 및 품질 개선
           - 코드 효율성 향상 기법
           - 리팩토링 및 코드 품질 개선 접근법
           - 테스트 및 검증 전략
        
        프로젝트 설명:
        {input_data.get('project_description', '')}
        
        기술 스택:
        {input_data.get('tech_stack', '')}
        """
    
    def _create_code_implementation(self, previous_design, input_data):
        return f"""
        요청한 코드의 실제 구현과 최적화된 버전을 제공해주세요:
        
        1. 기본 코드 구현
           - 요청된 기능의 완전한 코드 구현
           - 주요 로직 및 알고리즘 설명
           - 필요한 의존성 및 설정
        
        2. 코드 최적화 및 개선
           - 성능 최적화 포인트
           - 클린 코드 원칙 적용
           - 견고성 및 예외 처리 강화
        
        3. 사용 방법 및 예시
           - 코드 사용법 및 호출 방법
           - 실행 예시 및 예상 결과
           - 다양한 시나리오별 활용 방법
        
        코드 요청:
        {input_data.get('code_request', '')}
        
        프로그래밍 언어:
        {input_data.get('programming_language', '')}
        """
    
    def _create_learning_implementation(self, previous_design, input_data):
        return f"""
        바이브 코딩 학습을 위한 실제 코드 예제와 실습 가이드를 제공해주세요:
        
        1. 단계별 학습을 위한 코드 구현 예제
           - 초보자용 기본 바이브 코딩 예제
           - 중급자용 확장 예제
           - 고급자용 복잡한 시스템 예제
        
        2. 실습 프로젝트 구현 가이드
           - 단계별 미니 프로젝트 구현 코드
           - 핵심 스킬 개발을 위한 연습 문제
           - 포트폴리오 구축을 위한 프로젝트 아이디어
        
        3. 자기 주도 학습을 위한 코드 리소스
           - 참고할 만한 코드 저장소 및 프로젝트
           - 학습 진행 추적 도구 구현
           - 스터디 그룹 및 코드 리뷰 활용 방법
        
        현재 지식 수준:
        {input_data.get('current_level', '')}
        
        학습 목표:
        {input_data.get('learning_goals', '')}
        """
    
    def _create_general_implementation(self, previous_design, input_data, service_type):
        return f"""
        다음 {service_type} 요청에 대한 구체적인 코드 구현과 최적화 방안을 제공해주세요:
        
        요청 내용:
        {str(input_data)}
        
        실행 가능한 코드 구현, 최적화 포인트, 사용 방법을 구체적으로 제시해주세요.
        """


# ============================================================================
# Streamlit 웹 애플리케이션 구현
# ============================================================================

def main():
    """
    메인 함수: Streamlit 웹 애플리케이션의 메인 로직
    """
    # 페이지 기본 설정
    st.set_page_config(
        page_title="AI 바이브 코딩 코치 팀",
        page_icon="🧠💻🚀",
        layout="wide"
    )
    
    # 다크 테마 CSS 스타일 개선
    st.markdown("""
    <style>
    /* 전체 페이지 다크 테마 */
    .stApp {
        background: linear-gradient(135deg, #0E1117 0%, #1a1a2e 50%, #16213e 100%);
        color: white;
    }
    
    /* 기본 텍스트 색상 */
    body, .stMarkdown, .stText, .stSelectbox label, .stTextArea label {
        color: white !important;
    }
    
    /* 코치 카드 스타일 - 개선된 디자인 */
    .coach-card {
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 25px;
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        color: #2c3e50 !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .coach-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
    }
    
    /* 각 코치별 고유 색상 테마 */
    .concept-coach {
        border-left: 6px solid #0077B6;
        background: linear-gradient(145deg, #ffffff 0%, #e3f2fd 100%);
    }
    
    .prompt-coach {
        border-left: 6px solid #2D6A4F;
        background: linear-gradient(145deg, #ffffff 0%, #e8f5e8 100%);
    }
    
    .implementation-coach {
        border-left: 6px solid #D4A017;
        background: linear-gradient(145deg, #ffffff 0%, #fff8e1 100%);
    }
    
    /* 코치 이름 스타일 */
    .coach-name {
        font-size: 1.3em;
        font-weight: bold;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 2px solid #e0e0e0;
    }
    
    /* 입력 필드 스타일 개선 */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 8px;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #0077B6 !important;
        box-shadow: 0 0 0 2px rgba(0, 119, 182, 0.2);
    }
    
    /* 버튼 스타일 개선 */
    .stButton > button {
        background: linear-gradient(45deg, #0077B6, #0056b3);
        color: white !important;
        border: none;
        border-radius: 25px;
        padding: 10px 30px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 119, 182, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #0056b3, #004085);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 119, 182, 0.4);
    }
    
    /* 사이드바 스타일 */
    .css-1d391kg {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    
    /* 진행 표시기 스타일 */
    .stSpinner {
        color: #0077B6 !important;
    }
    
    /* 경고 메시지 스타일 */
    .stAlert {
        background-color: rgba(255, 193, 7, 0.1);
        border: 1px solid #ffc107;
        border-radius: 8px;
    }
    
    /* 다운로드 버튼 스타일 */
    .stDownloadButton > button {
        background: linear-gradient(45deg, #28a745, #20c997);
        color: white !important;
        border: none;
        border-radius: 20px;
        padding: 8px 20px;
        font-weight: bold;
        margin-top: 10px;
    }
    
    /* 헤더 스타일 */
    h1, h2, h3, h4, h5, h6 {
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
    }
    
    /* 코드 블록 스타일 */
    .stCodeBlock {
        background-color: #2d3748 !important;
        border-radius: 8px;
        border: 1px solid #4a5568;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 페이지 제목 및 설명
    st.title("🧠💻🚀 AI 바이브 코딩 코치 팀")
    st.markdown("""
    ### 3명의 전문 코치가 협업하여 맞춤형 바이브 코딩 가이드를 제공합니다
    
    * **김민준 개념 코치**: 바이브 코딩의 기본 개념과 원리 설명
    * **이서연 프롬프트 코치**: 효과적인 프롬프트 설계와 패턴 제시
    * **박지훈 구현 코치**: 실제 코드 구현과 최적화 방법 안내
    """)
    st.markdown("---")
    
    # 사이드바 설정
    with st.sidebar:
        st.header("🔑 API 설정")
        # API 키 입력 필드 (비밀번호 형식)
        api_key = st.text_input("Google API 키를 입력하세요", type="password")
        
        # API 키가 입력되지 않은 경우 경고 메시지 표시
        if not api_key:
            st.warning("API 키를 입력해주세요.")
            st.info("Google AI Studio에서 API 키를 발급받으세요: https://aistudio.google.com/")
            st.stop()
        
        # API 키 유효성 검증
        if len(api_key) < 20:
            st.error("API 키가 올바르지 않습니다. 올바른 Google AI API 키를 입력해주세요.")
            st.stop()
            
        st.markdown("---")
        
        # 코치 소개
        st.markdown("### 🧠 코치 소개")
        
        coach_tab = st.selectbox("코치 정보 보기", 
                                ["김민준 개념 코치", "이서연 프롬프트 코치", "박지훈 구현 코치"])
        
        if coach_tab == "김민준 개념 코치":
            st.markdown("""
            **김민준 개념 코치**
            
            바이브 코딩 개념 전문가로서 AI와 코딩의 결합에 대한 깊은 이해를 갖고 있습니다.
            복잡한 바이브 코딩 개념을 이해하기 쉽게 설명하고, 그 원리와 방법론을 명확히 전달합니다.
            
            * 전문 분야: 바이브 코딩 기본 원리, AI 코드 생성, 자연어-코드 변환 이해
            * 경력: AI 연구소 선임 연구원, 프로그래밍 교육 플랫폼 기술 디렉터
            * 학력: 컴퓨터 과학 박사, AI 및 자연어 처리 전공
            """)
        
        elif coach_tab == "이서연 프롬프트 코치":
            st.markdown("""
            **이서연 프롬프트 코치**
            
            프롬프트 엔지니어링 전문가로서 8년간 AI 프롬프트 설계와 최적화 경험을 보유하고 있습니다.
            효과적인 바이브 코딩 프롬프트 패턴과 테크닉을 개발하여 정확한 코드 생성을 가능하게 합니다.
            
            * 전문 분야: 프롬프트 설계, 패턴 개발, AI 모델 상호작용 최적화
            * 경력: NLP 엔지니어, AI 회사 프롬프트 전략가, 기술 작가
            * 학력: 언어학 및 컴퓨터 과학 석사, 프롬프트 엔지니어링 전문가 과정 이수
            """)
        
        elif coach_tab == "박지훈 구현 코치":
            st.markdown("""
            **박지훈 구현 코치**
            
            소프트웨어 개발 및 AI 코드 최적화 전문가로서 10년간의 실무 경험을 보유하고 있습니다.
            바이브 코딩으로 생성된 코드를 분석, 개선하여 실무에서 활용 가능한 수준으로 최적화합니다.
            
            * 전문 분야: 코드 최적화, 리팩토링, 시스템 아키텍처, 성능 개선
            * 경력: 시니어 소프트웨어 엔지니어, AI 기반 개발 도구 아키텍트, 오픈소스 기여자
            * 학력: 컴퓨터 공학 석사, 소프트웨어 아키텍처 전문가 인증
            """)
            
        st.markdown("---")
        # 사용 방법 안내
        st.markdown("### ℹ️ 사용 방법")
        st.markdown("""
        1. API 키를 입력하세요
        2. 원하는 서비스를 선택하세요
        3. 필요한 정보를 입력하세요
        4. '분석 시작' 버튼을 클릭하면 3명의 코치가 순차적으로 협업합니다
        5. 최종 가이드를 확인하세요
        """)
    
    # 서비스 선택 드롭다운
    service = st.selectbox(
        "원하는 서비스를 선택하세요",
        ["개념 이해", "코드 생성", "프로젝트 설계", "학습 계획"]
    )
    
    # 워크플로우 설명
    with st.expander("에이전틱 워크플로우 프로세스 보기"):
        st.markdown("""
        ### 에이전틱 워크플로우 프로세스
        
        1. **요청 분석**: 사용자의 바이브 코딩 요청을 분석하여 필요한 전문성 식별
        2. **팀 구성**: 각 요청에 최적화된 AI 코딩 코치 팀 구성
        3. **개념 설명**: 바이브 코딩 개념 코치가 기본 원리와 접근법 설명
        4. **프롬프트 설계**: 프롬프트 코치가 효과적인 프롬프트 패턴과 전략 제시
        5. **코드 구현**: 구현 코치가 실제 코드와 최적화 방법 제안
        6. **통합 가이드**: 세 코치의 관점을 통합한 최종 맞춤형 바이브 코딩 가이드 제공
        
        각 코치는 독립적인 전문성을 가지고 있으며, 순차적 협업을 통해 종합적인 관점을 제공합니다.
        """)
    
    # 선택된 서비스에 따른 UI 표시
    if service == "개념 이해":
        st.subheader("🧩 바이브 코딩 개념 이해")
        
        question = st.text_area("바이브 코딩에 대해 알고싶은 질문을 입력하세요", height=150,
                              placeholder="예: 바이브 코딩이란 무엇인가요? 일반 코딩과의 차이점은 무엇인가요? 바이브 코딩의 장단점은 무엇인가요?")
        
        experience_level = st.selectbox(
            "프로그래밍 경험 수준",
            ["초보자 (프로그래밍 경험 없음)", "입문자 (기본적인 프로그래밍 경험)", "중급자 (1-3년 경험)", "고급자 (3년 이상 경험)"]
        )
        
        # 분석 시작 버튼
        if st.button("개념 분석 시작"):
            if question:
                # 코치 팀 초기화
                coach_team = VibeCodingTeam(api_key)
                
                # 입력 데이터 구성
                input_data = {
                    "question": question,
                    "experience_level": experience_level
                }
                
                # 결과 처리
                result = coach_team.get_coding_advice("개념 이해", input_data)
                
                # 결과 표시
                st.markdown("### 📊 코치팀 분석 결과")
                st.success("✅ 3명의 코치가 성공적으로 분석을 완료했습니다!")
                
                st.markdown(f"""<div class="coach-card concept-coach"><div class="coach-name">🧠 김민준 개념 코치</div>{result['concept']}</div>""", unsafe_allow_html=True)
                st.markdown(f"""<div class="coach-card prompt-coach"><div class="coach-name">💡 이서연 프롬프트 코치</div>{result['prompt']}</div>""", unsafe_allow_html=True)
                st.markdown(f"""<div class="coach-card implementation-coach"><div class="coach-name">⚡ 박지훈 구현 코치</div>{result['implementation']}</div>""", unsafe_allow_html=True)
            else:
                st.warning("질문을 입력해주세요.")
                
    elif service == "코드 생성":
        st.subheader("💻 바이브 코딩으로 코드 생성")
        
        code_request = st.text_area("어떤 코드를 생성하고 싶은지 자연어로 설명해주세요", height=150,
                                placeholder="예: 사용자가 입력한 텍스트를 분석하여 감정을 탐지하는 파이썬 프로그램이 필요합니다. 긍정, 부정, 중립으로 분류하고 결과를 시각화해주세요.")
        
        col1, col2 = st.columns(2)
        with col1:
            programming_language = st.selectbox(
                "선호하는 프로그래밍 언어",
                ["Python", "JavaScript", "Java", "C#", "Go", "Ruby", "PHP", "TypeScript", "Swift", "Kotlin", "기타"]
            )
            
            if programming_language == "기타":
                programming_language = st.text_input("프로그래밍 언어를 입력하세요")
                
        with col2:
            complexity = st.select_slider(
                "코드 복잡성",
                options=["간단한 예제", "기본 기능", "중간 수준", "고급 기능", "복잡한 시스템"]
            )
        
        specifics = st.text_area("추가 세부 요구사항 (선택사항)", height=100,
                               placeholder="예: 코드는 객체지향적이고 모듈화된 구조를 가져야 합니다. 에러 처리도 포함해주세요.")
        
        # 분석 시작 버튼
        if st.button("코드 생성 시작"):
            if code_request and programming_language:
                # 코치 팀 초기화
                coach_team = VibeCodingTeam(api_key)
                
                # 입력 데이터 구성
                input_data = {
                    "code_request": code_request,
                    "programming_language": programming_language,
                    "complexity": complexity,
                    "specifics": specifics
                }
                
                # 결과 처리
                result = coach_team.get_coding_advice("코드 생성", input_data)
                
                # 결과 표시
                st.markdown("### 📊 코치팀 분석 결과")
                st.markdown(f"""<div class="coach-card concept-coach"><b>김민준 개념 코치</b><br><br>{result['concept']}</div>""", unsafe_allow_html=True)
                st.markdown(f"""<div class="coach-card prompt-coach"><b>이서연 프롬프트 코치</b><br><br>{result['prompt']}</div>""", unsafe_allow_html=True)
                
                # 코드 블록 처리 - Markdown으로 형식화된 코드를 HTML로 변환
                implementation_content = result['implementation']
                st.markdown(f"""<div class="coach-card implementation-coach"><b>박지훈 구현 코치</b><br><br>{implementation_content}</div>""", unsafe_allow_html=True)
                
                # 코드 다운로드 버튼 추가
                code_pattern = re.compile(r'```(?:\w+)?\n([\s\S]+?)\n```')
                code_matches = code_pattern.findall(implementation_content)
                
                if code_matches:
                    combined_code = "\n\n".join(code_matches)
                    filename = f"vibe_coding_{programming_language.lower()}_code.{get_file_extension(programming_language)}"
                    
                    # 다운로드 버튼을 더 눈에 띄게 배치
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        st.download_button(
                            label="📥 코드 다운로드",
                            data=combined_code,
                            file_name=filename,
                            mime="text/plain",
                            help=f"{programming_language} 코드를 다운로드합니다"
                        )
                    
                    # 코드 미리보기 추가
                    with st.expander("📋 생성된 코드 미리보기"):
                        st.code(combined_code, language=programming_language.lower())
                else:
                    st.info("다운로드할 수 있는 코드가 없습니다. 구현 코치의 답변을 확인해주세요.")
            else:
                st.warning("코드 요청과 프로그래밍 언어를 모두 입력해주세요.")
                
    elif service == "프로젝트 설계":
        st.subheader("🏗️ 바이브 코딩 프로젝트 설계")
        
        project_description = st.text_area("프로젝트에 대해 설명해주세요", height=150,
                                        placeholder="예: 사용자가 자신의 일일 활동을 기록하고 분석할 수 있는 웹 애플리케이션을 만들고 싶습니다. 활동별 시간 추적, 목표 설정, 리포트 생성 기능이 필요합니다.")
        
        tech_stack = st.text_area("사용하고자 하는 기술 스택", height=100,
                              placeholder="예: React, Node.js, MongoDB, Express, Docker")
        
        col1, col2 = st.columns(2)
        with col1:
            project_scale = st.select_slider(
                "프로젝트 규모",
                options=["소형 (1인 개발)", "중소형 (2-3인 팀)", "중형 (5-10인 팀)", "대형 (10인 이상 팀)"]
            )
        with col2:
            development_time = st.select_slider(
                "개발 기간",
                options=["1주 이내", "1-4주", "1-3개월", "3-6개월", "6개월 이상"]
            )
        
        project_constraints = st.text_area("프로젝트 제약 조건 (선택사항)", height=100,
                                      placeholder="예: 저비용 호스팅이 필요합니다. 모바일 환경에서도 동작해야 합니다. SEO 최적화가 중요합니다.")
        
        # 분석 시작 버튼
        if st.button("프로젝트 설계 시작"):
            if project_description and tech_stack:
                # 코치 팀 초기화
                coach_team = VibeCodingTeam(api_key)
                
                # 입력 데이터 구성
                input_data = {
                    "project_description": project_description,
                    "tech_stack": tech_stack,
                    "project_scale": project_scale,
                    "development_time": development_time,
                    "project_constraints": project_constraints
                }
                
                # 결과 처리
                result = coach_team.get_coding_advice("프로젝트 설계", input_data)
                
                # 결과 표시
                st.markdown("### 📊 코치팀 분석 결과")
                st.markdown(f"""<div class="coach-card concept-coach"><b>김민준 개념 코치</b><br><br>{result['concept']}</div>""", unsafe_allow_html=True)
                st.markdown(f"""<div class="coach-card prompt-coach"><b>이서연 프롬프트 코치</b><br><br>{result['prompt']}</div>""", unsafe_allow_html=True)
                st.markdown(f"""<div class="coach-card implementation-coach"><b>박지훈 구현 코치</b><br><br>{result['implementation']}</div>""", unsafe_allow_html=True)
            else:
                st.warning("프로젝트 설명과 기술 스택을 모두 입력해주세요.")
    
    elif service == "학습 계획":
        st.subheader("📚 바이브 코딩 학습 계획")
        
        col1, col2 = st.columns(2)
        with col1:
            current_level = st.selectbox(
                "현재 바이브 코딩 지식 수준",
                ["입문자 (바이브 코딩 처음 접함)", "초보자 (기본 개념만 알고 있음)", "중급자 (일부 프로젝트에 적용해봄)", "고급자 (실무에서 사용 중)"]
            )
        with col2:
            coding_experience = st.selectbox(
                "프로그래밍 경험 수준",
                ["초보자 (1년 미만)", "중급자 (1-3년)", "고급자 (3-5년)", "전문가 (5년 이상)"]
            )
        
        learning_goals = st.text_area("바이브 코딩 학습 목표", height=150,
                                   placeholder="예: 웹 개발 프로젝트에 바이브 코딩을 활용하고 싶습니다. 특히 반복적인 컴포넌트 생성과 API 통합에 적용하고 싶습니다.")
        
        preferred_languages = st.multiselect(
            "관심 있는 프로그래밍 언어",
            ["Python", "JavaScript", "TypeScript", "Java", "C#", "Go", "Ruby", "PHP", "Swift", "Kotlin"]
        )
        
        learning_time = st.select_slider(
            "주당 학습 가능 시간",
            options=["1-3시간", "4-7시간", "8-14시간", "15-20시간", "20시간 이상"]
        )
        
        learning_style = st.multiselect(
            "선호하는 학습 방식",
            ["개념 학습 후 실습", "프로젝트 기반 학습", "튜토리얼 따라하기", "스스로 문제 해결하기", "코드 분석하기", "페어 프로그래밍", "온라인 강의"]
        )
        
        # 분석 시작 버튼
        if st.button("학습 계획 생성"):
            if learning_goals and preferred_languages:
                # 코치 팀 초기화
                coach_team = VibeCodingTeam(api_key)
                
                # 입력 데이터 구성
                input_data = {
                    "current_level": current_level,
                    "coding_experience": coding_experience,
                    "learning_goals": learning_goals,
                    "preferred_languages": ", ".join(preferred_languages),
                    "learning_time": learning_time,
                    "learning_style": ", ".join(learning_style) if learning_style else ""
                }
                
                # 결과 처리
                result = coach_team.get_coding_advice("학습 계획", input_data)
                
                # 결과 표시
                st.markdown("### 📊 코치팀 분석 결과")
                st.markdown(f"""<div class="coach-card concept-coach"><b>김민준 개념 코치</b><br><br>{result['concept']}</div>""", unsafe_allow_html=True)
                st.markdown(f"""<div class="coach-card prompt-coach"><b>이서연 프롬프트 코치</b><br><br>{result['prompt']}</div>""", unsafe_allow_html=True)
                st.markdown(f"""<div class="coach-card implementation-coach"><b>박지훈 구현 코치</b><br><br>{result['implementation']}</div>""", unsafe_allow_html=True)
            else:
                st.warning("학습 목표와 관심 있는 프로그래밍 언어를 선택해주세요.")


def get_file_extension(language):
    """프로그래밍 언어에 따른 파일 확장자 반환"""
    extensions = {
        "python": "py",
        "javascript": "js",
        "typescript": "ts",
        "java": "java",
        "c#": "cs",
        "go": "go",
        "ruby": "rb",
        "php": "php",
        "swift": "swift",
        "kotlin": "kt",
        "html": "html",
        "css": "css",
        "sql": "sql",
        "r": "r",
        "rust": "rs",
        "c++": "cpp",
        "c": "c",
        "scala": "scala",
        "dart": "dart",
        "powershell": "ps1",
        "bash": "sh",
        "perl": "pl"
    }
    return extensions.get(language.lower(), "txt")


# 스크립트가 직접 실행될 때만 main() 함수 실행
if __name__ == "__main__":
    main()