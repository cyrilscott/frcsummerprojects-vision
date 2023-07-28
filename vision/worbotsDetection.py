class Detection:
    tag_id = None
    tvec = None
    rvec = None

    def __init__(self, tag_id, tvec, rvec):
        self.tag_id = tag_id
        self.tvec = tvec
        self.rvec = rvec
    