 # Local LLM API Server Development Log

## 2025-08-21 - Phase 1 완료: OpenAI 호환 API 서버 구축

### ✅ 완성된 기능들

#### 핵심 아키텍처
- **FastAPI 기반 REST API 서버** 구축
- **OpenAI Chat Completions API 완전 호환**
- **MLX-LM 백엔드** 연동으로 Apple Silicon 최적화
- **Pydantic 데이터 모델** 기반 타입 안전성

#### API 엔드포인트
```
GET  /                      - 서버 상태 확인
POST /v1/chat/completions  - OpenAI 호환 채팅 완료 API
```

#### 주요 모델 및 구조
- `ChatCompletionRequest`: OpenAI 요청 스펙 완전 호환
- `ChatCompletionResponse`: OpenAI 응답 스펙 완전 호환  
- `ModelManager`: 모델 생명주기 관리
- `ChatTemplate`: Strategy Pattern 기반 템플릿 시스템

#### 성능 최적화
- **서버 시작시 모델 프리로딩**: 매 요청마다 로딩하지 않음
- **정확한 토큰 계산**: 실제 토크나이저 기반 usage 정보
- **메모리 효율적 관리**: 4.3GB 메모리 상주로 즉시 응답

#### 설계 패턴 적용
- **Strategy Pattern**: `ChatTemplate` 추상화로 다양한 모델 지원
- **Factory Pattern**: `get_chat_template()`으로 모델별 템플릿 선택
- **의존성 주입**: `ModelManager`로 모델 상태 관리

#### 지원 기능
- **Qwen2.5-7B-Instruct** 모델 지원
- **Chat Template** 자동 변환 (`<|im_start|>` 형식)
- **max_tokens** 파라미터 지원
- **UUID 기반 고유 ID** 생성
- **Unix 타임스탬프** 기반 생성 시간

#### 개발 과정에서 학습한 내용
1. **MLX-LM 파라미터 제약**: `temperature`, `top_p` 등은 직접 지원하지 않음
2. **FastAPI Startup Event**: `@app.on_event("startup")`으로 초기화 작업
3. **Pydantic vs 딕셔너리**: 타입 안전성과 자동 검증의 중요성
4. **추상화 수준**: 학습용 vs 실용성 간의 트레이드오프

#### 현재 제약사항
- `temperature`, `top_p` 파라미터는 요청으로 받지만 내부적으로 사용되지 않음
- 단일 모델(Qwen2.5-7B)만 지원
- 동기 처리로 대량 요청 시 성능 이슈 예상

---

## 2025-08-22 - Phase 2 계획: 프로덕션 환경 준비

### 🎯 해결해야 할 과제들

#### 1. 프로젝트 구조 개선 
**현재 문제:**
- `main.py` 하나에 모든 코드 집중 (200줄 이상)
- 유지보수성과 확장성 제약

**해결 방안 검토:**
```
옵션 A - 레이어별 구조:
├── api/
│   ├── endpoints/
│   └── models/
├── services/
├── core/
└── utils/

옵션 B - 기능별 구조:
├── chat/
├── models/
├── templates/
└── config/
```

**TODO:**
- [ ] 프로젝트 구조 방식 결정
- [ ] 코드 분리 및 리팩토링
- [ ] import 경로 정리

#### 2. 네트워크 접근성 구성
**요구사항:**
- 나스 서버 → 맥북 API 서버 통신 가능
- 공유기 내부 네트워크 환경

**검토 사항:**
- [ ] 맥북 로컬 IP 고정
- [ ] 포트 포워딩 필요성 검토  
- [ ] 방화벽 설정 확인
- [ ] SSL/TLS 적용 필요성
- [ ] API 인증 방식 결정

#### 3. 대량 요청 처리 시스템 설계
**핵심 요구사항:**
- 30분마다 100~150개 코인 기사 분석 요청
- 각 요청은 순차적으로 전송됨

**성능 고려사항:**
- 현재 단일 요청 처리 시간: ~2-3초 추정
- 150개 * 3초 = 7.5분 (순차 처리시)
- 30분 주기를 고려하면 충분하지만 최적화 여지 존재

**검토할 접근 방식:**
- [ ] **Queue 시스템**: Redis/Celery 기반 비동기 처리
- [ ] **Connection Pooling**: MLX 모델 다중 인스턴스
- [ ] **Rate Limiting**: 서버 보호를 위한 제한
- [ ] **Batch Processing**: 여러 요청을 묶어서 처리
- [ ] **Streaming Response**: 실시간 응답 스트리밍

**추가 고려사항:**
- [ ] 에러 핸들링 및 재시도 로직
- [ ] 로깅 및 모니터링 시스템
- [ ] 메모리 사용량 최적화
- [ ] 캐싱 전략 (동일 요청 중복 방지)

#### 4. 로깅 시스템 구축
**현재 문제:**
- 단순한 `print()` 문으로만 출력
- 로그 레벨, 파일 저장, 구조화된 로깅 부재

**구현해야 할 기능:**
- [ ] **구조화된 로깅**: Python `logging` 모듈 활용
- [ ] **로그 레벨 관리**: DEBUG, INFO, WARNING, ERROR
- [ ] **파일 로깅**: 로그 파일 저장 및 rotation
- [ ] **요청 로깅**: API 호출 추적 (요청/응답 시간, 파라미터)
- [ ] **에러 로깅**: 상세한 에러 정보 및 스택 트레이스
- [ ] **성능 로깅**: 모델 추론 시간, 메모리 사용량
- [ ] **JSON 로깅**: 구조화된 로그 포맷으로 분석 용이성

---

### 🔍 다음 우선순위
1. **프로젝트 구조 개선** (코드 품질 향상)
2. **로깅 시스템 구축** (운영 가시성 확보)
3. **네트워크 설정** (연결성 확보)  
4. **성능 최적화** (대량 처리 대응)

### 📝 추가 고려사항
- Docker 컨테이너화 검토
- 환경 변수 기반 설정 관리
- 로그 레벨 및 파일 출력
- Health check 엔드포인트
- API 문서 자동 생성 (FastAPI Swagger)
