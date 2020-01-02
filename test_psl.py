import pytest

import psl


@pytest.mark.parametrize(
    ["dn", "private_suffix"],
    [
        ("COM", None),
        ("example.COM", "example.com"),
        ("WwW.example.COM", "example.com"),
        (".com", None),
        (".example", None),
        ("example..com", None),
        (".example.com", "example.com"),
        (".example.example.", "example.example"),
        ("example", None),
        ("example.example", "example.example"),
        ("b.example.example", "example.example"),
        ("a.b.example.example", "example.example"),
        ("biz", None),
        ("domain.biz", "domain.biz"),
        ("b.domain.biz", "domain.biz"),
        ("a.b.domain.biz", "domain.biz"),
        ("com", None),
        ("example.com", "example.com"),
        ("b.example.com", "example.com"),
        ("a.b.example.com", "example.com"),
        ("uk.com", None),
        ("example.uk.com", "example.uk.com"),
        ("b.example.uk.com", "example.uk.com"),
        ("a.b.example.uk.com", "example.uk.com"),
        ("test.ac", "test.ac"),
        ("mm", None),
        ("c.mm", None),
        ("b.c.mm", "b.c.mm"),
        ("a.b.c.mm", "b.c.mm"),
        ("jp", None),
        ("test.jp", "test.jp"),
        ("www.test.jp", "test.jp"),
        ("ac.jp", None),
        ("test.ac.jp", "test.ac.jp"),
        ("www.test.ac.jp", "test.ac.jp"),
        ("kyoto.jp", None),
        ("test.kyoto.jp", "test.kyoto.jp"),
        ("ide.kyoto.jp", None),
        ("b.ide.kyoto.jp", "b.ide.kyoto.jp"),
        ("a.b.ide.kyoto.jp", "b.ide.kyoto.jp"),
        ("c.kobe.jp", None),
        ("b.c.kobe.jp", "b.c.kobe.jp"),
        ("a.b.c.kobe.jp", "b.c.kobe.jp"),
        ("city.kobe.jp", "city.kobe.jp"),
        ("www.city.kobe.jp", "city.kobe.jp"),
        ("ck", None),
        ("test.ck", None),
        ("b.test.ck", "b.test.ck"),
        ("a.b.test.ck", "b.test.ck"),
        ("www.ck", "www.ck"),
        ("www.www.ck", "www.ck"),
        ("us", None),
        ("test.us", "test.us"),
        ("www.test.us", "test.us"),
        ("ak.us", None),
        ("test.ak.us", "test.ak.us"),
        ("www.test.ak.us", "test.ak.us"),
        ("k12.ak.us", None),
        ("test.k12.ak.us", "test.k12.ak.us"),
        ("www.test.k12.ak.us", "test.k12.ak.us"),
        ("xn--85x722f.com.cn", "xn--85x722f.com.cn"),
        ("xn--85x722f.xn--55qx5d.cn", "xn--85x722f.xn--55qx5d.cn"),
        ("www.xn--85x722f.xn--55qx5d.cn", "xn--85x722f.xn--55qx5d.cn"),
        ("shishi.xn--55qx5d.cn", "shishi.xn--55qx5d.cn"),
        ("xn--55qx5d.cn", None),
        ("xn--85x722f.xn--fiqs8s", "xn--85x722f.xn--fiqs8s"),
        ("www.xn--85x722f.xn--fiqs8s", "xn--85x722f.xn--fiqs8s"),
        ("shishi.xn--fiqs8s", "shishi.xn--fiqs8s"),
        ("xn--fiqs8s", None),
        ("localhost", None),
        ("LOCALhost", None),
    ],
)
def test_private_suffix(dn, private_suffix):
    suffixes = psl.domain_suffixes(dn)

    if private_suffix is not None:
        private_suffix = psl._labels_to_dn(psl._labels_from_dn(private_suffix))

    assert suffixes.private == private_suffix


@pytest.mark.parametrize(
    ["dn", "public_suffix"],
    [
        ("COM", "com"),
        ("example.COM", "com"),
        (".example.com", "com"),
        ("example.com.", "com"),
        ("example..com", None),
        ("localhost", "localhost"),
        ("LOCALhost", "localhost"),
    ],
)
def test_public_suffix(dn, public_suffix):
    suffixes = psl.domain_suffixes(dn)

    if public_suffix is not None:
        public_suffix = psl._labels_to_dn(psl._labels_from_dn(public_suffix))

    assert suffixes.public == public_suffix


@pytest.mark.parametrize(
    ["domain", "expected"],
    [
        ("foo.com", True),
        ("foo.bar.jm", True),
        ("bar.jm", False),
        ("foo.bar.kobe.jp", True),
        ("bar.kobe.jp", False),
        ("foo.bar.tokyo.jp", True),
        ("bar.tokyo.jp", True),
        ("bar.kawasaki.jp", False),
        ("city.kawasaki.jp", True),
        ("foo.city.kawasaki.jp", True),
    ],
)
def test_domain_can_set_cookie(domain, expected):
    assert psl.domain_can_set_cookie(domain) is expected
