/**
 * Customer Segmentation TypeScript Contract
 */
export interface ClusterSummaryItem {
  cluster: number;
  membership_tier: string;
  customer_count: number;
  customer_pct: number;
  recency_mean: number;
  recency_median: number;
  frequency_mean: number;
  frequency_median: number;
  monetary_mean: number;
  monetary_median: number;
  total_monetary: number;
  revenue_share_pct: number;
}

export interface KMeansEvaluationItem {
  k: number;
  inertia: number;
  silhouette_score: number;
}
