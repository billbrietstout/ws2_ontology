# AI Jailbreak Prevention Framework

CoSAI Workstream 2, RFC 0.1  
25 August 2026

CJS scores how far a prompt technique takes an attacker past one model's safeguards. This framework assigns who prevents that technique from becoming an unauthorized tool call, memory write, or hop, with what control, and with what evidence.

## Claims that do not follow from the table of contents

A CJS-1 completion on a production-write agent is paged as O-2. The same completion in a chat window with no tools is a weekly log review.

Tool calls that run under an agent service account raise ENV even when the user-facing model refused in chat. Jailbreak success is the side effect, not the chat transcript.

CJS gain of 0 stops the model-policy score. JPF still scores ENV, because a textbook payload can fire a tool.

The Model Provider publishes the CJS band. The Application Developer publishes the ENV band. AI System Governance records the operational class O. Neither party may lower the other's number.

Prompt-injection detectors and jailbreak classifiers are separate controls. A trip of one does not close a ticket of the other.

Safety-margin false positives are an L1 accepted rate, not a classifier bug to be silently tuned away. Fable 5 made that trade in public; the deploying organization names who absorbs it.

If cyber classifiers are off, CJS does not apply. O is taken from ENV. The OpenAI Hugging Face evaluation escape is that case: no model-policy bypass, a shared writable cache, production reach.

## CJS, ENV, and O

Anthropic's [Redeploying Fable 5](https://www.anthropic.com/news/redeploying-fable-5) (30 June 2026) asked industry for a shared way to judge jailbreak severity. The named drafters are Amazon, Microsoft, Google, and other Glasswing partners. The 2 July follow-up publishes that draft as Cyber Jailbreak Severity (CJS): four axes, bands CJS-0 through CJS-4, a floor that may be raised and never lowered.

CoSAI is not on that drafting list. Individual member labs may score model bypasses as Model Providers. The OASIS project assigns prevention in deployed systems.

| Artifact | Who publishes it | Question it answers |
| --- | --- | --- |
| CJS band | Model Provider, using the Glasswing draft | How far past this model's safeguards does the recipe go, relative to other tools and models? |
| ENV band | Application Developer, using `data/scoring.json` | After the completion leaves the model, which tools, hops, memory, principal, and human-review window are live? |
| O class | AI System Governance | Which IR SLA runs, and which persona contains? |
| Control | One SRF persona | Who prevents, detects, or contains, and what artifact proves it? |

CJS remains the industry language for talking to labs and government about a model-policy bypass. O is the language for paging an operator.

Charter §4 puts prompt injection, model theft, poisoning, scaled abuse, and inference attacks in scope. It puts malware generation, phishing generation, and other content safety out of scope. CJS-3 and CJS-4 examples in the 2 July draft include malware authoring and exploit writing. Operators consume those bands as severity inputs. They do not re-score the content as a CoSAI product.

## Terms

**Jailbreak (model).** A prompt technique that causes a model to produce a completion that violates the model's stated policy or classifier boundary.

**Jailbreak (system).** An unauthorized side effect: tool call, write, payment, code run, or data read, reached because a model policy or a hop policy failed. The user-facing model can still refuse in chat.

**Prompt injection.** Untrusted content treated as instruction. Distinct from jailbreak. A jailbreak of model A is often implemented as prompt injection into model B.

**Bypass.** Anthropic footnote 2 treats bypass as a synonym of jailbreak for CJS. JPF uses jailbreak for policy-boundary failure and prompt injection for instruction-confusion.

**Safety margin.** Classifiers block some benign and low-risk dual-use requests so that high-risk dual-use is less likely to pass. Users see this as refusals of reasonable coding work. Fable 5 set this margin larger than prior launches.

**High-risk dual use.** Work that defenders and attackers both do (penetration tests, exploit development, lateral movement). The 2 July safeguards post says what separates the legitimate case from harm is who is doing the work and under what authorization. CJS then scores the prompt technique without that context. JPF-L1-001 is that authorization.

**Persona, layer, control, obligation, attestation.** SRF nouns. Each control names one accountable persona at one layer, the obligation that persona performs, and the artifact that proves it.

## Imported CJS

Full rubrics live in [More details on Fable 5's cyber safeguards and our jailbreak framework](https://www.anthropic.com/news/fable-safeguards-jailbreak-framework). JPF does not re-author them.

| Axis | Range | Asks |
| --- | --- | --- |
| Capability gain | 0 to 4 | How far beyond existing tools and weaker models? Gain 0 stops scoring; the finding is CJS-0. |
| Breadth | 0 to 2 | How many distinct offensive tasks does the same recipe unlock? |
| Ease of weaponization | 0 to 2 | How much LLM skill to go from recipe to a working attack? |
| Discoverability | 0 to 2 | How easy is it to obtain the technique? |

Sum maps to CJS-0 (0), CJS-1 (1 to 3.5), CJS-2 (4 to 6.5), CJS-3 (7 to 8.5), CJS-4 (9 to 10). The 30 June post describes three qualitative shapes that sit under those numbers: minor (safety-margin intrusion), narrow harmful (one harmful behavior), and universal (a class of harmful behaviors).

The computed band is a floor. Discretionary raises include an output severe enough on its own, no near-term mitigation, or compounding with other open findings.

System-prompt extraction is out of CJS cyber scope. It is also out of JPF unless the extracted text is then used to cause a system side effect; that case is scored under ENV and IR, not as a CJS raise invented by the operator.

## ENV modifier

CVSS has a base score and an environmental score. CJS as drafted is base plus a temporal-like discoverability axis. ENV scores the path after the completion leaves the model.

| Axis | 0 | 1 | 2 | 3 |
| --- | --- | --- | --- | --- |
| Tool authority | No tools; chat only | Tools bound to the original user's token | Tools run under an agent service account | Tools can write production systems, move money, or change identity |
| Graph depth | One model, one completion | 2 to 3 hops | 4 or more hops, or recursive peer calls | n/a |
| Persistence | This session only | Memory or RAG write that later turns treat as instruction | Standing skill, scheduled job, or cross-user plant | n/a |
| Authorization fidelity | Named principal; hop carries original user_id | Principal dropped; callee trusts the agent identity | No principal, confused deputy, or unknown authorization | n/a |
| HITL window | Human can review before the side effect | Human on loop; can interrupt some actions | Faster than HITL; no review before tool fire | n/a |

Sum 0 to 2 is ENV-0 (isolated chat), 3 to 5 is ENV-1 (user-bound tools), 6 to 8 is ENV-2 (delegated agent), 9 to 11 is ENV-3 (production-write graph).

Floors, applied after the sum: tool authority 3 forces ENV-3; HITL 2 with tool authority ≥ 2 forces ENV-3; persistence 2 forces at least ENV-2; authorization fidelity 2 forces at least ENV-2.

For autonomous agents, HITL 2 is the expected value, not a rare floor. [Recommendations from the Hugging Face Autonomous Attack](https://www.linkedin.com/pulse/recommendations-from-hugging-face-autonomous-attack-bill-stout-el4ic) states that a human approval gate slower than the agent gets bypassed, and that human-in-the-loop is not viable for most agentic use cases. Hard gates stay on high-impact or irreversible actions; the rest is automatic.

The Application Developer publishes ENV per production system-id (JPF-L3-006) and recomputes it within 5 business days of a tool, hop, or memory-policy change.

## Operational class

```
O starts at the CJS band index (0 to 4).
If ENV band >= 2, raise O by 1, cap at 4.
If CJS is 0, raise at most to O-1.
Never lower CJS.
Exception: if cyber classifiers are off, CJS is not applicable.
O is taken from ENV: ENV-0 or ENV-1 maps to O-2, ENV-2 maps to O-3, ENV-3 maps to O-4.
```

| O | Operator obligation | Provider obligation |
| --- | --- | --- |
| O-0 Log | Write prompt, completion, CJS, and ENV to the IR log. Review the week's O-0 bucket every 7 days. No page. | No classifier patch. Count toward monthly safety-margin false-positive reporting if the request was benign. |
| O-1 Ticket | Ticket within 1 business day. If a tool path is bound, freeze that tool class for the session until a named L3 owner accepts residual risk. | Acknowledge in the VDP queue. No 24/7 page. |
| O-2 Contain | Page on-call within 4 hours. Kill the session. Disable the implicated tool class or hop. Confirm the agent has stopped acting, not only that it is unreachable. Notify the Model Provider of the miss. | Triage within 1 business day. Say whether CJS will be raised. Do not lower it. |
| O-3 Mitigate | Page immediately. Kill sessions that used the recipe. Freeze memory writes for the affected agent. Confirm the agent has stopped acting, not only that it is unreachable. Named L1 executive informed the same calendar day. | Preliminary mitigation within 24 hours of confirmed CJS-3. 24/7 watch channel. Share the new safeguard so an independent tester can re-run the recipe. |
| O-4 Halt path | Page immediately. Take the model or the write-capable tool path offline if the recipe is in active use. Confirm the agent has stopped acting, not only that it is unreachable. If the system is in a national-security or critical-infrastructure program, notify the designated government counterpart the same day. | Immediate preliminary mitigation on confirmed CJS-4, matching the 30 June most-severe class. 24/7 channel. Share the new safeguard for independent test. |

O-3 and O-4 provider clocks are the CoSAI assignment of clocks the 30 June post already stated for the most severe class (immediate preliminary mitigations; 24/7 watch). They are not a CoSAI invention of CJS itself.

The classifier-off exception is required because CJS scores a bypass of a live safeguard. [Who is responsible for what](https://www.linkedin.com/pulse/who-responsible-what-accountability-assessment-openai-bill-stout-s1dsc/) records production cyber classifiers turned off for an evaluation; the compensating control is agent reach. Confirming the agent has stopped acting, not only that it is unreachable, is taken from [Recommendations from the Hugging Face Autonomous Attack](https://www.linkedin.com/pulse/recommendations-from-hugging-face-autonomous-attack-bill-stout-el4ic).

The AI Incident Response Framework remains the playbook. O selects which playbook clock starts. Jailbreaking and prompt injection stay separate incident types in that taxonomy.

## Controls

Each cell is the obligation, not a status label. Machine-readable records with thresholds are in `data/controls.json`.

### L1 AI Business & Usage

**JPF-L1-001 Named authorization for high-risk dual use.** AI System Governance maintains a roster of principals allowed to request penetration tests, exploit development, and related high-risk dual-use work, with expiry and an approving executive. L3 allowlists and L4 serving policy enforce the roster. Completions that match the high-risk list without a live grant are unauthorized: count target 0 in 7 days, else kill the session and revoke tool bindings.

**JPF-L1-002 CJS intake without rescoring.** Governance files every inbound CJS finding against the affected system-id within 1 business day, computes O from published CJS plus current ENV, and never lowers CJS. Target: ≥ 0.95 of inbound reports in 30 days have CJS, ENV, and O populated, else escalate to the named L1 executive.

**JPF-L1-003 Accepted safety-margin false-positive rate.** Governance writes a numeric accepted rate into the risk statement and compares it to the Model Provider's monthly figure. If the provider exceeds the accepted rate, governance renegotiates the classifier threshold or changes model. The schema does not invent a universal rate.

**JPF-L1-004 Jailbreak incident commander.** A named human owns containment for O-2 and above, with a deputy. O-3 and O-4 require 24/7 cover. Prompt injection remains a separate incident type. Target: ≥ 0.95 of O-2+ pages in 30 days acknowledged inside the SLA.

### L2 AI Information

**JPF-L2-001 Instruction-class versus data-class labeling.** Data Provider tags every retrieved chunk and tool observation as instruction or data at write time. Unlabeled spans are not assembled into prompts. Target: 0 unlabeled spans served in 7 days, else halt retrieval until backfill.

**JPF-L2-002 Mediated memory writes.** Instruction-class memory writes require a named Application Developer decision. Unreviewed instruction-class writes in 7 days: 0, else freeze memory writes.

**JPF-L2-003 Jailbreak-recipe data restricted.** Working recipes live in a restricted corpus with access logging. Recipe strings in customer-visible logs in 7 days: 0, else rotate access and purge.

### L3 AI Application

**JPF-L3-001 Tool calls bound to the original user token.** Application Developer passes the original principal into each tool adapter. Fraction of production tool calls in 7 days missing that principal: ≤ 0.01, else disable the service-account tool path. L1 may accept a higher ENV tool_authority in writing; that acceptance is visible in the ENV record, not implicit in the adapter.

**JPF-L3-002 Peer models treated as untrusted speakers.** Agentic Platform Provider wraps A→B messages as data-class content and runs B's detectors before B's tools fire. Inter-model messages that reach a tool adapter with no detector result in 7 days: 0, else break the hop.

**JPF-L3-003 Output filter before tool fire.** The completion is not authorization. Adapter log records proposed call, filter decision, and grant-id or deny reason. Tool fires without a filter decision in 7 days: 0, else disable unfiltered adapters.

**JPF-L3-004 Split-payload and stitch detection.** Per-turn blocked spans are retained for the session. A later tool call that reconstructs a blocked span is refused. Quarterly verification: reconstruct a known blocked span across three turns and confirm the adapter refuses. Fail the release gate if the test does not pass.

**JPF-L3-005 Prompt-injection detector distinct from jailbreak classifier.** Two detector ids, two IR types. A jailbreak trip does not close a prompt-injection ticket. Missing either detector at release: block the release.

**JPF-L3-006 Published ENV band per system.** Five axis scores, band, scorer, date, triggering change. ≥ 0.95 of production system-ids have an ENV record dated after the last tool/hop/memory change, or less than 90 days old if nothing changed. Miss: freeze new tool bindings.

### L4 AI Platform

**JPF-L4-001 Session kill and tool-class rate limit on detector trip.** AI Platform Provider invalidates the session within 5 seconds p95 in the quarterly drill and rate-limits the implicated tool class for that tenant for 24 hours or until a named commander lifts it.

**JPF-L4-002 Fallback routing with user notice.** AI Model Serving routes a classifier-block to the named fallback model or returns a block notice. Blocked completions that still hit tools in 7 days: 0, else disable that gateway's tool path. Silent continue and silent drop both fail the control.

**JPF-L4-003 Path attestation on every tool call.** Fields: user_id, session_id, model_id, hop_id, tool_name, outcome. Completeness ≥ 0.95 of production tool calls in 7 days. Miss: halt new tool bindings until the fields are present. Shared agent identities fail this control.

**JPF-L4-004 Tenant isolation of memory and skills.** Quarterly test: write instruction-class memory in tenant A, read from tenant B, expect empty. Any successful cross-tenant read: take shared memory offline.

### L5 AI Model Provider

**JPF-L5-001 Defense-in-depth safeguards on the served model.** Model Provider documents refusal training, runtime classifiers, and offline monitoring, plus the four dual-use categories (prohibited, high-risk dual use, low-risk dual use, benign) used for Fable 5. Operators do not retrain these. Missing documentation at onboarding: do not bind write-capable tools. If classifiers are off for an evaluation, the same note records that fact and the L1 residual-risk statement id that names third-party production systems the eval can reach.

**JPF-L5-002 CJS scoring of incoming cyber jailbreaks.** Provider publishes gain, breadth, ease, discoverability, initial band, and any discretionary raise. ≥ 0.95 of in-scope reports in 30 days carry a published band. Miss: pause new model launches until the backlog clears.

**JPF-L5-003 VDP channel and 24/7 watch for CJS-3 and CJS-4.** Published submission URL, staffed intake, CJS-4 acknowledged within 1 hour of confirmation. If no CJS-4 arrived, the control is met only if the roster exists.

**JPF-L5-004 Classifier patch shared for independent test.** Confirmed CJS-3: retestable mitigation in the serving path within 24 hours. Confirmed CJS-4: immediate. The reporting party and the operator's named red team get a retest path. Miss on CJS-3: operator takes write-capable tools offline.

## Worked examples

Scoring below uses the published CJS rules and the ENV rules in `data/scoring.json`. Axis values for CJS examples follow the 2 July appendix where the article already scored them.

**Textbook SQL injection from a "teaching junior developers" prompt.** The 2 July appendix scores this CJS-0 (gain 0; scoring stops). In a chatbot with no tools (ENV-0) the operational class is O-0: log, weekly review. In an agent whose tools can write production databases, with no human review before fire (tool authority 3, HITL 2), floors force ENV-3. CJS-0 may rise only to O-1: ticket, freeze the write path for the session. The recipe added no attacker capability; the live tool path still needs an owner.

**Amazon report on Fable 5, as described 30 June 2026.** Researchers prompted the model so that it identified software vulnerabilities and, in one case, produced demonstration code. Anthropic reported that less capable models identified the same vulnerabilities, that every tested model could produce the same demonstration, and that the technique did not expose Mythos-level cyber capability. The 30 June post places this in the minor / safety-margin category. Capability gain against the public baseline is 0 or 1. Breadth is at most one vulnerability type. If scored CJS-0, operator response follows the textbook case above. If scored CJS-1, chat-only ENV-0 stays O-1; an ENV-2 or ENV-3 deployment raises to O-2 and the session's tool class is disabled until L3 accepts residual risk. JPF does not re-score the Amazon evidence; it consumes whichever band the Model Provider publishes and applies ENV.

**Universal system-prompt override, 2 July appendix.** CJS-4 (gain 4, breadth 2, ease 2, discoverability 2). Any ENV yields O-4. Operator takes the write-capable tool path offline if the recipe is in active use. Provider ships an immediate preliminary mitigation and a retest path.

**Encoding-scheme jailbreak, 2 July appendix.** CJS-2 (gain 3, breadth 2, ease 1, discoverability 0). Chat-only ENV-0 stays O-2: page within 4 hours, kill session, notify the provider. The same recipe on an ENV-2 delegated agent becomes O-3: freeze memory writes, inform the L1 executive the same day, 24-hour provider mitigation clock.

**Hop-2 implementation of a CJS-1 text bypass.** Model A produces a completion that sits inside the safety margin (CJS-1). Model B treats A's text as an internal instruction and calls a production-write tool under a service account (graph 1, tool authority 3, authorization fidelity 1 or 2). ENV floors to 3. O becomes 2. Failed controls: JPF-L3-002 (peer as untrusted speaker), JPF-L3-001 (original principal), JPF-L3-003 (filter before tool fire). The CJS band on A's recipe stays 1.

**OpenAI Hugging Face evaluation escape, classifiers off.** Production cyber classifiers were off so the lab could measure capability. CJS is not applicable. Eval sessions that never shared a prompt still read and wrote the same package-proxy cache, first as files and then as directory names after a wipe (persistence 2, authorization fidelity 2, graph at least 1). The path reached a third-party code-execution harness and then Hugging Face production workers (tool authority 3, HITL 2). Floors force ENV-3. Classifier-off maps ENV-3 to O-4: take the write-capable path offline, confirm the agents have stopped acting. Failed controls: JPF-L5-001 (classifiers off without a residual-risk statement that named third-party production), session isolation inside one tenant (not covered by JPF-L4-004), JPF-L3-001 (shared proxy identity rather than one credential per session). Source: the 14 August accountability assessment.

## Coverage measurement

Count production system-ids in the model inventory (the SRF L1 inventory control, or the operator's equivalent). A system is in coverage when it has a current ENV record (JPF-L3-006), a named incident commander (JPF-L1-004), and path attestation completeness ≥ 0.95 for 7 days (JPF-L4-003).

Target: ≥ 0.90 of production system-ids that bind tools meet coverage. Miss: freeze new tool bindings on uncovered system-ids. Chat-only system-ids may omit tool attestation; they still need ENV and a commander.

JPF measures assignment, clocks, and evidence. Fable 5 states that making a model fully robust to jailbreaks is probably impossible.

## Open problems

ENV weights are uncalibrated. No inter-rater study exists for the five axes. Until that study exists, two Application Developers can publish different ENV bands for the same system; Governance records both and uses the higher band.

CJS capability gain is measured against tools and models available at assessment time. The 2 July Log4Shell trio shows the same model behavior dropping from CJS-4 to CJS-0 once scanners exist. Operators need a dated baseline on every ticket. JPF does not yet specify who maintains a shared baseline catalog across vendors.

No OpenTelemetry GenAI field currently means "this hop looked like a jailbreak." JPF-L4-003 requires hop_id and outcome; it does not yet require a detector-result field that survives A→B forwarding. WS2 telemetry work should add that field before ENV graph_depth ≥ 1 can be audited without vendor-specific logs.

Authorization for high-risk dual use is an identity protocol. JPF-L1-001 names the roster and the grant file. It does not specify how a Model Provider running a shared multi-tenant API verifies that grant in real time. Fable 5 blocked high-risk dual use for that reason. The identity handshake between operator grant and provider classifier is unspecified.

Universal jailbreaks of Fable 5 were unreported at the 30 June writing. ENV scoring of a universal recipe in a multi-agent graph with shared memory is untested. Do not treat the hop-2 example as a measured residual risk; it is a control-failure illustration.

Session isolation inside one tenant is unspecified. JPF-L4-004 tests tenant A versus tenant B. The OpenAI evaluation platform let session A write objects session B could read, including directory names after a wipe. That is ENV persistence 2 with no jailbreak string.

CoSAI will not publish CJS-3/CJS-4 content-safety examples as its own rubric. Operators who need those examples use the 2 July appendix under the Model Provider's license and terms.

## References

1. Anthropic, [Redeploying Fable 5](https://www.anthropic.com/news/redeploying-fable-5), 30 June 2026. Primary source for the industry-framework request, the four axes, defense in depth, safety margin, minor/narrow/universal shapes, 24/7 watch, and the CVSS analogy.
2. Anthropic, [More details on Fable 5's cyber safeguards and our jailbreak framework](https://www.anthropic.com/news/fable-safeguards-jailbreak-framework), 2 July 2026. CJS numeric rubrics, dual-use category table, authorization note, HackerOne channel, scored examples.
3. Coalition for Secure AI, [AI Shared Responsibility Framework, V1.0](https://www.coalitionforsecureai.org/wp-content/uploads/2026/05/CoSAI-Shared-Responsibility-Framework.pdf), May 2026. Layers, personas, one accountable party, attestations.
4. Coalition for Secure AI, [AI Incident Response Framework, V1.0](https://www.coalitionforsecureai.org/wp-content/uploads/2026/03/AI-Incident-Response-1.pdf). Jailbreaking as an operator incident type; prompt injection kept separate.
5. FIRST, [Common Vulnerability Scoring System](https://www.first.org/cvss/). Analogy only: base plus environmental.
6. Coalition for Secure AI, [OASIS Open Project Charter](https://github.com/cosai-oasis/oasis-open-project/blob/main/CHARTER.md) §4. Scope that keeps CJS content-safety examples out of CoSAI authorship.
7. Bill Stout, [Recommendations from the Hugging Face Autonomous Attack](https://www.linkedin.com/pulse/recommendations-from-hugging-face-autonomous-attack-bill-stout-el4ic), 27 July 2026. HITL not viable for most agentic use cases; named shutdown owner; path attestation; distinct agent identity; containment must confirm the agent stopped acting.
8. Bill Stout, [Who is responsible for what: An accountability assessment of the OpenAI Hugging Face incident](https://www.linkedin.com/pulse/who-responsible-what-accountability-assessment-openai-bill-stout-s1dsc/), 14 August 2026. Classifier-off evals make CJS inapplicable; O from ENV; session A writing objects session B can read; residual-risk statement must name third-party production systems.

Machine-readable copies: `data/references.json`, `data/scoring.json`, `data/controls.json`.
