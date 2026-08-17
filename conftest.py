# Present so pytest puts the repository root on sys.path: in the default
# prepend import mode the directory inserted is the TEST FILE's basedir,
# so a suite under invariants/ cannot import this repo's own package
# without it.
