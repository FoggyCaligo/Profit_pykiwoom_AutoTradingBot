def codelist2string(codelist):
    if not codelist:
        return ""
    else:
        return ";".join(codelist)