# gen
This folder contains all of the code necessary to generate JSON files that contain informatics problem data. For example, to generate pbinfo problem data, execute `python pbinfo_gen.py <filename>`
# Format
## pbinfo / solinfo
The pbinfo and solinfo JSON files have the format `{name: id}`.
## infoarena
The infoarena JSON file has the format `{id: name}`. Note that unlike pbinfo, infoarena doesn't use numeric IDs. Also, due to Discord limitations, JSON cannot be sent through interactions, so `id` will also have a prefix indicating the archive it belongs to, with `$` as a separator:
- `pb$` - Arhiva de probleme
- `edu$` - Arhiva educațională
- `monthly$` - Arhiva monthly
- `acm$` - Arhiva ACM
- `varena$` - Arhiva de probleme varena