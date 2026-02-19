import re
from urllib.parse import urlparse

def extract_features(url):
    """
    Extracts features from a URL for phishing detection.
    Returns a dictionary of features.
    """
    features = {}
    
    # URL Length
    features['url_length'] = len(url)
    
    # Presence of @ symbol
    features['has_at'] = 1 if '@' in url else 0
    
    # Number of dots
    features['dot_count'] = url.count('.')
    
    # Presence of IP address instead of domain
    ip_pattern = r'(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])'
    features['has_ip'] = 1 if re.search(ip_pattern, url) else 0
    
    # Prefix-Suffix separation (Checking for '-' in domain)
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    features['has_dash_in_domain'] = 1 if '-' in domain else 0
    
    # Number of subdomains
    # e.g., www.google.com -> netloc is www.google.com, dots = 2 -> subdomains approx
    if domain:
        features['num_subdomains'] = domain.count('.')
    else:
        features['num_subdomains'] = 0
        
    # HTTPS usage
    features['is_https'] = 1 if parsed_url.scheme == 'https' else 0
    
    # Suspicious keywords
    suspicious_words = ['login', 'verify', 'update', 'secure', 'account', 'banking', 'confirm']
    features['suspicious_word_count'] = sum(1 for word in suspicious_words if word in url.lower())
    
    # URL Depth (number of directories)
    path = parsed_url.path
    features['url_depth'] = path.count('/')
    
    # Presence of HTTP in path (e.g., http://example.com/http://another.com)
    features['has_http_in_path'] = 1 if 'http' in path.lower() else 0

    return features

if __name__ == "__main__":
    # Test
    test_url = "http://secure-login-verify.com/account/update?id=123"
    print(f"Features for {test_url}:")
    print(extract_features(test_url))
