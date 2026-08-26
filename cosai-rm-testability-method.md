# Paired evidence packs for CoSAI-RM

Issue [#491](https://github.com/cosai-oasis/secure-ai-tooling/issues/491) asks for attacks that show each risk is real, and controls that change the outcome. The catalog already proves shape. The missing proof is efficacy. The method is a paired evidence pack per risk: one case without the mapped control, one case with it, both run against a reference subject, never against a live third-party system.

Source: CoSAI-RM schemas on [cosai-oasis/secure-ai-tooling](https://github.com/cosai-oasis/secure-ai-tooling/tree/main/risk-map) `main`, 25 Aug 2026. 36 closed-enum risks, 35 closed-enum controls, 7 universal controls with `risks: all`.

| Metric | Value |
| --- | --- |
| Risks in the closed enum | 36 |
| Efficacy packs on `main` today | 0 |
| Proposed C1 packs (PR CI) | 27 |
| Proposed C2 packs (nightly) | 6 |
| Proposed C3 packs (recorded replay) | 3 |

ADR-025 D1 already declines conventional integration and end-to-end tests. Class 1, 3, and 4 packs are unit tests and schema checks, the same pattern as the sanitizer attack corpus in ADR-015. Class 2 synthetic pipelines need an ADR-025 amendment and a named compute budget. They do not run on every pull request.

## Two proofs, not one

Current hooks in `scripts/hooks/` answer "is the YAML well-formed and cross-linked?" Issue 491 asks "does this risk happen, and does this control stop it?" Both proofs are required. Neither substitutes for the other.

| Proof | What it checks | Where it lives today | Oracle |
| --- | --- | --- | --- |
| Catalog consistency | Closed enums, control-risk reciprocity, component edges, framework pin drift | pre-commit, `validate-all.sh`, ADRs 018 to 022, 027, 034 | Schema and graph validators exit 0 |
| Catalog efficacy | A named attack produces the risk's claimed impact; enabling a mapped control changes that outcome | Missing. Issue 491. | Paired evidence pack: WITHOUT_CONTROL fails the security property; WITH_CONTROL holds it |

## The paired-test contract

Every evidence pack binds one risk id, one reference subject, one or more mapped control adapters, and an oracle. The pack is invalid unless both legs exist. A WITH_CONTROL-only pack never showed the risk. A WITHOUT_CONTROL-only pack never showed the control.

**WITHOUT_CONTROL (risk manifests).** Apply the fixture to the reference subject with the control adapter off. The oracle must report the impact named in the risk's short description: instruction override, unsigned load, planted document retrieved, backdoor trigger rate above bound.

**WITH_CONTROL (control changes the outcome).** Replay the same fixture with the named control adapter on. The oracle must report blocked, rejected, redacted, rate-limited, or contained. The adapter implements the testable obligation of the YAML control, not the prose paragraph itself.

TDD order for a new pack: write the oracle and both expected outcomes first (ADR-025 D2, required for agent work). Implement the subject until WITHOUT_CONTROL is red for the right reason. Implement the adapter until WITH_CONTROL is green. YAML mapping is last. A control does not claim it mitigates a risk until this pair is green.

## Four testability classes

"Unit tests for each risk" is true only after you classify how the oracle is computed. The closed enum has 36 risks. They do not share one runtime.

Proposed assignment of the 36 risks: 27 C1, 6 C2, 3 C3. C4 is reserved for the 7 universal controls (process evidence), not for extra risk rows. Source: schema enums on `main`.

### C1: Deterministic fixture

Exact oracle. No GPU. Runs on every PR. Stub orchestrator, digest check, allowlist, rate limit, inventory miss, cache key.

Gate: `pytest` or `node --test`. Wall clock per pack under 5s. Fits ADR-025 D1 as written.

### C2: Synthetic mini-pipeline

Threshold oracle on a tiny model or tiny train set: backdoor trigger rate, membership AUC, planted-eval score.

Gate: scheduled workflow, not PR CI. Budget named in the pack (CPU minutes, optional GPU minutes). Requires amending ADR-025 D1.

### C3: Recorded replay

Frozen request, response, or hardware trace from a cited study. The adapter predicate is tested against the trace. The live attack is not re-run.

Gate: PR CI. Proves the control would have fired on that evidence. Does not prove the attack still works on a new model.

### C4: Process evidence

One pack per universal control: red teaming, vulnerability management, threat detection, incident response, internal policies, product governance, risk governance.

Oracle is an attestation artifact that names a risk sample, owner persona, and date. Not 36 times 7 runtime tests.

## Evidence pack shape

Keep attack fixtures out of `risks.yaml`. The public catalog stays the reuse contract in ADR-014. Packs live in a sibling tree and cite closed-enum ids.

`risk-map/evidence/`

- `schema.json`: pack manifest (risk id, class, compute gate, reference subject id, control ids, oracle type, budgets).
- `packs/<riskId>/manifest.yaml`: one directory per risk, additional packs as suffixes when a risk needs more than one mechanism.
- `fixtures/`: inputs and expected oracle results for both legs. Minimum input that trips the oracle. No exploit writeup.
- `adapters/`: small functions that implement the testable obligation of a YAML control against this subject. `controlInputValidationAndSanitization` is a filter. `controlAgentExecutionBounds` is a step cap. `controlTrainingDataSanitization` is a dataset scanner.
- `subjects/`: the smallest stub that can exhibit the risk. Shared subjects are allowed (one stub orchestrator for several input-boundary risks).

## Coverage invariants

Copy the sanitizer meta-test: adding a risk id without a pack fails CI once the gate is on. Do not turn that gate on for the existing 36 until pathfinders land. ADR-034 D3a still allows orphan components and personas. Evidence is a risk obligation, not a leaf obligation.

| Invariant | Pass | Fail | When it blocks |
| --- | --- | --- | --- |
| Pack well-formed | Manifest schema, ids in closed enums, controls are a subset of `risk.controls` or universal | Unknown id, missing leg, control not mapped to that risk | Phase 0, every PR that touches `evidence/` |
| New risk has a pack | Layer 5 (or 4, if co-landed) includes at least one pack citing the new id | Risk YAML lands with no pack | Phase 2, amend ADR-034 landing guide |
| Existing risk coverage | Count of risks with a passing pack, reported on `main` | A mapped pack turns red | Never claim 36/36. Report N/36 and the miss list |
| Control attribution | Each non-universal control on a risk appears in at least one WITH_CONTROL leg, or the pack names which subset is the testable mechanism | YAML lists a control that no pack cites and no exception records | Phase 3 warning, then error |
| Wire-up (ADR-025 D10) | Harness invoked from `validate-all.sh` and a CI job | Packs exist but no execution path runs them | Phase 0 |

## Pathfinders

Five packs, four classes of mechanism, before any coverage gate on the rest of the catalog. Each row names the control adapter that must change the oracle.

| Risk | Class | Control adapter | WITHOUT | WITH |
| --- | --- | --- | --- | --- |
| `riskPromptInjection` | C1 | `controlInputValidationAndSanitization` | Stub agent follows injected instruction | Input boundary rejects or isolates the instruction |
| `riskMaliciousLoaderDeserialization` | C1 | `controlSecureByDefaultMLTooling` | Dummy load hook runs | Non-allowlisted format refused |
| `riskRunawayAgentToolLoops` | C1 | `controlAgentExecutionBounds` | Tool call count exceeds bound | Runtime stops at the bound |
| `riskRetrievalVectorStorePoisoning` | C1 | `controlRetrievalAndVectorSystemIntegrity` | Planted document is the top hit | Unsigned or mutated chunk rejected |
| `riskDataPoisoning` | C2 | `controlTrainingDataSanitization` | Tiny model trigger rate above bound | Scanner drops the poisoned slice; trigger rate falls below bound |

Add one C4 pack in the same phase: `controlRedTeaming` requires an attestation that names a risk sample, the persona who ran it, and a dated artifact path. That pack is the template for the other six universal controls.

## Proposed class for every risk

Starting assignment for maintainers to confirm, not a scored grade. Pathfinder rows are marked in the Pathfinder column.

A miss is a risk whose class is wrong, whose subject cannot exhibit the impact, or whose oracle is not measurable. Reclassify; do not force C1 onto a hardware side channel.

| Risk id | Title | Class | Pathfinder | Reference subject | Oracle |
| --- | --- | --- | --- | --- | --- |
| `riskPromptInjection` | Prompt Injection | C1 | yes | Stub orchestrator with a system instruction | Instruction override vs blocked at input boundary |
| `riskMaliciousLoaderDeserialization` | Malicious Loader Deserialization | C1 | yes | Dummy artifact whose load hook only sets a flag | Flag set vs load refused for unsigned format |
| `riskRunawayAgentToolLoops` | Runaway Agent Tool Loops | C1 | yes | Toy agent that re-calls a tool until a cap | Unbounded calls vs stop at execution bound |
| `riskInsecureModelOutput` | Insecure Model Output | C1 | | Output renderer with the site sanitizer contract | Unsafe token emitted vs escaped or rejected |
| `riskRogueActions` | Rogue Actions | C1 | | Tool dispatcher with an allowlist | Unlisted tool runs vs denied |
| `riskRetrievalVectorStorePoisoning` | Retrieval Vector Store Poisoning | C1 | yes | Stub embedder plus planted document | Planted doc retrieved vs integrity check rejects it |
| `riskPromptResponseCachePoisoning` | Prompt Response Cache Poisoning | C1 | | Shared cache keyed only on prompt text | Cross-tenant hit vs cache key includes tenant and auth |
| `riskOrchestratorRouteHijacking` | Orchestrator Route Hijacking | C1 | | Route table with a signed default path | Unsigned rewrite honored vs rejected |
| `riskToolRegistryTampering` | Tool Registry Tampering | C1 | | In-memory tool registry | Unsigned swap succeeds vs signature miss |
| `riskToolSourceProvenance` | Tool Source Provenance | C1 | | Tool install from a local path | Missing provenance accepted vs refused |
| `riskAdapterPEFTInjection` | Adapter PEFT Injection | C1 | | Adapter attach API | Unsigned adapter loads vs digest mismatch |
| `riskModelSourceTampering` | Model Source Tampering | C1 | | Pinned source snapshot | Altered bytes accepted vs digest fail |
| `riskModelDeploymentTampering` | Model Deployment Tampering | C1 | | Deploy slot with expected digest | Wrong artifact serves vs blocked |
| `riskModelExfiltration` | Model Exfiltration | C1 | | Egress stub with an allowlist | Weights leave vs deny |
| `riskInsecureIntegratedComponent` | Insecure Integrated Component | C1 | | Plugin load with SBOM check | Unknown component loads vs refused |
| `riskDenialOfMLService` | Denial of ML Service | C1 | | Fixed-cost inference stub | Request storm exhausts queue vs rate limit |
| `riskEconomicDenialOfWallet` | Economic Denial of Wallet | C1 | | Metered tool calls | Spend exceeds cap vs hard stop |
| `riskMCPTransportHijacking` | MCP Transport Hijacking | C1 | | Fake MCP channel with peer identity | Unverified peer accepted vs rejected |
| `riskCrossTenantCredentialPropagation` | Cross-Tenant Credential Propagation | C1 | | Two tenants sharing a runtime | Token visible across tenants vs isolated |
| `riskStaleAgentIdentityBinding` | Stale Agent Identity Binding | C1 | | Agent credential with expiry | Expired binding still authorizes vs revoked |
| `riskAgenticDelegationConfusedDeputy` | Agentic Delegation Confused Deputy | C1 | | Delegated tool call under reduced scope | Deputy exceeds grant vs permission check |
| `riskAgentDelegationChainOpacity` | Agent Delegation Chain Opacity | C1 | | Multi-hop agent call | Hop missing from log vs full chain recorded |
| `riskShadowAndUnknownAgents` | Shadow and Unknown Agents | C1 | | Inventory plus a running agent | Unlisted agent runs vs inventory miss |
| `riskZombieShadowMCPServers` | Zombie Shadow MCP Servers | C1 | | MCP listener not in inventory | Unregistered server answers vs blocked |
| `riskSensitiveDataDisclosure` | Sensitive Data Disclosure | C1 | | Context window with a canary string | Canary appears in output vs redacted |
| `riskExcessiveDataHandling` | Excessive Data Handling | C1 | | Store with a retention clock | Record remains after TTL vs deleted |
| `riskExcessiveDataHandlingDuringInference` | Excessive Data Handling During Inference | C1 | | Inference logger | Raw prompt persisted vs redacted |
| `riskDataPoisoning` | Data Poisoning | C2 | yes | Tiny classifier plus a labeled backdoor slice | Trigger accuracy above threshold vs sanitizer drops the slice |
| `riskUnauthorizedTrainingData` | Unauthorized Training Data | C2 | | Tiny train set with a license canary | Canary in fitted model vs scanner rejects the set |
| `riskEvaluationBenchmarkManipulation` | Evaluation Benchmark Manipulation | C2 | | Held-out set with planted items | Score inflates vs provenance check on eval set |
| `riskModelEvasion` | Model Evasion | C2 | | Tiny linear model with a known adversarial input | Label flips vs input validation or adversarial training adapter |
| `riskInferredSensitiveData` | Inferred Sensitive Data | C2 | | Tiny membership-inference setup | Attack AUC above bound vs PET adapter drops it |
| `riskFederatedDistributedTrainingPrivacy` | Federated Distributed Training Privacy | C2 | | Two-client toy federated round | Client record reconstructed vs noise or clip adapter |
| `riskModelReverseEngineering` | Model Reverse Engineering | C3 | | Frozen extraction-query trace | Trace would have exceeded query budget vs bound would fire |
| `riskCovertChannelsInModelOutputs` | Covert Channels in Model Outputs | C3 | | Recorded output that encodes a planted bit | Decoder recovers the bit vs output validator flags it |
| `riskAcceleratorAndSystemSideChannels` | Accelerator and System Side Channels | C3 | | Recorded timing or cache trace from a published study | Predicate matches the leak vs isolation control would apply |

## How this lands in the repo

| Phase | Deliverable | ADR / hook change | Compute |
| --- | --- | --- | --- |
| 0, Contract | Evidence schema, harness CLI, empty pack tree, well-formed and wire-up tests | New ADR (next after 037). Cite ADR-025 D1/D2/D10 and ADR-034 D3a. Hook in `validate-all.sh` | None |
| 1, Pathfinders | Five risk packs plus one C4 red-team attestation pack | No coverage gate on the other 31 risks | C1 on PR CI. C2 DataPoisoning on a scheduled job with a published minute budget |
| 2, New work | Any new Layer 4/5 risk includes a pack in the same PR | Amend `landing-sequence.md`. Existing 36 still uncovered until packs land | C1/C3/C4 on PR. C2 scheduled |
| 3, Backfill | Remaining C1, then C3, then C2. Report N/36 on `main` | Control-attribution warning, then error | Ask member orgs for a nightly runner if C2 exceeds GitHub-hosted minutes |

## What efficacy reports

Three counts, generated from pack results, not from YAML length. A miss is a risk with no passing pack, or a mapped non-universal control that no WITH_CONTROL leg cites.

**Risk coverage.** Passing packs / 36 closed-enum risks. Publish the miss list. Do not write "complete coverage."

**Control attribution.** WITH_CONTROL legs / non-universal control edges in `risks.yaml`. Universal controls counted separately as 7 attestation packs.

**Drift.** If YAML drops a control from a risk, the pack that cited it fails until updated. Mapping and evidence stay bidirectional, same as control-risk reciprocity.

## Open problems the current model does not answer

Live-model flakiness. A prompt-injection pack against a stub is stable. The same pack against a vendor LLM is not a unit test and is out of scope until someone names a model pin, a seed, and an acceptable attack-success bound.

Adapter fidelity. A step cap is a fair stand-in for `controlAgentExecutionBounds`. A one-page policy is not a fair stand-in for `controlInternalPoliciesAndEducation`. C4 exists because that gap is real.

Multi-control risks. `riskDataPoisoning` lists several controls. The pathfinder tests sanitization first. The method does not yet say whether remaining controls on that risk are independent legs or a documented subset.

Hardware and extraction. C3 replay never re-proves the original paper. If CoSAI-RM needs live side-channel evidence, that is a separate compute and lab ask, not a pytest file.

Style of the existing sanitizer corpus (ADR-015 / issue 241): fixtures as data, meta-test on ids, CI fails when an id ships without a fixture. That pattern, applied to risk ids, is the whole method.
