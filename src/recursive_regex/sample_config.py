SAMPLE_CONFIG = """\
pattern:  ho.a.
substitution: HOLA!
case_insensitive: False
exclude_dirs:
    - .git
    - __pycache__
    - zigbee_certification
exclude_files:
    - .swp
    - .bin
    - example1
"""


def sample_config() -> int:
    print(SAMPLE_CONFIG, end="")
    return 0
