#!/usr/bin/env bash
# Wake the Lead only when a goal bead's batch beads or Conductor panes change.
# Usage: watch-goal.sh <goal-id> <lead-name> <beads-dir> [--no-intercom]
#   <lead-name>: the Lead's Beads actor (and pi-intercom name for a Pi Lead).
#   --no-intercom: print only (Claude Code Lead under its Monitor tool).
# Every message line goes to stdout. Without --no-intercom it is also sent
# with pi-intercom. Conductor panes must be named after their batch bead ID
# (baton run --name <bead-id>); their state comes from `baton list`.
# Env: WATCH_INTERVAL (s, default 180), IDLE_LIMIT (s, default 900),
#      BATON (command, default baton), BATON_SESSION (Zellij session, default
#      $ZELLIJ_SESSION_NAME; required outside Zellij), PI_INTERCOM (command, default: pi-intercom on
#      PATH, else the Pi npm package).
set -u
goal=${1:?goal bead id}; lead=${2:?lead name}; store=${3:?beads dir}
intercom=1; [ "${4:-}" = --no-intercom ] && intercom=0
interval=${WATCH_INTERVAL:-180}; idle_limit=${IDLE_LIMIT:-900}
baton=${BATON:-baton}
session=${BATON_SESSION:-${ZELLIJ_SESSION_NAME:-}}
[ -n "$session" ] || { echo "watch-goal: set BATON_SESSION to the Conductors' Zellij session" >&2; exit 2; }
session_arg=(--session "$session")
if [ -n "${PI_INTERCOM:-}" ]; then ic=$PI_INTERCOM
elif command -v pi-intercom >/dev/null; then ic=pi-intercom
else ic="node $HOME/.pi/agent/npm/node_modules/pi-intercom/cli.mjs"; fi

declare -A last seen_count idle_since pane_last pane_count
say() {
  echo "$(date +%T) watch $goal: $1"
  [ "$intercom" = 1 ] || return 0
  $ic send --to "$lead" --text "watch $goal: $1" >/dev/null 2>&1 || echo "send failed: $1" >&2
}

while :; do
  beads=$(BEADS_DIR=$store bd --readonly list --parent "$goal" --all --limit 0 --json 2>/dev/null) || { echo "bd list failed" >&2; sleep "$interval"; continue; }
  panes=$($baton list "${session_arg[@]}" 2>/dev/null) && jq -e '.panes' >/dev/null 2>&1 <<<"$panes" || { echo "baton list failed" >&2; panes=; }
  now=$(date +%s); msgs=()

  while IFS='|' read -r id status assignee human; do
    [ -n "$id" ] || continue
    state="$status|$assignee|$human"
    signal=""
    [ "$assignee" = "$lead" ] && [ "$status" = in_progress ] && signal="handed back"
    [ "$status" = blocked ] && signal="blocked"
    [ "$human" = 1 ] && signal="needs owner"

    if [ "${last[$id]:-}" != "$state" ]; then
      [ -n "${last[$id]:-}" ] && msgs+=("$id ${signal:-$status}")
      last[$id]=$state; seen_count[$id]=0
    elif [ -n "$signal" ]; then
      seen_count[$id]=$(( ${seen_count[$id]:-0} + 1 ))
      [ "${seen_count[$id]}" -eq 2 ] && msgs+=("reminder: $id still $signal")
    fi

    # Pane check: only while the bead is in_progress under its Conductor.
    if [ -z "$panes" ] || [ "$status" != in_progress ] || [ "$assignee" = "$lead" ]; then
      unset 'idle_since[$id]' 'pane_last[$id]'; continue
    fi
    p=$(jq -r --arg n "$id" '[.panes[] | select(.name == $n) | .state][0] // "gone"' <<<"$panes")
    case $p in
      idle|done)
        idle_since[$id]=${idle_since[$id]:-$now}
        if [ $(( now - idle_since[$id] )) -ge "$idle_limit" ]; then
          msgs+=("$id conductor $p $(( (now - idle_since[$id]) / 60 )) min"); idle_since[$id]=$now
        fi ;;
      *) unset 'idle_since[$id]' ;;
    esac
    case $p in
      blocked|exited|gone)
        if [ "${pane_last[$id]:-}" != "$p" ]; then
          case $p in
            blocked) msgs+=("$id conductor blocked: waits for a person") ;;
            exited) msgs+=("$id conductor exited") ;;
            gone) msgs+=("$id conductor session not found") ;;
          esac
          pane_count[$id]=0
        else
          pane_count[$id]=$(( ${pane_count[$id]:-0} + 1 ))
          [ "${pane_count[$id]}" -eq 2 ] && [ "$p" != gone ] && msgs+=("reminder: $id conductor still $p")
        fi ;;
    esac
    pane_last[$id]=$p
  done < <(jq -r '.[] | [.id, .status, (.assignee // ""), (if any((.labels // [])[]; . == "human") then 1 else 0 end)] | map(tostring) | join("|")' <<<"$beads")

  if [ ${#msgs[@]} -gt 0 ]; then
    text=$(printf '%s; ' "${msgs[@]}"); say "${text%; }"
  fi
  if ! jq -e 'any(.[]; .status != "closed")' <<<"$beads" >/dev/null; then
    say "all batches closed"; exit 0
  fi
  sleep "$interval"
done
