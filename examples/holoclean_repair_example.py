import holoclean
from detect import NullDetector, ViolationDetector
from repair.featurize import InitAttFeaturizer
from repair.featurize import InitSimFeaturizer
from repair.featurize import FreqFeaturizer
from repair.featurize import OccurFeaturizer
from repair.featurize import ConstraintFeat
from repair.featurize import LangModelFeat


# 1. Setup a HoloClean session.
hc = holoclean.HoloClean(
    pruning_topk=0.0,
    weak_label_thresh=0.90,
    epochs=20,
    weight_decay=0.1,
    threads=20,
    batch_size=32,
    verbose=True,
    timeout=3*60000,
    print_fw=True
).session

# 2. Load training data and denial constraints.
hc.load_data('hospital', '../testdata/hospital.csv')
hc.load_dcs('../testdata/hospital_constraints_att.txt')
hc.ds.set_constraints(hc.get_dcs())

# 3. Detect erroneous cells using these two detectors.
detectors = [NullDetector(), ViolationDetector()]
hc.detect_errors(detectors)

# 4. Repair errors utilizing the defined features.
hc.setup_domain()
featurizers = [
    InitAttFeaturizer(),
    InitSimFeaturizer(),
    OccurFeaturizer(),
    FreqFeaturizer(),
    ConstraintFeat()
]
hc.repair_errors(featurizers)


# 5. Evaluate the correctness of the results.
hc.evaluate('../testdata/hospital_clean.csv', 'tid', 'attribute', 'correct_val')
