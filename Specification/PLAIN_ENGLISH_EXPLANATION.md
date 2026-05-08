# What the Agent Actually Does: Plain English Explanation

**For**: Non-technical stakeholders (executives, board members, customers)  
**Written**: May 2026  
**Scenario**: Apex Distribution Ltd ETA Inquiry Agent

---

## The Simple Answer

**Right now**: When a customer asks "Where's my delivery?", they wait 4-11 minutes to get a vague answer ("It'll arrive sometime between 1pm and 5pm").

**With the agent**: The customer gets an accurate answer in under 30 seconds ("Your delivery is currently in Watford, estimated arrival 2:15-2:45pm").

**What changed**: Instead of a human spending 11 minutes coordinating between three different computer systems, the agent checks everything instantly and gives the customer a precise answer.

---

## What It Looks Like for the Customer

### Example 1: Sarah Orders Office Supplies

**Today (Without Agent)**:
1. Sarah texts Apex: "Where is order AX-771-3344?"
2. She waits 8 minutes while the customer service agent:
   - Looks up her order in the CRM system
   - Calls the dispatch team to ask about the driver's location
   - Gets put on hold
   - Eventually gets GPS data that's 36 minutes old
   - Calculates a rough estimate in their head
3. She gets back: "Best guess, sometime around 2-3pm. We don't have a tighter estimate than that, sorry."
4. Sarah wastes her afternoon waiting at reception

**Tomorrow (With Agent)**:
1. Sarah texts Apex: "Where is order AX-771-3344?"
2. In 15 seconds, she receives: "Your order is out for delivery on route 028. Driver is currently in Watford (updated 12 minutes ago). Estimated arrival: 2:15-2:45pm. The driver has 4 stops remaining."
3. Sarah schedules her meeting accordingly, doesn't waste time waiting

**What the agent did in those 15 seconds**:
- Looked up Sarah's order in the system (instant)
- Found which route it's on (instant)
- Checked the driver's GPS location (instant)
- Counted how many stops are left (instant)
- Calculated travel time based on distance + traffic + typical stop duration (instant)
- Sent Sarah a clear, specific answer

**No human touched this request. No coordination. No hold time. Just instant, accurate information.**

---

## What It Looks Like for Your Team

### Example 2: Customer Service Agent's Day

**Before Agent**:

**9:00 AM** - Agent starts work  
**9:05 AM** - Customer asks about order AX-123-4567  
**9:15 AM** - Agent finishes (looked up order, called dispatch, got GPS, calculated estimate, replied)  
**9:16 AM** - Customer asks about order AX-234-5678  
**9:27 AM** - Agent finishes  
**9:28 AM** - Customer asks about order AX-345-6789  
**9:39 AM** - Agent finishes  

**By 10:00 AM**: Agent has handled **3 ETA inquiries** (60 minutes of work)  
**Daily capacity**: ~26 ETA inquiries per agent  
**Problem**: 400 ETA inquiries per day need 15 agents just for this one task

---

**After Agent**:

**9:00 AM** - Agent starts work  
**9:05 AM** - Customer asks about order AX-123-4567  
**9:05:15 AM** - **Agent handles it instantly** (agent looked it up, no human needed)  
**9:06 AM** - Customer asks about order AX-234-5678  
**9:06:15 AM** - **Agent handles it instantly**  
**9:07 AM** - Customer asks about order AX-345-6789  
**9:07:15 AM** - **Agent handles it instantly**  
**9:08 AM** - Customer asks about order XX-999-9999  
**9:08:15 AM** - **Agent flags this one**: "I couldn't find that order number. Passing to a specialist."  
**9:10 AM** - Human agent picks it up, helps customer verify their order details  

**By 10:00 AM**: Agent software has handled **360 ETA inquiries**, human agent has handled **40 complex cases**  
**Daily capacity**: Human agents now focus on problems that actually need human judgment  
**Result**: Same team handles 400 inquiries/day, but humans spend their time on meaningful work, not repetitive lookups

---

## When the Agent Says "I Don't Know"

**This is NOT a chatbot that pretends to help but frustrates customers.**

The agent is programmed to recognize when it **shouldn't** answer, and immediately pass the request to a human:

### Safety Net Example 1: Stale GPS Data

**Customer**: "Where is my delivery?"  
**Agent checks GPS**: Last updated 52 minutes ago (too old to be reliable)  
**Agent responds**: "I'm unable to provide a precise ETA due to outdated location data. Connecting you with a specialist who can contact the driver directly. Hold time: ~2 minutes."  
**Human takes over**: Calls driver, gets current status, updates customer

**Why this matters**: The agent doesn't guess. If the data isn't fresh enough to give a confident answer, it escalates. **No customer gets misleading information.**

---

### Safety Net Example 2: High-Value Delivery Exception

**Customer**: Stein-Allen Ltd (£1,250 delivery)  
**Order status**: EXCEPTION (driver reported damaged pallet)  
**Agent recognizes**: This is a £1,250 package with a delivery problem  
**Agent responds**: "Your high-value order requires specialist attention due to a delivery exception. Connecting you now. Hold time: ~2 minutes."  
**Human takes over**: Assesses damage, arranges redelivery or credit, manages customer relationship

**Why this matters**: High-value problems and exceptions need human judgment. The agent recognizes this and **immediately escalates** rather than trying to handle it poorly.

---

## What Makes This Different from Your Past Failures

### 2024 Chatbot Failure: "Customers hated it"

**What went wrong**:
- Chatbot tried to answer everything, even when it didn't know
- Got stuck in loops ("I didn't understand that, please rephrase")
- No way to escalate to a human quickly
- Felt like talking to a robot, not getting help

**How this agent is different**:
- **Knows when it doesn't know**: If GPS data is stale or order not found, it escalates immediately
- **No conversation loops**: Customer asks "Where's my delivery?", agent gives location + ETA. Done. No back-and-forth.
- **Always offers human option**: Every response has a "speak with someone" button
- **Transparent**: Admin panel shows every decision the agent makes, so you can audit it

---

### RPA Billing Failure: "Broke when Aurum schema changed"

**What went wrong**:
- RPA was brittle (relied on exact screen positions, field names)
- When Aurum changed its data format, RPA stopped working
- No one noticed for days until customers complained

**How this agent is different**:
- **Doesn't touch Aurum directly**: Works with the batch exports you already have (no brittle screen-scraping)
- **Handles missing data gracefully**: If today's invoice isn't in the system yet, agent says "Your invoice is still processing, I'll have details tomorrow morning. Would you like to speak with someone now, or is tomorrow acceptable?"
- **Monitored constantly**: Admin panel tracks every request. If agent starts failing, you see it immediately (not days later).

---

## Real-World Scenarios

### Scenario 1: Normal Day

**11:00 AM - 12:00 PM (1 hour)**

- **380 customers ask "Where's my delivery?"**
  - 340 get instant answers from agent (standard lookups: <30 seconds each)
  - 40 ask for more precision ("Can you be more specific than 1-5pm?")
    - 30 get GPS-based precise estimates from agent (2:15-2:45pm)
    - 10 have stale GPS data → agent escalates to human
- **4 customers have delivery exceptions** (damaged, refused, wrong address)
  - Agent recognizes these need human judgment → escalates all 4 immediately
- **16 customers explicitly ask to "speak with someone"**
  - Agent immediately transfers them (no trying to "help" first)

**Human team handled**: 10 GPS issues + 4 exceptions + 16 callback requests = **30 cases in 1 hour**  
**Agent handled**: **370 cases in 1 hour** (instant, no human needed)

**Result**: Customers get faster service, human agents focus on problems that actually need expertise

---

### Scenario 2: System Issue (GPS Down)

**2:00 PM - GPS system stops updating**

**Without agent**: 
- Customers start calling: "Where's my delivery?"
- Human agents spend 15 minutes each saying "Sorry, our tracking system is down, we can only give you the scheduled window"
- Customers frustrated, call volume spikes, hold times increase

**With agent**:
- Agent detects GPS data hasn't updated in 45 minutes (over threshold)
- **Agent automatically stops giving precision estimates**
- Customers get: "Your delivery is scheduled for 1-5pm today. Our live tracking is currently unavailable, but I can connect you with someone who can call the driver directly if you need a more specific time."
- **100% of precision requests escalate to human** until GPS recovers
- Admin panel immediately alerts operations team: "Escalation rate 10% → 80% in last 15 minutes" (indicates system problem)

**Result**: Agent doesn't give bad information, operations team knows immediately there's a problem, customers still get help

---

## The Business Case in Plain English

### What You're Spending Now

- **400 ETA inquiries per day** × **8.5 minutes each** = **56 hours of work per day**
- Plus coordination time (calling dispatch, waiting on hold): **+17 hours**
- **Total**: 73 hours/day = 9.7 full-time people just answering "Where's my delivery?"

**Annual cost**: £301,000 in labor for repetitive lookups

---

### What You'll Spend After

- **360 inquiries handled by agent** (90%) × **0.5 minutes** = **3 hours** (mostly just system overhead)
- **40 inquiries handled by humans** (10% that need judgment) × **8 minutes** = **5.3 hours**
- **Total**: 8.3 hours/day = 1.1 full-time people

**Annual savings**: £271,000 (90% reduction)  
**Capacity freed**: 66 hours/day (8.8 people) can now focus on billing disputes, exceptions, or handle growth

---

### What This Means in Practice

**Option 1 (Cost Reduction)**: Reduce headcount by 8.8 FTE through attrition/redeployment  
**Option 2 (Growth Absorption)**: Handle 20% more volume without hiring  
**Option 3 (Service Improvement)**: Redirect freed capacity to billing disputes (currently 6-day response time → 24-hour response time)

**You choose the business outcome. The agent just frees up the capacity.**

---

## Implementation: Low-Risk Proof

### Phase 1A: Pilot (Months 1-2)

**What happens**:
- Agent runs in "shadow mode" for 2 weeks (handles inquiries, but human reviews every response before sending)
- Then live with 10% of traffic (40 inquiries/day)
- Human monitors admin panel: Are answers accurate? What's escalating? Any customer complaints?

**Decision point at 2 months**:
- **If it works**: 90%+ deflection rate, no customer complaints, accurate answers → proceed to Phase 1B
- **If it doesn't work**: Stop. No sunk cost. You've spent 2 months, not 2 years and £500K.

---

### Phase 1B: Scale (Months 3-4)

**What happens**:
- Scale to 100% of ETA inquiries (400/day)
- Measure actual savings (hours freed, deflection rate, customer satisfaction)
- Tune thresholds (GPS staleness, escalation triggers) based on real data

**Decision point at 4 months**:
- **If savings validated**: £301K annual savings confirmed → plan Phase 2 (billing disputes)
- **If savings below target**: Diagnose (too many escalations? GPS data quality issue?) → fix or stop

---

### Phase 2-3: Expand (Months 5-9)

**Only if Phase 1 successful**:
- Billing Dispute Investigation Agent (agent gathers data, human approves credit)
- Delivery Exception Triage Agent (agent handles routine cases, escalates complex)

**You're never committed beyond the current phase. Every 2 months, you decide: continue, adjust, or stop.**

---

## Summary: What You're Actually Getting

1. **For customers**: Instant, accurate answers instead of 8-minute waits and vague estimates
2. **For your team**: 66 hours/day freed up to work on complex problems instead of repetitive lookups
3. **For you (COO)**: £301K annual savings, or capacity to handle 20% growth, or faster service on billing disputes
4. **For risk management**: Agent knows when to escalate, never guesses, every decision logged

**This isn't AI replacing people. It's AI handling the repetitive parts so your people can focus on the parts that need human judgment.**

**The agent is a tool, not a replacement. Like giving your team a forklift instead of making them carry boxes by hand.**

---

## Questions Anyone Should Be Able to Answer After Reading This

**Q: What does the agent do?**  
A: Instantly looks up order status and calculates delivery ETAs so customers don't wait 8 minutes for a vague answer.

**Q: When does it NOT handle requests?**  
A: When GPS data is too old (>30 min), when the order is high-value with an exception, when the customer explicitly asks for a human.

**Q: How is this different from the 2024 chatbot?**  
A: The chatbot tried to handle everything and got stuck in loops. This agent knows when to escalate immediately.

**Q: How is this different from the RPA project?**  
A: RPA was brittle (broke when Aurum changed). This agent works with batch exports and handles missing data gracefully.

**Q: What if it gives wrong answers?**  
A: Admin panel logs every decision. If accuracy drops, operations sees it immediately. Plus, agent escalates when uncertain.

**Q: How much does it save?**  
A: £301K annual for ETA inquiries alone (66 hours/day freed up). You decide whether to reduce costs, absorb growth, or improve service.

**Q: What's the risk?**  
A: 2-month pilot. If it doesn't work (90%+ deflection, accurate answers), you stop. No long-term commitment.

---

**The bottom line**: Your customers get faster, more accurate answers. Your team focuses on problems that need expertise. You save £301K/year or handle growth without hiring. And if it doesn't work in 2 months, you stop — no sunk cost fallacy.

That's what the agent does.
