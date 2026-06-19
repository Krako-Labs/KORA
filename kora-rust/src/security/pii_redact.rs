use std::sync::OnceLock;
use regex::Regex;
use serde_json::Value;

// Regex patterns compiled once using std::sync::OnceLock
static EMAIL_REGEX: OnceLock<Regex> = OnceLock::new();
static SSN_REGEX: OnceLock<Regex> = OnceLock::new();
static CARD_REGEX: OnceLock<Regex> = OnceLock::new();
static PHONE_REGEX: OnceLock<Regex> = OnceLock::new();
static OPENAI_KEY_REGEX: OnceLock<Regex> = OnceLock::new();
static AWS_KEY_REGEX: OnceLock<Regex> = OnceLock::new();
static JWT_REGEX: OnceLock<Regex> = OnceLock::new();
static GITHUB_TOKEN_REGEX: OnceLock<Regex> = OnceLock::new();
static BEARER_TOKEN_REGEX: OnceLock<Regex> = OnceLock::new();

fn get_email_regex() -> &'static Regex {
    EMAIL_REGEX.get_or_init(|| {
        Regex::new(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b").unwrap()
    })
}

fn get_ssn_regex() -> &'static Regex {
    SSN_REGEX.get_or_init(|| {
        Regex::new(r"\b\d{3}-\d{2}-\d{4}\b").unwrap()
    })
}

fn get_card_regex() -> &'static Regex {
    CARD_REGEX.get_or_init(|| {
        Regex::new(r"\b(?:\d[ -]*?){13,19}\b").unwrap()
    })
}

fn get_phone_regex() -> &'static Regex {
    PHONE_REGEX.get_or_init(|| {
        Regex::new(r"(?:\+\d{1,3}[- ]?)?\(?\d{3}\)?[- ]?\d{3}[- ]?\d{4}").unwrap()
    })
}

fn get_openai_key_regex() -> &'static Regex {
    OPENAI_KEY_REGEX.get_or_init(|| {
        Regex::new(r"\bsk-[a-zA-Z0-9_-]{32,}\b").unwrap()
    })
}

fn get_aws_key_regex() -> &'static Regex {
    AWS_KEY_REGEX.get_or_init(|| {
        Regex::new(r"\bAKIA[0-9A-Z]{16}\b").unwrap()
    })
}

fn get_jwt_regex() -> &'static Regex {
    JWT_REGEX.get_or_init(|| {
        Regex::new(r"\beyJ[A-Za-z0-9-_=]+\.eyJ[A-Za-z0-9-_=]+\.[A-Za-z0-9-_+/=]+\b").unwrap()
    })
}

fn get_github_token_regex() -> &'static Regex {
    GITHUB_TOKEN_REGEX.get_or_init(|| {
        Regex::new(r"\bghp_[a-zA-Z0-9]{36,255}\b").unwrap()
    })
}

fn get_bearer_token_regex() -> &'static Regex {
    BEARER_TOKEN_REGEX.get_or_init(|| {
        Regex::new(r"(?i)\bbearer\s+[a-zA-Z0-9_\-\.\~/\+\=]{20,}\b").unwrap()
    })
}

/// Helper to check Luhn validity of potential credit card strings
fn is_luhn_valid(digits_str: &str) -> bool {
    let cleaned: String = digits_str.chars().filter(|c| c.is_ascii_digit()).collect();
    if cleaned.len() < 13 || cleaned.len() > 19 {
        return false;
    }

    let mut sum = 0;
    let mut double = false;

    for c in cleaned.chars().rev() {
        let mut digit = c.to_digit(10).unwrap();
        if double {
            digit *= 2;
            if digit > 9 {
                digit -= 9;
            }
        }
        sum += digit;
        double = !double;
    }

    sum % 10 == 0
}

/// Scan and redact PII patterns inside a string
pub fn redact_string(input: &str) -> String {
    let mut result = input.to_string();

    // 1. Redact OpenAI API Keys
    result = get_openai_key_regex().replace_all(&result, "[REDACTED_OPENAI_KEY]").into_owned();

    // 2. Redact AWS Access Keys
    result = get_aws_key_regex().replace_all(&result, "[REDACTED_AWS_KEY]").into_owned();

    // 3. Redact JWTs
    result = get_jwt_regex().replace_all(&result, "[REDACTED_JWT]").into_owned();

    // 4. Redact GitHub API Keys
    result = get_github_token_regex().replace_all(&result, "[REDACTED_GITHUB_TOKEN]").into_owned();

    // 5. Redact Bearer Tokens
    result = get_bearer_token_regex().replace_all(&result, "[REDACTED_BEARER_TOKEN]").into_owned();

    // 6. Redact Emails
    result = get_email_regex().replace_all(&result, "[REDACTED_EMAIL]").into_owned();

    // 7. Redact SSN
    result = get_ssn_regex().replace_all(&result, "[REDACTED_SSN]").into_owned();

    // 8. Redact Phone Numbers
    result = get_phone_regex().replace_all(&result, "[REDACTED_PHONE]").into_owned();

    // 9. Redact Credit Cards (requires Luhn check to prevent replacing random digit sequences)
    let card_re = get_card_regex();
    let mut offset = 0;
    let matches: Vec<(usize, usize, String)> = card_re
        .find_iter(&result)
        .map(|m| (m.start(), m.end(), m.as_str().to_string()))
        .collect();

    for (start, end, text) in matches {
        if is_luhn_valid(&text) {
            let actual_start = start - offset;
            let actual_end = end - offset;
            let replacement = "[REDACTED_CARD]";
            result.replace_range(actual_start..actual_end, replacement);
            offset += (end - start) - replacement.len();
        }
    }

    result
}

/// Recursively traverses and redacts PII/PCI inside a JSON structure
pub fn redact_json_value(value: &mut Value) {
    match value {
        Value::String(s) => {
            *s = redact_string(s);
        }
        Value::Array(arr) => {
            for item in arr.iter_mut() {
                redact_json_value(item);
            }
        }
        Value::Object(map) => {
            for (_, val) in map.iter_mut() {
                redact_json_value(val);
            }
        }
        _ => {}
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use serde_json::json;

    #[test]
    fn test_email_redaction() {
        assert_eq!(
            redact_string("Contact me at test@example.com immediately"),
            "Contact me at [REDACTED_EMAIL] immediately"
        );
    }

    #[test]
    fn test_ssn_redaction() {
        assert_eq!(
            redact_string("My SSN is 123-45-6789."),
            "My SSN is [REDACTED_SSN]."
        );
    }

    #[test]
    fn test_phone_redaction() {
        assert_eq!(
            redact_string("Call 123-456-7890"),
            "Call [REDACTED_PHONE]"
        );
    }

    #[test]
    fn test_luhn_validation_for_card() {
        // Valid Luhn card (using a typical test card number)
        let valid_card = "4111111111111111"; // standard test card
        assert!(is_luhn_valid(valid_card));
        
        let invalid_card = "4111111111111112";
        assert!(!is_luhn_valid(invalid_card));
    }

    #[test]
    fn test_json_payload_redaction() {
        let mut payload = json!({
            "user": "Alice",
            "details": {
                "email": "alice@site.co.uk",
                "phone": "+1 (555) 123-4567"
            },
            "history": [
                "Paid with card 4111-1111-1111-1111",
                "No PII here"
            ]
        });

        redact_json_value(&mut payload);

        assert_eq!(payload["details"]["email"], "[REDACTED_EMAIL]");
        assert_eq!(payload["details"]["phone"], "[REDACTED_PHONE]");
        assert_eq!(payload["history"][0], "Paid with card [REDACTED_CARD]");
    }

    #[test]
    fn test_secret_redaction() {
        assert_eq!(
            redact_string("My key is sk-proj-12345ABCDEabcdef12345ABCDEabcdef12345ABCDEabcdef"),
            "My key is [REDACTED_OPENAI_KEY]"
        );
        assert_eq!(
            redact_string("AWS ID: AKIAIOSFODNN7EXAMPLE"),
            "AWS ID: [REDACTED_AWS_KEY]"
        );
        assert_eq!(
            redact_string("Use this token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"),
            "Use this token: [REDACTED_JWT]"
        );
        assert_eq!(
            redact_string("GitHub token: ghp_1234567890abcdefghijklmnopqrstuvwxyzABCD"),
            "GitHub token: [REDACTED_GITHUB_TOKEN]"
        );
        assert_eq!(
            redact_string("Authorization: Bearer mySecretTokenValue12345!"),
            "Authorization: [REDACTED_BEARER_TOKEN]!"
        );
    }
}
