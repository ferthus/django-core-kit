Always maintain two branches: `main` and `develop`.
The issue should exist for each commit, then the change can be relation to a issue.
However, there are some special cases where the issue is not required for a commit, e.g.: update README.md or fix pep8, etc.

Branches style:
* `release/0.1.0`
* `feat/0.1.0/issue-1-lorem-lorem`
* `fix/0.1.0/issue-5-lorem-lorem`
* `docs/0.1.0/issue-21-lorem-lorem`
* `style/0.1.0/issue-15-lorem-lorem`
* `refactor/0.1.0/issue-33-lorem-lorem`
* `test/0.1.0/issue-21-lorem-lorem`
* `chore/0.1.0/issue-9-lorem-lorem`
* `ci/0.1.0/issue-15-lorem-lorem`
* `perf/0.1.0/issue-89-lorem-lorem`

Relation between the style branch and commit prefix.

| Branch     | Commit Prefix  | Comments                                                        |
|------------|----------------|-----------------------------------------------------------------|
| `feature`  | feat           | Always has its own branch                                       |
| `fix`      | fix            | Always has its own branch                                       |
| `hotfix`   | fix            | Always has its own branch                                       |
| `refactor` | refactor       | When the refactor is large or planned in advance.               |
| `ci`       | ci             | When the change is big.                                         |
| `release`  | chore          | The last-minute commits can occur before creating the release.  |
| `pref`     | perf           | Recommended to have its own branch                              |

Then branch name is defined by the developer. For small, non-critical changes, the team should decide if to create a branch or commit directly to develop.

| Branch     | Commit Prefix      |  Comments                                      |
|------------|--------------------|------------------------------------------------|
| `develop`  | chore              | It can go directly in develop.                 | 
| `develop`  | test               | In some special cases a branch can be created. |
| `develop`  | docs               | It can go in the fix or feat branch            |
| `develop`  | style              | It can go in the fix or feat branch            |
