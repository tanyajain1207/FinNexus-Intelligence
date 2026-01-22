"""
Test script for chart generation functionality.
Tests various chart questions to verify improvements work correctly.
"""
import sys
import os

# Add backend_api to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend_api'))

try:
    from hybrid_graph_rag import chain, rag_chart_image, chart_data_chain
    print("✅ Successfully imported chart generation modules")
except ImportError as e:
    print(f"❌ Error importing modules: {e}")
    print("Make sure you're in the correct directory and dependencies are installed")
    sys.exit(1)

def test_rag_response(question):
    """Test if RAG chain can retrieve relevant context."""
    print(f"\n{'='*80}")
    print(f"Testing RAG Response for: {question}")
    print(f"{'='*80}")
    
    try:
        response = chain.invoke({
            "question": question,
            "chat_history": []
        })
        
        print(f"\n📝 RAG Response (first 500 chars):")
        print("-" * 80)
        print(response[:500])
        if len(response) > 500:
            print("...")
        print("-" * 80)
        
        # Check if response indicates missing data
        missing_indicators = [
            "not available", "not found", "no information", 
            "cannot find", "unable to", "does not contain"
        ]
        
        response_lower = response.lower()
        has_missing_data = any(indicator in response_lower for indicator in missing_indicators)
        
        if has_missing_data:
            print("\n⚠️  Response suggests data may not be available")
            return False, response
        else:
            print("\n✅ Response appears to have relevant data")
            return True, response
            
    except Exception as e:
        print(f"\n❌ Error getting RAG response: {e}")
        import traceback
        traceback.print_exc()
        return False, None

def test_chart_data_extraction(rag_response):
    """Test if chart data can be extracted from RAG response."""
    print(f"\n{'='*80}")
    print("Testing Chart Data Extraction")
    print(f"{'='*80}")
    
    try:
        chart_data = chart_data_chain.invoke({"text": rag_response})
        
        print(f"\n📊 Extracted Chart Data:")
        print("-" * 80)
        print(f"Can Generate Chart: {chart_data.can_generate_chart}")
        print(f"Chart Type: {chart_data.chart_type}")
        print(f"Title: {chart_data.title}")
        print(f"Y-Axis Label: {chart_data.y_axis_label}")
        print(f"Labels: {chart_data.labels}")
        print(f"Values: {chart_data.values}")
        if chart_data.message:
            print(f"Message: {chart_data.message}")
        print("-" * 80)
        
        if chart_data.can_generate_chart and chart_data.labels and chart_data.values:
            print("\n✅ Chart data extraction successful!")
            if len(chart_data.labels) != len(chart_data.values):
                print(f"⚠️  Warning: Label count ({len(chart_data.labels)}) != Value count ({len(chart_data.values)})")
            return True, chart_data
        else:
            print("\n❌ Chart data extraction failed or insufficient data")
            return False, chart_data
            
    except Exception as e:
        print(f"\n❌ Error extracting chart data: {e}")
        import traceback
        traceback.print_exc()
        return False, None

def test_chart_generation(question):
    """Test full chart generation pipeline."""
    print(f"\n{'='*80}")
    print(f"Testing Full Chart Generation for: {question}")
    print(f"{'='*80}")
    
    try:
        img_bytes = rag_chart_image(question)
        
        print(f"\n✅ Chart generated successfully!")
        print(f"📦 Image size: {len(img_bytes)} bytes")
        
        # Save test image
        test_output_dir = "test_charts"
        os.makedirs(test_output_dir, exist_ok=True)
        
        # Create safe filename from question
        safe_filename = "".join(c if c.isalnum() or c in (' ', '-', '_') else '' for c in question[:50])
        safe_filename = safe_filename.replace(' ', '_').lower()
        
        output_path = os.path.join(test_output_dir, f"{safe_filename}.png")
        with open(output_path, 'wb') as f:
            f.write(img_bytes)
        
        print(f"💾 Chart saved to: {output_path}")
        return True
        
    except ValueError as ve:
        print(f"\n⚠️  Expected error (missing data): {str(ve)}")
        print("✅ Error handling working correctly!")
        return "error_handled"
    except Exception as e:
        print(f"\n❌ Error generating chart: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run comprehensive tests."""
    print("\n" + "="*80)
    print("CHART GENERATION TEST SUITE")
    print("="*80)
    print("\nTesting improvements to chart generation system...")
    
    # Test questions based on what should be available in the PDF
    test_cases = [
        {
            "question": "Create a chart showing revenue trends",
            "expected": "Should extract revenue values for multiple years (2022, 2023, 2024)",
            "category": "Time Series"
        },
        {
            "question": "Show me geographical revenue distribution",
            "expected": "Should extract revenue by region (Americas, Europe, Greater China, etc.)",
            "category": "Geographic"
        },
        {
            "question": "Create a chart of revenue by product category",
            "expected": "Should extract revenue by product (iPhone, Mac, iPad, Services, etc.)",
            "category": "Product Segment"
        },
        {
            "question": "Show me capital expenditure evolution",
            "expected": "Should extract CapEx values over time",
            "category": "Financial Metric"
        },
        {
            "question": "Show me revenue for 2030",
            "expected": "Should show error message about data not being available",
            "category": "Error Handling (Future Data)"
        },
        {
            "question": "Create a chart showing Microsoft's revenue",
            "expected": "Should show error message explaining only Apple data available",
            "category": "Error Handling (Wrong Company)"
        },
    ]
    
    results = {
        "passed": [],
        "failed": [],
        "error_handled": []
    }
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n\n{'#'*80}")
        print(f"TEST {i}/{len(test_cases)}: {test_case['category']}")
        print(f"{'#'*80}")
        print(f"Question: {test_case['question']}")
        print(f"Expected: {test_case['expected']}")
        
        # Test RAG response first
        has_data, rag_response = test_rag_response(test_case['question'])
        
        if rag_response:
            # Test chart data extraction
            extraction_success, chart_data = test_chart_data_extraction(rag_response)
            
            # Test full chart generation
            if test_case['category'].startswith("Error Handling"):
                # For error cases, we expect an error to be raised
                result = test_chart_generation(test_case['question'])
                if result == "error_handled":
                    results["error_handled"].append(test_case)
                    print(f"\n✅ TEST {i} PASSED (Error handled correctly)")
                else:
                    results["failed"].append(test_case)
                    print(f"\n❌ TEST {i} FAILED (Expected error handling)")
            else:
                # For valid cases, test chart generation
                if extraction_success:
                    result = test_chart_generation(test_case['question'])
                    if result:
                        results["passed"].append(test_case)
                        print(f"\n✅ TEST {i} PASSED")
                    else:
                        results["failed"].append(test_case)
                        print(f"\n❌ TEST {i} FAILED (Chart generation failed)")
                else:
                    results["failed"].append(test_case)
                    print(f"\n❌ TEST {i} FAILED (Data extraction failed)")
        else:
            results["failed"].append(test_case)
            print(f"\n❌ TEST {i} FAILED (RAG response error)")
    
    # Print summary
    print("\n\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"✅ Passed: {len(results['passed'])}/{len(test_cases)}")
    print(f"❌ Failed: {len(results['failed'])}/{len(test_cases)}")
    print(f"⚠️  Error Handling (Expected): {len(results['error_handled'])}/{len(test_cases)}")
    
    if results['passed']:
        print(f"\n✅ Successful Tests:")
        for test in results['passed']:
            print(f"   - {test['category']}: {test['question']}")
    
    if results['error_handled']:
        print(f"\n✅ Error Handling Tests (Correct Behavior):")
        for test in results['error_handled']:
            print(f"   - {test['category']}: {test['question']}")
    
    if results['failed']:
        print(f"\n❌ Failed Tests:")
        for test in results['failed']:
            print(f"   - {test['category']}: {test['question']}")
    
    print("\n" + "="*80)
    
    return len(results['failed']) == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

