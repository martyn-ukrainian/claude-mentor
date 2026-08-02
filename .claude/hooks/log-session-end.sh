#!/bin/bash
# SessionEnd: save the session dialogue, then spawn a learning-summary in the background.
# NOTE: project path contains a space ("ML Learning") — every path MUST stay quoted.
input=$(cat)
sid=$(echo "$input" | jq -r '.session_id // "unknown"')
tp=$(echo "$input" | jq -r '.transcript_path // empty')

# Skip internal/automated sessions: if the FIRST user prompt starts with "HOOK:",
# don't archive it and don't launch a summary (breaks the summary->session->summary loop,
# and lets you exclude any session by prefixing its prompt with HOOK:).
first_user=$(jq -r 'select(.type=="user" and .isMeta != true) | .message.content | select(type=="string")' "$tp" 2>/dev/null | sed -n '1p')
case "$first_user" in
  HOOK:*) exit 0 ;;
esac

out="${CLAUDE_PROJECT_DIR}/memories/conversations/${sid}"
mkdir -p "$out"

# extract dialogue only (user + assistant text, no tool noise) — instant, finishes before teardown
jq -r '
  select(.type=="user" or .type=="assistant")
  | select(.isMeta != true)
  | if .type=="user" then
      (.message.content | if type=="string" then "USER: " + . else empty end)
    else
      (.message.content[]? | select(.type=="text") | "ASSISTANT: " + .text)
    end
' "$tp" > "$out/dialogue.md" 2>/dev/null

# spawn the summarizer detached — runs in parallel and survives session teardown.
# HOOK:SUMMARY marker => this run is skipped by the check above (no loop).
# haiku => cheap/fast. Direct write (no subagent — a subagent can't write files in headless -p).
nohup claude -p --model haiku --dangerously-skip-permissions \
  "HOOK:SUMMARY $(cat "${CLAUDE_PROJECT_DIR}/.claude/prompts/summarize.md") Folder: $out/" \
  < /dev/null >/dev/null 2>&1 &

exit 0
