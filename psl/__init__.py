import functools
import pathlib
import typing

__version__ = "2024.11.18"
__checksum__ = "82d97d01c11649527d9928a80a7f75d5124e952a"
__all__ = ["PUBLIC_SUFFIX_URL", "domain_suffixes", "Suffixes", "domain_can_set_cookie"]


PUBLIC_SUFFIX_URL = "https://publicsuffix.org/list/public_suffix_list.dat"
_PUBLIC_SUFFIX_PATH = pathlib.Path(__file__).parent / "psl.txt"


class Suffixes(typing.NamedTuple):
    public: typing.Optional[str]
    private: typing.Optional[str]


def domain_can_set_cookie(cookie_domain: str) -> bool:
    """Checks to see if a domain that was navigated to (http_domain) can set
    a cookie with a given 'Domain' attribute (cookie_domain).
    """

    def is_subdomain(child: str, parent: str) -> bool:
        child_labels = _labels_from_dn(child)
        parent_labels = _labels_from_dn(parent)
        rule = Rule(False, parent_labels)
        return rule.match(child_labels)

    suffixes = domain_suffixes(cookie_domain)
    if suffixes.private is None:
        return False
    elif not is_subdomain(cookie_domain, suffixes.private):
        return False

    return True


@functools.lru_cache(maxsize=1024)
def domain_suffixes(dn: str, *, icann_only: bool = False) -> Suffixes:
    """Gets the public and private suffixes of a given domain name

    :param str dn: Domain name to get the public and private suffixes of.
    :param bool icann_only:
        Flag to only use ICANN or IANA root zone domains instead of
        allowing privately owned domains/TLDs.
    """

    labels = _labels_from_dn(dn)

    if b"" in labels:  # Empty inner A-labels are not allowed.
        return Suffixes(private=None, public=None)

    matched_rule = None
    for rule in _load_public_suffix_list(labels, icann_only=icann_only):
        if matched_rule is None:
            matched_rule = rule
        elif len(matched_rule.labels) < len(rule.labels):
            matched_rule = rule
        elif rule.is_exception:
            matched_rule = rule
            break

    if matched_rule is None:
        matched_rule = Rule(False, (b"*",))

    rules_to_match = list(matched_rule.labels)
    if matched_rule.is_exception:
        rules_to_match.pop(0)

    public_suffix: typing.Optional[str]
    if rules_to_match:
        public_suffix = _labels_to_dn(labels[-len(rules_to_match) :])
        if len(rules_to_match) == len(labels):
            private_suffix = None
        else:
            private_suffix = _labels_to_dn(labels[-len(rules_to_match) - 1 :])
    else:
        public_suffix = None
        private_suffix = _labels_to_dn(labels)

    return Suffixes(public=public_suffix, private=private_suffix)


class Rule(typing.NamedTuple):
    is_exception: bool
    labels: typing.Tuple[bytes, ...]

    def match(self, labels: typing.Tuple[bytes, ...]) -> bool:
        self_len = len(self.labels)
        return len(labels) >= self_len and all(
            self.labels[i] in (b"*", labels[i]) for i in range(-self_len, 0, 1)
        )


def _load_public_suffix_list(
    labels: typing.Tuple[bytes, ...], icann_only: bool = False
) -> typing.Iterable[Rule]:
    with open(_PUBLIC_SUFFIX_PATH) as f:
        for line in f:
            line = line.strip()
            if icann_only and "===END ICANN DOMAINS===" in line:
                break
            if not line or line.startswith("//"):
                continue
            is_exception = line[0] == "!"
            line = line.lstrip("!")
            rule = Rule(is_exception, _labels_from_dn(line))
            if rule.match(labels):
                yield rule


def _labels_from_dn(dn: str) -> typing.Tuple[bytes, ...]:
    """Splits a domain name into A-labels. Does IDNA encoding if needed"""
    if dn.startswith("."):
        dn = dn[1:]
    if dn.endswith("."):
        dn = dn[:-1]
    for char in dn:
        if ord(char) > 0x7F:
            raise ValueError(f"Domain name '{dn}' is not IDNA-encoded")
    return tuple((label.encode() for label in dn.lower().split(".")))


def _labels_to_dn(labels: typing.Tuple[bytes, ...]) -> str:
    return (b".".join(labels)).decode()
