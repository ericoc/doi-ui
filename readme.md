# DOI-UI
##### (pronounced "_doughy_", as in cookie dough 🙂🍪)

Experimenting with searching/displaying Digital Object Identifiers (DOIs).

### Requires Python `requests`!

### DOI?
> A DOI is a digital identifier of an object, any object -
physical, digital, or abstract. DOIs solve a common problem:
keeping track of things. Things can be matter, material, content, or
activities. Designed to be used by humans as well as machines,
DOIs identify objects persistently. They allow things to be uniquely
identified and accessed reliably. You know what you have, where it is,
and others can track it too.

-- https://www.doi.org/

## Examples

- [`https://doi.org/10.1038/s41586-024-08156-8`](https://doi.org/10.1038/s41586-024-08156-8)

### Interactive
```py
(venv) ➜ doi-ui git:(main) $ python3
Python 3.11.7 (v3.11.7:fa7a6f2303, Dec  4 2023, 15:22:56) [Clang 13.0.0 (clang-1300.0.29.30)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>>
>>> from DOI import DOI
>>> test = DOI('10.1038/s41586-024-08156-8')
>>> test
DOI: 10.1038/s41586-024-08156-8 (Electrically driven long-range solid-state amorphization in ferroic In2Se3)
>>> print(test)
10.1038/s41586-024-08156-8 (Electrically driven long-range solid-state amorphization in ferroic In2Se3)
>>> test.author
{'ORCID': 'https://orcid.org/0000-0001-6883-814X', 'authenticated-orcid': False, 'given': 'Gaurav', 'family': 'Modi', 'sequence': 'first', 'affiliation': []}
>>> test.authors
[{'ORCID': 'https://orcid.org/0000-0001-6883-814X', 'authenticated-orcid': False, 'given': 'Gaurav', 'family': 'Modi', 'sequence': 'first', 'affiliation': []}, .... {'ORCID': 'https://orcid.org/0000-0002-3366-2153', 'authenticated-orcid': False, 'given': 'Eric A.', 'family': 'Stach', 'sequence': 'additional', 'affiliation': []}, {'ORCID': 'https://orcid.org/0000-0002-7841-8058', 'authenticated-orcid': False, 'given': 'Ju', 'family': 'Li', 'sequence': 'additional', 'affiliation': []}, ..., {'ORCID': 'https://orcid.org/0000-0002-1289-4334', 'authenticated-orcid': False, 'given': 'Ritesh', 'family': 'Agarwal', 'sequence': 'additional', 'affiliation': []}]
>>> test.title
'Electrically driven long-range solid-state amorphization in ferroic In2Se3'
>>> test.url
'http://dx.doi.org/10.1038/s41586-024-08156-8'
>>>
```

### `doi-cli.py`
```py
(venv) ➜ doi-ui git:(main) $ python3 doi-cli.py 10.1038/s41586-024-08156-8
2025-05-30 17:52:25 EDT (-0400) [INFO] (66196): Electrically driven long-range solid-state amorphization in ferroic In2Se3
2025-05-30 17:52:25 EDT (-0400) [INFO] (66196): http://dx.doi.org/10.1038/s41586-024-08156-8
2025-05-30 17:52:25 EDT (-0400) [INFO] (66196): 12 author(s) found:
2025-05-30 17:52:25 EDT (-0400) [INFO] (66196):   1. Gaurav Modi (first) [https://orcid.org/0000-0001-6883-814X]
2025-05-30 17:52:25 EDT (-0400) [INFO] (66196):   2. Shubham K. Parate (additional) [https://orcid.org/0009-0004-5991-9609]
2025-05-30 17:52:25 EDT (-0400) [INFO] (66196):   3. Choah Kwon (additional) [None]
2025-05-30 17:52:25 EDT (-0400) [INFO] (66196):   4. Andrew C. Meng (additional) [None]
2025-05-30 17:52:25 EDT (-0400) [INFO] (66196):   5. Utkarsh Khandelwal (additional) [None]
2025-05-30 17:52:25 EDT (-0400) [INFO] (66196):   6. Anudeep Tullibilli (additional) [None]
2025-05-30 17:52:25 EDT (-0400) [INFO] (66196):   7. James Horwath (additional) [None]
2025-05-30 17:52:25 EDT (-0400) [INFO] (66196):   8. Peter K. Davies (additional) [None]
2025-05-30 17:52:25 EDT (-0400) [INFO] (66196):   9. Eric A. Stach (additional) [https://orcid.org/0000-0002-3366-2153]
2025-05-30 17:52:25 EDT (-0400) [INFO] (66196):   10. Ju Li (additional) [https://orcid.org/0000-0002-7841-8058]
2025-05-30 17:52:25 EDT (-0400) [INFO] (66196):   11. Pavan Nukala (additional) [None]
2025-05-30 17:52:25 EDT (-0400) [INFO] (66196):   12. Ritesh Agarwal (additional) [https://orcid.org/0000-0002-1289-4334]
```
