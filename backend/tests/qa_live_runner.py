"""
Script QA Live Runner with AsyncClient (replicates Uvicorn lifecycle)
"""
import sys
import asyncio
from pathlib import Path
import pandas as pd
import httpx

BACKEND_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BACKEND_DIR.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.main import app
from app.core.mongodb import mongodb_manager

errors = []

async def run_live_qa():
    # Lifespan: connect once in the running loop
    mongodb_manager.connect()
    
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        async def test_endpoint(name, method, url, expected_status=200):
            resp = await client.request(method, url)
            if resp.status_code != expected_status:
                err = f"FAIL {name}: {method} {url} returned {resp.status_code}, expected {expected_status}. Body: {resp.text}"
                errors.append(err)
                print(err)
                return None
            print(f"PASS {name}: {method} {url} -> {resp.status_code}")
            if "application/json" in resp.headers.get("content-type", ""):
                return resp.json()
            return resp.text

        print("==================================================")
        print("1. HEALTH & METADATA TESTS")
        print("==================================================")
        await test_endpoint("Health", "GET", "/health")
        await test_endpoint("DB Health", "GET", "/health/db")
        await test_endpoint("Swagger Docs", "GET", "/docs")
        await test_endpoint("Redoc", "GET", "/redoc")
        await test_endpoint("OpenAPI Schema", "GET", "/api/v1/openapi.json")

        print("\n==================================================")
        print("2. DASHBOARD ENDPOINTS")
        print("==================================================")
        summary = await test_endpoint("Dashboard Summary", "GET", "/api/v1/dashboard/summary")
        revenue_trend = await test_endpoint("Revenue Trend", "GET", "/api/v1/dashboard/revenue-trend")
        top_products = await test_endpoint("Top Products", "GET", "/api/v1/dashboard/top-products")
        top_countries = await test_endpoint("Top Countries", "GET", "/api/v1/dashboard/top-countries")

        print("\n==================================================")
        print("3. SALES ENDPOINTS")
        print("==================================================")
        sales_monthly = await test_endpoint("Sales Monthly", "GET", "/api/v1/sales/monthly")
        sales_products = await test_endpoint("Sales Products Paginated", "GET", "/api/v1/sales/products?page=1&page_size=10")
        sales_countries = await test_endpoint("Sales Countries", "GET", "/api/v1/sales/countries")
        sales_invoices = await test_endpoint("Sales Invoices Paginated", "GET", "/api/v1/sales/invoices?page=1&page_size=10")

        print("\n==================================================")
        print("4. CUSTOMER & SEGMENTATION ENDPOINTS")
        print("==================================================")
        customers = await test_endpoint("Customers Paginated", "GET", "/api/v1/customers?page=1&page_size=10")
        if customers and customers.get("items"):
            cust_id = customers["items"][0]["customer_id"]
            await test_endpoint("Customer Detail", "GET", f"/api/v1/customers/{cust_id}")

        seg_summary = await test_endpoint("Segmentation Summary", "GET", "/api/v1/segmentation/summary")
        seg_cluster_0 = await test_endpoint("Cluster 0 Detail", "GET", "/api/v1/segmentation/clusters/0")
        seg_eval = await test_endpoint("Segmentation Evaluation", "GET", "/api/v1/segmentation/evaluation")

        print("\n==================================================")
        print("5. STATISTICS ENDPOINTS")
        print("==================================================")
        stat_tests = await test_endpoint("Statistical Tests", "GET", "/api/v1/statistics/tests")
        inv_value_sum = await test_endpoint("Invoice Value Summary", "GET", "/api/v1/statistics/invoice-value-summary")

        print("\n==================================================")
        print("6. EDGE CASES & VALIDATION TESTS")
        print("==================================================")
        await test_endpoint("Invalid Page (0)", "GET", "/api/v1/sales/products?page=0", expected_status=422)
        await test_endpoint("Invalid Page Size (0)", "GET", "/api/v1/sales/products?page_size=0", expected_status=422)
        await test_endpoint("Invalid Page Size (>100)", "GET", "/api/v1/sales/products?page_size=101", expected_status=422)
        await test_endpoint("Invalid Range (min > max)", "GET", "/api/v1/customers?min_monetary=1000&max_monetary=100", expected_status=400)
        await test_endpoint("Nonexistent Customer ID", "GET", "/api/v1/customers/NOT_FOUND_99999", expected_status=404)
        await test_endpoint("Nonexistent Cluster ID", "GET", "/api/v1/segmentation/clusters/999", expected_status=404)
        await test_endpoint("Invalid Cluster ID Type", "GET", "/api/v1/segmentation/clusters/abc", expected_status=422)
        await test_endpoint("Nonexistent Endpoint", "GET", "/api/v1/unknown_route", expected_status=404)

        print("\n==================================================")
        print("7. DATA CONSISTENCY CHECK AGAINST CSV FILES")
        print("==================================================")
        # Check 1: monthly_revenue.csv
        monthly_csv_path = PROJECT_ROOT / "outputs" / "tables" / "monthly_revenue.csv"
        if monthly_csv_path.exists() and revenue_trend:
            df_m = pd.read_csv(monthly_csv_path)
            csv_total_rev = round(df_m["NetRevenue"].sum(), 2)
            api_items = revenue_trend["items"] if isinstance(revenue_trend, dict) else revenue_trend
            api_total_rev = round(sum(item["revenue"] for item in api_items), 2)
            diff = abs(csv_total_rev - api_total_rev)
            if diff < 0.01:
                print(f"CONSISTENCY PASS: monthly_revenue sum: CSV={csv_total_rev} == API={api_total_rev}")
            else:
                err = f"CONSISTENCY MISMATCH: monthly_revenue sum: CSV={csv_total_rev} != API={api_total_rev}"
                errors.append(err)
                print(err)

        # Check 2: customer_segments_summary.csv
        seg_csv_path = PROJECT_ROOT / "outputs" / "tables" / "customer_segments_summary.csv"
        if seg_csv_path.exists() and seg_summary:
            df_s = pd.read_csv(seg_csv_path)
            csv_cust_count = int(df_s["CustomerCount"].sum())
            api_cust_count = sum(c["customer_count"] for c in seg_summary)
            if csv_cust_count == api_cust_count:
                print(f"CONSISTENCY PASS: customer_segments customer count: CSV={csv_cust_count} == API={api_cust_count}")
            else:
                err = f"CONSISTENCY MISMATCH: customer_segments count: CSV={csv_cust_count} != API={api_cust_count}"
                errors.append(err)
                print(err)

        # Check 3: statistical_tests_summary.csv
        stat_csv_path = PROJECT_ROOT / "outputs" / "tables" / "statistical_tests_summary.csv"
        if stat_csv_path.exists() and stat_tests:
            df_stat = pd.read_csv(stat_csv_path)
            csv_rows = len(df_stat)
            api_rows = len(stat_tests)
            if csv_rows == api_rows:
                print(f"CONSISTENCY PASS: statistical_tests count: CSV={csv_rows} == API={api_rows}")
            else:
                err = f"CONSISTENCY MISMATCH: statistical_tests: CSV={csv_rows} != API={api_rows}"
                errors.append(err)
                print(err)

        # Check 4: kmeans_evaluation_metrics.csv
        kmeans_csv_path = PROJECT_ROOT / "outputs" / "tables" / "kmeans_evaluation_metrics.csv"
        if kmeans_csv_path.exists() and seg_eval:
            df_k = pd.read_csv(kmeans_csv_path)
            csv_k = len(df_k)
            api_k = len(seg_eval)
            if csv_k == api_k:
                print(f"CONSISTENCY PASS: kmeans_evaluation count: CSV={csv_k} == API={api_k}")
            else:
                err = f"CONSISTENCY MISMATCH: kmeans_evaluation: CSV={csv_k} != API={api_k}"
                errors.append(err)
                print(err)

        # Check 5: top_products_revenue.csv
        top_p_csv_path = PROJECT_ROOT / "outputs" / "tables" / "top_products_revenue.csv"
        if top_p_csv_path.exists() and top_products:
            df_top_p = pd.read_csv(top_p_csv_path)
            csv_top_code = str(df_top_p.iloc[0]["StockCode"])
            api_top_code = str(top_products[0]["stock_code"])
            if csv_top_code == api_top_code:
                print(f"CONSISTENCY PASS: top_product #1: CSV={csv_top_code} == API={api_top_code}")
            else:
                err = f"CONSISTENCY MISMATCH: top_product #1: CSV={csv_top_code} != API={api_top_code}"
                errors.append(err)
                print(err)

        # Check 6: country_revenue.csv
        country_csv_path = PROJECT_ROOT / "outputs" / "tables" / "country_revenue.csv"
        if country_csv_path.exists() and top_countries:
            df_country = pd.read_csv(country_csv_path)
            csv_top_country = str(df_country.iloc[0]["Country"])
            api_top_country = str(top_countries[0]["country"])
            if csv_top_country == api_top_country:
                print(f"CONSISTENCY PASS: top_country #1: CSV={csv_top_country} == API={api_top_country}")
            else:
                err = f"CONSISTENCY MISMATCH: top_country #1: CSV={csv_top_country} != API={api_top_country}"
                errors.append(err)
                print(err)

    mongodb_manager.close()
    print("\n==================================================")
    print(f"FINAL RESULT: {len(errors)} errors found.")
    print("==================================================")

asyncio.run(run_live_qa())
sys.exit(0 if len(errors) == 0 else 1)
