################# Harcoded arguments #########################
def custom_postfilter() -> bool:
    pass


def custom_conversion(input_str_) -> str:
    ret = ""
    return ret


PATTERN = "ho.a."
SUBSTITUTION = "HOLA!"
CUSTOM_POSTFILTER = custom_postfilter
# name it ADITIONAL_FILTER ?
CUSTOM_CONVERSION = custom_conversion
# name it ADVANCED_SUBSTITUTION?

# TODO: Join the previous 2 functions? sometimes is useful to not convert when it fails.
# but in thas case, the 'original_capture' attribute could be used
################################################################

# TODO: Create this class that contain the re.match object
# It that way, it would be better documented and I could group methods
class Match:
    init_pos: int
    end_pos: int

    # The full file
    string: str

    # The regex groups
    groups: List[str]

    # Unaltered caputured string
    original_capture: str

    def regex_substitute(self, substitution: str) -> str:
        pass


def sub_func(match_obj: Match) -> str:
    if CUSTOM_POSTFILTER:
        if not CUSTOM_POSTFILTER(match_obj):
            # don't change that piece
            return match_obj.original_capture

    if CUSTOM_CONVERSION:
        return CUSTOM_CONVERSION(match_obj)
    else:
        match_obj.regex_substitute(SUBSTITUTION)


#    SUBSTITUTION


for f in os.walk("target/dir/"):
    re.sub(PATTERN, f, sub_func)
