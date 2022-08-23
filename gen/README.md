# gen
This folder contains all of the code necessary to generate JSON files that contain informatics problem data. For example, to generate pbinfo problem data, execute `python pbinfo_gen.py <filename>`
# Format
## pbinfo / solinfo
The pbinfo and solinfo JSON files have the format `{name: id}`.
## infoarena
The infoarena JSON file has the format `{id: {"name": name, "archive": archive}`. Note that unlike pbinfo, infoarena doesn't use numeric IDs. `archive` is one of the following:
- `pb` - Arhiva de probleme
- `edu` - Arhiva educațională
- `monthly` - Arhiva monthly
- `acm` - Arhiva ACM
- `varena` - Arhiva de probleme varena

Due to Discord limitations, JSON cannot be sent through interactions, so in code the archive may also appear as a prefix before the ID.