import types


def doimport(ddir, imports=[]):
    if not type(imports) is types.ListType:
        imports = [imports]
    if imports == [] and len(ddir.split('.')) > 1:
        tmpdir = ddir.split(".")
        imports = [tmpdir[-1]]
        ddir = ".".join(tmpdir[:-1])
    modules = __import__(ddir, fromlist=imports)
    if len(imports) == 1:
        return getattr(modules, imports[0])
    elif len(imports) > 1:
        res = {}
        for imp_ in imports:
            res[imp_] = getattr(modules, imp_)
        return res
    else:
        return modules


def modulejoin(*args):
    return ".".join(str(arg) for arg in args)
