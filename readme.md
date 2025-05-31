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

## Example

- [`https://doi.org/10.1038/s41586-024-08156-8`](https://doi.org/10.1038/s41586-024-08156-8)

```py
$ ./doi-cli.py -h
usage: doi-cli.py [-h] [-a] [-d] [-r] [-v] doi

positional arguments:
doi               Digital Object Identifier (DOI)
e.g. 10.1038/s41586-024-08156-8

options:
-h, --help        show this help message and exit
-a, --authors     Show authors.
-d, --dates       Show dates.
-r, --references  Show reference information.
-v, --verbose     Verbose output.
```
```py
$ ./doi-cli.py -ad 10.1038/s41586-024-08156-8
2025-05-30 21:48:47 EDT (-0400) [INFO] (75423): Electrically driven long-range solid-state amorphization in ferroic In2Se3 (journal-article)
2025-05-30 21:48:47 EDT (-0400) [INFO] (75423): http://dx.doi.org/10.1038/s41586-024-08156-8
2025-05-30 21:48:47 EDT (-0400) [INFO] (75423): Springer Science and Business Media LLC
2025-05-30 21:48:47 EDT (-0400) [INFO] (75423): Created: Wed Nov  6 17:05:26 2024 (2024-11-06 17:05:26+00:00)
2025-05-30 21:48:47 EDT (-0400) [INFO] (75423): Deposited: Wed Nov 27 13:09:13 2024 (2024-11-27 13:09:13+00:00)
2025-05-30 21:48:47 EDT (-0400) [INFO] (75423): Indexed: Tue May 27 16:29:56 2025 (2025-05-27 16:29:56+00:00)
2025-05-30 21:48:47 EDT (-0400) [INFO] (75423): Issued: Wed Nov  6 00:00:00 2024 (2024-11-06)
2025-05-30 21:48:47 EDT (-0400) [INFO] (75423): Published: Wed Nov  6 00:00:00 2024 (2024-11-06)
2025-05-30 21:48:47 EDT (-0400) [INFO] (75423): Published Online: Wed Nov  6 00:00:00 2024 (2024-11-06)
2025-05-30 21:48:47 EDT (-0400) [INFO] (75423): Published Print: Thu Nov 28 00:00:00 2024 (2024-11-28)
2025-05-30 21:48:47 EDT (-0400) [INFO] (75423): 12 author(s):
2025-05-30 21:48:47 EDT (-0400) [INFO] (75423):   1. Gaurav Modi (first) [ORCID: https://orcid.org/0000-0001-6883-814X]
2025-05-30 21:48:47 EDT (-0400) [INFO] (75423):   2. Shubham K. Parate (additional) [ORCID: https://orcid.org/0009-0004-5991-9609]
2025-05-30 21:48:47 EDT (-0400) [INFO] (75423):   3. Choah Kwon (additional) [ORCID: None]
2025-05-30 21:48:47 EDT (-0400) [INFO] (75423):   4. Andrew C. Meng (additional) [ORCID: None]
2025-05-30 21:48:47 EDT (-0400) [INFO] (75423):   5. Utkarsh Khandelwal (additional) [ORCID: None]
2025-05-30 21:48:47 EDT (-0400) [INFO] (75423):   6. Anudeep Tullibilli (additional) [ORCID: None]
2025-05-30 21:48:47 EDT (-0400) [INFO] (75423):   7. James Horwath (additional) [ORCID: None]
2025-05-30 21:48:47 EDT (-0400) [INFO] (75423):   8. Peter K. Davies (additional) [ORCID: None]
2025-05-30 21:48:47 EDT (-0400) [INFO] (75423):   9. Eric A. Stach (additional) [ORCID: https://orcid.org/0000-0002-3366-2153]
2025-05-30 21:48:47 EDT (-0400) [INFO] (75423):   10. Ju Li (additional) [ORCID: https://orcid.org/0000-0002-7841-8058]
2025-05-30 21:48:47 EDT (-0400) [INFO] (75423):   11. Pavan Nukala (additional) [ORCID: None]
2025-05-30 21:48:47 EDT (-0400) [INFO] (75423):   12. Ritesh Agarwal (additional) [ORCID: https://orcid.org/0000-0002-1289-4334]
```
