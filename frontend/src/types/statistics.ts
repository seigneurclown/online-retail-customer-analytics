/**
 * Statistical Tests TypeScript Contract
 */
export interface StatisticalTestItem {
  id: number;
  research_question: string;
  test_name: string;
  reason: string;
  test_statistic: string;
  p_value: number | null;
  significance_level: string;
  conclusion: string;
}

export interface InvoiceValueSummaryItem {
  metric: string;
  value: number;
}
