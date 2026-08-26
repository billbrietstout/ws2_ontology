# AI Jailbreak Prevention Framework

CoSAI Workstream 2, RFC 0.1  
25 August 2026

The Jailbreak Prevention Framework (JPF) is a CoSAI Workstream 2 draft. It consumes Cyber Jailbreak Severity (CJS), the model-safeguard score that Anthropic and Glasswing partners proposed in June and July 2026. JPF then names who stops that bypass from becoming an unauthorized tool call, memory write, or hop to another model: which persona, which control, and which attestation proves the control ran.

## What CJS, ENV, and operational class change in the incident clock

A low-severity model bypass on an agent that can write production systems is paged as a containment incident. The same bypass in a chat window with no tools is a weekly log review.

Tool calls that run under a shared agent service account raise the environmental score even when the user-facing model refused in chat. Jailbreak success is the unauthorized tool call, write, or hop.

If the model adds no attacker capability beyond existing public tools, CJS scoring stops at informational. JPF still scores the environment, because a textbook payload can fire a tool.

The Model Provider publishes the CJS band. The Application Developer publishes the environmental band. AI System Governance records the operational class that starts the incident clock. Neither party may lower the other's number.

Prompt-injection detectors and jailbreak classifiers are separate controls. A trip of one does not close a ticket of the other.

Classifiers that block some benign coding work are a published Fable 5 trade. The deploying organization writes the accepted false-positive rate into its risk statement and names who absorbs user impact when that rate is exceeded.

If cyber classifiers are off, CJS does not apply. The operational class is taken from the environment. The OpenAI Hugging Face evaluation escape is that case: no model-policy bypass, a shared writable cache, and production reach.

## Three scores and who publishes them

Anthropic's [Redeploying Fable 5](https://www.anthropic.com/news/redeploying-fable-5) (30 June 2026) asked industry for a shared way to judge jailbreak severity. The named drafters are Amazon, Microsoft, Google, and other Glasswing partners. The 2 July follow-up publishes that draft as Cyber Jailbreak Severity: four axes, bands from informational (CJS-0) through critical (CJS-4). The computed band is a floor. It may be raised. It may not be lowered.

CoSAI is not on that drafting list. Individual member labs may score model bypasses as Model Providers. The OASIS project names the controls that stop a bypass from becoming a tool call, memory write, or hop.

| Score | Who publishes it | Question it answers |
| --- | --- | --- |
| Cyber Jailbreak Severity (CJS) | Model Provider, using the Glasswing draft | How far past this model's safeguards does the recipe go, relative to other tools and models? |
| Environment (ENV) | Application Developer | After the completion leaves the model, which tools, hops, memory, principal, and human-review window are live? |
| Operational class | AI System Governance | Which incident-response clock starts, and which persona contains? |
| Control | One persona from the Shared Responsibility Framework | Who prevents, detects, or contains, and what artifact proves it? |

CJS is the Glasswing draft's language for a model-policy bypass. The operational class is the language for paging an operator.

CoSAI's charter, section 4, puts prompt injection, model theft, poisoning, scaled abuse, and inference attacks in scope. It puts malware generation, phishing generation, and other content safety out of scope. High and critical CJS examples in the 2 July draft include malware authoring and exploit writing. Operators consume those bands as severity inputs. They do not re-score the content as a CoSAI product.

## Terms

**Jailbreak (model).** A prompt technique that causes a model to produce a completion that violates the model's stated policy or classifier boundary.

**Jailbreak (system).** An unauthorized tool call, write, payment, code run, or data read, reached because a model policy or a hop policy failed. The user-facing model can still refuse in chat.

**Prompt injection.** Untrusted content treated as instruction. Distinct from jailbreak. A jailbreak of model A is often implemented as prompt injection into model B.

**Bypass.** Anthropic footnote 2 treats bypass as a synonym of jailbreak for CJS. JPF uses jailbreak for policy-boundary failure and prompt injection for instruction-confusion.

**Safety margin.** Classifiers block some benign and low-risk dual-use requests so that high-risk dual-use is less likely to pass. Users see this as refusals of reasonable coding work. Fable 5 set this margin larger than prior launches.

**High-risk dual use.** Work that defenders and attackers both do: penetration tests, exploit development, lateral movement. The 2 July safeguards post says what separates the legitimate case from harm is who is doing the work and under what authorization. CJS then scores the prompt technique without that context. The named-authorization control in Business and usage is that assignment.

**Persona, layer, control, obligation, attestation.** Nouns from the Shared Responsibility Framework (SRF). Each control names one accountable persona at one layer, the obligation that persona performs, and the artifact that proves it.

**Human in the loop.** Whether a person can review or interrupt before a tool fires. Written HITL in the environment table.

## Imported CJS

Full scoring rubrics live in [More details on Fable 5's cyber safeguards and our jailbreak framework](https://www.anthropic.com/news/fable-safeguards-jailbreak-framework). JPF does not re-author them.

| Axis | Range | Asks |
| --- | --- | --- |
| Capability gain | 0 to 4 | How far beyond existing tools and weaker models? Gain 0 stops scoring; the finding is informational. |
| Breadth | 0 to 2 | How many distinct offensive tasks does the same recipe unlock? |
| Ease of weaponization | 0 to 2 | How much skill at using language models does it take to go from recipe to a working attack? |
| Discoverability | 0 to 2 | How easy is it to obtain the technique? |

The four numbers are added. The sum maps to informational (0), low (1 to 3.5), medium (4 to 6.5), high (7 to 8.5), or critical (9 to 10). The 30 June post describes three qualitative shapes that sit under those numbers: minor (the request only enters the safety margin), narrow harmful (one harmful behavior), and universal (a class of harmful behaviors).

The computed band is a floor. Discretionary raises include an output severe enough on its own, no near-term mitigation, or compounding with other open findings.

System-prompt extraction is out of CJS cyber scope. JPF scores it only when the extracted text is used to cause a tool call, write, or hop; that case uses the environment score and incident response. The operator may not invent a CJS raise for it.

## Environment score

The Common Vulnerability Scoring System has a base score and an environmental score. CJS as drafted is a base score plus a discoverability axis that behaves like a temporal factor. The environment score covers what happens after the completion leaves the model.

| Axis | 0 | 1 | 2 | 3 |
| --- | --- | --- | --- | --- |
| Tool authority | No tools; chat only | Tools bound to the original user's token | Tools run under an agent service account | Tools can write production systems, move money, or change identity |
| Graph depth | One model, one completion | Two or three hops | Four or more hops, or recursive peer calls | n/a |
| Persistence | This session only | Memory or retrieval write that later turns treat as instruction | Standing skill, scheduled job, or cross-user plant | n/a |
| Authorization fidelity | Named principal; hop carries the original user | Principal dropped; callee trusts the agent identity | No principal, confused deputy, or unknown authorization | n/a |
| Human in the loop | Human can review before the side effect | Human on loop; can interrupt some actions | Faster than a human can review; tools fire first | n/a |

Add the five axis scores. Sum 0 to 2 is isolated chat. Sum 3 to 5 is user-bound tools. Sum 6 to 8 is a delegated agent. Sum 9 to 11 is a production-write graph.

Some values force a minimum band after that sum. Production-write tools force a production-write graph. Tools that fire faster than human review, when they already run under an agent account or with production write, also force a production-write graph. A standing skill or cross-user plant forces at least a delegated-agent band. Unknown principal or confused deputy also forces at least a delegated-agent band.

For autonomous agents, faster-than-review is the expected human-in-the-loop value. [Recommendations from the Hugging Face Autonomous Attack](https://www.linkedin.com/pulse/recommendations-from-hugging-face-autonomous-attack-bill-stout-el4ic) states that a human approval gate slower than the agent gets bypassed, and that human-in-the-loop is not viable for most agentic use cases. Hard gates stay on high-impact or irreversible actions; the rest is automatic.

The Application Developer publishes an environment record for every production system and recomputes it within five business days of a tool, hop, or memory-policy change. That record is the published environment band control under Application.

## Operational class

Start from the CJS band: informational is 0, low is 1, medium is 2, high is 3, critical is 4.

If the environment is a delegated agent or a production-write graph, raise the operational class by one step, and stop at halt-path.

If CJS is informational, raise at most to ticket. A textbook payload on a live tool path is an investigation.

Never lower CJS.

If cyber classifiers are off, CJS is not applicable. Take the operational class from the environment: isolated chat or user-bound tools maps to contain; delegated agent maps to mitigate; production-write graph maps to halt-path.

| Operational class | What the operator does | What the Model Provider does |
| --- | --- | --- |
| Log | Write the prompt, completion, CJS band, and environment band to the incident log. Review that week's log bucket every seven days. Do not page. | No classifier patch. Count benign blocks toward the monthly safety-margin false-positive figure. |
| Ticket | Open a ticket within one business day. If a tool path is bound, freeze that tool class for the session until a named application owner accepts residual risk. | Acknowledge in the vulnerability-disclosure queue. Do not page a 24/7 watch. |
| Contain | Page on-call within four hours. Kill the session. Disable the implicated tool class or hop. Confirm the agent has stopped acting, not only that it is unreachable. Notify the Model Provider of the miss. | Triage within one business day. Say whether CJS will be raised. Do not lower it. |
| Mitigate | Page immediately. Kill sessions that used the recipe. Freeze memory writes for the affected agent. Confirm the agent has stopped acting. Inform the named business executive the same calendar day. | Preliminary mitigation within 24 hours of a confirmed high CJS finding. 24/7 watch channel. Share the new safeguard so an independent tester can re-run the recipe. |
| Halt path | Page immediately. Take the model or the write-capable tool path offline if the recipe is in active use. Confirm the agent has stopped acting. If the system is in a national-security or critical-infrastructure program, notify the designated government counterpart the same day. | Immediate preliminary mitigation on a confirmed critical CJS finding, matching the 30 June most-severe class. 24/7 channel. Share the new safeguard for independent test. |

Mitigate and halt-path provider clocks match the clocks the 30 June post already stated for the most severe class: immediate preliminary mitigations, and 24/7 watch.

The classifier-off exception exists because CJS scores a bypass of a live safeguard. [Who is responsible for what](https://www.linkedin.com/pulse/who-responsible-what-accountability-assessment-openai-bill-stout-s1dsc/) records production cyber classifiers turned off for an evaluation. The remaining control is the privileges the agent can mint and the systems it can talk to. Confirming the agent has stopped acting, not only that it is unreachable, is taken from [Recommendations from the Hugging Face Autonomous Attack](https://www.linkedin.com/pulse/recommendations-from-hugging-face-autonomous-attack-bill-stout-el4ic).

The AI Incident Response Framework remains the playbook. The operational class selects which playbook clock starts. Jailbreaking and prompt injection stay separate incident types in that taxonomy.

## Controls

Each entry names the obligation and what happens when the threshold is missed. Catalog identifiers in parentheses are for tickets and machine-readable records.

### Business and usage

**Named authorization for high-risk dual use** (JPF-L1-001). AI System Governance maintains a roster of people allowed to request penetration tests, exploit development, and related high-risk dual-use work. Each grant has an expiry and an approving executive. Application allowlists and platform serving policy enforce that roster. Completions that match the high-risk list without a live grant are unauthorized. The seven-day count of those completions is zero; otherwise kill the session and revoke tool bindings.

**CJS intake without rescoring** (JPF-L1-002). When a Model Provider or researcher publishes a CJS band, Governance files it against the affected system within one business day. Governance computes the operational class from that band plus the system's current environment record. It may not lower CJS, recompute the four CJS axes, or substitute a local severity label. At least 95 percent of inbound reports in 30 days must have CJS, environment, and operational class populated; otherwise escalate to the named business executive.

**Accepted safety-margin false-positive rate** (JPF-L1-003). Governance writes a numeric accepted rate into the risk statement and compares it to the Model Provider's monthly figure. If the provider exceeds the accepted rate, governance renegotiates the classifier threshold or changes model. This framework does not invent a universal rate.

**Jailbreak incident commander** (JPF-L1-004). A named human owns containment for contain, mitigate, and halt-path, with a deputy. Mitigate and halt-path require 24/7 cover. Prompt injection remains a separate incident type. At least 95 percent of those pages in 30 days must be acknowledged inside the clock in the operational-class table.

### Information

**Instruction-class versus data-class labeling** (JPF-L2-001). The Data Provider tags every retrieved chunk and tool observation as instruction or data at write time. Unlabeled spans are not assembled into prompts. Unlabeled spans served in seven days: zero; otherwise halt retrieval until the labels are backfilled.

**Mediated memory writes** (JPF-L2-002). A write that would change a future instruction stream needs a named Application Developer decision. Unreviewed instruction-class writes in seven days: zero; otherwise freeze memory writes.

**Jailbreak-recipe data restricted** (JPF-L2-003). Working jailbreak recipes live in a restricted corpus with access logging. Recipe strings in customer-visible logs in seven days: zero; otherwise rotate access and purge those logs.

### Application

**Tool calls bound to the original user token** (JPF-L3-001). The Application Developer passes the original user's identity into each tool adapter. At most 1 percent of production tool calls in seven days may be missing that principal; otherwise disable the service-account tool path. Governance may accept a higher tool-authority environment score in writing. That acceptance lives in the environment record, not as an implicit adapter default.

**Peer models treated as untrusted speakers** (JPF-L3-002). The Agentic Platform Provider wraps a message from one model to another as data, not as an instruction, and runs the receiving model's detectors before that model's tools fire. Inter-model messages that reach a tool adapter with no detector result in seven days: zero; otherwise break the hop until detectors sit inline.

**Output filter before tool fire** (JPF-L3-003). The model's completion is not authorization to run a tool. The adapter log records the proposed call, the filter decision, and the grant identifier or the deny reason. Tool fires without a filter decision in seven days: zero; otherwise disable unfiltered adapters.

**Split-payload and stitch detection** (JPF-L3-004). Blocked spans from earlier turns are kept for the session. A later tool call that reconstructs a blocked span is refused. Each quarter, reconstruct a known blocked span across three turns and confirm the adapter refuses. Fail the release gate if that test does not pass.

**Prompt-injection detector distinct from jailbreak classifier** (JPF-L3-005). Ship two named detectors, with separate configurations, logs, and incident types. A jailbreak trip does not close a prompt-injection ticket. Missing either detector at release blocks the release.

**Published environment band per system** (JPF-L3-006). For every production system, record the five environment axis scores, the resulting band, who scored it, the date, and the change that triggered a rescore. At least 95 percent of production systems must have a record dated after the last tool, hop, or memory change, or less than 90 days old if nothing changed. Miss: freeze new tool bindings.

### Platform

**Session kill and tool-class rate limit on detector trip** (JPF-L4-001). The AI Platform Provider invalidates the session within five seconds at the 95th percentile in the quarterly drill, and rate-limits the implicated tool class for that tenant for 24 hours or until a named commander lifts it.

**Fallback routing with user notice** (JPF-L4-002). When a classifier blocks a request, AI Model Serving routes it to the named fallback model or returns a block notice. Blocked completions that still hit tools in seven days: zero; otherwise disable that gateway's tool path. Silent continue and silent drop both fail the control.

**Path attestation on every tool call** (JPF-L4-003). Each tool call record carries the user, session, model, hop, tool name, and outcome. At least 95 percent of production tool calls in seven days must include all six. Miss: halt new tool bindings until the fields are present. Shared agent identities fail this control.

**Tenant isolation of memory and skills** (JPF-L4-004). Each quarter, write instruction-class memory in tenant A and read from tenant B. The read must be empty. Any successful cross-tenant read: take shared memory offline. This test does not cover two sessions inside the same tenant; that gap is listed under Open problems.

### Model Provider

**Documented safeguards on the served model** (JPF-L5-001). The Model Provider documents refusal training, runtime classifiers, and offline monitoring, plus the four dual-use categories used for Fable 5: prohibited, high-risk dual use, low-risk dual use, and benign. Operators do not retrain these. Missing documentation at onboarding: do not bind write-capable tools. If classifiers are off for an evaluation, the same note records that fact and the business residual-risk statement that names third-party production systems the evaluation can reach.

**CJS scoring of incoming cyber jailbreaks** (JPF-L5-002). The Model Provider publishes capability gain, breadth, ease, discoverability, the initial band, and any discretionary raise. At least 95 percent of in-scope reports in 30 days must carry a published band. Miss: pause new model launches until the backlog clears.

**Vulnerability-disclosure channel and 24/7 watch for high and critical findings** (JPF-L5-003). Publish a submission URL. Staff intake for high and critical CJS findings around the clock. Acknowledge a confirmed critical finding within one hour. If no critical finding arrived, the control is met only if the roster exists.

**Classifier patch shared for independent test** (JPF-L5-004). A confirmed high CJS finding gets a retestable mitigation in the serving path within 24 hours. A confirmed critical finding gets that mitigation immediately. The reporting party and the operator's named red team get a retest path. Miss on a high finding: the operator takes write-capable tools offline.

## Worked examples

Scoring below uses the published CJS rules and the environment rules above. Axis values for CJS examples follow the 2 July appendix where that article already scored them.

**Textbook SQL injection from a "teaching junior developers" prompt.** The 2 July appendix scores this informational: capability gain is zero, so CJS scoring stops. In a chatbot with no tools (isolated chat) the operational class is log: write it down, review the week's bucket. In an agent whose tools can write production databases, with no human review before fire, the environment floors to production-write graph. Informational CJS may rise only to ticket: freeze the write path for the session. The recipe added no attacker capability; the live tool path still needs an owner.

**Amazon report on Fable 5, as described 30 June 2026.** Researchers prompted the model so that it identified software vulnerabilities and, in one case, produced demonstration code. Anthropic reported that less capable models identified the same vulnerabilities, that every tested model could produce the same demonstration, and that the technique did not expose Mythos-level cyber capability. The 30 June post places this in the minor, safety-margin category. Capability gain against the public baseline is 0 or 1. Breadth is at most one vulnerability type. If scored informational, operator response follows the textbook case above. If scored low, a chat-only system stays at ticket. A delegated-agent or production-write deployment raises to contain, and the session's tool class is disabled until the Application Developer accepts residual risk. JPF does not re-score the Amazon evidence; it consumes whichever band the Model Provider publishes and applies the environment.

**Universal system-prompt override, 2 July appendix.** Critical CJS (gain 4, breadth 2, ease 2, discoverability 2). Any environment yields halt-path. The operator takes the write-capable tool path offline if the recipe is in active use. The provider ships an immediate preliminary mitigation and a retest path.

**Encoding-scheme jailbreak, 2 July appendix.** Medium CJS (gain 3, breadth 2, ease 1, discoverability 0). Chat-only stays at contain: page within four hours, kill the session, notify the provider. The same recipe on a delegated agent becomes mitigate: freeze memory writes, inform the business executive the same day, 24-hour provider mitigation clock.

**A low-severity text bypass implemented on the second hop.** Model A produces a completion that sits inside the safety margin (low CJS). Model B treats A's text as an internal instruction and calls a production-write tool under a service account. The environment floors to production-write graph. The operational class becomes contain. Failed controls: peer models treated as untrusted speakers, tool calls bound to the original user, and output filter before tool fire. The CJS band on A's recipe stays low.

**OpenAI Hugging Face evaluation escape, classifiers off.** Production cyber classifiers were off so the lab could measure capability. CJS is not applicable. Evaluation sessions that never shared a prompt still read and wrote the same package-proxy cache, first as files and then as directory names after a wipe (standing persistence, unknown or confused-deputy authorization, at least one extra hop). The path reached a third-party code-execution harness and then Hugging Face production workers (production-write tools, faster than human review). The environment floors to production-write graph. Classifiers off maps that environment to halt-path: take the write-capable path offline, confirm the agents have stopped acting. Failed controls: documented safeguards (classifiers off without a residual-risk statement that named third-party production), session isolation inside one tenant (not covered by tenant isolation of memory), and tool calls bound to the original user (shared proxy identity rather than one credential per session). Source: the 14 August accountability assessment.

## Coverage measurement

Count production systems in the model inventory (the Shared Responsibility Framework business-layer inventory control, or the operator's equivalent). A system that binds tools is in coverage when it has a current environment record, a named incident commander, and path-attestation completeness of at least 95 percent of tool calls over seven days.

Target: at least 90 percent of production systems that bind tools meet coverage. Miss: freeze new tool bindings on uncovered systems. Chat-only systems may omit tool attestation; they still need an environment record and a commander.

Fable 5 states that making a model fully robust to jailbreaks is probably impossible.

## Open problems

Environment-axis weights are uncalibrated. No inter-rater study exists for the five axes. Until that study exists, two Application Developers can publish different environment bands for the same system. Governance records both and uses the higher band.

CJS capability gain is measured against tools and models available at assessment time. The 2 July Log4Shell trio shows the same model behavior dropping from critical to informational once scanners exist. Operators need a dated baseline on every ticket. JPF does not yet specify who maintains a shared baseline catalog across vendors.

No OpenTelemetry GenAI field currently means "this hop looked like a jailbreak." Path attestation requires hop identity and outcome. It does not yet require a detector-result field that survives forwarding from one model to another. Workstream 2 telemetry work should add that field before a two-or-three-hop environment can be audited without vendor-specific logs.

Authorization for high-risk dual use is an identity protocol. The named-authorization control names the roster and the grant file. It does not specify how a Model Provider running a shared multi-tenant API verifies that grant in real time. Fable 5 blocked high-risk dual use for that reason. The identity handshake between operator grant and provider classifier is unspecified.

Universal jailbreaks of Fable 5 were unreported at the 30 June writing. Environment scoring of a universal recipe in a multi-agent graph with shared memory is untested. The second-hop example is a control-failure illustration, not a measured residual risk.

Session isolation inside one tenant is unspecified. Tenant isolation of memory tests tenant A versus tenant B. The OpenAI evaluation platform let session A write objects session B could read, including directory names after a wipe. That is standing persistence with no jailbreak string.

CoSAI will not publish high or critical CJS content-safety examples as its own rubric. Operators who need those examples use the 2 July appendix under the Model Provider's license and terms.

## References

1. Anthropic, [Redeploying Fable 5](https://www.anthropic.com/news/redeploying-fable-5), 30 June 2026. Primary source for the industry-framework request, the four axes, layered safeguards, safety margin, minor/narrow/universal shapes, 24/7 watch, and the Common Vulnerability Scoring System analogy.
2. Anthropic, [More details on Fable 5's cyber safeguards and our jailbreak framework](https://www.anthropic.com/news/fable-safeguards-jailbreak-framework), 2 July 2026. CJS numeric rubrics, dual-use category table, authorization note, HackerOne channel, scored examples.
3. Coalition for Secure AI, [AI Shared Responsibility Framework, V1.0](https://www.coalitionforsecureai.org/wp-content/uploads/2026/05/CoSAI-Shared-Responsibility-Framework.pdf), May 2026. Layers, personas, one accountable party, attestations.
4. Coalition for Secure AI, [AI Incident Response Framework, V1.0](https://www.coalitionforsecureai.org/wp-content/uploads/2026/03/AI-Incident-Response-1.pdf). Jailbreaking as an operator incident type; prompt injection kept separate.
5. FIRST, [Common Vulnerability Scoring System](https://www.first.org/cvss/). Analogy only: base plus environmental.
6. Coalition for Secure AI, [OASIS Open Project Charter](https://github.com/cosai-oasis/oasis-open-project/blob/main/CHARTER.md) section 4. Scope that keeps CJS content-safety examples out of CoSAI authorship.
7. Bill Stout, [Recommendations from the Hugging Face Autonomous Attack](https://www.linkedin.com/pulse/recommendations-from-hugging-face-autonomous-attack-bill-stout-el4ic), 27 July 2026. Human-in-the-loop not viable for most agentic use cases; named shutdown owner; path attestation; distinct agent identity; containment must confirm the agent stopped acting.
8. Bill Stout, [Who is responsible for what: An accountability assessment of the OpenAI Hugging Face incident](https://www.linkedin.com/pulse/who-responsible-what-accountability-assessment-openai-bill-stout-s1dsc/), 14 August 2026. Classifier-off evaluations make CJS inapplicable; operational class from the environment; session A writing objects session B can read; residual-risk statement must name third-party production systems.

## Appendix: control catalog

Catalog identifiers are for tickets. The title is the name to use in prose.

| Catalog id | Title | Layer | Accountable persona | What proves it | When it fails |
| --- | --- | --- | --- | --- | --- |
| JPF-L1-001 | Named authorization for high-risk dual use | Business and usage | AI System Governance | Signed grant file (principal, scope, expiry, approving executive) and a revocation list | Unauthorized high-risk completions in seven days: kill the session and revoke tool bindings |
| JPF-L1-002 | CJS intake without rescoring | Business and usage | AI System Governance | Incident ticket with CJS band, source, environment band, operational class, and who recorded it | Fewer than 95 percent of inbound reports filed in 30 days: escalate to the named business executive |
| JPF-L1-003 | Accepted safety-margin false-positive rate | Business and usage | AI System Governance | Risk-statement paragraph with numeric rate, review date, and accepting executive | Monthly rate above the accepted figure: renegotiate the classifier threshold or change model |
| JPF-L1-004 | Jailbreak incident commander | Business and usage | AI System Governance | On-call calendar with named humans, backup, and which operational classes the shift covers | Fewer than 95 percent of contain-or-higher pages acknowledged on clock: page the deputy and review the roster |
| JPF-L2-001 | Instruction-class versus data-class labeling | Information | Data Provider | content_class field (instruction or data) on retrieved chunks and tool observations | Unlabeled spans served into prompts: halt retrieval until backfill |
| JPF-L2-002 | Mediated memory writes | Information | Data Provider | Memory-write log (source, proposed instruction, reviewer, decision, time) | Unreviewed instruction-class writes: freeze memory writes |
| JPF-L2-003 | Jailbreak-recipe data restricted | Information | Data Provider | Access log for the restricted corpus; tickets with recipes redacted | Recipe strings in customer-visible logs: rotate access and purge logs |
| JPF-L3-001 | Tool calls bound to the original user token | Application | Application Developer | Sample of 100 production tool calls whose authorization matches the session's original user | More than 1 percent of tool calls missing that user: disable the service-account tool path |
| JPF-L3-002 | Peer models treated as untrusted speakers | Application | Agentic Platform Provider | Hop trace showing detector results on every production model-to-model message in the sample | Messages reaching a tool with no detector result: break the hop until detectors sit inline |
| JPF-L3-003 | Output filter before tool fire | Application | Application Developer | Adapter log (proposed call, filter decision, grant or deny reason, time) | Tool fires with no filter decision: disable unfiltered adapters |
| JPF-L3-004 | Split-payload and stitch detection | Application | Application Developer | Session traces with blocked-span store and stitch-block events | Quarterly stitch test fails: fail the release gate |
| JPF-L3-005 | Prompt-injection detector distinct from jailbreak classifier | Application | Application Developer | Two detector identifiers in production config; incident taxonomy has both types | Either detector missing at release: block the release |
| JPF-L3-006 | Published environment band per system | Application | Application Developer | Environment record (system, five scores, band, scorer, date, triggering change) | Fewer than 95 percent of production systems current: freeze new tool bindings |
| JPF-L4-001 | Session kill and tool-class rate limit | Platform | AI Platform Provider | Kill-latency from the quarterly drill; rate-limit config by tenant and tool class | 95th-percentile kill slower than five seconds: page platform on-call |
| JPF-L4-002 | Fallback routing with user notice | Platform | AI Model Serving | Gateway traces (block event, user-visible notice, fallback model or explicit none) | Blocked completions that still hit tools: disable that gateway's tool path |
| JPF-L4-003 | Path attestation on every tool call | Platform | AI Platform Provider | Seven-day completeness report for user, session, model, hop, tool, outcome | Completeness below 95 percent: halt new tool bindings until the fields are present |
| JPF-L4-004 | Tenant isolation of memory and skills | Platform | AI Platform Provider | Isolation test report (tenant pair, write, read, result) | Tenant B reads tenant A's instruction-class memory: take shared memory offline |
| JPF-L5-001 | Documented safeguards on the served model | Model Provider | Model Provider | Model card or safeguards note covering refusal training, classifiers, offline monitoring, dual-use table, and classifier-on or classifier-off with residual-risk statement | Missing at onboarding: do not bind write-capable tools |
| JPF-L5-002 | CJS scoring of incoming cyber jailbreaks | Model Provider | Model Provider | Scored report or disclosure record with the four axis values and the band | Fewer than 95 percent of in-scope reports scored in 30 days: pause new model launches until the backlog clears |
| JPF-L5-003 | Vulnerability-disclosure channel and 24/7 watch | Model Provider | Model Provider | Submission URL, staffing roster, time-to-acknowledge for high and critical findings (or a signed none-received note) | Critical finding not acknowledged within one hour: notify operator executives and freeze the affected model |
| JPF-L5-004 | Classifier patch shared for independent test | Model Provider | Model Provider | Patch note (finding, CJS band, mitigation version, retest result) | High finding without a retestable mitigation in 24 hours: operator takes write-capable tools offline |
