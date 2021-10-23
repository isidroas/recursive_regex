from recursive_regex.recursive_regex import main, Match


def custom_conversion(match: Match) -> str:
    return match.original_capture * 2


# def main(target, dry_run, config_file, custom_conversion = None):
main("./d1", True, "./rere_parameters.yaml")
main(
    "./d1", True, "./rere_parameters.yaml", custom_conversion=custom_conversion
)
