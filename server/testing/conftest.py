#!/usr/bin/env python3
import pytest
from app import app
from models import db

def pytest_itemcollected(item):
    par = item.parent.obj
    node = item.obj
    pref = par.__doc__.strip() if par.__doc__ else par.__class__.__name__
    suf = node.__doc__.strip() if node.__doc__ else node.__name__
    if pref or suf:
        item._nodeid = ' '.join((pref, suf))

@pytest.fixture(scope='function')
def app_context():
    """Create application context for tests."""
    with app.app_context():
        yield

@pytest.fixture(scope='function')
def db_session(app_context):
    """Create database tables before tests and clean up after."""
    # Create all tables
    db.create_all()
    yield
    # Clean up after tests
    db.session.remove()
    db.drop_all()

def pytest_runtest_setup(item):
    """Create database tables before each test runs."""
    with app.app_context():
        db.create_all()
