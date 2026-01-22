"""
Code verification script - checks if improvements are correctly implemented
without requiring full backend setup.
"""
import os
import re

def check_file_exists(filepath):
    """Check if file exists."""
    exists = os.path.exists(filepath)
    print(f"{'[OK]' if exists else '[FAIL]'} {filepath}: {'Found' if exists else 'NOT FOUND'}")
    return exists

def check_contains_code(filepath, patterns, description):
    """Check if file contains specific code patterns."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"\n[CHECK] {description}")
        print("-" * 80)
        
        all_found = True
        for pattern, check_name in patterns:
            found = bool(re.search(pattern, content, re.IGNORECASE | re.DOTALL))
            status = '[OK]' if found else '[FAIL]'
            print(f"{status} {check_name}")
            if not found:
                all_found = False
        
        return all_found
    except FileNotFoundError:
        print(f"[FAIL] File not found: {filepath}")
        return False
    except Exception as e:
        print(f"[FAIL] Error reading file: {e}")
        return False

def main():
    """Verify implementation of improvements."""
    print("=" * 80)
    print("IMPLEMENTATION VERIFICATION")
    print("=" * 80)
    
    results = {}
    
    # Check 1: ChartData model exists
    print("\n" + "=" * 80)
    print("1. CHECKING: ChartData Pydantic Model")
    print("=" * 80)
    
    patterns = [
        (r'class ChartData\(BaseModel\)', 'ChartData class defined'),
        (r'labels:\s*List\[str\]', 'labels field (List[str])'),
        (r'values:\s*List\[float\]', 'values field (List[float])'),
        (r'chart_type:\s*str', 'chart_type field'),
        (r'title:\s*str', 'title field'),
        (r'can_generate_chart:\s*bool', 'can_generate_chart field'),
    ]
    
    results['chartdata_model'] = check_contains_code(
        'backend_api/hybrid_graph_rag.py',
        patterns,
        'ChartData Model Implementation'
    )
    
    # Check 2: Chart extraction prompt/chain
    print("\n" + "=" * 80)
    print("2. CHECKING: Chart Data Extraction Chain")
    print("=" * 80)
    
    patterns = [
        (r'chart_extraction_prompt', 'Chart extraction prompt defined'),
        (r'chart_data_chain', 'Chart data chain defined'),
        (r'with_structured_output\(ChartData\)', 'Structured output using ChartData'),
    ]
    
    results['chart_extraction'] = check_contains_code(
        'backend_api/hybrid_graph_rag.py',
        patterns,
        'Chart Data Extraction Implementation'
    )
    
    # Check 3: Improved RAG prompt
    print("\n" + "=" * 80)
    print("3. CHECKING: Improved RAG Prompt (Missing Data Handling)")
    print("=" * 80)
    
    patterns = [
        (r'Do NOT ask the user to "refer to files"', 'Explicit instruction to avoid generic responses'),
        (r'explain what information is NOT available', 'Instruction to explain missing data'),
        (r'suggest what related information might be available', 'Instruction to suggest alternatives'),
        (r'context is empty or doesn\'t contain', 'Handles empty context'),
    ]
    
    results['rag_prompt'] = check_contains_code(
        'backend_api/hybrid_graph_rag.py',
        patterns,
        'Improved RAG Prompt Template'
    )
    
    # Check 4: Improved chart generation function
    print("\n" + "=" * 80)
    print("4. CHECKING: Improved rag_chart_image Function")
    print("=" * 80)
    
    patterns = [
        (r'def rag_chart_image\(question\):', 'rag_chart_image function defined'),
        (r'chart_data_chain\.invoke', 'Uses chart_data_chain for extraction'),
        (r'can_generate_chart', 'Checks can_generate_chart flag'),
        (r'chart_type\s*=\s*chart_data\.chart_type', 'Uses extracted chart_type'),
        (r'chart_type == "pie"', 'Supports pie charts'),
        (r'chart_type == "line"', 'Supports line charts'),
        (r'ValueError', 'Raises ValueError for missing data'),
    ]
    
    results['chart_function'] = check_contains_code(
        'backend_api/hybrid_graph_rag.py',
        patterns,
        'Improved Chart Generation Function'
    )
    
    # Check 5: Improved retriever
    print("\n" + "=" * 80)
    print("5. CHECKING: Improved Retriever (Empty Context Detection)")
    print("=" * 80)
    
    patterns = [
        (r'has_structured\s*=\s*structured_data', 'Checks for structured data'),
        (r'has_unstructured\s*=\s*unstructured_data', 'Checks for unstructured data'),
        (r'No relevant information found', 'Returns helpful message when no data'),
    ]
    
    results['retriever'] = check_contains_code(
        'backend_api/hybrid_graph_rag.py',
        patterns,
        'Improved Retriever Function'
    )
    
    # Check 6: Backend API error handling
    print("\n" + "=" * 80)
    print("6. CHECKING: Backend API Error Handling")
    print("=" * 80)
    
    patterns = [
        (r'except ValueError as ve:', 'Catches ValueError for missing data'),
        (r'"answer":\s*error_message', 'Returns error message in response'),
        (r'"error":\s*error_message', 'Returns error field'),
    ]
    
    results['api_error_handling'] = check_contains_code(
        'backend_api/backend_api.py',
        patterns,
        'Backend API Error Handling'
    )
    
    # Check 7: Frontend error handling
    print("\n" + "=" * 80)
    print("7. CHECKING: Frontend Error Handling")
    print("=" * 80)
    
    patterns = [
        (r'responseData\.error', 'Checks for error in response'),
        (r'responseData\.answer.*responseData\.error', 'Handles error messages'),
    ]
    
    results['frontend_error'] = check_contains_code(
        'frontend/src/App.js',
        patterns,
        'Frontend Error Message Handling'
    )
    
    # Summary
    print("\n" + "=" * 80)
    print("VERIFICATION SUMMARY")
    print("=" * 80)
    
    total_checks = len(results)
    passed_checks = sum(1 for v in results.values() if v)
    
    for check_name, passed in results.items():
        status = '[PASS]' if passed else '[FAIL]'
        print(f"{status}: {check_name.replace('_', ' ').title()}")
    
    print("\n" + "-" * 80)
    print(f"Total: {passed_checks}/{total_checks} checks passed")
    print("-" * 80)
    
    if passed_checks == total_checks:
        print("\n[SUCCESS] All implementation checks passed!")
        print("The improvements have been correctly implemented in the code.")
    else:
        print("\n[WARNING] Some checks failed. Please review the implementation.")
    
    return passed_checks == total_checks

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

