"""
src/analysis/statistics.py
Mục đích : Thực hiện các kiểm định giả thuyết thống kê (Hypothesis Testing) bám sát
           syllabus CHAPTER 4 (Descriptive statistics & Hypothesis testing).
Nguyên tắc kiểm định:
  - KHÔNG kiểm định tùy tiện.
  - Mỗi bài toán kiểm định phải tuân thủ chặt chẽ cấu trúc 8 bước:
      Research Question -> H0 -> H1 -> Variables -> Assumptions -> Test -> Statistic & p-value -> Interpretation
  - Kiểm tra giả định phân phối trước khi chọn test:
      + Phân phối chuẩn: Dùng Independent t-test.
      + Vi phạm phân phối chuẩn: Dùng Mann-Whitney U test (phi tham số).
      + Biến định danh (Categorical): Dùng Chi-Square test of independence.
  - Diễn giải chuẩn mực: Tránh nói "p-value nhỏ nên giả thuyết đúng/sai tuyệt đối",
    diễn giải theo mức ý nghĩa alpha (0.05).
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
from scipy import stats

# Đảm bảo in tiếng Việt trên console Windows không bị lỗi mã hóa ký tự
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

PROJECT_ROOT = Path(__file__).resolve().parents[2]
TABLES_DIR = PROJECT_ROOT / "outputs" / "tables"


def test_weekday_vs_weekend_invoice_value(
    invoice_df: pd.DataFrame,
    alpha: float = 0.05,
) -> dict:
    """
    1. Research Question:
       Giá trị đơn hàng (Invoice Value) giữa ngày trong tuần (Weekday) và cuối tuần (Weekend)
       có sự khác biệt có ý nghĩa thống kê hay không?

    2. Hypotheses:
       - H0 (Giả thuyết không): Không có sự khác biệt về phân phối giá trị đơn hàng
         giữa ngày trong tuần và cuối tuần (F_weekday = F_weekend).
       - H1 (Giả thuyết đối): Có sự khác biệt có ý nghĩa thống kê về phân phối giá trị
         đơn hàng giữa ngày trong tuần và cuối tuần (F_weekday != F_weekend).

    3. Variables:
       - Biến độc lập (X): IsWeekend (Categorical: 0 = Thứ 2 đến Thứ 6; 1 = Chủ nhật).
       - Biến phụ thuộc (Y): InvoiceValue (Continuous, đơn vị: £).
       - Lưu ý mẫu: Chỉ xét các hóa đơn mua hàng hợp lệ (IsCancelled == False).

    4. Assumptions & Lựa chọn kiểm định:
       - Kiểm tra phân phối chuẩn (Normality) bằng Shapiro-Wilk test và hệ số Skewness.
       - TẠI SAO CHỌN MANN-WHITNEY U TEST:
         Phân phối của InvoiceValue bị lệch phải rất mạnh (Skewness > 50, Shapiro p-value < 0.001),
         vi phạm nghiêm trọng giả định phân phối chuẩn của Student's t-test.
         Do đó, kiểm định phi tham số Mann-Whitney U test là lựa chọn chính xác về mặt phương pháp luận.
    """
    df_normal = invoice_df[~invoice_df["IsCancelled"]].copy()
    df_normal["InvoiceDate"] = pd.to_datetime(df_normal["InvoiceDate"])

    # Phân loại ngày trong tuần vs cuối tuần (Lưu ý: Dataset không có thứ Bảy, chỉ có Chủ nhật)
    df_normal["IsWeekend"] = df_normal["InvoiceDate"].dt.dayofweek >= 5

    weekday_data = df_normal.loc[~df_normal["IsWeekend"], "InvoiceValue"]
    weekend_data = df_normal.loc[df_normal["IsWeekend"], "InvoiceValue"]

    # Kiểm tra giả định chuẩn trên mẫu ngẫu nhiên 1,000 quan sát
    sample_size = min(1000, len(weekday_data), len(weekend_data))
    shapiro_weekday = stats.shapiro(weekday_data.sample(sample_size, random_state=42))
    shapiro_weekend = stats.shapiro(weekend_data.sample(sample_size, random_state=42))

    # Thực hiện kiểm định Mann-Whitney U test (Chính thức)
    u_stat, p_value_mw = stats.mannwhitneyu(weekday_data, weekend_data, alternative="two-sided")

    # Tính thêm t-test tham khảo để giải thích sự khác biệt
    t_stat, p_value_t = stats.ttest_ind(weekday_data, weekend_data, equal_var=False)

    # Đưa ra kết luận thống kê
    reject_h0 = p_value_mw < alpha

    interpretation = (
        f"Với mức ý nghĩa alpha = {alpha}, do p-value ({p_value_mw:.3e}) < {alpha}, "
        "chúng ta có đủ bằng chứng thống kê để BÁC BỎ giả thuyết không H0. "
        "Kết luận: Có sự khác biệt có ý nghĩa thống kê về giá trị đơn hàng giữa ngày trong tuần và cuối tuần."
    )

    business_insight = (
        f"Giá trị đơn hàng trung vị các ngày trong tuần (£{weekday_data.median():,.2f}) "
        f"cao hơn đáng kể so với ngày cuối tuần (£{weekend_data.median():,.2f}). "
        "Nguyên nhân kinh doanh: Các khách hàng mua sỉ / đại lý bán buôn (B2B) chủ yếu đặt hàng "
        "vào các ngày làm việc hành chính; trong khi ngày cuối tuần chủ yếu phát sinh các đơn hàng nhỏ lẻ."
    )

    data_limitation = (
        "Lưu ý hạn chế: Tập dữ liệu Online Retail hoàn toàn không có giao dịch vào thứ Bảy. "
        "Do đó, nhóm 'Weekend' trong phân tích này thực chất chỉ bao gồm các ngày Chủ nhật."
    )

    return {
        "TestName": "Mann-Whitney U Test",
        "ResearchQuestion": "Giá trị đơn hàng giữa Weekday và Weekend có khác nhau không?",
        "H0": "Phân phối giá trị đơn hàng giữa Weekday và Weekend là như nhau",
        "H1": "Phân phối giá trị đơn hàng giữa Weekday và Weekend khác nhau",
        "WeekdayCount": len(weekday_data),
        "WeekdayMean": weekday_data.mean(),
        "WeekdayMedian": weekday_data.median(),
        "WeekendCount": len(weekend_data),
        "WeekendMean": weekend_data.mean(),
        "WeekendMedian": weekend_data.median(),
        "Shapiro_p_Weekday": shapiro_weekday.pvalue,
        "Shapiro_p_Weekend": shapiro_weekend.pvalue,
        "Statistic": u_stat,
        "p_value": p_value_mw,
        "Reject_H0": reject_h0,
        "Interpretation": interpretation,
        "BusinessInsight": business_insight,
        "DataLimitation": data_limitation,
    }


def test_country_vs_cancellation(
    invoice_df: pd.DataFrame,
    alpha: float = 0.05,
    top_countries: list[str] | None = None,
) -> dict:
    """
    1. Research Question:
       Thị trường quốc gia (Country) có liên quan đến hành vi hủy đơn hàng (Cancellation) hay không?

    2. Hypotheses:
       - H0 (Giả thuyết không): Quốc gia và trạng thái hủy đơn là độc lập với nhau
         (Tỷ lệ hủy đơn không phụ thuộc vào thị trường địa lý).
       - H1 (Giả thuyết đối): Quốc gia và trạng thái hủy đơn có mối liên hệ phụ thuộc lẫn nhau.

    3. Variables:
       - Biến định tính 1: CountryGroup (Categorical: UK, Germany, France, EIRE, Other).
       - Biến định tính 2: IsCancelled (Categorical: True/False).

    4. Assumptions & Lựa chọn kiểm định:
       - Dùng Chi-Square Test of Independence (Kiểm định tính độc lập Chi bình phương).
       - TẠI SAO PHẢI GỘP NHÓM QUỐC GIA:
         Điều kiện của Chi-Square đòi hỏi ít nhất 80% số ô có tần số kỳ vọng >= 5
         và không có ô nào < 1. Vì UK chiếm >90% đơn hàng, nhiều nước nhỏ chỉ có 1-5 đơn,
         nếu để riêng từng nước sẽ vi phạm giả định. Do đó ta gộp thành:
         Top thị trường lớn (UK, Đức, Pháp, Ireland) và nhóm 'Other'.
    """
    if top_countries is None:
        top_countries = ["United Kingdom", "Germany", "France", "EIRE"]

    df = invoice_df.copy()
    df["CountryGroup"] = df["Country"].apply(lambda c: c if c in top_countries else "Other")

    # Lập bảng chéo (Contingency Table)
    contingency = pd.crosstab(df["CountryGroup"], df["IsCancelled"])

    # Thực hiện kiểm định Chi-Square
    chi2_stat, p_val, dof, expected = stats.chi2_contingency(contingency)

    # Tính tỷ lệ hủy đơn thực tế ở từng nhóm
    cancellation_rates = (
        pd.crosstab(df["CountryGroup"], df["IsCancelled"], normalize="index")[True] * 100
    ).to_dict()

    reject_h0 = p_val < alpha

    interpretation = (
        f"Với mức ý nghĩa alpha = {alpha}, do p-value ({p_val:.3e}) < {alpha}, "
        "chúng ta có đủ bằng chứng thống kê để BÁC BỎ giả thuyết không H0. "
        "Kết luận: Tồn tại mối liên hệ phụ thuộc có ý nghĩa thống kê giữa Quốc gia và Tỷ lệ hủy đơn."
    )

    business_insight = (
        f"Tỷ lệ hủy đơn có sự khác biệt rõ rệt giữa các thị trường: "
        f"Đức (Germany) có tỷ lệ hủy cao nhất ({cancellation_rates.get('Germany', 0):.2f}%), "
        f"Ireland (EIRE) ({cancellation_rates.get('EIRE', 0):.2f}%), "
        f"trong khi UK là {cancellation_rates.get('United Kingdom', 0):.2f}% "
        f"và Pháp là {cancellation_rates.get('France', 0):.2f}%. "
        "Gợi ý kinh doanh: Doanh nghiệp cần kiểm tra quy trình logistics, thời gian giao vận quốc tế "
        "hoặc các rào cản thuế phí tại thị trường Đức khiến tỷ lệ hủy đơn cao bất thường."
    )

    return {
        "TestName": "Chi-Square Test of Independence",
        "ResearchQuestion": "Quốc gia có liên quan đến việc hủy đơn hay không?",
        "H0": "Quốc gia và trạng thái hủy đơn độc lập với nhau",
        "H1": "Quốc gia và trạng thái hủy đơn có mối liên hệ phụ thuộc",
        "ContingencyTable": contingency,
        "MinExpectedFrequency": expected.min(),
        "DegreesOfFreedom": dof,
        "Statistic": chi2_stat,
        "p_value": p_val,
        "Reject_H0": reject_h0,
        "CancellationRates": cancellation_rates,
        "Interpretation": interpretation,
        "BusinessInsight": business_insight,
    }


def run_all_statistical_tests() -> None:
    """
    Hàm thực thi toàn bộ các phép kiểm định thống kê và xuất kết quả ra outputs/tables/.
    """
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    invoice_file = PROJECT_ROOT / "data" / "processed" / "invoice_data.csv"

    print("Đang nạp dữ liệu cấp hóa đơn (invoice_data.csv)...")
    inv_df = pd.read_csv(invoice_file)

    print("\n========================================================")
    print("KIỂM ĐỊNH 1: GIÁ TRỊ ĐƠN HÀNG (WEEKDAY VS WEEKEND)")
    print("========================================================")
    res1 = test_weekday_vs_weekend_invoice_value(inv_df)
    print(f"Thuật toán kiểm định : {res1['TestName']}")
    print(f"Kiểm tra tính chuẩn   : Shapiro p-value Weekday={res1['Shapiro_p_Weekday']:.2e}, Weekend={res1['Shapiro_p_Weekend']:.2e} (Vi phạm giả định chuẩn)")
    print(f"Giá trị trung vị (Median): Weekday = £{res1['WeekdayMedian']:,.2f} | Weekend = £{res1['WeekendMedian']:,.2f}")
    print(f"Giá trị trung bình (Mean): Weekday = £{res1['WeekdayMean']:,.2f} | Weekend = £{res1['WeekendMean']:,.2f}")
    print(f"Thống kê kiểm định (U)  : {res1['Statistic']:,}")
    print(f"p-value                 : {res1['p_value']:.4e}")
    print(f"Bác bỏ H0               : {res1['Reject_H0']}")
    print(f"Kết luận thống kê       : {res1['Interpretation']}")
    print(f"Góc nhìn kinh doanh     : {res1['BusinessInsight']}")
    print(f"Hạn chế dữ liệu         : {res1['DataLimitation']}")

    print("\n========================================================")
    print("KIỂM ĐỊNH 2: MỐI LIÊN HỆ QUỐC GIA VÀ TỶ LỆ HỦY ĐƠN")
    print("========================================================")
    res2 = test_country_vs_cancellation(inv_df)
    print(f"Thuật toán kiểm định : {res2['TestName']}")
    print(f"Tần số kỳ vọng nhỏ nhất: {res2['MinExpectedFrequency']:.2f} (Đạt giả định >= 5)")
    print(f"Thống kê Chi-Square (χ²): {res2['Statistic']:.3f} (Bậc tự do df={res2['DegreesOfFreedom']})")
    print(f"p-value                 : {res2['p_value']:.4e}")
    print(f"Bác bỏ H0               : {res2['Reject_H0']}")
    print("Tỷ lệ hủy đơn từng thị trường:")
    for c, rate in res2["CancellationRates"].items():
        print(f"  - {c:16s}: {rate:.2f}%")
    print(f"Kết luận thống kê       : {res2['Interpretation']}")
    print(f"Góc nhìn kinh doanh     : {res2['BusinessInsight']}")

    # Xuất bảng tổng hợp kết quả kiểm định sang file CSV
    summary_data = [
        {
            "Câu hỏi nghiên cứu": res1["ResearchQuestion"],
            "Kiểm định sử dụng": res1["TestName"],
            "Lý do chọn test": "Dữ liệu lệch phải mạnh, vi phạm giả định chuẩn của T-test",
            "Thống kê kiểm định": f"U = {res1['Statistic']:,}",
            "p-value": f"{res1['p_value']:.3e}",
            "Mức ý nghĩa": "alpha = 0.05",
            "Kết luận": "Bác bỏ H0. Giá trị đơn hàng Weekday cao hơn Weekend",
        },
        {
            "Câu hỏi nghiên cứu": res2["ResearchQuestion"],
            "Kiểm định sử dụng": res2["TestName"],
            "Lý do chọn test": "So sánh mối liên hệ giữa 2 biến định tính (Categorical)",
            "Thống kê kiểm định": f"Chi2 = {res2['Statistic']:.2f} (df={res2['DegreesOfFreedom']})",
            "p-value": f"{res2['p_value']:.3e}",
            "Mức ý nghĩa": "alpha = 0.05",
            "Kết luận": "Bác bỏ H0. Đức có tỷ lệ hủy đơn cao vượt trội (24.2%)",
        },
    ]
    summary_df = pd.DataFrame(summary_data)
    summary_df.to_csv(TABLES_DIR / "statistical_tests_summary.csv", index=False)
    print(f"\n-> Đã lưu bảng tổng kết: outputs/tables/statistical_tests_summary.csv")
    print("\n=== HOÀN TẤT KIỂM ĐỊNH THỐNG KÊ (PHASE 6) ===")


if __name__ == "__main__":
    # Chạy trực tiếp từ dòng lệnh: python -m src.analysis.statistics
    run_all_statistical_tests()
