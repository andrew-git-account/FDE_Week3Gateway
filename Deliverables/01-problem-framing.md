# D#1 — Problem Framing & Success Metrics

**Client:** MedFlex Healthcare Staffing  
**Engagement:** AI-native shift matching transformation  
**Prepared by:** Andrzej Bihun | Thursday interim draft

---

## 1. The Real Problem (Not the Stated Request)

Marcus's stated ask — *"10x the business without 10x-ing the coordinators"* — is a growth constraint, not a technical requirement. Decoded:

- Current: $14M revenue, 8 coordinators, ~960 shift proposals/day
- Board target: $200M in 24 months (~14x)
- At current productivity: 112 coordinators needed — not viable

**What 14x demands architecturally:** the coordinator role must shift from *doing the matching* to *supervising matching agents*. Agents must autonomously handle standard cases; coordinators handle exceptions and relationship-sensitive decisions only.

### The Three Failure Modes Causing Lost Revenue Today

**1. Speed loss (primary competitive damage)**  
Hospitals submit requests to multiple agencies simultaneously. At 4.2h average fill time, MedFlex loses bids to faster competitors before a proposal is even submitted. Every hour of delay is a lost contract.

**2. Throughput ceiling**  
8 coordinators at 120 decisions/day is a hard ceiling. Inbound demand spikes create a queue; queue creates further delay; delay compounds competitive loss. The ceiling can't be raised by adding staff at the rate business is growing.

**3. Matching inconsistency and tribal knowledge lock**  
Senior coordinators (10+ years) carry undocumented pattern recognition — which nurse fits which hospital specialty, which hospital accepts borderline credentials, which nurse has a track record. New coordinators take measurably longer and produce inconsistent outcomes. 8 coordinators = up to 8 different decisions for equivalent requests. This knowledge evaporates when people leave and can't be scaled.

### Hidden Problems Surfaced in Discovery

**4. Free-text intake parsing is a bottleneck nobody named**  
Hospital shift requests arrive as unstructured free text (email, portal, phone). Coordinators manually parse credential requirements before matching begins. This is a hidden latency step that compounds the 4.2h fill time.

**5. Passive nurse confirmation generates 12% no-show rate**  
Notifications are sent by SMS/email; silence = accepted. MedFlex discovers no-shows when the hospital calls. No proactive detection, no confirmation loop. One client has already received a discount; reputational damage is ongoing.

**6. Unmanaged concurrency in multi-hospital submission**  
The same nurse is submitted to multiple hospitals simultaneously. If two hospitals accept, MedFlex has an overcommitment with no automated resolution protocol. Currently handled ad hoc by coordinators.

---

## 2. Success Metrics

### MedFlex (Business Outcomes)
| Metric | Baseline | Phase 1 Target (6w) | Phase 2 Target (24w) |
|--------|----------|---------------------|----------------------|
| Avg. time to fill | 4.2h | <1h | <20 min |
| Coordinator throughput (proposals/day) | 120/coordinator | 300/coordinator (agent handles 50%) | 600/coordinator (agent handles 80%) |
| Qualification mismatch rate | 7% | <6% | <4% |
| No-show rate | 12% | — | <7% |
| Revenue capacity (without headcount increase) | $14M baseline | — | Supports $100M+ pipeline |

*Note: The 7% mismatch conflates two failure modes — credential mismatch (solvable by better matching) and hospital preference rejection (requires reputation signals). Metrics must be tracked separately from Phase 1.*

*Note on Phase 1 measurement: the mismatch rate is a lagging indicator — it appears only after a hospital reports a problem. Phase 1 tracks two leading signals visible from week 2: (1) hospital acceptance rate trend per confidence band (weekly), and (2) coordinator shadow-review flag rate per week. A declining acceptance rate or rising flag count triggers investigation before any mismatch is reported.*

### Hospitals (Client Outcomes)
| Metric | Target |
|--------|--------|
| Proposal response time | <30 min from request receipt |
| Credential-qualified match rate | >96% |
| Double-booking incidents | 0 (with reservation protocol) |

### Nurses (Worker Outcomes)
| Metric | Target |
|--------|--------|
| Unintended multi-assignment conflicts | 0 |
| Shift confirmation lead time | Same-day notification with explicit confirmation request |
| False-acceptance (no-show due to missed SMS) | <2% |

---

## 3. What "10x Without 10x-ing" Actually Demands

| Architectural Requirement | Why |
|---------------------------|-----|
| Agent must process intake intake parsing autonomously | Eliminates hidden free-text latency step; scales with volume |
| Agent must autonomously match and propose for high-confidence cases | Removes coordinator from standard decision loop; enables throughput ceiling break |
| Coordinator role shifts to exception handling + oversight | Maintains quality control without linear headcount growth |
| Agent must implement atomic nurse reservation | Prevents double-booking at scale; current ad hoc handling breaks at 10x volume |
| Agent must track explicit nurse confirmation | Reduces 12% no-show rate; proactive vs. reactive |
| Coordinator tribal knowledge must be encoded in matching logic | Prevents knowledge loss; enables consistent quality across all 8 coordinator workloads |

---

## 4. Why Previous AI Projects Failed (and How This Is Different)

**Chatbot (hospital-facing):** Tried to change how hospitals interact with MedFlex — adding a new channel hospitals didn't want. This engagement explicitly keeps hospital interaction channels unchanged.

**Recommendation engine (internal):** Made too many mistakes; insufficient training, insufficient coordinator trust. This engagement:
- Starts with high-confidence automation only (Phase 1), building trust incrementally
- Keeps coordinators visible in the loop for MEDIUM confidence cases
- Builds on existing systems (ServiceNow queue) rather than replacing workflows
- Validates incrementally via weekly drift signals (acceptance rate trend, coordinator flag rate) — not a 30-day black box where nobody knows if it's working until it isn't

The key difference: previous projects added AI features to existing systems. This engagement makes agents the *mechanism* for shift matching — the decision logic lives in the agent, not the coordinator's head.
