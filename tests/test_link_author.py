from loader import Load
from app import db

author_data = [
    ["Joe Fitzgerald <jfitz@gopivotal.com> (http://github.com/joefitzgerald)", "Joe Fitzgerald"],
    ["tcarlsen", "tcarlsen"],
    ["Tom Kadwill", "Tom Kadwill"],
    ["Travis Jacobs (github.com/travs)", "Travis Jacobs"],
    ["2014+ Rob Loach (http://robloach.net)", "2014+ Rob Loach"],
    ["Kay-Uwe (Kiwi) Lorenz <kiwi@franka.dyndns.org> (http://quelltexter.org)", "Kay-Uwe"],
    [{
        "name": "Barney Rubble",
        "email": "b@rubble.com",
        "url": "http://barnyrubble.tumblr.com/"
    }, "Barney Rubble"]
]

link_data = [
    [
        "https://github.com/alokedesai/Atom-Grace",
        "https://github.com/alokedesai/Atom-Grace"
    ],
    [
        {'url': 'https://github.com/mpgirro/language-forth', 'type': 'git'},
        'https://github.com/mpgirro/language-forth'
    ]
]


def test_get_link(session):
    loader = Load(db.app, session)
    for link in link_data:
        link_val = loader.get_link({"repository": link[0]})
        assert link_val == link[1]


def test_get_author(session):
    loader = Load(db.app, session)
    for author in author_data:
        author_value = loader.get_author({'author': author[0]}, "")
        assert author_value == author[1]

    author_value = loader.get_author({}, "https://github.com/yuji/atom")
    assert author_value == "yuji"
