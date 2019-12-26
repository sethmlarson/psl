import functools
import pathlib
import typing

import idna

__version__ = "2019.12.26"
__checksum__ = "290274492d9b317cb2210ad866ac9c714340ddd1"
__all__ = ["PUBLIC_SUFFIX_URL", "domain_suffixes", "Suffixes", "domain_can_set_cookie"]


PUBLIC_SUFFIX_URL = "https://publicsuffix.org/list/public_suffix_list.dat"
PUBLIC_SUFFIX_PATH = pathlib.Path(__file__).parent / "psl.txt"


class Suffixes(typing.NamedTuple):
    public: typing.Optional[str]
    private: typing.Optional[str]


def domain_can_set_cookie(*, http_domain: str, cookie_domain: str) -> bool:
    """Checks to see if a domain that was navigated to (http_domain) can set
    a cookie with a given 'Domain' attribute (cookie_domain).
    """
    if (
        "*" in http_domain
        or _contains_empty_labels(http_domain)
        or _contains_empty_labels(cookie_domain)
    ):
        return False

    def is_subdomain(child: str, parent: str) -> bool:
        child_labels = _labels_from_dn(child)
        parent_labels = _labels_from_dn(parent)
        rule = Rule(False, parent_labels)
        return rule.match(child_labels)

    # See if the cookie_domain is a sub-domain of http_domain
    if not is_subdomain(http_domain, cookie_domain):
        return False

    suffixes = domain_suffixes(http_domain)
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

    if _contains_empty_labels(dn):  # Empty A-labels are not allowed.
        return Suffixes(private=None, public=None)

    labels = _labels_from_dn(dn)

    # For security reasons disallow cookies for 'localhost' and '.local' domains
    if labels[-1] == b"local" or labels == [b"localhost"]:
        return Suffixes(private=None, public=labels[-1].decode("ascii"))

    matched_rule = None
    for rule in _load_public_suffix_list(icann_only=icann_only):
        if rule.match(labels):
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


def _load_public_suffix_list(icann_only: bool = False) -> typing.Iterable[Rule]:
    with open(PUBLIC_SUFFIX_PATH) as f:
        for line in f:
            line = line.strip()
            if icann_only and "===END ICANN DOMAINS===" in line:
                break
            if not line or line.startswith("//"):
                continue
            is_exception = line[0] == "!"
            line = line.lstrip("!")
            yield Rule(is_exception, _labels_from_dn(line))


def _labels_from_dn(dn: str) -> typing.Tuple[bytes, ...]:
    """Splits a domain name into A-labels. Does IDNA encoding if needed"""
    if dn.endswith("."):
        raise ValueError(f"Domain name '{dn}' ends with a dot")
    return tuple(
        [
            typing.cast(
                bytes,
                (
                    label.encode()
                    if all(ord(c) <= 0x7F for c in label)
                    else idna.encode(label, strict=True, std3_rules=True)
                ),
            )
            for label in dn.lower().split(".")
        ]
    )


def _labels_to_dn(labels: typing.Tuple[bytes, ...]) -> str:
    return (b".".join(labels)).decode()


def _contains_empty_labels(dn: str) -> bool:
    return "" in dn.split(".")
