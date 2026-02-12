"""
computeSales.py 

This program computes the total cost of sales based on a price catalogue
and sales records provided in two different JSON format.

Example:
    python computeSales.py priceCatalogue.json salesRecord.json
"""

import argparse
import time
import json
from typing import Dict, List, Tuple


def load_json_file(filename: str) -> Dict:
    """
    Load and parse a JSON file.

    Args:
        filename: Path to the JSON file

    Returns:
        Parsed JSON data as a dictionary

    Raises:
        FileNotFoundError: If file doesn"t exist
        json.JSONDecodeError: If JSON is malformed
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found {filename}")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            f"Invalid JSON format for {filename}: {e.msg}"
        )


def load_price_catalogue(filename: str) -> Dict:
    """
    Load the price catalogue from a JSON file.

    Args:
        filename: Path to the price catalogue JSON file

    Returns:
        Dictionary containing product prices
    """
    data = load_json_file(filename)

    if isinstance(data, list):
        price_dict = {}
        for item in data:
            if isinstance(item, dict) and 'title' in item and 'price' in item:
                price_dict[item['title']] = item['price']
        return price_dict

    return data


def load_sales_record(filename: str) -> List:
    """
    Load the sales record from a JSON file.

    Args:
        filename: Path to the sales record JSON file

    Returns:
        List of sales transactions
    """
    return load_json_file(filename)


def compute_sale_total(sale: Dict, prices_dict: Dict) -> Tuple[float, List[str]]:
    """
    Compute the total cost for a single sale.

    Args:
        sale: Dictionary containing sale information
        prices_dict: Dictionary with product prices

    Returns:
        Tuple of (total_cost, list_of_errors)
    """
    errors = []
    total = 0.0

    try:
        sale_id = sale.get("SALE_ID", "Unknown")
        product = sale.get("Product", None)
        quantity = sale.get("Quantity", None)

        # validation
        if product is None:
            errors.append(f"Missing product information")
            return 0.0, errors

        if quantity is None:
            errors.append(f"Missing quantity information")
            return 0.0, errors

        try:
            quantity = float(quantity)
            if quantity < 0:
                errors.append(f"Sale {sale_id}: Negative quantity ({quantity})")
                return 0.0, errors
        except (ValueError, TypeError):
            errors.append(f"Sale {sale_id}: Invalid quantity value ({quantity})")
            return 0.0, errors

        if product not in prices_dict:
            errors.append(f"Sale {sale_id}: Product '{product}' not found in price catalogue")
            return 0.0, errors

        price = prices_dict[product]
        try:
            price = float(price)
            if price < 0:
                errors.append(f"Sale {sale_id}: Negative price for product '{product}'")
                return 0.0, errors
        except (ValueError, TypeError):
            errors.append(f"Sale {sale_id}: Invalid price for product '{product}'")
            return 0.0, errors

        total = price * quantity

    except Exception as e:
        errors.append(f"Sale {sale.get('Sale', 'Unknown')}: Unexpected error - {str(e)}")
        return 0.0, errors

    return total, errors
        

    
def compute_all_sales(sales_records: List, sales_dict: Dict) -> Tuple[float, int, List[str]]:
    """
    Compute total cost for all sales.

    Args:
        sales_records: List of all sales transactions
        sales_dict: Dictionary with product prices

    Returns:
        Tuple of (grand_total, successful_sales_count, list_of_errors)
    """
    total = 0.0
    errors = []

    if not isinstance(sales_records, list):
        errors.append("Sales records is not a list")
        return 0.0, 0, errors
    
    if not isinstance(sales_dict, dict):
        errors.append("Sales dict is not a dict")
        return 0.0, 0, errors
    
    for idx, sale in enumerate(sales_records):
        if not isinstance(sale, dict):
            errors.append(f"Sale number {idx} is not a dict")
            continue
        
        sale_total, errors = compute_sale_total(sale, sales_dict)

        if errors:
            errors.extend(errors)
        else: 
            total += sale_total


    return total, errors


def format_output(total: float, execution_time: float, 
                  errors: list[str]) -> str:
    """
    Format the results in a human-readable format.

    Args:
        total: Total cost of all sales
        sales_count: Number of successfully processed sales
        execution_time: Time elapsed during execution

    Returns:
        Formatted string for output
    """
    if errors is None:
        errors = []

    output_lines = []
    output_lines.append("=" * 60)
    output_lines.append("RESULTS")
    output_lines.append("")
    output_lines.append(f"Total Sales: ${total:,.2f}")
    output_lines.append(f"Execution Time: {execution_time:.4f} seconds")
    output_lines.append("")

    if errors:
        output_lines.append("=" * 60)
        output_lines.append(f"ERRORS ENCOUNTERED: {len(errors)}")
        
        for idx, error in enumerate(errors, 1):
            output_lines.append(f'{idx}: {error}')
        output_lines.append("")

    return "\n".join(output_lines)



def write_results_to_file(output: str, filename: str = "SalesResults.txt") -> None:
    """
    Write the results to a text file.

    Args:
        output: Formatted output string
        filename: Name of the output file (default: SalesResults.txt)
    """
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(output)


def display_results(output: str) -> None:
    """
    Display results on the console.

    Args:
        output: Formatted output string
    """
    print(output)


def parse_arguments():
    """
    Parse command line arguments using argparse.

    Returns:
        Namespace object with parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Compute total cost of sales based on price and sales records.",
        epilog="Example: python computeSales.py price.json sales.json"
    )
    
    parser.add_argument(
        "price_file",
        type=str,
        help="Path to the price JSON file"
    )
    
    parser.add_argument(
        "sales_file",
        type=str,
        help="Path to the sales JSON file"
    )
    
    return parser.parse_args()


def main():
    """
    Main function to orchestrate the sales computation process.
    """
    start_time = time.time()
    
    # Parse command line arguments
    args = parse_arguments()
    
    price_file = args.price_catalogue
    sales_file = args.sales_record
    
    all_errors = []
    
    try:
        prices_dict = load_price_catalogue(price_file)
    except Exception as e:
        print(f"Error loading price file: {e}")
        all_errors.append(f"Price file error: {e}")
        prices_dict = {}
    
    try:
        sales = load_sales_record(sales_file)
    except Exception as e:
        print(f"Error loading sales file: {e}")
        all_errors.append(f"Sales file error: {e}")
        sales = []
    
    total, computation_errors = compute_all_sales(
        sales, prices_dict
    )
    all_errors.extend(computation_errors)
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    output = format_output(total, execution_time, all_errors)
    
    display_results(output)
    
    try:
        write_results_to_file(output)
        print(f"\nResults have been saved to SalesResults.txt")
    except Exception as e:
        print(f"Error writing results to file: {e}")


if __name__ == "__main__":
    main()