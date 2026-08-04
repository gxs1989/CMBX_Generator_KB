# Quality Control & Database

## FOQ Quick Check

- [[../../FOQ/TCC/FOQ_TCC_VX_C10_A_TD_KNOWLEDGE_MANAGEMENT|TCC FOQ knowledge]]
- [[../../FOQ/TCC/TCC_TEST_KNOWLEDGE_NODE_MODEL|TCC test knowledge nodes]]
- [[../../FOQ/RID/RID_OQ_TEST_KNOWLEDGE_BASE|RID OQ knowledge]]
- [[../../FOQ/Detector/FOQ_VDAD_VMWD_TD_KNOWLEDGE_MANAGEMENT|VDAD/VMWD knowledge]]
- [[../../FOQ/Pump/FOQ_VPUMP_TD_KNOWLEDGE_MANAGEMENT|Pump knowledge]]
- [[../../FOQ/Autosampler/FOQ_VAS_TD_KNOWLEDGE_MANAGEMENT|Autosampler knowledge]]

FOQ Quick Check uses FOQ Location mappings to calculate selected metrics from
completed CMBX data, compare them with report Definitions/SPEC evidence, and
optionally compare current values with filtered historical database populations.

## Quality Data & Database

- Production history is read-only for ordinary users.
- Controlled writes require administrator approval.
- Historical filters include table, metric, model, and date scope.
- QC means, variation, control limits, and current CMBX points must retain their
  selected database scope in exported evidence.
