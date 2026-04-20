from git import Repo
from pydriller.domain.commit import ModificationType

repo_path = "C:/Users/jahan/lucene"

issue_ids = [
    "LUCENE-12",
    "LUCENE-17",
    "LUCENE-701",
    "LUCENE-1200",
    "LUCENE-1799"
]

# Load repo once (fast)
repo = Repo(repo_path)

# Read prefiltered commits (VERY IMPORTANT SPEED BOOST)
with open("commits.txt", "r") as f:
    commit_hashes = [line.strip() for line in f if line.strip()]

total_files = 0
total_dmm = 0
valid_commits = 0
unique_files_global = set()

print("Processing filtered commits...")

for h in commit_hashes:

    commit = repo.commit(h)
    msg = commit.message.upper()

    if not any(issue in msg for issue in issue_ids):
        continue

    valid_commits += 1

    files = set()

    for diff in commit.diff(commit.parents[0] if commit.parents else None):

        if diff.change_type in ["A", "M", "D"]:
            files.add(diff.a_path or diff.b_path)

    unique_files_global.update(files)
    total_files += len(files)

    # DMM (safe + fast access)
    try:
        if hasattr(commit, "dmm_unit_size"):
            total_dmm += (
                commit.dmm_unit_size +
                commit.dmm_unit_complexity +
                commit.dmm_unit_interfacing
            ) / 3
    except:
        pass


print("\n========== RESULT ==========")
print("TOTAL COMMITS ANALYZED:", valid_commits)
print("AVERAGE FILES CHANGED:", total_files / valid_commits if valid_commits else 0)
print("AVERAGE DMM METRICS:", total_dmm / valid_commits if valid_commits else 0)