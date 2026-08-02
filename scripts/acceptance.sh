#!/usr/bin/env sh
set -eu

profile="${1:-all}"

case "$profile" in
    all | foundation)
        scripts/smoke_foundation.sh
        ;;
    list)
        echo "foundation"
        ;;
    *)
        echo "unknown acceptance profile: $profile" >&2
        echo "run 'scripts/acceptance.sh list' for implemented profiles" >&2
        exit 2
        ;;
esac

echo "acceptance profile passed: $profile"
