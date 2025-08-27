#!/usr/bin/env python3
import asyncio
import statistics
import time
from concurrent.futures import ThreadPoolExecutor

import aiohttp
import psycopg2


class ConcurrencyTester:
    def __init__(self):
        # PostgreSQL 연결 설정 (실제 DB 정보로 수정 필요)
        self.db_config = {
            "host": "localhost",
            "database": "coin_trading_system",  # 실제 DB명으로 변경
            "user": "yhyuntak",  # 실제 사용자명으로 변경
            "password": "0164532hT!",  # 실제 비밀번호로 변경
        }

        # API 엔드포인트
        self.ollama_url = "http://localhost:11434/v1/chat/completions"
        self.mlx_url = "http://localhost:8000/v1/chat/completions"

        self.articles = []

    def fetch_articles_from_db(self, limit=30):
        """PostgreSQL DB에서 기사 가져오기"""
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()

            # 테이블명과 컬럼명을 실제 DB 구조에 맞게 수정
            query = """
            SELECT title, content FROM articles 
            WHERE LENGTH(content) >= 500 
            ORDER BY created_at DESC 
            LIMIT %s
            """

            cursor.execute(query, (limit,))
            rows = cursor.fetchall()

            self.articles = []
            for i, (title, content) in enumerate(rows):
                # 약 500토큰 정도로 자르기 (1토큰 ≈ 4글자)
                truncated_content = content[:8000] if len(content) > 8000 else content
                self.articles.append(
                    {"id": i + 1, "title": title, "content": truncated_content}
                )

            cursor.close()
            conn.close()

            print(f"📄 DB에서 {len(self.articles)}개 기사를 가져왔습니다")
            return True

        except Exception as e:
            print(f"❌ DB 연결 오류: {e}")
            print("💡 DB 설정을 확인해주세요 (host, database, user, password)")
            return False

    async def test_api_request(self, session, url, article, model_name):
        """단일 API 요청 테스트"""
        payload = {
            "model": model_name,
            "messages": [
                {
                    "role": "user",
                    "content": f"다음 뉴스 기사를 간단히 요약해주세요:\n\n제목: {article['title']}\n\n내용: {article['content'][:1000]}",  # 내용을 1000자로 제한
                }
            ],
            "max_tokens": 100,  # 토큰 수 줄임
        }

        start_time = time.time()
        try:
            async with session.post(
                url, json=payload, timeout=60
            ) as response:  # 타임아웃 60초로 줄임
                if response.status == 200:
                    await response.json()
                    end_time = time.time()
                    return {
                        "article_id": article["id"],
                        "success": True,
                        "duration": end_time - start_time,
                        "start_time": start_time,
                        "end_time": end_time,
                    }
                else:
                    return {
                        "article_id": article["id"],
                        "success": False,
                        "error": f"HTTP {response.status}",
                        "duration": time.time() - start_time,
                    }
        except Exception as e:
            return {
                "article_id": article["id"],
                "success": False,
                "error": str(e),
                "duration": time.time() - start_time,
            }

    async def warmup_model(self, url, model_name, api_name):
        """모델 워밍업 - 로딩 시간 제외하기 위해"""
        print(f"🔥 {api_name} 모델 워밍업 중...")

        async with aiohttp.ClientSession() as session:
            warmup_payload = {
                "model": model_name,
                "messages": [{"role": "user", "content": "Hello"}],
                "max_tokens": 5,
            }

            try:
                async with session.post(
                    url, json=warmup_payload, timeout=120
                ) as response:
                    if response.status == 200:
                        await response.json()
                        print(f"✅ {api_name} 모델 워밍업 완료")
                        return True
            except Exception as e:
                print(f"⚠️ {api_name} 워밍업 실패: {e}")
                return False

        return False

    async def test_concurrent_requests(self, url, model_name, api_name):
        """동시 요청 테스트 - 8개씩 단계적 처리"""
        print(f"\n🚀 {api_name} 테스트 시작 (8개씩 동시 요청)")
        print("-" * 50)

        # 모델 워밍업
        if not await self.warmup_model(url, model_name, api_name):
            return {
                "api_name": api_name,
                "total_duration": 0,
                "successful_count": 0,
                "failed_count": 0,
                "individual_durations": [],
                "parallel_processing": False,
            }

        total_start_time = time.time()
        all_results = []

        # 8개씩 배치로 처리
        batch_size = 8
        for batch_start in range(0, min(24, len(self.articles)), batch_size):
            batch_articles = self.articles[batch_start : batch_start + batch_size]

            print(
                f"배치 {batch_start // batch_size + 1} 처리 중... ({len(batch_articles)}개 요청)"
            )

            async with aiohttp.ClientSession() as session:
                tasks = [
                    self.test_api_request(session, url, article, model_name)
                    for article in batch_articles
                ]

                batch_results = await asyncio.gather(*tasks)
                all_results.extend(batch_results)

            print(f"배치 {batch_start // batch_size + 1} 완료")

        results = all_results

        total_end_time = time.time()
        total_duration = total_end_time - total_start_time

        # 결과 분석
        successful_results = [r for r in results if r["success"]]
        failed_results = [r for r in results if not r["success"]]

        total_requests = len(results)
        print(f"\n📊 {api_name} 테스트 결과:")
        print(f"총 실행 시간: {total_duration:.2f}초")
        print(f"성공한 요청: {len(successful_results)}/{total_requests}")
        print(f"실패한 요청: {len(failed_results)}/{total_requests}")

        if successful_results:
            durations = [r["duration"] for r in successful_results]
            print(f"개별 요청 시간 - 평균: {statistics.mean(durations):.2f}초")
            print(f"개별 요청 시간 - 최소: {min(durations):.2f}초")
            print(f"개별 요청 시간 - 최대: {max(durations):.2f}초")

            # 시간 순서대로 완료된 요청들 확인
            sorted_results = sorted(successful_results, key=lambda x: x["end_time"])
            print(f"첫 번째 완료: {sorted_results[0]['duration']:.2f}초")
            print(f"마지막 완료: {sorted_results[-1]['duration']:.2f}초")

            # 병렬 처리 여부 판단
            first_complete = min([r["end_time"] for r in successful_results])
            last_complete = max([r["end_time"] for r in successful_results])
            parallel_window = last_complete - first_complete

            print(f"병렬 처리 윈도우: {parallel_window:.2f}초")
            if parallel_window < total_duration * 0.3:
                print("✅ 진짜 병렬 처리로 보입니다!")
            else:
                print("⚠️ 순차 처리에 가까워 보입니다.")

        if failed_results:
            print(f"\n❌ 실패한 요청들:")
            for result in failed_results:
                print(
                    f"  기사 ID {result['article_id']}: {result.get('error', 'Unknown error')}"
                )

        return {
            "api_name": api_name,
            "total_duration": total_duration,
            "successful_count": len(successful_results),
            "failed_count": len(failed_results),
            "individual_durations": [r["duration"] for r in successful_results]
            if successful_results
            else [],
            "parallel_processing": parallel_window < total_duration * 0.3
            if successful_results
            else False,
        }

    async def run_tests(self):
        """전체 테스트 실행"""
        print("=" * 60)
        print("🧪 LLM API 동시 처리 성능 테스트")
        print("=" * 60)

        # DB에서 기사 가져오기
        if not self.fetch_articles_from_db():
            return

        if len(self.articles) < 30:
            print(f"⚠️ 기사가 {len(self.articles)}개뿐입니다. 30개 필요합니다.")
            return

        # Ollama 테스트
        ollama_result = await self.test_concurrent_requests(
            self.ollama_url, "qwen2.5:7b", "Ollama"
        )

        print("\n" + "=" * 60)

        # MLX 테스트
        mlx_result = await self.test_concurrent_requests(
            self.mlx_url, "qwen2.5-7b", "MLX"
        )

        # 최종 비교
        print("\n" + "=" * 60)
        print("🏁 최종 비교 결과")
        print("=" * 60)

        print(
            f"Ollama - 총 시간: {ollama_result['total_duration']:.2f}초, "
            f"성공률: {ollama_result['successful_count']}/{ollama_result['successful_count'] + ollama_result['failed_count']}, "
            f"병렬처리: {'✅' if ollama_result['parallel_processing'] else '❌'}"
        )

        print(
            f"MLX    - 총 시간: {mlx_result['total_duration']:.2f}초, "
            f"성공률: {mlx_result['successful_count']}/{mlx_result['successful_count'] + mlx_result['failed_count']}, "
            f"병렬처리: {'✅' if mlx_result['parallel_processing'] else '❌'}"
        )

        if ollama_result["successful_count"] > 0 and mlx_result["successful_count"] > 0:
            speedup = mlx_result["total_duration"] / ollama_result["total_duration"]
            if speedup > 1:
                print(f"\n🏆 Ollama가 {speedup:.1f}배 빠름!")
            else:
                print(f"\n🏆 MLX가 {1 / speedup:.1f}배 빠름!")


def main():
    tester = ConcurrencyTester()
    asyncio.run(tester.run_tests())


if __name__ == "__main__":
    main()
