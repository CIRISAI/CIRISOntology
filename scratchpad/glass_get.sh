#!/bin/bash
# One sequential driver: download a member, convert it to the compact form,
# purge the tarball.  Peak extra disk is one tarball.  Under flock so a second
# invocation cannot race the first onto the same partial file -- which is
# exactly how the 2026-07-27 corruption happened.
cd /home/emoore/CIRISOntology/scratchpad || exit 1
for spec in "KA_models:KA:0.44" "KA_models:KA:0.50" "KA_models:KA:0.56" "KA_models:KA:0.64" \
            "KA2D_models:KA2D:0.23" "KA2D_models:KA2D:0.30"; do
  IFS=: read -r dir tag t <<< "$spec"
  f="${tag}_T${t}"
  [ -f "glass/compact/$f.npz" ] && { echo "SKIP $f (already converted)"; continue; }
  echo "FETCH $f $(date)"
  python3 glass_zipfetch.py get "GlassBench/$dir/T${t}.tar.gz" "glass/raw/$f.tar.gz" || { echo "FETCHFAIL $f"; continue; }
  echo "CONVERT $f $(date)"
  python3 glass_convert.py "glass/raw/$f.tar.gz" "glass/compact/$f.npz" "glass/compact/$f.meta.json" \
    && rm -f "glass/raw/$f.tar.gz" \
    && echo "OK $f $(date) free=$(df -h / | tail -1 | awk '{print $4}')"
done
echo ALLDONE
