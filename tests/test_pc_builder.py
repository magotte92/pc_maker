"""Smoke tests for the console menu. They do not launch a browser."""

import pc_builder


def test_module_imports_runtime_libraries():
    assert pc_builder.pd.__name__ == "pandas"
    assert pc_builder.BeautifulSoup.__name__ == "BeautifulSoup"
    assert pc_builder.Image is not None
    assert pc_builder.webdriver is not None


def test_menu_lists_are_unchanged():
    assert pc_builder.style_list == [
        "Browsing",
        "Gaming",
        "Programming",
        "Digital Editing",
        "Game Developing",
        "Architecting",
        "Hacking",
    ]
    assert pc_builder.mode_list == ["Simple", "Advanced"]


def test_banner_prints_a_choice(capsys, monkeypatch):
    monkeypatch.setattr(pc_builder.random, "choice", lambda options: options[0])
    pc_builder.banner()
    output = capsys.readouterr().out
    assert "_______" in output


def test_menu_picker_returns_in_range_choice(monkeypatch):
    monkeypatch.setattr(pc_builder.os, "system", lambda command: 0)
    assert pc_builder.menu_picker("1", ["a", "b", "c"]) == "1"
    assert pc_builder.menu_picker("0", ["a", "b"]) == "0"


def test_menu_picker_clears_screen_on_invalid_choice(monkeypatch):
    commands = []
    monkeypatch.setattr(pc_builder.os, "system", lambda command: commands.append(command))
    assert pc_builder.menu_picker("9", ["a", "b"]) is None
    assert pc_builder.menu_picker("nope", ["a", "b"]) is None
    assert commands == ["cls", "cls"]


def test_local_chromedriver_prefers_windows_binary(monkeypatch, tmp_path):
    (tmp_path / "chromedriver.exe").write_text("windows", encoding="utf-8")
    (tmp_path / "chromedriver").write_text("posix", encoding="utf-8")
    monkeypatch.setattr(pc_builder.os.path, "abspath", lambda _path: str(tmp_path / "pc_builder.py"))
    assert pc_builder._local_chromedriver() == str(tmp_path / "chromedriver.exe")


def test_local_chromedriver_falls_back_to_posix_name(monkeypatch, tmp_path):
    (tmp_path / "chromedriver").write_text("posix", encoding="utf-8")
    monkeypatch.setattr(pc_builder.os.path, "abspath", lambda _path: str(tmp_path / "pc_builder.py"))
    assert pc_builder._local_chromedriver() == str(tmp_path / "chromedriver")


def test_local_chromedriver_missing(monkeypatch, tmp_path):
    monkeypatch.setattr(pc_builder.os.path, "abspath", lambda _path: str(tmp_path / "pc_builder.py"))
    assert pc_builder._local_chromedriver() is None


def test_init_browser_uses_selenium4_service_for_local_driver(monkeypatch):
    captured = {}

    class FakeChrome:
        def __init__(self, options=None, service=None, keep_alive=True):
            captured["options"] = options
            captured["service"] = service

    monkeypatch.setattr(pc_builder, "_local_chromedriver", lambda: "/opt/driver/chromedriver.exe")
    monkeypatch.setattr(pc_builder.webdriver, "Chrome", FakeChrome)

    driver = pc_builder.init_browser()

    assert isinstance(driver, FakeChrome)
    assert captured["service"].path == "/opt/driver/chromedriver.exe"
    assert isinstance(captured["options"], pc_builder.Options)


def test_init_browser_defers_to_selenium_manager_without_local_driver(monkeypatch):
    captured = {}

    class FakeChrome:
        def __init__(self, options=None, service=None, keep_alive=True):
            captured["options"] = options
            captured["service"] = service

    monkeypatch.setattr(pc_builder, "_local_chromedriver", lambda: None)
    monkeypatch.setattr(pc_builder.webdriver, "Chrome", FakeChrome)

    pc_builder.init_browser()

    assert captured["service"] is None
    assert isinstance(captured["options"], pc_builder.Options)
