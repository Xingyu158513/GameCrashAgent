## Summary

## Safety and privacy

- [ ] The read-only default is preserved.
- [ ] No diagnostic collection scope was silently broadened.
- [ ] New or changed fields are covered by privacy review.
- [ ] No real user data is included.

## Verification

- [ ] `python -m unittest discover -s tests -v`
- [ ] `python -m compileall -q gamecrashagent main.py`
