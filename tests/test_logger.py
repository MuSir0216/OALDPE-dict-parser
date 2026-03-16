import logging


def test_logger_write(tmp_path):
    log_file = tmp_path / "test.log"

    logger = logging.getLogger("test_logger")
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler(log_file, encoding="utf-8")
    logger.addHandler(handler)

    logger.info("hello pytest")

    content = log_file.read_text(encoding="utf-8")

    assert "hello pytest" in content
