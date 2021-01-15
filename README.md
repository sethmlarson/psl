# psl

[![Version](https://img.shields.io/pypi/v/psl)](https://pypi.org/project/psl)
[![Downloads](https://pepy.tech/badge/psl)](https://pepy.tech/project/psl)
![CI](https://img.shields.io/github/workflow/status/sethmlarson/psl/CI/master)

Mozilla Public Suffix list as a Python package and updated daily.

Install via `python -m pip install psl`

See https://publicsuffix.org for more information regarding the list itself.

## API

The package provides the following members as an API:

### `domain_suffixes()`

```python
def domain_suffixes(dn: str, *, icann_only: bool=False) -> Suffixes: ...
```

Queries the Public Suffix list for the given domain and returns a named tuple containing
the public and private suffixes for the domain.  Either value can be `None` if that
field isn't available. (eg `private=None` for the domain `com`)

### `domain_can_set_cookie()`

```python
def domain_can_set_cookie(*, http_domain: str, cookie_domain: str) -> bool: ...
```

Determines if a user-agent that receives an HTTP response from domain `<http_domain>`
with `Set-Cookie` headers with parameter `Domain=<cookie_domain>` should allow
that cookie to be set.  This disallows cookies from being set on public suffixes
and on domains that the HTTP domain has no authority over.

This is the same mechanism that modern browsers use to determine whether it's safe
to set a cookie to prevent 'super-cookies'.

## License

MPL-2.0
