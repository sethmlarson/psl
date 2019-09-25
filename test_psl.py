import pytest
import psl


@pytest.mark.parametrize(["dn", "private_suffix"], [
('COM', None),
('example.COM', 'example.com'),
('WwW.example.COM', 'example.com'),

('.com', None),
('.example', None),
('.example.com', None),
('.example.example', None),

('example', None),
('example.example', 'example.example'),
('b.example.example', 'example.example'),
('a.b.example.example', 'example.example'),

('local', None),
('example.local', None),
('b.example.local', None),
('a.b.example.local', None),

('biz', None),
('domain.biz', 'domain.biz'),
('b.domain.biz', 'domain.biz'),
('a.b.domain.biz', 'domain.biz'),

('com', None),
('example.com', 'example.com'),
('b.example.com', 'example.com'),
('a.b.example.com', 'example.com'),
('uk.com', None),
('example.uk.com', 'example.uk.com'),
('b.example.uk.com', 'example.uk.com'),
('a.b.example.uk.com', 'example.uk.com'),
('test.ac', 'test.ac'),

('mm', None),
('c.mm', None),
('b.c.mm', 'b.c.mm'),
('a.b.c.mm', 'b.c.mm'),

('jp', None),
('test.jp', 'test.jp'),
('www.test.jp', 'test.jp'),
('ac.jp', None),
('test.ac.jp', 'test.ac.jp'),
('www.test.ac.jp', 'test.ac.jp'),
('kyoto.jp', None),
('test.kyoto.jp', 'test.kyoto.jp'),
('ide.kyoto.jp', None),
('b.ide.kyoto.jp', 'b.ide.kyoto.jp'),
('a.b.ide.kyoto.jp', 'b.ide.kyoto.jp'),
('c.kobe.jp', None),
('b.c.kobe.jp', 'b.c.kobe.jp'),
('a.b.c.kobe.jp', 'b.c.kobe.jp'),
('city.kobe.jp', 'city.kobe.jp'),
('www.city.kobe.jp', 'city.kobe.jp'),

('ck', None),
('test.ck', None),
('b.test.ck', 'b.test.ck'),
('a.b.test.ck', 'b.test.ck'),
('www.ck', 'www.ck'),
('www.www.ck', 'www.ck'),

('us', None),
('test.us', 'test.us'),
('www.test.us', 'test.us'),
('ak.us', None),
('test.ak.us', 'test.ak.us'),
('www.test.ak.us', 'test.ak.us'),
('k12.ak.us', None),
('test.k12.ak.us', 'test.k12.ak.us'),
('www.test.k12.ak.us', 'test.k12.ak.us'),

('食狮.com.cn', '食狮.com.cn'),
('食狮.公司.cn', '食狮.公司.cn'),
('www.食狮.公司.cn', '食狮.公司.cn'),
('shishi.公司.cn', 'shishi.公司.cn'),
('公司.cn', None),
('食狮.中国', '食狮.中国'),
('www.食狮.中国', '食狮.中国'),
('shishi.中国', 'shishi.中国'),
('中国', None),

('xn--85x722f.com.cn', 'xn--85x722f.com.cn'),
('xn--85x722f.xn--55qx5d.cn', 'xn--85x722f.xn--55qx5d.cn'),
('www.xn--85x722f.xn--55qx5d.cn', 'xn--85x722f.xn--55qx5d.cn'),
('shishi.xn--55qx5d.cn', 'shishi.xn--55qx5d.cn'),
('xn--55qx5d.cn', None),
('xn--85x722f.xn--fiqs8s', 'xn--85x722f.xn--fiqs8s'),
('www.xn--85x722f.xn--fiqs8s', 'xn--85x722f.xn--fiqs8s'),
('shishi.xn--fiqs8s', 'shishi.xn--fiqs8s'),
('xn--fiqs8s', None),
])
def test_private_suffix(dn, private_suffix):
    suffixes = psl.domain_suffixes(dn)

    if private_suffix is not None:
        private_suffix = psl._labels_to_dn(psl._labels_from_dn(private_suffix))

    assert suffixes.private == private_suffix


@pytest.mark.parametrize(
    ["http_domain", "cookie_domain", "expected"],
    [("foo.example.com", "example.com", True),
     ("foo.example.com", "foo.example.com", True),
     ("foo.example.com", "baz.foo.example.com", False),
     ("foo.example.com", "bar.example.com", False),
     ("foo.example.com", "com", False),
     ("foo.example.com", "example.org", False),
     ("foo.example.com", ".example.com", False),
     ("foo.example.com", "example.com.", False)]
)
def test_domain_can_set_cookie(http_domain, cookie_domain, expected):
    assert psl.domain_can_set_cookie(http_domain=http_domain, cookie_domain=cookie_domain) is expected
