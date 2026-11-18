#!/usr/bin/env bash
# Wake the Lead through pi-intercom only when a goal bead's batch beads change.
# Usage: watch-goal.sh <goal-id> <lead-intercom-name> <beads-dir>
# Conductor sessions must be named after their batch bead ID.
# Env: WATCH_INTERVAL (s, default 180), IDLE_LIMIT (s, default 900),
#      PI_INTERCOM (command, default: pi-intercom on PATH, else the Pi npm package).
set -u
goal=${1:?goal bead id}; lead=${2:?lead intercom name}; store=${3:?beads dir}
interval=${WATCH_INTERVAL:-180}; idle_limit=${IDLE_LIMIT:-900}
if [ -n "${PI_INTERCOM:-}" ]; then ic=$PI_INTERCOM
elif command -v pi-intercom >/dev/null; then ic=pi-intercom
else ic="node $HOME/.pi/agent/npm/node_modules/pi-intercom/cli.mjs"; fi

declare -A last seen_count idle_since
send() { $ic send --to "$lead" --text "watch $goal: $1" >/dev/null 2>&1 || echo "send failed: $1" >&2; }

while :; do
  beads=$(BEADS_DIR=$store bd --readonly list --parent "$goal" --all --limit 0 --json 2>/dev/null) || { echo "bd list failed" >&2; sleep "$interval"; continue; }
  sessions=$($ic list --json 2>/dev/null || echo '{}')
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

    # Idle check: the Conductor session carries the bead ID as its name.
    if [ "$status" = in_progress ] && [ "$assignee" != "$lead" ]; then
      s=$(jq -r --arg n "$id" '[.. | objects | select(.name? == $n) | .status][0] // "gone"' <<<"$sessions")
      if [ "$s" = idle ]; then
        [ "${idle_since[$id]:-}" = gone ] && unset 'idle_since[$id]'
        idle_since[$id]=${idle_since[$id]:-$now}
        [ $(( now - idle_since[$id] )) -ge "$idle_limit" ] && { msgs+=("$id conductor idle $(( (now - idle_since[$id]) / 60 )) min"); idle_since[$id]=$now; }
      elif [ "$s" = gone ]; then
        [ "${idle_since[$id]:-}" = gone ] || msgs+=("$id conductor session not found")
        idle_since[$id]=gone
      else unset 'idle_since[$id]'; fi
    fi
  done < <(jq -r '.[] | [.id, .status, (.assignee // ""), (if any((.labels // [])[]; . == "human") then 1 else 0 end)] | map(tostring) | join("|")' <<<"$beads")

  if [ ${#msgs[@]} -gt 0 ]; then
    text=$(printf '%s; ' "${msgs[@]}"); text=${text%; }
    echo "$(date +%T) $text"; send "$text"
  fi
  if ! jq -e 'any(.[]; .status != "closed")' <<<"$beads" >/dev/null; then
    send "all batches closed"; exit 0
  fi
  sleep "$interval"
done
