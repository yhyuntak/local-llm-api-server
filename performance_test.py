#!/usr/bin/env python3
"""
Ollama 성능 테스트 스크립트
KV 캐시 워밍업 + 병렬 처리 성능 측정
"""

import asyncio
import aiohttp
import time
import json
from datetime import datetime
import argparse

# Test prompts with approximately 1000 tokens each
TEST_PROMPTS = [
    "Please provide a detailed analysis of approximately 500 words on the following topic: Discuss the impact of artificial intelligence development on society. Focus particularly on changes in education, healthcare, transportation, and finance sectors. Present a balanced view of both positive and negative impacts, and provide future prospects and response strategies. Include specific examples and case studies where possible.",
    
    "Please provide a detailed analysis and solution for the following situation: The global climate change problem is becoming increasingly serious. Diagnose the current situation, analyze each country's response policies, and present specific action plans that individuals, businesses, and governments can implement. Focus particularly on renewable energy transition, carbon neutrality policies, and eco-friendly technology development.",
    
    "Please provide a comprehensive analysis of digital transformation in modern society. Explain how digitalization accelerated after COVID-19 has changed our lives, with specific examples in remote work, online education, digital healthcare, and e-commerce sectors. Also discuss the digital divide problem and its solutions.",
    
    "Please write a comprehensive report on sustainable urban development. Explain how elements such as smart city technology, eco-friendly architecture, public transportation systems, green infrastructure, and circular economy can harmonize to create future cities. Compare and analyze success and failure cases to propose applicable solutions.",
    
    "Please provide an in-depth analysis of educational paradigm changes in the Fourth Industrial Revolution era. Explain what innovations AI, big data, IoT, and blockchain technologies are bringing to educational settings. Introduce new educational methodologies such as personalized learning, virtual reality education, and lifelong learning systems, and present the changing roles of educators and learners and the direction future education systems should take."
]

class PerformanceTest:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.results = []
        self.warmup_result = None
        
    async def send_request(self, session: aiohttp.ClientSession, prompt: str, request_id: int):
        """단일 요청 전송 및 성능 측정"""
        start_time = time.time()
        
        payload = {
            "model": "qwen3:14b",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 500
        }
        
        try:
            async with session.post(
                f"{self.base_url}/v1/chat/completions",
                json=payload,
                timeout=aiohttp.ClientTimeout(total=120)
            ) as response:
                end_time = time.time()
                duration = end_time - start_time
                
                if response.status == 200:
                    data = await response.json()
                    return {
                        'request_id': request_id,
                        'success': True,
                        'duration': duration,
                        'response_length': len(data['choices'][0]['message']['content']),
                        'prompt_tokens': data.get('usage', {}).get('prompt_tokens', 0),
                        'completion_tokens': data.get('usage', {}).get('completion_tokens', 0),
                        'total_tokens': data.get('usage', {}).get('total_tokens', 0)
                    }
                else:
                    return {
                        'request_id': request_id,
                        'success': False,
                        'duration': duration,
                        'error': f"HTTP {response.status}"
                    }
                    
        except Exception as e:
            end_time = time.time()
            return {
                'request_id': request_id,
                'success': False,
                'duration': end_time - start_time,
                'error': str(e)
            }

    async def warmup_request(self, session: aiohttp.ClientSession):
        """KV 캐시 워밍업을 위한 단일 요청"""
        print("🔥 Warming up KV cache with single request...")
        warmup_prompt = TEST_PROMPTS[0]
        
        start_time = time.time()
        result = await self.send_request(session, warmup_prompt, 0)
        warmup_time = time.time() - start_time
        
        self.warmup_result = {
            'warmup_duration': warmup_time,
            'warmup_result': result
        }
        
        print(f"✅ Warmup completed in {warmup_time:.2f}s")
        if result['success']:
            print(f"   Response length: {result['response_length']} chars")
            print(f"   Total tokens: {result['total_tokens']}")
        print()

    async def run_concurrent_test(self, num_requests: int = 100, max_concurrent: int = 10):
        """병렬 요청 테스트 실행"""
        print(f"Starting performance test: {num_requests} requests, max {max_concurrent} concurrent")
        print(f"Target URL: {self.base_url}")
        print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 80)
        
        async with aiohttp.ClientSession() as session:
            # 1. KV 캐시 워밍업
            await self.warmup_request(session)
            
            # 2. 병렬 테스트 준비
            requests_data = []
            for i in range(num_requests):
                prompt = TEST_PROMPTS[i % len(TEST_PROMPTS)]
                requests_data.append((prompt, i + 1))
            
            # 세마포어로 동시 요청 수 제한
            semaphore = asyncio.Semaphore(max_concurrent)
            
            async def limited_request(session, prompt, request_id):
                async with semaphore:
                    return await self.send_request(session, prompt, request_id)
            
            # 3. 병렬 테스트 시작 (워밍업 제외)
            print("🚀 Starting parallel performance test...")
            start_time = time.time()
            
            tasks = [
                limited_request(session, prompt, request_id)
                for prompt, request_id in requests_data
            ]
            
            # 진행상황 표시하면서 실행
            completed = 0
            for coro in asyncio.as_completed(tasks):
                result = await coro
                completed += 1
                self.results.append(result)
                
                if completed % 10 == 0:
                    print(f"Completed: {completed}/{num_requests}")
        
        total_time = time.time() - start_time
        
        # 결과 분석 및 출력
        self.analyze_results(total_time)
        
    def analyze_results(self, total_time: float):
        """결과 분석 및 리포트 생성"""
        successful = [r for r in self.results if r['success']]
        failed = [r for r in self.results if not r['success']]
        
        print("\n" + "=" * 80)
        print("PERFORMANCE TEST RESULTS")
        print("=" * 80)
        
        # 워밍업 결과 표시
        if self.warmup_result:
            warmup = self.warmup_result['warmup_result']
            print(f"🔥 Warmup Request (TTFT):")
            print(f"  Duration: {self.warmup_result['warmup_duration']:.2f}s")
            if warmup['success']:
                print(f"  Response length: {warmup['response_length']} chars")
                print(f"  Total tokens: {warmup['total_tokens']}")
            print()
        
        print(f"📊 Parallel Test Results:")
        print(f"Total requests: {len(self.results)}")
        print(f"Successful: {len(successful)}")
        print(f"Failed: {len(failed)}")
        print(f"Success rate: {len(successful)/len(self.results)*100:.1f}%")
        print(f"Total test time: {total_time:.2f} seconds")
        print(f"Requests per second: {len(self.results)/total_time:.2f}")
        
        if successful:
            durations = [r['duration'] for r in successful]
            tokens = [r.get('total_tokens', 0) for r in successful]
            
            print(f"\nResponse Time Statistics:")
            print(f"  Average: {sum(durations)/len(durations):.2f}s")
            print(f"  Min: {min(durations):.2f}s")
            print(f"  Max: {max(durations):.2f}s")
            
            if tokens and any(tokens):
                print(f"\nToken Statistics:")
                print(f"  Average total tokens: {sum(tokens)/len(tokens):.0f}")
                print(f"  Tokens per second: {sum(tokens)/sum(durations):.1f}")
        
        if failed:
            print(f"\nFailure Analysis:")
            error_types = {}
            for f in failed:
                error = f.get('error', 'Unknown')
                error_types[error] = error_types.get(error, 0) + 1
            for error, count in error_types.items():
                print(f"  {error}: {count}")
        
        # 결과를 파일로 저장
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"performance_test_{timestamp}.json"
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'warmup_result': self.warmup_result,
            'total_requests': len(self.results),
            'successful': len(successful),
            'failed': len(failed),
            'total_time': total_time,
            'requests_per_second': len(self.results)/total_time,
            'results': self.results
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\nDetailed results saved to: {filename}")

async def main():
    parser = argparse.ArgumentParser(description='Ollama Performance Test')
    parser.add_argument('--requests', '-r', type=int, default=100, help='Number of requests (default: 100)')
    parser.add_argument('--concurrent', '-c', type=int, default=10, help='Max concurrent requests (default: 10)')
    parser.add_argument('--url', '-u', default='http://localhost:8000', help='Base URL (default: http://localhost:8000)')
    
    args = parser.parse_args()
    
    test = PerformanceTest(args.url)
    await test.run_concurrent_test(args.requests, args.concurrent)

if __name__ == "__main__":
    asyncio.run(main())