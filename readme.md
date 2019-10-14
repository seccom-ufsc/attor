Attendance Validator
====================

Gets SECCOM's Sympla check-ins and validates attendances for UFSC's students.

Usage
-----

Convert xlsx attendances into csv:

```console
$ python -m attor convert attendances.xlsx attendances.csv
```

Fetch members from a class:

```console
$ python -m attor fetch_members INE5417 04208A 20192 ./
$ python -m attor fetch_members INE5413 04208 20192 ./
$ tree .
.
└── 20192
    ├── INE5413
    │   └── 04208.csv
    └── INE5417
        └── 04208A.csv
```

Filter for those who is in both CSVs at the same time

```console
$ python -m attor filter attendances.csv class_members.csv filtered.csv
```
