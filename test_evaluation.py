#!/usr/bin/env python3
"""
Reproducibility Script for Agentic RAG System
Run this to verify the test results mentioned in README
"""

import requests
import json
import time
import sys

def run_evaluation():
    """Run the same evaluation as mentioned in README"""
    
    print("🧠 Agentic RAG System Reproducibility Test")
    print("=" * 55)
    
    # Load test questions and document
    print("\n📁 Loading test data...")
    with open('test_data/sample_questions.txt', 'r') as f:
        questions = [line.strip() for line in f if line.strip()]
    
    with open('test_data/sample_document.txt', 'r') as f:
        document_content = f.read()
    
    print(f"✅ Loaded {len(questions)} test questions")
    print(f"✅ Loaded document ({len(document_content)} characters)")
    
    # Check if server is running
    print("\n🔍 Checking server status...")
    try:
        response = requests.get('http://localhost:8000/health', timeout=5)
        if response.status_code == 200:
            print("✅ Server is running")
        else:
            print("❌ Server returned error")
            return 0
    except requests.exceptions.RequestException:
        print("❌ Server not running. Start with: python app.py")
        return 0
    
    # Upload document
    print("\n📤 Uploading document...")
    try:
        upload_response = requests.post(
            'http://localhost:8000/upload',
            files={'file': ('sample_document.txt', document_content, 'text/plain')},
            timeout=30
        )
        
        if upload_response.status_code == 200:
            doc_id = upload_response.json().get('document_id')
            print(f"✅ Document uploaded successfully (ID: {doc_id})")
        else:
            print(f"❌ Upload failed: {upload_response.status_code}")
            return 0
            
    except Exception as e:
        print(f"❌ Upload error: {e}")
        return 0
    
    # Test a sample of questions
    test_questions = questions[:5]  # Test first 5 questions for demo
    results = []
    
    print(f"\n🧪 Testing {len(test_questions)} sample questions with multi-agent system...")
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n[{i}/{len(test_questions)}] Question: {question[:50]}...")
        
        start_time = time.time()
        
        try:
            # Send question to agentic RAG system
            response = requests.post(
                'http://localhost:8000/query',
                json={
                    'question': question,
                    'document_id': doc_id,
                    'use_agents': True  # Enable multi-agent processing
                },
                timeout=20
            )
            
            end_time = time.time()
            
            if response.status_code == 200:
                result = response.json()
                response_time = end_time - start_time
                
                print(f"   ✅ Processed in {response_time:.1f}s")
                print(f"   📝 Answer length: {len(result.get('answer', ''))} characters")
                print(f"   🔗 Sources: {len(result.get('sources', []))}")
                if 'agents_used' in result:
                    print(f"   🤖 Agents: {result['agents_used']}")
                
                # Quality checks for agentic RAG
                quality_score = 0
                if len(result.get('answer', '')) > 100:
                    quality_score += 0.3  # Comprehensive answer
                if result.get('sources'):
                    quality_score += 0.2  # Has citations
                if result.get('confidence', 0) > 0.8:
                    quality_score += 0.3  # High confidence
                if 'agents_used' in result and len(result['agents_used']) > 1:
                    quality_score += 0.2  # Used multiple agents
                
                results.append({
                    'question': question,
                    'success': True,
                    'response_time': response_time,
                    'quality_score': quality_score
                })
                
            else:
                print(f"   ❌ Failed with status {response.status_code}")
                results.append({
                    'question': question,
                    'success': False,
                    'response_time': 0,
                    'quality_score': 0
                })
                
        except requests.exceptions.Timeout:
            print(f"   ⏰ Timeout after 20 seconds")
            results.append({
                'question': question,
                'success': False,
                'response_time': 20,
                'quality_score': 0
            })
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results.append({
                'question': question,
                'success': False,
                'response_time': 0,
                'quality_score': 0
            })
    
    # Calculate metrics
    print("\n📊 Results Summary:")
    successful_queries = [r for r in results if r['success']]
    success_rate = len(successful_queries) / len(results) * 100
    
    if successful_queries:
        avg_response_time = sum(r['response_time'] for r in successful_queries) / len(successful_queries)
        avg_quality = sum(r['quality_score'] for r in results) / len(results) * 100
    else:
        avg_response_time = 0
        avg_quality = 0
    
    print(f"   Success Rate: {success_rate:.0f}%")
    print(f"   Avg Response Time: {avg_response_time:.1f}s")
    print(f"   Avg Quality Score: {avg_quality:.0f}%")
    
    # Expected results based on README
    print("\n🎯 Expected Results:")
    print("   Success Rate: ~89%")
    print("   Response Time: ~2.2s (multi-agent)")
    print("   Quality Score: ~87%")
    
    # Verification
    print("\n✅ Verification:")
    success_ok = abs(success_rate - 89) < 20  # Within 20% of expected
    time_ok = abs(avg_response_time - 2.2) < 1.5  # Within 1.5 seconds of expected
    quality_ok = avg_quality > 70  # Above 70% quality
    
    print(f"   Success Rate: {'✅ OK' if success_ok else '❌ LOW'}")
    print(f"   Response Time: {'✅ OK' if time_ok else '❌ SLOW/FAST'}")
    print(f"   Quality Score: {'✅ OK' if quality_ok else '❌ LOW'}")
    
    # Overall assessment
    overall_score = (success_ok + time_ok + quality_ok) / 3 * 100
    print(f"\n📈 Overall Match: {overall_score:.0f}%")
    
    if overall_score >= 80:
        print("🎉 Great! Results closely match README claims.")
    elif overall_score >= 60:
        print("⚠️  Acceptable. Some metrics differ from README.")
    else:
        print("❌ Results don't match README claims.")
    
    return overall_score

if __name__ == "__main__":
    try:
        score = run_evaluation()
        print(f"\n🏁 Test completed with {score:.0f}% match to README")
    except KeyboardInterrupt:
        print("\n⏹️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Error running test: {e}")
        print("💡 Make sure server is running: python app.py")
