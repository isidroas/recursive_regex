from recursive_regex import main, Match


def custom_conversion(match: Match) -> str:
    return match.original_capture * 2


# def main(target, dry_run, config_file, custom_conversion = None):
main("hola", "adios", "./d1", dry_run = True)
main("hola", "adios", "./d1", dry_run = True, custom_conversion=custom_conversion)
