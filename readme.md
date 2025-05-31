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
$ python3
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
$ ./doi-cli.py -h
usage: doi-cli.py [-h] [-a] [-d] [-r] [-v] doi

positional arguments:
doi               Digital Object Identifier (DOI)
e.g. 10.1038/s41586-024-08156-8

options:
-h, --help        show this help message and exit
-a, --authors     Show authors.
-d, --dates       Show dates.
-r, --references  Show reference DOI(s).
-v, --verbose     Verbose output.
```
```py
$ ./doi-cli.py -adr 10.1038/s41586-024-08156-8

2025-05-30 21:11:59 EDT (-0400) [INFO] (73347): Electrically driven long-range solid-state amorphization in ferroic In2Se3 (http://dx.doi.org/10.1038/s41586-024-08156-8)
2025-05-30 21:11:59 EDT (-0400) [INFO] (73347): Created: Wed Nov  6 17:05:26 2024 (2024-11-06 17:05:26+00:00)
2025-05-30 21:11:59 EDT (-0400) [INFO] (73347): Published: Wed Nov  6 00:00:00 2024 (2024-11-06)
2025-05-30 21:11:59 EDT (-0400) [INFO] (73347): Published Online: Wed Nov  6 00:00:00 2024 (2024-11-06)
2025-05-30 21:11:59 EDT (-0400) [INFO] (73347): Published Print: Thu Nov 28 00:00:00 2024 (2024-11-28)
2025-05-30 21:11:59 EDT (-0400) [INFO] (73347): 12 author(s):
2025-05-30 21:11:59 EDT (-0400) [INFO] (73347):   1. Gaurav Modi (first) [ORCID: https://orcid.org/0000-0001-6883-814X]
2025-05-30 21:11:59 EDT (-0400) [INFO] (73347):   2. Shubham K. Parate (additional) [ORCID: https://orcid.org/0009-0004-5991-9609]
2025-05-30 21:11:59 EDT (-0400) [INFO] (73347):   3. Choah Kwon (additional) [ORCID: None]
2025-05-30 21:11:59 EDT (-0400) [INFO] (73347):   4. Andrew C. Meng (additional) [ORCID: None]
2025-05-30 21:11:59 EDT (-0400) [INFO] (73347):   5. Utkarsh Khandelwal (additional) [ORCID: None]
2025-05-30 21:11:59 EDT (-0400) [INFO] (73347):   6. Anudeep Tullibilli (additional) [ORCID: None]
2025-05-30 21:11:59 EDT (-0400) [INFO] (73347):   7. James Horwath (additional) [ORCID: None]
2025-05-30 21:11:59 EDT (-0400) [INFO] (73347):   8. Peter K. Davies (additional) [ORCID: None]
2025-05-30 21:11:59 EDT (-0400) [INFO] (73347):   9. Eric A. Stach (additional) [ORCID: https://orcid.org/0000-0002-3366-2153]
2025-05-30 21:11:59 EDT (-0400) [INFO] (73347):   10. Ju Li (additional) [ORCID: https://orcid.org/0000-0002-7841-8058]
2025-05-30 21:11:59 EDT (-0400) [INFO] (73347):   11. Pavan Nukala (additional) [ORCID: None]
2025-05-30 21:11:59 EDT (-0400) [INFO] (73347):   12. Ritesh Agarwal (additional) [ORCID: https://orcid.org/0000-0002-1289-4334]
2025-05-30 21:11:59 EDT (-0400) [INFO] (73347): 48/48 reference(s):
2025-05-30 21:11:59 EDT (-0400) [INFO] (73347):       1. Phase Change Memory (https://doi.org/10.1109/JPROC.2010.2070050)
2025-05-30 21:12:00 EDT (-0400) [INFO] (73347):       2. Electrical Wind Force–Driven and Dislocation-Templated Amorphization in Phase-Change Nanowires (https://doi.org/10.1126/science.1220119)
2025-05-30 21:12:00 EDT (-0400) [INFO] (73347):       3. Ultralow-power switching via defect engineering in germanium telluride phase-change memory devices (https://doi.org/10.1038/ncomms10482)
2025-05-30 21:12:00 EDT (-0400) [INFO] (73347):       4. Highly scalable non-volatile and ultra-low-power phase-change nanowire memory (https://doi.org/10.1038/nnano.2007.291)
2025-05-30 21:12:00 EDT (-0400) [INFO] (73347):       5. High-Resolution Transmission Electron Microscopy Study of Electrically-Driven Reversible Phase Change in Ge<sub>2</sub>Sb<sub>2</sub>Te<sub>5</sub> Nanowires (https://doi.org/10.1021/nl104537c)
2025-05-30 21:12:00 EDT (-0400) [INFO] (73347):       6. Defect-induced melting and solid-state amorphization (https://doi.org/10.1038/356133a0)
2025-05-30 21:12:00 EDT (-0400) [INFO] (73347):       7. Dynamics of a ferromagnetic domain wall: Avalanches, depinning transition, and the Barkhausen effect (https://doi.org/10.1103/PhysRevB.58.6353)
2025-05-30 21:12:00 EDT (-0400) [INFO] (73347):       8. Avalanche criticality during ferroelectric/ferroelastic switching (https://doi.org/10.1038/s41467-020-20477-6)
2025-05-30 21:12:01 EDT (-0400) [INFO] (73347):       9. In search of the perfect glass (https://doi.org/10.1038/nphys3054)
2025-05-30 21:12:01 EDT (-0400) [INFO] (73347):       10. Theoretical perspective on the glass transition and amorphous materials (https://doi.org/10.1103/RevModPhys.83.587)
2025-05-30 21:12:01 EDT (-0400) [INFO] (73347):       11. Glass Forming Ability in Systems with Competing Orderings (https://doi.org/10.1103/PhysRevX.8.021040)
2025-05-30 21:12:01 EDT (-0400) [INFO] (73347):       12. Non-crystalline Structure in Solidified Gold–Silicon Alloys (https://doi.org/10.1038/187869b0)
2025-05-30 21:12:02 EDT (-0400) [INFO] (73347):       13. Amorphous martensite in β-Ti alloys (https://doi.org/10.1038/s41467-018-02961-2)
2025-05-30 21:12:02 EDT (-0400) [INFO] (73347):       14. Solid-State Amorphization of<mml:math xmlns:mml="http://www.w3.org/1998/Math/MathML" display="inline"><mml:mrow><mml:msub><mml:mrow><mml:mi mathvariant="normal">Zr</mml:mi></mml:mrow><mml:mrow><mml:mn>3</mml:mn></mml:mrow></mml:msub></mml:mrow></mml:math>Al: Evidence of an Elastic Instability and First-Order Phase Transformation (https://doi.org/10.1103/PhysRevLett.59.2987)
2025-05-30 21:12:02 EDT (-0400) [INFO] (73347):       15. Pressure-Induced Amorphization and Negative Thermal Expansion in ZrW
            <sub>2</sub>
            O
            <sub>8</sub> (https://doi.org/10.1126/science.280.5365.886)
2025-05-30 21:12:02 EDT (-0400) [INFO] (73347):       16. In situ observation of shear-driven amorphization in silicon crystals (https://doi.org/10.1038/nnano.2016.166)
2025-05-30 21:12:03 EDT (-0400) [INFO] (73347):       17. Resonant bonding in crystalline phase-change materials (https://doi.org/10.1038/nmat2226)
2025-05-30 21:12:03 EDT (-0400) [INFO] (73347):       18. Inverting polar domains via electrical pulsing in metallic germanium telluride (https://doi.org/10.1038/ncomms15033)
2025-05-30 21:12:03 EDT (-0400) [INFO] (73347):       19. Electronic structure of intrinsic defects in crystalline germanium telluride (https://doi.org/10.1103/PhysRevB.73.045210)
2025-05-30 21:12:03 EDT (-0400) [INFO] (73347):       20. Principles and Applications of Ferroelectrics and Related Materials (https://doi.org/10.1093/acprof:oso/9780198507789.001.0001)
2025-05-30 21:12:03 EDT (-0400) [INFO] (73347):       21. Prediction of intrinsic two-dimensional ferroelectrics in In2Se3 and other III2-VI3 van der Waals materials (https://doi.org/10.1038/ncomms14956)
2025-05-30 21:12:03 EDT (-0400) [INFO] (73347):       22. Intrinsic Two-Dimensional Ferroelectricity with Dipole Locking (https://doi.org/10.1103/PhysRevLett.120.227601)
2025-05-30 21:12:03 EDT (-0400) [INFO] (73347):       23. Two-Dimensional Antiferroelectricity in Nanostripe-Ordered 
<mml:math xmlns:mml="http://www.w3.org/1998/Math/MathML" display="inline"><mml:mrow><mml:msub><mml:mrow><mml:mi>In</mml:mi></mml:mrow><mml:mrow><mml:mn>2</mml:mn></mml:mrow></mml:msub></mml:mrow><mml:mrow><mml:msub><mml:mrow><mml:mi>Se</mml:mi></mml:mrow><mml:mrow><mml:mn>3</mml:mn></mml:mrow></mml:msub></mml:mrow></mml:math> (https://doi.org/10.1103/PhysRevLett.125.047601)
2025-05-30 21:12:04 EDT (-0400) [INFO] (73347):       24. Two-dimensional ferroelasticity in van der Waals β’-In2Se3 (https://doi.org/10.1038/s41467-021-23882-7)
2025-05-30 21:12:04 EDT (-0400) [INFO] (73347):       25. Atomic Visualization and Switching of Ferroelectric Order in β‐In<sub>2</sub>Se<sub>3</sub> Films at the Single Layer Limit (https://doi.org/10.1002/adma.202106951)
2025-05-30 21:12:04 EDT (-0400) [INFO] (73347):       26. In-Plane Ferrielectric Order in van der Waals β′-In<sub>2</sub>Se<sub>3</sub> (https://doi.org/10.1021/acsnano.3c09250)
2025-05-30 21:12:04 EDT (-0400) [INFO] (73347):       27. Synthesis and Phase Transformation of In<sub>2</sub>Se<sub>3</sub> and CuInSe<sub>2</sub> Nanowires (https://doi.org/10.1021/ja067436k)
2025-05-30 21:12:04 EDT (-0400) [INFO] (73347):       28. Atomically Resolving Polymorphs and Crystal Structures of In<sub>2</sub>Se<sub>3</sub> (https://doi.org/10.1021/acs.chemmater.9b03499)
2025-05-30 21:12:04 EDT (-0400) [INFO] (73347):       29. The domain structure of β-In2S3 “single crystals” due to the ordering of indium vacancies (https://doi.org/10.1016/0025-5408(68)90077-9)
2025-05-30 21:12:05 EDT (-0400) [INFO] (73347):       30. Antiphase Boundaries and Twins Associated with Ordering of Indium Vacancies in β‐In<sub>2</sub>S<sub>3</sub> (https://doi.org/10.1002/pssb.19690310219)
2025-05-30 21:12:05 EDT (-0400) [INFO] (73347):       31. A macroscopic theory for the existence of the hysteresis and butterfly loops in ferroelectricity (https://doi.org/10.1080/00150198008018803)
2025-05-30 21:12:05 EDT (-0400) [INFO] (73347):       32. Low-Power Switching through Disorder and Carrier Localization in Bismuth-Doped Germanium Telluride Phase Change Memory Nanowires (https://doi.org/10.1021/acsnano.9b08986)
2025-05-30 21:12:05 EDT (-0400) [INFO] (73347):       33. Controlled Self-Assembly of Nanoscale Superstructures in Phase-Change Ge–Sb–Te Nanowires (https://doi.org/10.1021/acs.nanolett.4c00878)
2025-05-30 21:12:05 EDT (-0400) [INFO] (73347):       34. Inverse melting in the Ti-Cr system (https://doi.org/10.1103/PhysRevB.47.8520)
2025-05-30 21:12:06 EDT (-0400) [INFO] (73347):       35. Phase transitions in 2D materials (https://doi.org/10.1038/s41578-021-00304-0)
2025-05-30 21:12:06 EDT (-0400) [INFO] (73347):       36. Super switching and control of in-plane ferroelectric nanodomains in strained thin films (https://doi.org/10.1038/ncomms5415)
2025-05-30 21:12:06 EDT (-0400) [INFO] (73347):       37. Revealing the role of defects in ferroelectric switching with atomic resolution (https://doi.org/10.1038/ncomms1600)
2025-05-30 21:12:06 EDT (-0400) [INFO] (73347):       38. Polarization rotation mechanism for ultrahigh electromechanical response in single-crystal piezoelectrics (https://doi.org/10.1038/35002022)
2025-05-30 21:12:07 EDT (-0400) [INFO] (73347):       39. Ultrafast Switching in Avalanche‐Driven Ferroelectrics by Supersonic Kink Movements (https://doi.org/10.1002/adfm.201700367)
2025-05-30 21:12:07 EDT (-0400) [INFO] (73347):       40. Atomic-level polarization reversal in sliding ferroelectric semiconductors (https://doi.org/10.1038/s41467-024-48218-z)
2025-05-30 21:12:07 EDT (-0400) [INFO] (73347):       41. Atomap: a new software tool for the automated analysis of atomic resolution images using two-dimensional Gaussian fitting (https://doi.org/10.1186/s40679-017-0042-5)
2025-05-30 21:12:07 EDT (-0400) [INFO] (73347):       42. Towards universal neural network potential for material discovery applicable to arbitrary combination of 45 elements (https://doi.org/10.1038/s41467-022-30687-9)
2025-05-30 21:12:07 EDT (-0400) [INFO] (73347):       43. {'key': '8156_CR43', 'first-page': '447', 'volume': '9', 'author': 'S Takamoto', 'year': '2023', 'unstructured': 'Takamoto, S., Okanohara, D., Li, Q. J. & Li, J. Towards universal neural network interatomic potential. J. Mater. 9, 447–454 (2023).', 'journal-title': 'J. Mater.'}
2025-05-30 21:12:07 EDT (-0400) [INFO] (73347):       44. From ultrasoft pseudopotentials to the projector augmented-wave method (https://doi.org/10.1103/PhysRevB.59.1758)
2025-05-30 21:12:07 EDT (-0400) [INFO] (73347):       45. Generalized Gradient Approximation Made Simple (https://doi.org/10.1103/PhysRevLett.77.3865)
2025-05-30 21:12:08 EDT (-0400) [INFO] (73347):       46. <i>Ab initio</i>molecular dynamics for liquid metals (https://doi.org/10.1103/PhysRevB.47.558)
2025-05-30 21:12:08 EDT (-0400) [INFO] (73347):       47. Efficient iterative schemes for<i>ab initio</i>total-energy calculations using a plane-wave basis set (https://doi.org/10.1103/PhysRevB.54.11169)
2025-05-30 21:12:08 EDT (-0400) [INFO] (73347):       48. A climbing image nudged elastic band method for finding saddle points and minimum energy paths (https://doi.org/10.1063/1.1329672)
```
