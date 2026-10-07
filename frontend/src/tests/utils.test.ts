import { describe, it, expect } from 'vitest';
import { formatCurrency } from '../utils/formatCurrency';
import { formatNumber, formatPercent } from '../utils/formatNumber';
import { formatDate } from '../utils/formatDate';

describe('Format Utilities QA Test Suite', () => {
  describe('formatCurrency', () => {
    it('should format standard positive values in GBP', () => {
      expect(formatCurrency(8291748.56)).toBe('£8,291,748.56');
      expect(formatCurrency(533.17)).toBe('£533.17');
    });

    it('should handle zero, null, undefined, and NaN gracefully', () => {
      expect(formatCurrency(0)).toBe('£0.00');
      expect(formatCurrency(null)).toBe('£0.00');
      expect(formatCurrency(undefined)).toBe('£0.00');
      expect(formatCurrency(NaN)).toBe('£0.00');
    });

    it('should format negative values (cancelled invoices)', () => {
      expect(formatCurrency(-150.5)).toBe('-£150.50');
    });
  });

  describe('formatNumber & formatPercent', () => {
    it('should format integers and floats', () => {
      expect(formatNumber(19960)).toBe('19,960');
      expect(formatNumber(4317)).toBe('4,317');
      expect(formatNumber(0)).toBe('0');
      expect(formatNumber(null)).toBe('0');
      expect(formatNumber(undefined)).toBe('0');
    });

    it('should format percentages with 1 decimal digit', () => {
      expect(formatPercent(63.7)).toBe('63.7%');
      expect(formatPercent(0)).toBe('0.0%');
      expect(formatPercent(null)).toBe('0%');
      expect(formatPercent(undefined)).toBe('0%');
    });
  });

  describe('formatDate', () => {
    it('should format standard ISO dates', () => {
      const formatted = formatDate('2011-12-09T12:50:00');
      expect(formatted).toBeTruthy();
      expect(formatted).not.toBe('N/A');
    });

    it('should handle null, undefined, empty string safely', () => {
      expect(formatDate(null)).toBe('N/A');
      expect(formatDate(undefined)).toBe('N/A');
      expect(formatDate('')).toBe('N/A');
      expect(formatDate('invalid-date')).toBe('N/A');
    });
  });
});
