# Just a fake enum and namespace to keep status-related things in. If we use a
# real Enum, Django weirdly doesn't want to display the human-readable version.

INITIAL_IDEA = "II"
AWAITING_EDITOR = "AE"
NEEDS_DISCUSSION = "ND"
WAITING_FOR_ROUND = "WR"
AWAITING_REVIEW = "AR"
AWAITING_ANSWER = "AA"
WRITING = "W"
WRITING_FLEXIBLE = "WF"
AWAITING_EDITOR_PRE_TESTSOLVE = "AT"
TESTSOLVING = "T"
AWAITING_TESTSOLVE_REVIEW = "TR"
REVISING = "R"
REVISING_POST_TESTSOLVING = "RP"
AWAITING_APPROVAL_POST_TESTSOLVING = "AO"
NEEDS_SOLUTION_SKETCH = "SS"
NEEDS_SOLUTION = "NS"
AWAITING_SOLUTION_AND_HINTS_APPROVAL = "AS"
NEEDS_POSTPROD = "NP"
ACTIVELY_POSTPRODDING = "PP"
POSTPROD_BLOCKED = "PB"
POSTPROD_BLOCKED_ON_TECH = "BT"
AWAITING_POSTPROD_APPROVAL = "AP"
NEEDS_FACTCHECK = "NF"
NEEDS_COPY_EDITS = "NC"
NEEDS_ART_CHECK = "NA"
NEEDS_FINAL_DAY_FACTCHECK = "NK"
NEEDS_FINAL_REVISIONS = "NR"
DONE = "D"
DEFERRED = "DF"
DEAD = "X"

# for ordering
# unclear if this was a good idea, but it does mean we can insert and reorder
# statuses without a database migration (?)
STATUSES = [
    INITIAL_IDEA,
    AWAITING_EDITOR,
    NEEDS_DISCUSSION,
    WAITING_FOR_ROUND,
    AWAITING_REVIEW,
    AWAITING_ANSWER,
    WRITING,
    WRITING_FLEXIBLE,
    AWAITING_EDITOR_PRE_TESTSOLVE,
    TESTSOLVING,
    AWAITING_TESTSOLVE_REVIEW,
    REVISING,
    REVISING_POST_TESTSOLVING,
    AWAITING_APPROVAL_POST_TESTSOLVING,
    NEEDS_SOLUTION_SKETCH,
    NEEDS_SOLUTION,
    AWAITING_SOLUTION_AND_HINTS_APPROVAL,
    NEEDS_POSTPROD,
    ACTIVELY_POSTPRODDING,
    POSTPROD_BLOCKED,
    POSTPROD_BLOCKED_ON_TECH,
    AWAITING_POSTPROD_APPROVAL,
    NEEDS_FACTCHECK,
    NEEDS_FINAL_REVISIONS,
    NEEDS_COPY_EDITS,
    NEEDS_ART_CHECK,
    NEEDS_FINAL_DAY_FACTCHECK,
    DONE,
    DEFERRED,
    DEAD,
]


def get_status_rank(status):
    try:
        return STATUSES.index(status)
    except ValueError:  # not worth crashing imo
        return -1


def past_writing(status):
    return get_status_rank(status) > get_status_rank(
        WRITING_FLEXIBLE
    ) and get_status_rank(status) <= get_status_rank(DONE)


def past_testsolving(status):
    return get_status_rank(status) > get_status_rank(REVISING) and get_status_rank(
        status
    ) <= get_status_rank(DONE)


# Possible blockers:

EIC = "editor-in-chief"
EDITORS = "editor(s)"
AUTHORS = "the author(s)"
TESTSOLVERS = "testsolve coordinators"
POSTPRODDERS = "postprodders"
FACTCHECKERS = "factcheckers"
NOBODY = "nobody"

BLOCKERS_AND_TRANSITIONS = {
    INITIAL_IDEA: (
        AUTHORS,
        [
            (AWAITING_EDITOR, "✅ Ready for an editor"),
            (DEFERRED, "⏸️  Mark deferred"),
            (DEAD, "⏹️  Mark as dead"),
        ],
    ),
    AWAITING_EDITOR: (
        EIC,
        [
            (AWAITING_REVIEW, "✅ Editors assigned 👍 Answer confirmed"),
            (AWAITING_REVIEW, "✅ Editors assigned 🤷🏽‍♀️ No answer yet"),
            (NEEDS_DISCUSSION, "🗣 Need to discuss with EICs"),
            (INITIAL_IDEA, "🔄 Puzzle needs more work"),
        ],
    ),
    NEEDS_DISCUSSION: (
        EIC,
        [
            (AWAITING_REVIEW, "✅ Editors assigned 👍 Answer confirmed"),
            (AWAITING_REVIEW, "✅ Editors assigned 🤷🏽‍♀️ No answer yet"),
            (INITIAL_IDEA, "🔄 Send back to author(s)"),
        ],
    ),
    WAITING_FOR_ROUND: (
        EIC,
        [
            (AWAITING_REVIEW, "✅ Editors assigned 👍 Answer confirmed"),
            (AWAITING_REVIEW, "✅ Editors assigned 🤷🏽‍♀️ No answer yet"),
            (INITIAL_IDEA, "🔄 Send back to author(s)"),
        ],
    ),
    AWAITING_REVIEW: (
        EDITORS,
        [
            (AWAITING_ANSWER, "✅ Idea approved 🤷🏽‍♀️ need answer"),
            (WRITING, "✅ Idea approved 👍 Answer assigned"),
            (TESTSOLVING, "✏️ Ready to testsolve!"),
        ],
    ),
    AWAITING_ANSWER: (
        EIC,
        [
            (WRITING, "✅ Mark as answer assigned"),
        ],
    ),
    WRITING: (
        AUTHORS,
        [
            (AWAITING_ANSWER, "❌ Reject answer"),
            (AWAITING_EDITOR_PRE_TESTSOLVE, "📝 Request Editor Pre-testsolve"),
        ],
    ),
    WRITING_FLEXIBLE: (
        AUTHORS,
        [
            (WRITING, "✅ Mark as answer assigned"),
            (AWAITING_EDITOR_PRE_TESTSOLVE, "📝 Request Editor Pre-testsolve"),
        ],
    ),
    AWAITING_EDITOR_PRE_TESTSOLVE: (
        EDITORS,
        [
            (TESTSOLVING, "✅ Puzzle is ready to be testsolved"),
            (REVISING, "❌ Request puzzle revision"),
            (NEEDS_SOLUTION_SKETCH, "📝 Request Solution Sketch"),
        ],
    ),
    TESTSOLVING: (
        EDITORS,
        [
            (AWAITING_TESTSOLVE_REVIEW, "🧐 Testsolve done; author to review feedback"),
            (REVISING, "❌ Testsolve done; needs revision and more testsolving"),
            (
                REVISING_POST_TESTSOLVING,
                "⭕ Testsolve done; needs revision (but not testsolving)",
            ),
        ],
    ),
    AWAITING_TESTSOLVE_REVIEW: (
        AUTHORS,
        [
            (AWAITING_EDITOR_PRE_TESTSOLVE, "🔄 Ready for editor pre-testsolve"),
            (REVISING, "❌ Needs revision (then more testsolving)"),
            (REVISING_POST_TESTSOLVING, "⭕ Needs revision (but can skip testsolving)"),
            (AWAITING_APPROVAL_POST_TESTSOLVING, "📝 Send to editors for approval"),
            (NEEDS_SOLUTION, "✅ Accept testsolve; request solution walkthru"),
            (NEEDS_POSTPROD, "⏩ Accept testsolve and solution; request postprod"),
        ],
    ),
    REVISING: (
        AUTHORS,
        [
            (AWAITING_EDITOR_PRE_TESTSOLVE, "📝 Request Editor Pre-testsolve"),
            (TESTSOLVING, "⏩ Put into testsolving"),
            (
                AWAITING_APPROVAL_POST_TESTSOLVING,
                "⏭️  Request approval to skip testsolving",
            ),
        ],
    ),
    REVISING_POST_TESTSOLVING: (
        AUTHORS,
        [
            (
                AWAITING_APPROVAL_POST_TESTSOLVING,
                "📝 Request approval for post-testsolving",
            ),
            (NEEDS_SOLUTION, "⏩ Mark revision as done"),
        ],
    ),
    AWAITING_APPROVAL_POST_TESTSOLVING: (
        EDITORS,
        [
            (
                REVISING_POST_TESTSOLVING,
                "❌ Request puzzle revision (done with testsolving)",
            ),
            (TESTSOLVING, "🔙 Return to testsolving"),
            (NEEDS_SOLUTION, "✅ Accept revision; request solution"),
            (NEEDS_POSTPROD, "⏩ Accept revision and solution; request postprod"),
        ],
    ),
    NEEDS_SOLUTION_SKETCH: (
        AUTHORS,
        [
            (AWAITING_EDITOR_PRE_TESTSOLVE, "📝 Request Editor Pre-testsolve"),
        ],
    ),
    NEEDS_SOLUTION: (
        AUTHORS,
        [
            (
                AWAITING_SOLUTION_AND_HINTS_APPROVAL,
                "📝 Request approval for solution and hints",
            ),
            (NEEDS_POSTPROD, "✅ Mark solution as finished; request postprod"),
        ],
    ),
    AWAITING_SOLUTION_AND_HINTS_APPROVAL: (
        EDITORS,
        [
            (NEEDS_SOLUTION, "❌ Request revisions to solution"),
            (NEEDS_POSTPROD, "✅ Mark solution as finished; request postprod"),
        ],
    ),
    NEEDS_POSTPROD: (
        POSTPRODDERS,
        [
            (ACTIVELY_POSTPRODDING, "🏠 Postprodding has started"),
            (AWAITING_POSTPROD_APPROVAL, "📝 Request approval after postprod"),
            (POSTPROD_BLOCKED, "❌✏️ Request revisions from author/art"),
            (POSTPROD_BLOCKED_ON_TECH, "❌💻 Blocked on tech request"),
        ],
    ),
    ACTIVELY_POSTPRODDING: (
        POSTPRODDERS,
        [
            (AWAITING_POSTPROD_APPROVAL, "📝 Request approval after postprod"),
            (NEEDS_FACTCHECK, "⏩ Mark postprod as finished; request factcheck"),
            (POSTPROD_BLOCKED, "❌✏️ Request revisions from author/art"),
            (POSTPROD_BLOCKED_ON_TECH, "❌💻 Blocked on tech request"),
        ],
    ),
    POSTPROD_BLOCKED: (
        AUTHORS,
        [
            (ACTIVELY_POSTPRODDING, "🏠 Postprodding can resume"),
            (NEEDS_POSTPROD, "📝 Mark as Ready for Postprod"),
            (POSTPROD_BLOCKED_ON_TECH, "❌💻 Blocked on tech request"),
            (AWAITING_POSTPROD_APPROVAL, "📝 Request approval after postprod"),
        ],
    ),
    POSTPROD_BLOCKED_ON_TECH: (
        POSTPRODDERS,
        [
            (ACTIVELY_POSTPRODDING, "🏠 Postprodding can resume"),
            (NEEDS_POSTPROD, "📝 Mark as Ready for Postprod"),
            (POSTPROD_BLOCKED, "❌✏️ Request revisions from author/art"),
            (AWAITING_POSTPROD_APPROVAL, "📝 Request approval after postprod"),
        ],
    ),
    AWAITING_POSTPROD_APPROVAL: (
        AUTHORS,
        [
            (ACTIVELY_POSTPRODDING, "❌ Request revisions to postprod"),
            (NEEDS_FACTCHECK, "⏩ Mark postprod as finished; request factcheck"),
        ],
    ),
    NEEDS_FACTCHECK: (
        FACTCHECKERS,
        [
            (REVISING, "❌ Request large revisions (needs more testsolving)"),
            (
                REVISING_POST_TESTSOLVING,
                "❌ Request large revisions (doesn't need testsolving)",
            ),
            (NEEDS_FINAL_REVISIONS, "🟡 Needs minor revisions"),
            (NEEDS_ART_CHECK, "🎨 Needs art check"),
            (NEEDS_FINAL_DAY_FACTCHECK, "📆 Needs final day factcheck"),
            (DONE, "⏩🎆 Mark as done! 🎆⏩"),
        ],
    ),
    NEEDS_FINAL_REVISIONS: (
        AUTHORS,
        [
            (NEEDS_FACTCHECK, "📝 Request factcheck (for large revisions)"),
            (NEEDS_COPY_EDITS, "✅ Request copy edits (for small revisions)"),
        ],
    ),
    NEEDS_COPY_EDITS: (
        FACTCHECKERS,
        [
            (NEEDS_ART_CHECK, "🎨 Needs art check"),
            (NEEDS_FINAL_DAY_FACTCHECK, "📆 Needs final day factcheck"),
            (DONE, "⏩🎆 Mark as done! 🎆⏩"),
        ],
    ),
    NEEDS_FINAL_DAY_FACTCHECK: (
        FACTCHECKERS,
        [
            (DONE, "⏩🎆 Mark as done! 🎆⏩"),
        ],
    ),
    DEFERRED: (
        NOBODY,
        [],
    ),
}


def get_blocker(status):
    value = BLOCKERS_AND_TRANSITIONS.get(status)
    if value:
        return value[0]
    else:
        return NOBODY


def get_transitions(status, puzzle=None):
    value = BLOCKERS_AND_TRANSITIONS.get(status)
    if value:
        # add any transition logic here
        additions = []
        exclusions = []
        if puzzle and puzzle.editors.exists():
            exclusions.append(AWAITING_EDITOR)
            if status == INITIAL_IDEA:
                additions.append((AWAITING_REVIEW, "📝 Send to editors for input"))

        return [s for s in [*additions, *value[1]] if s[0] not in exclusions]
    else:
        return []


STATUSES_BLOCKED_ON_EDITORS = [
    status
    for status, (blocker, _) in BLOCKERS_AND_TRANSITIONS.items()
    if blocker == EDITORS
]
STATUSES_BLOCKED_ON_AUTHORS = [
    status
    for status, (blocker, _) in BLOCKERS_AND_TRANSITIONS.items()
    if blocker == AUTHORS
]

DESCRIPTIONS = {
    INITIAL_IDEA: "Initial Idea",
    AWAITING_EDITOR: "Awaiting Approval By EIC",
    NEEDS_DISCUSSION: "EICs are Discussing",
    WAITING_FOR_ROUND: "Waiting for Round to Open",
    AWAITING_REVIEW: "Awaiting Input By Editor(s)",
    AWAITING_ANSWER: "Awaiting Answer",
    WRITING: "Writing (Answer Assigned)",
    WRITING_FLEXIBLE: "Writing (Answer Flexible)",
    AWAITING_EDITOR_PRE_TESTSOLVE: "Awaiting Editor Pre-testsolve",
    TESTSOLVING: "Ready to be Testsolved",
    AWAITING_TESTSOLVE_REVIEW: "Awaiting Testsolve Review",
    REVISING: "Revising (Needs Testsolving)",
    REVISING_POST_TESTSOLVING: "Revising (Done with Testsolving)",
    AWAITING_APPROVAL_POST_TESTSOLVING: "Awaiting Approval (Done with Testsolving)",
    NEEDS_SOLUTION_SKETCH: "Needs Solution Sketch",
    NEEDS_SOLUTION: "Needs Solution",
    AWAITING_SOLUTION_AND_HINTS_APPROVAL: "Awaiting Solution and Hints Approval",
    POSTPROD_BLOCKED: "Postproduction Blocked",
    POSTPROD_BLOCKED_ON_TECH: "Postproduction Blocked On Tech Request",
    NEEDS_POSTPROD: "Ready for Postprodding",
    ACTIVELY_POSTPRODDING: "Actively Postprodding",
    AWAITING_POSTPROD_APPROVAL: "Awaiting Approval After Postprod",
    NEEDS_FACTCHECK: "Needs Factcheck",
    NEEDS_FINAL_REVISIONS: "Needs Final Revisions",
    NEEDS_COPY_EDITS: "Needs Copy Edits",
    NEEDS_ART_CHECK: "Needs Art Check",
    NEEDS_FINAL_DAY_FACTCHECK: "Needs Final Day Factcheck",
    DONE: "Done",
    DEFERRED: "Deferred",
    DEAD: "Dead",
}


EMOJIS = {
    INITIAL_IDEA: "🥚",
    AWAITING_EDITOR: "🎩",
    NEEDS_DISCUSSION: "🗣",
    WAITING_FOR_ROUND: "⏳",
    AWAITING_ANSWER: "🤷🏽‍♀️",
    AWAITING_REVIEW: "👒",
    WRITING: "✏️",
    WRITING_FLEXIBLE: "✏️",
    AWAITING_EDITOR_PRE_TESTSOLVE: "⏳✅",
    TESTSOLVING: "💡",
    REVISING: "✏️🔄",
    REVISING_POST_TESTSOLVING: "✏️🔄",
    NEEDS_POSTPROD: "🪵",
    ACTIVELY_POSTPRODDING: "🏠",
    POSTPROD_BLOCKED: "⚠️✏️",
    POSTPROD_BLOCKED_ON_TECH: "⚠️💻",
    AWAITING_POSTPROD_APPROVAL: "🧐",
    NEEDS_COPY_EDITS: "📃",
    NEEDS_FINAL_DAY_FACTCHECK: "📆",
    NEEDS_FACTCHECK: "📋",
    NEEDS_ART_CHECK: "🎨",
    NEEDS_FINAL_REVISIONS: "🔬",
    DONE: "🏁",
    DEFERRED: "💤",
    DEAD: "💀",
}

TEMPLATES = {
    AWAITING_EDITOR: "awaiting_editor",
}

MAX_LENGTH = 2


def get_display(status):
    return DESCRIPTIONS.get(status, status)


def get_emoji(status):
    return EMOJIS.get(status, "")


def get_template(status):
    return TEMPLATES.get(status, "status_update_email")


ALL_STATUSES = [
    {
        "value": status,
        "display": description,
        "emoji": get_emoji(status),
    }
    for status, description in DESCRIPTIONS.items()
]


def get_message_for_status(status, puzzle, status_display):
    additional_msg = ""
    if status == AWAITING_POSTPROD_APPROVAL:
        postprod_url = puzzle.postprod_url
        if postprod_url:
            additional_msg = f"\nView the postprod at {postprod_url}"

    return f"This puzzle is now **{status_display}**." + additional_msg
