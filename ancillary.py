
def get_dataclass_member(dc, member_path):
    try:
        for part in member_path.split('.'):
            dc = getattr(dc, part)
        return dc
    except AttributeError:
        print(f"Member {member_path} not found!")
        sys.exit(1)

