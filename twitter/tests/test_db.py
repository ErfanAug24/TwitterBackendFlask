import pytest


def test_init_tables_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_tables():
        Recorder.called = True

    monkeypatch.setattr("twitter.Config.sqlalchemy_conf.init_tables", fake_init_tables)
    result = runner.invoke(args="init-tables")
    assert "initialized" in result.output
    assert Recorder.called
