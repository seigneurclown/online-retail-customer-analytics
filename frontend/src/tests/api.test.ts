import { describe, it, expect } from 'vitest';
import { formatApiErrorMessage } from '../services/api';

describe('API Error Handling QA Test Suite', () => {
  it('should parse FastAPI Pydantic 422 array errors into human-readable strings', () => {
    const errorObj = {
      isAxiosError: true,
      response: {
        status: 422,
        data: {
          detail: [
            { loc: ['query', 'min_monetary'], msg: 'Input should be greater than or equal to 0' },
            { loc: ['query', 'page'], msg: 'Input should be a valid integer' },
          ],
        },
      },
    };

    const message = formatApiErrorMessage(errorObj);
    expect(message).toContain('Input should be greater than or equal to 0');
    expect(message).toContain('Input should be a valid integer');
  });

  it('should handle string error details', () => {
    const errorObj = {
      isAxiosError: true,
      response: {
        status: 404,
        data: {
          detail: 'Customer with ID 99999 not found.',
        },
      },
    };

    const message = formatApiErrorMessage(errorObj);
    expect(message).toBe('Customer with ID 99999 not found.');
  });

  it('should handle server unreachable / network disconnect', () => {
    const errorObj = {
      isAxiosError: true,
      request: {},
    };

    const message = formatApiErrorMessage(errorObj);
    expect(message).toContain('Cannot reach backend server');
  });

  it('should handle generic standard errors', () => {
    const err = new Error('Generic internal exception');
    expect(formatApiErrorMessage(err)).toBe('Generic internal exception');
    expect(formatApiErrorMessage('Unknown string error')).toBe('An unexpected network error occurred.');
  });
});
