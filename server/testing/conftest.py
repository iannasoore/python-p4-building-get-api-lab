#!/usr/bin/env python3

def pytest_configure():
    """Create tables and minimal seed data for tests.

    The lab uses a local SQLite DB; in fresh environments it may exist
    without migrations applied, which causes tests to fail with
    "no such table" errors.
    """

    from app import app
    from models import db, Bakery, BakedGood

    with app.app_context():
        db.drop_all()
        db.create_all()

        # Some tests assume at least one BakedGood exists so they can
        # compute max(prices) safely.
        bakery = Bakery(name="Seed Bakery")
        db.session.add(bakery)
        db.session.commit()

        baked_good = BakedGood(name="Seed Good", price=2, bakery_id=bakery.id)
        db.session.add(baked_good)
        db.session.commit()

def pytest_itemcollected(item):
    par = item.parent.obj
    node = item.obj
    pref = par.__doc__.strip() if par.__doc__ else par.__class__.__name__
    suf = node.__doc__.strip() if node.__doc__ else node.__name__
    if pref or suf:
        item._nodeid = ' '.join((pref, suf))