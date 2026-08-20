"""Run the frozen panel runner on the stackex corpus under the PREREG's spend cap.

plane_annotate.py is the frozen instrument and is not modified; this wrapper only
lowers its hard cap from the study default ($10) to the forward stake's $0.25 and
calls its main() with the prereg's settings (BASE condition, the three judge families).
"""
import sys
sys.path.insert(0, "/home/emoore/CIRISOntology/scratchpad")
import plane_annotate

plane_annotate.HARD_CAP_USD = 0.25          # GROSS4_FORWARD_PREREG.md spend cap

R = "/home/emoore/CIRISOntology/scratchpad/plane_corpus"
rc = plane_annotate.main(f"{R}/eco_stackex.jsonl", f"{R}/stackex_judgments.jsonl",
                         conditions=["BASE"], models=None, limit=None, workers=8)
print("models:", plane_annotate.MODELS)
sys.exit(rc)
