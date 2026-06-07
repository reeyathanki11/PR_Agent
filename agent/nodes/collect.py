from agent.tools.github_tools import repo


def collect_node(state):

    pr_number = state["pr_number"]

    pr = repo.get_pull(pr_number)

    files = pr.get_files()

    changed_files = []

    code = ""

    for file in files:

        changed_files.append(
            file.filename
        )

        try:

            file_content = repo.get_contents(
                file.filename,
                ref=pr.head.ref
            )

            code += (
                f"\n\nFILE: {file.filename}\n"
            )

            code += file_content.decoded_content.decode()

        except Exception:
            pass

    return {
        "changed_files": changed_files,
        "file_contents": code
    }