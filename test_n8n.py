#!/usr/bin/env python3
"""
สคริปต์ทดสอบการเชื่อมต่อ n8n webhook
"""

import asyncio
import httpx
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()

N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")

async def test_n8n_connection():
    """ทดสอบการเชื่อมต่อ n8n webhook"""
    
    if not N8N_WEBHOOK_URL:
        print("❌ N8N_WEBHOOK_URL not configured in .env file")
        print("Please add: N8N_WEBHOOK_URL=your_webhook_url")
        return
    
    print("🔄 Testing n8n webhook connection...")
    print(f"📍 URL: {N8N_WEBHOOK_URL}")
    print()
    
    test_data = {
        "word": "Runway",
        "sentence": "The airplane landed safely on the runway."
    }
    
    print(f"📤 Sending test data:")
    print(json.dumps(test_data, indent=2))
    print()
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                N8N_WEBHOOK_URL,
                json=test_data,
                headers={"Content-Type": "application/json"}
            )
            
            response.raise_for_status()
            result = response.json()
            
            print("✅ Connection successful!")
            print()
            print("📥 Response:")
            print(json.dumps(result, indent=2))
            print()
            
            # Validate response structure
            required_fields = ["score", "level", "suggestion", "corrected_sentence"]
            missing_fields = [f for f in required_fields if f not in result]
            
            if missing_fields:
                print(f"⚠️  Warning: Missing fields in response: {missing_fields}")
            else:
                print("✅ Response structure is valid!")
                
                # Check score range
                score = float(result["score"])
                if 0 <= score <= 10:
                    print(f"✅ Score is valid: {score}/10")
                else:
                    print(f"⚠️  Warning: Score out of range: {score}")
            
            return True
            
    except httpx.TimeoutException:
        print("❌ Connection timeout!")
        print("Check if n8n is running and the URL is correct.")
        
    except httpx.HTTPStatusError as e:
        print(f"❌ HTTP Error: {e.response.status_code}")
        print(f"Response: {e.response.text}")
        
    except json.JSONDecodeError:
        print("❌ Invalid JSON response from webhook")
        print(f"Response: {response.text}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    return False

async def test_backend_api():
    """ทดสอบการเรียก API ของ backend"""
    
    print("\n" + "="*50)
    print("Testing Backend API")
    print("="*50 + "\n")
    
    backend_url = "http://localhost:8000"
    
    print(f"🔄 Testing backend API at {backend_url}")
    print()
    
    test_data = {
        "word": "Resilient",
        "sentence": "The team showed resilient spirit during tough times."
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Test health endpoint
            print("1️⃣ Testing health endpoint...")
            health_response = await client.get(f"{backend_url}/health")
            print(f"   Status: {health_response.status_code}")
            print(f"   Response: {health_response.json()}")
            print()
            
            # Test validation endpoint
            print("2️⃣ Testing validation endpoint...")
            print(f"   Sending: {json.dumps(test_data, indent=2)}")
            
            validate_response = await client.post(
                f"{backend_url}/api/validate-sentence",
                json=test_data
            )
            
            validate_response.raise_for_status()
            result = validate_response.json()
            
            print(f"   Status: {validate_response.status_code}")
            print(f"   Response: {json.dumps(result, indent=2)}")
            print()
            print("✅ Backend API is working!")
            
            return True
            
    except httpx.ConnectError:
        print("❌ Cannot connect to backend!")
        print("Make sure the backend is running on port 8000")
        print("Run: uvicorn app.main:app --reload --port 8000")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    return False

async def main():
    """Main test function"""
    
    print("="*50)
    print("Worddee.ai n8n Integration Test")
    print("="*50)
    print()
    
    # Test n8n webhook
    n8n_ok = await test_n8n_connection()
    
    # Test backend API
    backend_ok = await test_backend_api()
    
    # Summary
    print("\n" + "="*50)
    print("Test Summary")
    print("="*50)
    print(f"n8n Webhook: {'✅ PASS' if n8n_ok else '❌ FAIL'}")
    print(f"Backend API: {'✅ PASS' if backend_ok else '❌ FAIL'}")
    print()
    
    if n8n_ok and backend_ok:
        print("🎉 All tests passed! Your integration is working!")
    elif backend_ok and not n8n_ok:
        print("⚠️  Backend is working but n8n is not connected.")
        print("The app will use mock responses until n8n is configured.")
    else:
        print("❌ Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    asyncio.run(main())