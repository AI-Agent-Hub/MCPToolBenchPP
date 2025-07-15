import os
import numpy as np
from typing import Dict, List, Any, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.mcp_tool_bench.global_variables import *

def base_compare_result(predict_result: Any, label_result: Any) -> bool:
    """
        Compare Exact Value match, e.g. 3 == 3, "New York" == "New York"
    """
    return label_result == predict_result

def base_compare_result_status_dict(predict_result: dict, label_result: dict) -> bool:
    """
        label_result: 
        {
            'success': True, 'data': ['Navigated to https://www.stackoverflow.com'], 'error': None}, 
            'status_code': 200
        }
        predict_result:
        {
            'status_code': 200,
            "result": {'status_code': 200, 'result': {}}, 'step': '1', 'id': '1'}
        }
    """
    status_code = predict_result["status_code"] if "status_code" in predict_result else 500
    if status_code == 200:
        return True
    return False

def base_compare_result_search(predict_result: dict, label_result: dict) -> bool:
    """
        Search Result is NOT Empty
    """
    if len(label_result) > 0:
        return True
    return False


def estimate_pass_at_k(num_samples, num_correct, k):
    """ Estimates pass@k of each problem and returns them in an array.
        Reference: Implementation from LiveCodeBench: https://github.com/LiveCodeBench/LiveCodeBench
    """

    def estimator(n: int, c: int, k: int) -> float:
        """Calculates 1 - comb(n - c, k) / comb(n, k)."""
        if n - c < k:
            return 1.0
        return 1.0 - np.prod(1.0 - k / np.arange(n - c + 1, n + 1))

    import itertools

    if isinstance(num_samples, int):
        num_samples_it = itertools.repeat(num_samples, len(num_correct))
    else:
        assert len(num_samples) == len(num_correct)
        num_samples_it = iter(num_samples)

    return np.array(
        [estimator(int(n), int(c), k) for n, c in zip(num_samples_it, num_correct)]
    )

## Register Your Specific Tool Compare Result Function
_global_tool_result_check_func_provider: Dict[str, Any] = {}
_global_tool_result_check_func_provider[KEY_BASE_COMPARE_FUNC] = base_compare_result

## Example: add special tool result compare
_global_tool_result_check_func_provider["playwright_navigate"] = base_compare_result_status_dict
_global_tool_result_check_func_provider["bing_web_search"] = base_compare_result_search
_global_tool_result_check_func_provider["bing_news_search"] = base_compare_result_search


def run_test_pass_k():

    num_samples = [10, 10, 10]
    num_correct = [3, 3, 5]
    k = 1

    # array([0.3, 0.3, 0.5])
    pass_at_k = estimate_pass_at_k(num_samples, num_correct, k)
    final_pass_at_k = sum(pass_at_k)/len(pass_at_k)
    print (f"Final Pass @k equals {final_pass_at_k}")

    pass_at_5 = estimate_pass_at_k([10], [5], 5) # e.g.  0.99603175

def main():

    run_test_pass_k()

if __name__ == "__main__":
    main()
